# Exploración FE / BE — Carpetas en la lista de tableros (SWAT-577)

**Issue:** [SWAT-577 — [ENHANCEMENT] [Dashboards] Add folder/organization structure for dashboard list](https://linear.app/simetrik/issue/SWAT-577/enhancement-dashboards-add-folderorganization-structure-for-dashboard)
**Estado en Linear:** Backlog · Prioridad High · Proyecto Operation Center · Team Swat AI · Asignado a Andrés Ladino
**Fecha de exploración:** 2026-08-03
**Repos leídos:** `fe-solutions-mf` (commit `8aebc1879`) · `op-center-backend` (commit `8cc5bc3b`) · `@simetrikinc/desyk-components@1.30.0-0`

> Objetivo de este doc: dejar por escrito **qué existe hoy** en FE y BE antes de diseñar,
> para que el prototipo y el handoff se apoyen en el código real y no en supuestos.

---

## 1. Resumen ejecutivo

| Pregunta | Respuesta |
|----------|-----------|
| ¿Existe algún concepto de carpeta/grupo en tableros? | **No.** `grep -ri "folder"` en `op-center-backend/apps` y `migrations` → 0 resultados. En el FE tampoco hay nada en `features/dashboards`. Es campo verde. |
| ¿Hay un precedente de agrupación por usuario? | **Sí: Favoritos.** Modelo `dashboard_favorites` con `(user_id, account_id, dashboard_id)` + `order`. Es el patrón más cercano y reutilizable como referencia de arquitectura. |
| ¿Hay un precedente de carpetas en el producto? | **Sí, en Almacenamiento** (`features/storage/components/folders/`): `FolderNameDialog`, `MoveFolderDialog`, `BreadcrumbNav`, con copy ya traducido en `storage.main.json`. Su backend vive **fuera** de `op-center-backend`. |
| ¿Cuánto código FE toca esto? | El panel de Tableros son ~1.900 líneas en 5 componentes; el cambio es **aditivo** sobre `DashboardSection` + `DashboardList`. |
| Riesgo principal | La lista es **paginada e infinita** (20 por página, orden y búsqueda **server-side**). Agrupar en carpetas del lado del cliente rompe con la paginación → el agrupamiento tiene que resolverse en el BE. Ver §5. |

---

## 2. Frontend — qué existe hoy

Ruta base: `fe-solutions-mf/src/oc/features/dashboards/`

### 2.1 Anatomía del panel "Tableros"

```
SidebarList                         shared/components/SidebarList (48 líneas)
├── topAction        → Button "Nuevo tablero" (outline, w-full, icono Plus)
├── search           → input "Buscar tablero" (debounce 300 ms)
└── children
    ├── PendingInstallationsSection  "Configuraciones pendientes (12)"
    ├── FavoritesSection             "Favoritos (5/15)"   ← drop target "dashed"
    └── DashboardSection             "Tableros (155)"     ← drop target "subtle"
```

| Archivo | Líneas | Rol |
|---------|--------|-----|
| `components/DashboardList/DashboardList.tsx` | 520 | Orquestador del panel. Estado de búsqueda, sort, y **los 3 diálogos únicos** (renombrar, eliminar, gestionar acceso) compartidos por todos los ítems. |
| `components/DashboardListItem/DashboardListItem.tsx` | 316 | La fila. Grip (solo favoritos) · icono `Lock`/`Globe` (privacidad) o badge `Info` ámbar (instalación pendiente) · nombre truncado · `AwaitingDataDot` · botón pin · `⋮` DropdownMenu **y** ContextMenu de click derecho con los mismos ítems. |
| `components/DashboardSection/DashboardSection.tsx` | 142 | **Sección presentacional reutilizable**: header (`label` + `counter` + `headerAction`) sobre un body que resuelve `loading` / `error` / `empty` / `items`, con soporte de `dropTarget` (variantes `dashed` y `subtle`). **Este es el componente a extender para carpetas.** |
| `components/FavoritesSection/FavoritesSection.tsx` | 310 | Favoritos con tope de 15, reorder por drag (`useHtml5Sortable`), cross-drag pin/unpin con inserción posicional y optimistic updates + rollback. |
| `components/PendingInstallationsSection/` | — | Sección de instalaciones de template pendientes. |
| `pages/DashboardsPage.tsx` | 613 | Página contenedora. |

### 2.2 Acciones que ya viven en la fila de tablero

`DashboardListItem` (mismos ítems en `⋮` y en click derecho):

| Acción | Copy es | Condición |
|--------|---------|-----------|
| Renombrar | "Cambiar nombre" | `hasAccess` |
| Agregar contexto | "Agregar contexto" | `hasAccess`, deshabilitado si install pendiente |
| Duplicar | "Duplicar" | `hasAccess`, deshabilitado si install pendiente |
| Gestionar acceso | "Gestionar acceso" | permiso `oc:manage_access` |
| Eliminar | "Eliminar tablero" | `hasAccess`, estilo `text-destructive`, tras `Separator` |
| Fijar/quitar favorito | "Fijar favorito" / "Quitar favorito" | botón pin propio, no menú |

**Implicación de diseño:** "Mover a carpeta" y "Quitar de la carpeta" entran en **este** menú, no en una UI nueva. El menú ya tiene 5 ítems → sumar 1 (no 2 simultáneos) es lo consistente con el criterio de *una tarea a la vez*.

### 2.3 Capa de servicios

`fe-solutions-mf/src/oc/services/dashboards/`

- `basePath = "/api/v1/dashboards"`
- `dashboards/queriesFn.ts`: `GET /` (lista) · `GET /{id}` · `POST /` · `PATCH /{id}` · `DELETE /{id}` · `POST /{id}/clone` · `POST /{id}/configure` · `GET /{id}/install-sources`
- `favorites/queriesFn.ts`: base `/api/v1/dashboards/favorites` → `POST` (pin) · `DELETE /{dashboardId}` (unpin) · `PATCH /reorder`
- `dashboards/queryKeys.ts`: `["dashboards","list",params]` y `["dashboards","list-infinite",params]`, con helpers `isDashboardInfiniteListKey` / `isFavoriteTrueListKey` usados por los optimistic updates.

**Parámetros de la lista (`GetDashboardListParams`):** `page`, `page_size`, `search`, `favorite`, `sort_by` (`name` | `created_at` | `updated_at`), `sort_order` (`asc` | `desc`), `accountId`.

**Schema del ítem (`dashboardItemSchema`, zod):**
`id`, `name`, `description`, `account_id`, `created_by`, `is_deleted`, `access_type` (`public`/`private`), `global_entity_id`, `has_access?`, `favorite` (`{ order }` \| null), `install_metadata`, `is_awaiting_data`, `created_at`, `updated_at`, `is_draft?` (decorado en cliente).

→ **Un campo `folder` va acá**, siguiendo exactamente la forma de `favorite`: objeto embebido nullable (`{ id, name }`) en vez de un id suelto, para que la fila pinte contexto sin un segundo fetch.

### 2.4 Configuración actual de la lista (dato duro para el diseño)

```ts
useGetDashboardListInfinite({
  pageSize: 20, initialPage: 1, favorite: false,
  search: debouncedSearch, sort_by: "name", sort_order: sortAsc ? "asc" : "desc",
})
```

- **Infinite scroll** con `IntersectionObserver` sobre un sentinel + skeletons de 3 filas.
- **Búsqueda server-side** con debounce de 300 ms; empty state `noResults` con el término.
- **Orden server-side** A→Z / Z→A, con toggle en el header de la sección (`ArrowDownAZ` / `ArrowUpZA`).
- El contador "Tableros (N)" sale de `pagination_data.totalItems`, **menos** los pendientes.
- Tope de favoritos: `FAVORITES_LIMIT = 15`, verificado contra una query **sin filtro** para que la búsqueda no permita saltarse el tope.

### 2.5 Drag & drop ya implementado

- `hooks/useDashboardCrossDrag.ts` — MIME types `FAVORITE_DASHBOARD_MIME` y `NON_FAVORITE_DASHBOARD_MIME`, hook `useDashboardDropTarget({ acceptMime, onDrop })`.
- `shared/hooks/useHtml5Sortable.ts` — reorder vertical con línea de inserción (`before`/`after`).
- `utils/favoriteOptimisticUpdates.ts` — pin/unpin/reorder optimista + rollback + invalidación.

→ Hay **infra de DnD nativa (HTML5) ya probada** en este mismo panel. Un drop target por carpeta reusa `useDashboardDropTarget` con un MIME nuevo. No hace falta traer `@formkit/drag-and-drop` (el que expone desyk en `drag-and-drop`).

### 2.6 Precedente interno de carpetas — Almacenamiento

`src/oc/features/storage/components/folders/`: `FolderNameDialog.tsx` (modo `create` | `rename`, valida duplicados contra `siblings`), `MoveFolderDialog.tsx`, `BreadcrumbNav.tsx`.

Copy ya existente en `locales/es/storage.main.json` — **reutilizable tal cual** para no inventar lenguaje:

| Key | Copy es |
|-----|---------|
| `files.view.newFolder` | Nueva carpeta |
| `folders.nameDialog.createTitle` | Crear carpeta |
| `folders.nameDialog.renameTitle` | Renombrar carpeta |
| `folders.nameDialog.namePlaceholder` | Nombre de la carpeta |
| `folders.validation.duplicate` | Ya existe una carpeta con este nombre en esta ubicación |
| `files.view.deleteFolder.title` | ¿Eliminar carpeta? |
| `files.view.deleteFolder.confirmDescription` | La carpeta "{{name}}" se eliminará. {{content}} |
| `files.view.toast.folderCreated` / `folderRenamed` / `folderDeleted` / `folderMoved` | Carpeta creada correctamente. / Carpeta renombrada / Carpeta eliminada / Carpeta movida |

**Nota:** ese árbol de carpetas de Almacenamiento **no** vive en `op-center-backend` (no hay app `storage` ahí); consume otro servicio. Sirve como precedente de **UI y copy**, no de backend.

---

## 3. Backend — qué existe hoy

Repo: `op-center-backend`, app `apps/dashboards/`. Arquitectura DDD (`api/views` → `services` → `domain/repositories` → `domain/models`), DI por `container.py`, migraciones Alembic en `migrations/`.

### 3.1 Modelo `Dashboard` (`domain/models/dashboard.py`, tabla `dashboards`)

```
id (UUID, pk) · name (255) · description (500, null) · account_id (255, index)
created_by (255, null) · is_deleted (bool) · created_at · updated_at
access_type (20, default "public") · global_entity_id (255, unique, null)
install_metadata (JSONB, null) · is_awaiting_data (bool)
pages → relationship(Page, cascade all, delete-orphan)
```

### 3.2 Modelo `DashboardFavorite` (`domain/models/dashboard_favorite.py`) — **el molde a copiar**

```
id (int, pk autoincrement)
user_id (int, index)            ← scope por usuario
account_id (255, index)         ← scope por cuenta
dashboard_id (UUID, FK dashboards.id ON DELETE CASCADE, index)
order (int, default 0)
created_at
UniqueConstraint(user_id, account_id, dashboard_id)
```

Repositorio: `domain/repositories/dashboard_favorite_repository.py`. Servicio: `dashboard_favorite_service` (métodos `pin` / `unpin` / reorder).

### 3.3 Endpoints existentes relevantes

| Endpoint | Notas |
|----------|-------|
| `GET /dashboards` | `search` (ilike por nombre, case-insensitive), `sort_by`, `sort_order`, paginación, `favorite`, enriquecido con `has_access` y `favorite`. |
| `POST /dashboards/favorites` | Pin. Devuelve `DashboardSummaryOut` con `favorite.order = max(order)+1`. 409 si ya está. 403 cross-account. |
| `DELETE /dashboards/favorites/{dashboard_id}` | Unpin **idempotente** (204 siempre). |
| `PATCH /dashboards/favorites/reorder` | Reorder **total**: el payload debe cubrir exactamente el set actual, sin duplicados de `order`. 400 si no. |

Detalles de auth reutilizables: `require_user_id(auth)` rechaza llamadas por API key (400) porque necesita identidad de usuario; `AUTH_FAILURE_RESPONSES` y `DASHBOARD_SCOPES` estandarizan los responses.

---

## 4. Sistema de diseño — inventario desyk relevante

`@simetrikinc/desyk-components@1.30.0-0`. Componentes ya usados por el panel: `button`, `dialog`, `alert-dialog`, `alert`, `empty-state`, `tooltip`, `dropdown-menu`, `context-menu`, `sonner` (toast), `input`, `label`, `skeleton`, `scroll-area`, `utils/cn`.

Disponibles y **no** usados aún acá, candidatos para carpetas: `collapsible` (Radix: `Collapsible` / `CollapsibleTrigger` / `CollapsibleContent`), `sidebar`, `command`, `combobox`, `popover`, `separator`, `drag-and-drop` (`@formkit/drag-and-drop`), `panel`, `accordion`.

El paquete trae su propia doc en `node_modules/@simetrikinc/desyk-components/skills/desyk/` (`SKILL.md`, `references/*.md` por componente, `patterns/data-list.md`, `patterns/data-table-rules.md`) → **fuente de verdad para el `design.md`** de la Etapa 2.

Tokens reales (`dist/styles.css`, HSL en `:root`): `--primary: 240 94% 60%` · `--muted-foreground: 0 0% 55%` · `--accent: 240 5% 96%` · `--border: 0 0% 85%` · `--radius: 0.5rem` · familia `Inter` · set `--sidebar-*` propio · `--info`, `--success`, `--warning`, `--destructive` · `--ai-purple` / `--ai-blue` + gradientes.

---

## 5. Consecuencias técnicas para el diseño (lo que condiciona el prototipo)

1. **El agrupamiento no puede ser client-side.** Con 155 tableros paginados de 20 en 20 y orden server-side, agrupar en el cliente mostraría carpetas incompletas. El BE debe exponer o (a) la lista de carpetas con su conteo + una lista de tableros filtrable por carpeta, o (b) un endpoint de "árbol" paginado por carpeta. → Decisión a tomar en el handoff BE (Etapa 7).
2. **La búsqueda ya es server-side y debe seguir cruzando carpetas** (criterio del issue). El resultado necesita decir **en qué carpeta está** cada tablero → el ítem debe traer `folder: { id, name } | null`, y en modo búsqueda la lista se aplana con la carpeta como metadato de la fila.
3. **Jerarquía visual:** el criterio pide que los grupos tengan **más jerarquía** que los tableros suertos. `DashboardSection` ya define el patrón de header de sección (`SECTION_LABEL_CLASS`) — las carpetas deben leerse como un nivel **entre** el header de sección y la fila de tablero, no como otro header de sección (si no, "Favoritos" y "Carpeta X" compiten).
4. **Coexistencia de secciones:** el panel ya tiene 3 secciones fijas (Pendientes, Favoritos, Tableros). Las carpetas viven **dentro** de "Tableros"; hay que definir el orden carpetas-primero-luego-sueltos y qué pasa con el toggle A→Z existente (¿ordena carpetas, tableros, o ambos?).
5. **Scope del dato — la decisión más caras de cambiar después:** ¿las carpetas son **por usuario** (como Favoritos: cada uno organiza su vista) o **por cuenta** (compartidas, como los tableros)? Cambia el modelo, los permisos y el copy. Ver Etapa 1 y decisión **D1** del índice de planes.
6. **Migración de 155 tableros existentes:** todo tablero arranca sin carpeta ("sueltos"). No hay backfill; el empty state de carpetas y el onboarding del primer uso son parte del diseño.

---

## 6. Preguntas abiertas (se resuelven en Etapas 1, 4 y 7)

| # | Pregunta | Impacto |
|---|----------|---------|
| D1 | ¿Carpetas por usuario o por cuenta? | Modelo BE, permisos, copy |
| D2 | ¿Un solo nivel o subcarpetas anidadas? | Complejidad de UI y de query |
| D3 | ¿Un tablero en una sola carpeta (carpeta) o en varias (etiqueta)? | Modelo de datos y modelo mental |
| D4 | ¿Cómo convive con Favoritos y con "Configuraciones pendientes"? | Jerarquía del panel |
| D5 | ¿El orden A→Z aplica a carpetas, a tableros dentro, o a ambos? | Comportamiento del control existente |
| D6 | ¿Eliminar carpeta = desagrupar siempre? (el criterio dice que sí: borrar carpeta **no** borra tableros) | Copy del diálogo destructivo |
| D7 | ¿Drag & drop es la vía principal de mover, o el menú `⋮`? ¿Ambas? | Accesibilidad y "una tarea a la vez" |

---

## 7. Archivos que tocará la implementación (mapa preliminar)

**FE — nuevos:** `features/dashboards/components/FolderSection/` · `components/FolderRow/` · `components/CreateFolderWizard/` (2 pasos, usa `stepper` + `checkbox` de desyk — D8) · `components/DashboardPicker/` (selector múltiple **compartido** por el wizard y por "Agregar tableros" — D9) · `components/MoveToFolderDialog/` · `components/DeleteFolderDialog/` · `services/dashboards/folders/{queriesFn,queryKeys,schemas,types}.ts` · keys en `locales/{es,en,pt}/dashboards.main.json`.

> **Nota (2026-08-04):** D8 y D9 salieron de probar el prototipo, después de esta exploración. Suman dos componentes (wizard + picker compartido) y **tres requisitos de transaccionalidad en BE** — ver abajo.

**FE — modificados:** `DashboardList.tsx` (composición + diálogos) · `DashboardListItem.tsx` (ítems de menú + drag source) · `DashboardSection.tsx` (anidar carpetas) · `dashboards/schemas.ts` (campo `folder`) · `dashboards/types.ts` (params `folder_id`).

**BE — nuevos:** `domain/models/dashboard_folder.py` · `domain/repositories/dashboard_folder_repository.py` · `services/dashboard_folder_service.py` · `api/views/folders.py` · `api/serializers_folders.py` · migración Alembic · registro en `container.py` y `main.py` · tests en `tests/apps/dashboards/`.

**BE — modificados:** `api/views/dashboards.py` (filtro `folder_id` en la lista) · `api/serializers.py` (`folder` embebido en `DashboardSummaryOut`) · repo de dashboards (join).


---

## 8. Requisitos de API que aparecieron al prototipar (2026-08-04)

Las pruebas del prototipo (D8, D9) agregan **transaccionalidad** al contrato. Sin esto el FE hace 1 + N llamadas y una falla parcial deja la operación a medias — y el "Deshacer" deja de ser confiable.

| # | Necesidad | Propuesta |
|---|-----------|-----------|
| 1 | **Crear carpeta con tableros** en un solo paso (D8) | `POST /dashboards/folders` acepta `dashboard_ids: UUID[]` opcional; crea y asigna en una transacción |
| 2 | **Agregar N tableros** a una carpeta existente (D9) | `PATCH /dashboards/folder` con `{ dashboard_ids: UUID[], folder_id }`, o `POST /dashboards/folders/{id}/dashboards` |
| 3 | **Deshacer** una asignación en lote | La respuesta debe devolver el `folder_id` **anterior** de cada tablero, para que el FE pueda revertir sin recordar estado que puede haber cambiado |

El endpoint de un solo tablero (`PATCH /dashboards/{id}/folder`) se mantiene para mover y quitar de a uno.
