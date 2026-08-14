# Etapa 7 — Handoff FE + BE

**Objetivo:** que FE y BE puedan estimar e implementar sin volver a preguntar el "qué", y que el "antes → después" quede enumerado contra producción.
**Entregables:** `handoff/07-handoff-fe.md` · `handoff/07-handoff-be.md` · `handoff/07-antes-despues.md`
**Precondición:** Etapas 5 (historias) y 6 (prototipo).

> **Actualizado el 2026-08-14** tras revisar `op-center-backend` @ `8cc5bc3b` y
> `fe-solutions-mf` @ `8aebc1879`. Tres decisiones cambiaron lo que este plan pedía:
> **D2** (3 niveles de anidamiento), **D6** (eliminar disuelve un nivel, ya no es
> `ON DELETE SET NULL`) y **D10** (solo Tableros). Y apareció **D15**: el agrupamiento
> tiene que resolverse server-side, algo que este plan listaba como pregunta abierta
> y que ahora es un requisito con datos.

---

## 0. Lo que hay que cerrar sí o sí

Esta etapa es la única pendiente que bloquea todo lo demás. Y tiene un requisito
duro que no estaba cuando se planeó:

| Verificado en código | Consecuencia |
|---|---|
| `DASHBOARDS_PAGE_SIZE = 20` + `useInfiniteQuery` + `IntersectionObserver` (`DashboardList.tsx:117`) | El FE nunca tiene la lista completa |
| `page_size` con tope duro `le=100` (`utils/common/dependencies/pagination.py:8`) | Con 155 tableros no hay «traer todo» posible |
| `search`, `sort_by`, `sort_order` server-side (`api/views/dashboards.py:68-106`) | El orden del árbol lo decide el BE, no `localeCompare` |
| `grep -ril folder apps/ migrations/` → 0 resultados | Campo verde: no hay nada que migrar |

**El prototipo construye el árbol en cliente y calcula los contadores de subárbol
recorriendo los 159 tableros en memoria. Eso es válido como exploración de
interacción y NO es implementable.** El handoff tiene que llevar el contrato que
lo hace posible; si no, BE lo inventa y FE lo descubre en integración.

---

## 1. `handoff/07-antes-despues.md` — el diff contra producción

Convención del equipo: los cambios se enumeran contra el **estado real de producción** (`fe-solutions-mf` @ `8aebc1879`), no contra una versión idealizada.

| # | Antes (hoy) | Después | Archivo real |
|---|-------------|---------|--------------|
| 1 | Sección "Tableros (155)" = lista plana paginada | Árbol de hasta 3 niveles + sueltos después | `DashboardSection.tsx`, `DashboardList.tsx` |
| 2 | Menú de fila con 5 acciones | + "Mover a carpeta" / "Quitar de la carpeta" | `DashboardListItem.tsx` |
| 3 | Sin disparador de crear carpeta | `FolderPlus` en el header + "Nueva subcarpeta" en el `⋮` de la carpeta | `DashboardList.tsx` |
| 4 | Búsqueda devuelve lista plana sin contexto | Cada resultado indica su **ruta completa** | `DashboardList.tsx`, schema del ítem |
| 5 | `dashboardItemSchema` sin `folder` | `folder: { id, name, path } \| null` | `services/dashboards/dashboards/schemas.ts` |
| 6 | `GET /dashboards` sin filtro de carpeta | + `folder_id` (y `unfiled=true`) | `api/views/dashboards.py` |
| 7 | No existe entidad carpeta | Tabla con `parent_id` + `path` + CRUD + endpoints | `apps/dashboards/**` + migración |
| 8 | Las 3 secciones del panel no colapsan | Las 4 colapsan, persistido (D12) | `DashboardSection.tsx` |
| 9 | Datasets comparte el componente de lista | **Sin cambios** — Datasets no lleva carpetas (D10) | — |

Cada fila con captura antes/después del prototipo.

---

## 2. `handoff/07-handoff-be.md`

### Modelo — con anidamiento (D2)

```python
class DashboardFolder(Base):
    __tablename__ = "dashboard_folders"
    id: UUID (pk, default uuid4)
    name: str(255)
    account_id: str(255), index                # D1: scope de cuenta, igual que Dashboard
    parent_id: UUID | None                     # D2: self-FK, NULL = raíz
    path: str(255), index                      # path materializado: '/uuid/uuid/uuid/'
    created_by: str(255) | None                # trazabilidad (D1, consecuencia 2)
    created_at / updated_at
```

**`path` materializado es la pieza clave.** Resuelve tres necesidades que si no
requieren tres mecanismos distintos:

| Necesidad | Con `path` |
|---|---|
| Guarda de ciclos (no meter una carpeta en su propio subárbol) | comparación de prefijo — sin CTE recursivo |
| `subtree_count` (el contador que se muestra) | `WHERE path LIKE '/a/b/%'` |
| Tope de 3 niveles (D2) | contar separadores · `CHECK` en la columna |

Costo: mover una carpeta reescribe el `path` de todo su subárbol. Es aceptable —
mover es raro y con tope 3 los subárboles son chicos. Alternativa a evaluar: `ltree`.

> **Gotcha de Postgres que hay que dejar escrito.** `UniqueConstraint(account_id, parent_id, lower(name))`
> **no impide duplicados en la raíz**: los `NULL` son distintos entre sí, así que dos carpetas
> raíz podrían llamarse igual. Hacen falta dos índices parciales:
>
> ```sql
> CREATE UNIQUE INDEX uq_folder_sibling ON dashboard_folders (account_id, parent_id, lower(name))
>   WHERE parent_id IS NOT NULL;
> CREATE UNIQUE INDEX uq_folder_root ON dashboard_folders (account_id, lower(name))
>   WHERE parent_id IS NULL;
> ```

**Asignación tablero↔carpeta — D1 + D3: columna en `dashboards`.**

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
- **D1 (por cuenta)** hace innecesario el `user_id`, así que no hay fila por usuario.

> **⚠️ D6 cambió y esto ya no basta.** Antes se apoyaba en `ON DELETE SET NULL` para
> «desagrupar en el motor de base de datos». Ahora eliminar una carpeta debe **subir el
> contenido un nivel**, a la madre — no a la raíz. Eso es **lógica de servicio que
> reparenta antes de borrar**, en una transacción:
>
> 1. `UPDATE dashboards SET folder_id = <parent> WHERE folder_id = <id>`
> 2. `UPDATE dashboard_folders SET parent_id = <parent>, path = … WHERE parent_id = <id>`
> 3. `DELETE FROM dashboard_folders WHERE id = <id>`
>
> El `ON DELETE SET NULL` se conserva como **red de seguridad** (si algo borra la fila
> por fuera, los tableros no se van con ella), no como el mecanismo del feature.

### Endpoints — el contrato que cierra D15

La forma que hace compatible el árbol con la paginación: **las carpetas son pocas
y van completas; los tableros son muchos y van paginados por carpeta.**

| Método | Ruta | Notas |
|--------|------|-------|
| `GET` | `/api/v1/dashboards/folders` | **TODAS las carpetas, sin paginar** (son ~7-15, I5). Cada una con `parent_id`, `path`, `direct_count` y `subtree_count`. Este endpoint es el que hace innecesario contar en cliente. |
| `GET` | `/api/v1/dashboards?folder_id={id}` | Tableros **directos** de esa carpeta, paginado. Se pide **al expandir**, no al cargar. |
| `GET` | `/api/v1/dashboards?unfiled=true` | Los sueltos, paginado. |
| `POST` | `/api/v1/dashboards/folders` | `{ name, parent_id?, dashboard_ids?: UUID[] }`. Crea **y asigna** en una transacción (D8). **409** nombre duplicado entre hermanas · **422** si excede los 3 niveles. |
| `PATCH` | `/api/v1/dashboards/folders/{id}` | `{ name }`. 409 duplicado entre hermanas · 404 · 403 cross-account. |
| `PATCH` | `/api/v1/dashboards/folders/{id}/parent` | **Nuevo (D2):** `{ parent_id: UUID \| null }`. Mueve la carpeta con su subárbol. **409** si el destino cuelga de ella (ciclo) · **422** si el subárbol excedería los 3 niveles. Reescribe `path` del subárbol. |
| `DELETE` | `/api/v1/dashboards/folders/{id}` | **Nunca cascade a dashboards.** Reparenta a la madre (D6) y borra. Devolver cuántos tableros y subcarpetas subieron, para el copy del toast. |
| `PATCH` | `/api/v1/dashboards/{id}/folder` | `{ folder_id: UUID \| null }` — mover uno (`null` = quitar). F2 y F3. |
| `PATCH` | `/api/v1/dashboards/folder` | **Lote (D9):** `{ dashboard_ids: UUID[], folder_id }`. Devuelve el `folder_id` anterior de cada tablero para poder deshacer. F8. |

### Cambios en endpoints existentes

- `GET /dashboards`: + `folder_id: UUID | None` y + `unfiled: bool`. `search` **ignora** ambos filtros para cumplir C5 → documentarlo explícito en el Swagger, porque es contra-intuitivo.
- `DashboardSummaryOut`: + `folder: FolderInfo | None` con **`path` incluido** (embebido, igual que `favorite`). El `path` es lo que permite mostrar `Adquirencia / Visa` en los resultados de búsqueda sin un segundo fetch.

### Reglas de negocio a especificar

1. Eliminar carpeta **nunca** elimina tableros (criterio explícito del issue, D6).
2. Eliminar carpeta **sube su contenido un nivel**, no a la raíz (D6 revisada).
3. Tope de **3 niveles** de carpeta, validado en servicio **y** con `CHECK` sobre `path` — la UI no puede ser la única guarda.
4. **Ciclos:** una carpeta no puede colgar de su propio subárbol. Validado por prefijo de `path` dentro de la transacción del move.
5. Nombre único **entre hermanas**, case-insensitive, con trim (ver los dos índices parciales arriba).
6. Borrado de tablero: al ser columna en `dashboards`, la asignación desaparece con la fila. Sin limpieza extra.
7. Cross-account → 403; inexistente → 404. **No** hace falta `require_user_id` (D1: el scope es la cuenta) — pero sí registrar `created_by` cuando haya identidad.
8. Máximo de carpetas por cuenta (I5: aviso suave > 15, tope técnico 50).
9. Performance: `GET /dashboards` no puede degradarse; índice por `folder_id`, y los conteos del endpoint de carpetas en **una sola query agregada**, no N+1.

### Convenciones del repo a cumplir

`apps/dashboards/` DDD (`api/views` → `services` → `domain/repositories` → `domain/models`), DI por `container.py`, migración Alembic registrada, tests en `tests/apps/dashboards/`, plan del cambio en `docs/plans/YYYY-MM-dd-<slug>.md`, `make check-code` + `make test` verdes.

---

## 3. `handoff/07-handoff-fe.md`

### Componentes nuevos

| Componente | Rol |
|-----------|-----|
| `FolderTree/` | El árbol de hasta 3 niveles. Aplana la estructura en filas con `depth` y pinta una sola lista — recursión de componentes por nivel es innecesaria y cara. |
| `FolderRow/` | Fila de carpeta: icono con estado (D13, **sin chevron**) + nombre + contador de subárbol + `⋮`. |
| `CreateFolderWizard/` | Crear en **2 pasos** (D8): elegir tableros → nombre + resumen. Muestra `Dentro de: <ruta>` cuando hay carpeta madre. |
| `DashboardPicker/` | Selector múltiple **compartido** (D9): paso 1 del wizard y "Agregar tableros". Tope de **10 filas visibles**, resto en scroll. |
| `FolderNameDialog/` | Solo renombrar. **No** reusar el de storage: su validación rechaza tildes y `_`. |
| `DeleteFolderDialog/` | `AlertDialog` destructivo diciendo **a dónde sube** el contenido (D6). |
| `MoveToFolderDialog/` | **Árbol de destinos con ruta**, no lista simple: con anidamiento puede haber tres carpetas «2026». Incluye destino «Primer nivel» y esconde los destinos inválidos por ciclo o por tope. |
| `services/dashboards/folders/` | `queriesFn` · `queryKeys` · `schemas` · `types`, siguiendo el patrón exacto de `services/dashboards/favorites/`. |

### Componentes modificados

- `DashboardList.tsx` — composición árbol + sueltos; diálogos nuevos como **instancia única** (como ya hace con rename/delete/access); modo búsqueda aplanado con ruta.
- `DashboardListItem.tsx` — ítems nuevos en `renderActionItems` (aparecen en `⋮` **y** en click derecho automáticamente); ruta de carpeta en modo búsqueda; drag source (D7).
- `DashboardSection.tsx` — **colapsable** (D12), manteniendo `loading`/`error`/`empty`/`dropTarget`.
- `dashboards/schemas.ts` + `types.ts` — campo `folder` con `path`, params `folder_id` / `unfiled`.
- `locales/{es,en,pt}/dashboards.main.json` — keys nuevas bajo `dashboardsMain.sidebar.folders.*`.

### Puntos técnicos que el handoff debe cerrar

1. **Estrategia de datos — ya decidida por D15:** una query de **todas** las carpetas (sin paginar) + una query paginada **por carpeta al expandir**. Los contadores vienen del BE. Es coherente con el scroll infinito existente y con carpetas colapsadas por defecto (I2).
2. **Query keys nuevas** y qué invalida qué al mover/crear/borrar (el panel ya tiene un mapa fino de invalidaciones para favoritos — seguirlo). Ojo: mover una carpeta invalida el **subárbol entero**, no una key.
3. **Optimistic updates:** mover un tablero debe sentirse instantáneo. Molde en `utils/favoriteOptimisticUpdates.ts` (mutate → rollback → settled). Mover una **carpeta** probablemente no conviene optimista: reescribe paths.
4. **Persistencia del estado de expansión:** `localStorage`, y **dos claves separadas** — carpetas expandidas y secciones colapsadas (D12), porque la segunda guarda lo colapsado y la primera lo abierto. Precedente: `SIDEBAR_COLLAPSED_KEY = "oc_sidebar_collapsed"`.
5. **Transaccionalidad de las operaciones en lote (D8/D9):** con 1 + N llamadas, una falla parcial deja la carpeta a medio llenar y el "Deshacer" deja de ser confiable. **El punto de negociación más importante con BE.**
6. **Revelar después de actuar:** al crear, mover, agregar o renombrar, se abre **toda la cadena de ancestros**, se hace scroll y se resalta ~2s. Con anidamiento esto es más crítico que antes: expandir la hoja sin expandir la madre no revela nada.
7. **Drag & drop (D7):** reusar `useDashboardCrossDrag` con un MIME nuevo (`DASHBOARD_TO_FOLDER_MIME`), **no** traer `@formkit/drag-and-drop`. A resolver: (a) drop sobre carpeta **colapsada** sin expandirla, (b) autoscroll al arrastrar fuera del viewport, (c) que una fila arrastrada no active a la vez el drop target de Favoritos y el de carpetas, (d) **arrastrar una carpeta** sobre otra respeta ciclo y tope. Equivalente por menú y teclado **obligatorio**; si el alcance aprieta, se corta el drag, no el menú.
8. **Telemetría:** `folder_created`, `subfolder_created`, `folder_moved`, `dashboard_moved_to_folder`, `dashboard_removed_from_folder`, `folder_deleted`, `folder_expanded`, `section_collapsed`, `search_used`. Incluir `depth` en los de carpeta: es el dato que dirá si 3 niveles alcanzan.
9. **Feature flag:** el panel es la navegación principal del OC; un flag reduce el riesgo.

### Lo que NO entra en este handoff

**El ancho útil de la fila (D14)** — truncado al medio y botones en hover — se extrajo a
un issue aparte porque no depende de carpetas y mejora la lista tal como está hoy:
[`ancho-util-lista-tableros/`](../../ancho-util-lista-tableros/).

El prototipo los tiene activos, así que al comparar capturas hay que tenerlo presente:
parte de la mejora visual que se ve ahí **no la entrega SWAT-577**.

---

## 4. Documentación para usuario final (criterio C8)

Borrador de la ayuda: qué es una carpeta, cómo crear una subcarpeta, cómo mover tableros y carpetas, qué pasa al eliminar una carpeta (el contenido sube, no se pierde), el tope de 3 niveles, y que la búsqueda encuentra en cualquier carpeta.

## 5. Definition of done

- [ ] Los 3 documentos escritos, con capturas del prototipo.
- [ ] `07-antes-despues.md` enumera cada cambio contra archivos reales de producción.
- [ ] Contrato de API completo: rutas, payloads, códigos de error, y **D15 resuelta en el documento**, no delegada.
- [ ] Modelo con `parent_id` + `path`, los dos índices parciales, y el `CHECK` de profundidad.
- [ ] Reparentado de D6 especificado como transacción, no como FK.
- [ ] Lista cerrada de archivos FE nuevos/modificados y de keys de i18n.
- [ ] Eventos de telemetría definidos, con `depth`.
- [ ] Riesgos y trade-offs escritos.
- [ ] Revisado con un dev de FE y uno de BE antes de crear los tickets.

## 6. Riesgos

- **Handoff que describe pantallas y no contratos** — sin el contrato de API, BE lo inventa y FE lo descubre en integración.
- **Copiar el prototipo tal cual.** Su árbol es client-side sobre la lista completa. Es el riesgo #1 de este handoff: se ve implementable y no lo es (D15).
- **Confiar el tope de 3 niveles solo a la UI.** Sin `CHECK` en el modelo, un import o un script lo rompe y el `path` deja de tener largo acotado.
- **La unicidad en la raíz** — el `NULL` de Postgres hace pasar duplicados si se usa un solo `UniqueConstraint`.
- **Duplicar el diálogo de carpeta** que ya existe en Almacenamiento en vez de reusarlo o extraerlo a `shared/`.
