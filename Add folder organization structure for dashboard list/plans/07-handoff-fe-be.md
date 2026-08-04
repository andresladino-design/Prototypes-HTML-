# Etapa 7 — Handoff FE + BE

**Objetivo:** que FE y BE puedan estimar e implementar sin volver a preguntar el "qué", y que el "antes → después" quede enumerado contra producción.
**Entregables:** `handoff/07-handoff-fe.md` · `handoff/07-handoff-be.md` · `handoff/07-antes-despues.md`
**Precondición:** Etapas 5 (historias) y 6 (prototipo).

---

## 1. `handoff/07-antes-despues.md` — el diff contra producción

Convención del equipo: los cambios se enumeran contra el **estado real de producción** (`fe-solutions-mf` @ `8aebc1879`), no contra una versión idealizada.

| # | Antes (hoy) | Después | Archivo real |
|---|-------------|---------|--------------|
| 1 | Sección "Tableros (155)" = lista plana paginada | Carpetas primero + sueltos después | `DashboardSection.tsx`, `DashboardList.tsx` |
| 2 | Menú de fila con 5 acciones | 6–7 acciones: + "Mover a carpeta" / "Quitar de la carpeta" | `DashboardListItem.tsx` |
| 3 | Sin disparador de crear carpeta | Nuevo disparador (definido en F1) | `DashboardList.tsx` |
| 4 | Búsqueda devuelve lista plana sin contexto | Cada resultado indica su carpeta | `DashboardList.tsx`, schema del ítem |
| 5 | `dashboardItemSchema` sin `folder` | `folder: { id, name } \| null` | `services/dashboards/dashboards/schemas.ts` |
| 6 | `GET /dashboards` sin filtro de carpeta | + `folder_id` (y `unfiled=true`) | `api/views/dashboards.py` |
| 7 | No existe entidad carpeta | Tabla + CRUD + endpoints | `apps/dashboards/**` + migración |

Cada fila con captura antes/después del prototipo.

---

## 2. `handoff/07-handoff-be.md`

### Modelo propuesto (siguiendo el molde de `DashboardFavorite`)

```python
class DashboardFolder(Base):
    __tablename__ = "dashboard_folders"
    id: UUID (pk, default uuid4)
    name: str(255)
    account_id: str(255), index                # D1: scope de cuenta, igual que Dashboard
    created_by: str(255) | None                # trazabilidad (D1, consecuencia 2)
    order: int                                 # reservado; el orden de la v1 es A→Z (D5)
    created_at / updated_at
    __table_args__ = (
        UniqueConstraint("account_id", "name", name="uq_dashboard_folder_account_name"),
    )
```

**Asignación tablero↔carpeta — decidida por D1 + D3: columna en `dashboards`.**

```python
# apps/dashboards/domain/models/dashboard.py
folder_id: Mapped[uuid.UUID | None] = mapped_column(
    UUID(as_uuid=True),
    ForeignKey("dashboard_folders.id", ondelete="SET NULL"),
    nullable=True, index=True,
)
```

Por qué esta forma y no una tabla puente:

- **D3 (pertenencia exclusiva)** queda garantizada por el esquema, no por lógica de aplicación.
- **D6 (eliminar carpeta desagrupa)** lo implementa `ON DELETE SET NULL` **en el motor de base de datos** — es imposible que un bug borre tableros al borrar una carpeta.
- **D1 (por cuenta)** hace innecesario el `user_id`, así que no hay fila por usuario.

La tabla puente `dashboard_folder_items` solo sería necesaria para carpetas personales o pertenencia múltiple, ambas **fuera del alcance de la v1**. Si esas capas llegan después, se suman **sin migrar** lo existente (la columna sigue sirviendo a la carpeta de cuenta).

### Endpoints propuestos

| Método | Ruta | Notas |
|--------|------|-------|
| `GET` | `/api/v1/dashboards/folders` | Lista con `dashboard_count` por carpeta. Sin paginar (o page_size alto: son pocas). |
| `POST` | `/api/v1/dashboards/folders` | `{ name, dashboard_ids?: UUID[] }`. Crea **y asigna** en una transacción (D8). **409** si el nombre ya existe en el scope. |
| `PATCH` | `/api/v1/dashboards/folders/{id}` | `{ name }`. 409 duplicado · 404 · 403 cross-account. |
| `DELETE` | `/api/v1/dashboards/folders/{id}` | **Nunca cascade a dashboards.** Desagrupa (SET NULL / borra filas puente). 204. Devolver o documentar cuántos se desagruparon. |
| `PATCH` | `/api/v1/dashboards/{id}/folder` | `{ folder_id: UUID \| null }` — mover uno (`null` = quitar de la carpeta). F2 y F3. |
| `PATCH` | `/api/v1/dashboards/folder` | **Lote (D9):** `{ dashboard_ids: UUID[], folder_id }`. Devuelve el `folder_id` anterior de cada tablero para poder deshacer. F8. |
| `PATCH` | `/api/v1/dashboards/folders/reorder` | Opcional; copiar el contrato **total** de `favorites/reorder` (payload completo, sin duplicados de `order`, 400 si no calza). |

### Cambios en endpoints existentes

- `GET /dashboards`: + `folder_id: UUID | None` y + `unfiled: bool` (tableros sin carpeta). `search` **ignora** ambos filtros para cumplir C5 → documentarlo explícito en el Swagger, porque es contra-intuitivo.
- `DashboardSummaryOut`: + `folder: FolderInfo | None` (embebido, igual que `favorite`) → evita un segundo fetch en la lista y en los resultados de búsqueda.

### Reglas de negocio a especificar

1. Eliminar carpeta **nunca** elimina tableros (criterio explícito del issue, D6).
2. Borrado de tablero: al ser columna en `dashboards`, la asignación desaparece con la fila. Sin limpieza extra.
3. Nombre único **por cuenta**, case-insensitive, con trim, largo máximo alineado a `dashboards.name` (255).
4. Cross-account → 403; inexistente → 404. **No** hace falta `require_user_id` (D1: el scope es la cuenta, no el usuario) — pero sí registrar `created_by` cuando haya identidad.
5. Máximo de carpetas por cuenta (definir en I5; evita que el panel vuelva a ser una lista larga, ya que D2 descartó la anidación).
6. Performance: la lista con carpetas no puede degradar `GET /dashboards`; índice por `folder_id` y conteos con una sola query agregada, no N+1.

### Convenciones del repo a cumplir

`apps/dashboards/` DDD (`api/views` → `services` → `domain/repositories` → `domain/models`), DI por `container.py`, migración Alembic registrada, tests en `tests/apps/dashboards/`, plan del cambio en `docs/plans/YYYY-MM-dd-<slug>.md`, `make check-code` + `make test` verdes.

---

## 3. `handoff/07-handoff-fe.md`

### Componentes nuevos

| Componente | Rol |
|-----------|-----|
| `FolderSection/` | Contenedor de una carpeta: header (icono + nombre + contador + `⋮`) + `Collapsible` con las filas. Reusa `DashboardSection` para los estados internos. |
| `CreateFolderWizard/` | Crear en **2 pasos** (D8): elegir tableros → nombre + resumen. Usa `stepper` y `checkbox` de desyk. |
| `DashboardPicker/` | Selector múltiple **compartido** (D9): lo usan el paso 1 del wizard y "Agregar tableros". Excluye los ya presentes en la carpeta destino. |
| `FolderNameDialog/` | Solo renombrar. **No** reusar el de storage: su validación rechaza tildes y `_`. |
| `DeleteFolderDialog/` | `AlertDialog` destructivo con el conteo de tableros a desagrupar. |
| `MoveToFolderDialog/` | Selector de carpeta con buscador (`command`/`combobox`) + acceso a "Nueva carpeta". |
| `services/dashboards/folders/` | `queriesFn` · `queryKeys` · `schemas` · `types`, siguiendo el patrón exacto de `services/dashboards/favorites/`. |

### Componentes modificados

- `DashboardList.tsx` — composición carpetas + sueltos; los diálogos nuevos como **instancia única** (como ya hace con rename/delete/access); modo búsqueda aplanado.
- `DashboardListItem.tsx` — 1–2 ítems nuevos en `renderActionItems` (aparecen en `⋮` **y** en click derecho automáticamente); metadato de carpeta en modo búsqueda; drag source si D7.
- `DashboardSection.tsx` — permitir anidar carpetas manteniendo `loading`/`error`/`empty`/`dropTarget`.
- `dashboards/schemas.ts` + `types.ts` — campo `folder`, params `folder_id` / `unfiled`.
- `locales/{es,en,pt}/dashboards.main.json` — keys nuevas bajo `dashboardsMain.sidebar.folders.*`, con el copy del prototipo (y reuso del lenguaje de `storage.main.json`).

### Puntos técnicos que el handoff debe cerrar

1. **Estrategia de datos:** ¿una query de carpetas + una query por carpeta al expandir (lazy), o carpetas + lista filtrada? Recomendación: **lazy al expandir**, coherente con el scroll infinito ya existente y con carpetas colapsadas por defecto.
2. **Query keys nuevas** y qué invalida qué al mover/crear/borrar (el panel ya tiene un mapa fino de invalidaciones para favoritos — seguirlo).
3. **Optimistic updates:** mover un tablero debería sentirse instantáneo. Ya existe el molde en `utils/favoriteOptimisticUpdates.ts` (mutate → rollback → settled).
4. **Persistencia del estado de expansión:** `localStorage` por cuenta+usuario (no requiere BE) vs. preferencia en BE. Recomendación: `localStorage` en la v1. **Precedente:** `SIDEBAR_COLLAPSED_KEY = "oc_sidebar_collapsed"` ya persiste el colapso del panel en el mismo archivo.
4b. **Transaccionalidad de las operaciones en lote (D8/D9):** con 1 + N llamadas, una falla parcial deja la carpeta a medio llenar y el "Deshacer" deja de ser confiable. Es el punto de negociación más importante con BE.
4c. **Revelar la carpeta después de actuar:** al crear, mover, agregar o renombrar, la carpeta se expande, se hace scroll hasta ella y se resalta ~2s. Fue el hallazgo de las pruebas; sin esto el usuario queda buscando su propio resultado.
5. **Drag & drop (entra en la v1 como atajo, D7):** reusar `useDashboardCrossDrag` con un MIME nuevo (`DASHBOARD_TO_FOLDER_MIME`), **no** traer `@formkit/drag-and-drop`. A resolver explícitamente: (a) drop sobre carpeta **colapsada** sin expandirla, (b) autoscroll del panel al arrastrar hacia una carpeta fuera del viewport, (c) que una fila arrastrada no active a la vez el drop target de Favoritos y el de carpetas. Equivalente por menú y teclado **obligatorio**; si el alcance aprieta, se corta el drag, no el menú.
6. **Telemetría:** eventos para las métricas de la Etapa 5 (`folder_created`, `dashboard_moved_to_folder`, `dashboard_removed_from_folder`, `folder_deleted`, `folder_expanded`, `search_used`), definidos acá para que se instrumenten con el feature.
7. **Feature flag:** ¿se lanza detrás de flag? El panel es la navegación principal del OC; un flag reduce el riesgo.

---

## 4. Documentación para usuario final (criterio C8)

Borrador de la ayuda: qué es una carpeta, cómo crearla, cómo mover tableros, qué pasa al eliminar una carpeta (no se pierden tableros), y que la búsqueda encuentra en cualquier carpeta. Va como sección del handoff y como insumo del equipo de contenido/soporte.

## 5. Definition of done

- [ ] Los 3 documentos escritos, con capturas del prototipo.
- [ ] `07-antes-despues.md` enumera cada cambio contra archivos reales de producción.
- [ ] Contrato de API completo: rutas, payloads, códigos de error, y **la decisión (a) vs. (b) tomada**, no delegada.
- [ ] Lista cerrada de archivos FE nuevos/modificados y de keys de i18n.
- [ ] Eventos de telemetría definidos.
- [ ] Riesgos y trade-offs escritos (paginación + agrupamiento es el principal).
- [ ] Revisado con un dev de FE y uno de BE antes de crear los tickets.

## 6. Riesgos

- **Handoff que describe pantallas y no contratos** — sin el contrato de API, BE lo inventa y FE lo descubre en integración.
- **Ignorar la paginación** — es el riesgo técnico #1 del feature (exploración §5.1). El handoff tiene que decidirlo explícitamente.
- **Duplicar el diálogo de carpeta** que ya existe en Almacenamiento en vez de reusarlo o extraerlo a `shared/`.
