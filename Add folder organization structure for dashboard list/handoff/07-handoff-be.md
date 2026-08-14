# Handoff BE — Carpetas en la lista de tableros (SWAT-577)

**Repo:** `op-center-backend` · app `apps/dashboards/` · verificado en `8cc5bc3b`
**Alcance:** solo Tableros (D10). Datasets, Anomalías y Pendientes **no se tocan**.
**Campo verde:** `grep -ril folder apps/ migrations/` → 0 resultados. No hay nada que migrar.

Decisiones que gobiernan este documento: [`01-decisiones.md`](01-decisiones.md) — en
particular **D1** (scope de cuenta), **D2** (3 niveles), **D3** (pertenencia exclusiva),
**D6** (eliminar disuelve un nivel) y **D15** (agrupamiento server-side).

---

## 0. Lo primero, porque condiciona todo lo demás

**El frontend nunca tiene la lista completa de tableros.** Verificado:

| Hecho | Fuente |
|---|---|
| `DASHBOARDS_PAGE_SIZE = 20` con `useInfiniteQuery` + `IntersectionObserver` | `fe-solutions-mf` · `DashboardList.tsx:117` |
| `page_size` con tope duro `le=100` | `utils/common/dependencies/pagination.py:8` |
| `search`, `sort_by`, `sort_order` ya son server-side | `apps/dashboards/api/views/dashboards.py:68-106` |

Con 155 tableros y tope de 100 por página no existe un «traer todo». Por eso **el
agrupamiento no puede resolverse en el cliente** (D15), y por eso el contrato de abajo
separa dos cosas:

- **Las carpetas son pocas** (I5: objetivo 7±2, aviso >15, tope técnico 50) → van **completas y sin paginar**, con sus contadores ya calculados.
- **Los tableros son muchos** → van **paginados por carpeta**, y se piden **al expandir**.

> ⚠️ **El prototipo HTML construye el árbol en cliente** recorriendo los 159 tableros en
> memoria y calculando los contadores de subárbol ahí. Es válido como exploración de
> interacción y **no es implementable tal cual**. Si se copia esa forma, el árbol se rompe
> en la segunda página.

---

## 1. Modelo

### 1.1 `dashboard_folders` — nueva tabla

```python
# apps/dashboards/domain/models/dashboard_folder.py

class DashboardFolder(Base):
    __tablename__ = "dashboard_folders"

    id:         Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name:       Mapped[str]       = mapped_column(String(255), nullable=False)
    account_id: Mapped[str]       = mapped_column(String(255), nullable=False, index=True)   # D1

    # D2 — anidamiento de 3 niveles
    parent_id:  Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("dashboard_folders.id", ondelete="RESTRICT"),   # ver §1.3
        nullable=True, index=True,
    )
    path:       Mapped[str] = mapped_column(String(120), nullable=False, index=True)

    created_by: Mapped[str | None] = mapped_column(String(255), nullable=True)   # D1, trazabilidad
    created_at / updated_at
```

**Molde seguido:** `DashboardFavorite` (`domain/models/dashboard_favorite.py`) — mismo
patrón de `account_id` indexado y `created_at`. La diferencia es que **no lleva `user_id`**:
D1 decidió scope de cuenta, así que no hay fila por usuario.

### 1.2 `path` materializado — la pieza clave

`path` guarda la cadena de ancestros incluyendo la propia carpeta:

```
Adquirencia                    /a1b2c3/
Adquirencia › Visa             /a1b2c3/d4e5f6/
Adquirencia › Visa › Contrac.  /a1b2c3/d4e5f6/g7h8i9/
```

Resuelve **tres** necesidades que si no requieren tres mecanismos distintos:

| Necesidad | Con `path` | Sin `path` |
|---|---|---|
| Guarda de ciclos (D2) | `dest.path LIKE folder.path \|\| '%'` | CTE recursivo en cada move |
| `subtree_count` (el contador visible) | `WHERE path LIKE '/a1b2c3/%'` | CTE recursivo por carpeta |
| Tope de 3 niveles (D2) | contar separadores → `CHECK` | validación solo en aplicación |

`String(120)` alcanza: 3 niveles × (32 hex + 1 separador) + 1 = 100 caracteres.

**Costo:** mover una carpeta reescribe el `path` de todo su subárbol. Aceptable — mover es
raro y con tope 3 los subárboles son chicos. **Alternativa a evaluar por BE:** la extensión
`ltree` de Postgres da los mismos beneficios con operadores nativos (`<@`, `nlevel()`); la
decisión es de BE, no de UX.

**`CHECK` de profundidad** (la UI no puede ser la única guarda):

```sql
ALTER TABLE dashboard_folders ADD CONSTRAINT ck_folder_max_depth
  CHECK (length(path) - length(replace(path, '/', '')) <= 4);  -- 3 niveles = 4 separadores
```

### 1.3 Unicidad de nombre — **el gotcha de Postgres**

D2 cambió la unicidad de global a **entre hermanas**: `Adquirencia / 2026` y
`Cierre contable / 2026` deben convivir.

> ⚠️ **`UniqueConstraint("account_id", "parent_id", lower(name))` NO funciona en la raíz.**
> En Postgres los `NULL` son **distintos entre sí**, así que dos carpetas de primer nivel
> con el mismo nombre pasarían la restricción sin error.

Solución — **dos índices parciales**:

```sql
CREATE UNIQUE INDEX uq_folder_sibling_name
  ON dashboard_folders (account_id, parent_id, lower(name))
  WHERE parent_id IS NOT NULL;

CREATE UNIQUE INDEX uq_folder_root_name
  ON dashboard_folders (account_id, lower(name))
  WHERE parent_id IS NULL;
```

Reglas de nombre: `trim`, case-insensitive, máx **100** caracteres. **Sin patrón de
caracteres** — el validador de Almacenamiento (`/^[a-zA-Z0-9- ]+$/`) rechaza tildes y `_`,
así que «Conciliación diaria» no pasaría. Se usan las reglas de nombre de **tablero**.

### 1.4 Asignación tablero ↔ carpeta

**D1 + D3 → columna en `dashboards`**, no tabla puente:

```python
# apps/dashboards/domain/models/dashboard.py
folder_id: Mapped[uuid.UUID | None] = mapped_column(
    UUID(as_uuid=True),
    ForeignKey("dashboard_folders.id", ondelete="SET NULL"),
    nullable=True, index=True,
)
```

- **D3 (pertenencia exclusiva)** queda garantizada por el esquema, no por lógica.
- **D1 (por cuenta)** hace innecesario el `user_id`.
- La tabla puente solo haría falta para carpetas personales o pertenencia múltiple, ambas
  fuera de alcance. Si llegan, se **suman sin migrar** lo existente.

> **`ON DELETE SET NULL` ya no implementa el feature — ver §3.** Se conserva como red de
> seguridad, no como mecanismo.

---

## 2. Endpoints

### 2.1 Nuevos

| Método | Ruta | Contrato |
|--------|------|----------|
| `GET` | `/dashboards/folders` | **Todas las carpetas, sin paginar.** Cada una: `{ id, name, parent_id, path, depth, direct_count, subtree_count }`. Es el endpoint que hace innecesario contar en cliente. |
| `POST` | `/dashboards/folders` | `{ name, parent_id?: UUID, dashboard_ids?: UUID[] }` → crea **y asigna en una transacción** (D8). `409` nombre duplicado entre hermanas · `422` excede 3 niveles. |
| `PATCH` | `/dashboards/folders/{id}` | `{ name }` → renombrar. `409` duplicado entre hermanas · `404` · `403` cross-account. |
| `PATCH` | `/dashboards/folders/{id}/parent` | **Mover carpeta (D2, nuevo).** `{ parent_id: UUID \| null }`. `null` = primer nivel. Ver §4. |
| `DELETE` | `/dashboards/folders/{id}` | **Disolver (D6).** Ver §3. Devuelve `{ dashboards_moved, subfolders_moved, moved_to: UUID \| null }` para el copy del toast. |
| `PATCH` | `/dashboards/{id}/folder` | `{ folder_id: UUID \| null }` → mover un tablero (`null` = quitar). Flujos F2 y F3. |
| `PATCH` | `/dashboards/folder` | **Lote (D9).** `{ dashboard_ids: UUID[], folder_id }`. **Devuelve el `folder_id` anterior de cada tablero** — sin eso el "Deshacer" no es posible. Flujo F8. |

### 2.2 Cambios en `GET /dashboards`

```
+ folder_id: UUID | None    → tableros DIRECTOS de esa carpeta (no del subárbol)
+ unfiled: bool             → tableros sin carpeta
```

Y en `DashboardSummaryOut`, embebido igual que `favorite`:

```python
class FolderInfo(BaseModel):
    id: UUID
    name: str
    path: str        # «Adquirencia / Visa» — resuelto a nombres, no a UUIDs

folder: FolderInfo | None
```

> **El `path` legible es un requisito de UX, no un extra.** Los resultados de búsqueda
> muestran la ruta completa (`Adquirencia / Visa`) porque con anidamiento puede haber tres
> carpetas «2026» y el nombre solo no desambigua. Sin `path` en la respuesta, el FE
> necesitaría un segundo fetch por resultado.

**`search` ignora `folder_id` y `unfiled`** para cumplir C5 (la búsqueda cruza todas las
carpetas). Es contra-intuitivo → **documentarlo explícito en el Swagger**.

---

## 3. Eliminar una carpeta = disolver un nivel (D6)

**Lo que cambió:** antes se apoyaba en `ON DELETE SET NULL` («lo garantiza el motor de base
de datos»). Con anidamiento eso **teletransporta** los tableros de una subcarpeta profunda al
primer nivel. El usuario que elimina «Visa» espera que sus tableros queden en «Adquirencia».

**Implementación — transacción de tres pasos:**

```sql
BEGIN;
  -- 1. los tableros suben a la madre
  UPDATE dashboards
     SET folder_id = :parent_id
   WHERE folder_id = :id;

  -- 2. las subcarpetas suben a la madre y se les reescribe el path
  UPDATE dashboard_folders
     SET parent_id = :parent_id,
         path = :parent_path || substring(path from length(:own_path) + 1)
   WHERE path LIKE :own_path || '%' AND id <> :id;

  -- 3. y ahora sí, borrar
  DELETE FROM dashboard_folders WHERE id = :id;
COMMIT;
```

Si `parent_id` es `NULL`, los tableros quedan sueltos y las subcarpetas pasan a primer nivel
— que es el comportamiento anterior, ahora como caso particular.

> **Consecuencia de test, no negociable.** Perdimos la garantía de motor. Que **eliminar una
> carpeta no elimine tableros** es criterio explícito del issue, así que pasa a ser un test
> obligatorio de la suite de BE:
>
> - eliminar carpeta de nivel 1 → tableros quedan sueltos, subcarpetas a primer nivel
> - eliminar carpeta de nivel 2 → tableros y subcarpetas suben a la de nivel 1
> - eliminar carpeta con 0 contenido → no afecta nada más
> - en todos: `SELECT count(*) FROM dashboards` **no cambia**

---

## 4. Mover una carpeta (D2, operación nueva)

`PATCH /dashboards/folders/{id}/parent` con `{ parent_id }`.

Dos validaciones, ambas **dentro de la transacción** (si se hacen antes, hay carrera):

**a) Ciclo — `409`.** Una carpeta no puede colgar de su propio subárbol.

```sql
-- rechazar si el destino está dentro del subárbol de la carpeta que se mueve
SELECT 1 FROM dashboard_folders
 WHERE id = :new_parent_id AND path LIKE (SELECT path FROM dashboard_folders WHERE id = :id) || '%';
```

**b) Profundidad — `422`.** No basta con mirar el destino: hay que sumar la **altura** del
subárbol que se mueve.

```
depth(destino) + 1 + altura(carpeta_movida)  <=  3
```

> Este es el caso que se escapa si se valida solo el destino: **«Adquirencia» (que arrastra
> «Visa › Contracargos») no cabe dentro de «Conciliación diaria»**, aunque esa carpeta esté en
> el nivel 1 y parezca que hay lugar. La UI ya no ofrece esos destinos, pero el BE tiene que
> rechazarlos igual.

**Después de validar:** reescribir el `path` de todo el subárbol (mismo `UPDATE` del paso 2
de §3, con el nuevo prefijo).

---

## 5. Contadores

El endpoint de carpetas devuelve **dos** números por carpeta:

| Campo | Qué es | Query |
|---|---|---|
| `direct_count` | tableros con `folder_id = <id>` | `GROUP BY folder_id` |
| `subtree_count` | tableros en la carpeta **y sus descendientes** | join por `path LIKE` |

**El que se muestra en la UI es `subtree_count`.** Colapsada, «24» significa «hay 24 acá
dentro», no «24 sueltos y quién sabe cuántos más abajo». `direct_count` alimenta el desglose
del tooltip (*«16 directos · 24 en total»*).

> Esta es la lección de Grafana ([#124158](https://github.com/grafana/grafana/issues/124158)):
> un contador que significa cosas distintas según el contexto se rompe al anidar. Acá se
> define una sola vez.

**Requisito de performance:** ambos en **una sola query agregada**, no N+1. Con ≤50 carpetas
por cuenta es un join sobre `dashboards` agrupado por prefijo de `path`.

---

## 6. Reglas de negocio — checklist

1. Eliminar carpeta **nunca** elimina tableros (criterio del issue · D6) → test obligatorio.
2. Eliminar carpeta **sube el contenido un nivel**, no a la raíz (D6 revisada).
3. Tope de **3 niveles**, validado en servicio **y** con `CHECK` sobre `path`.
4. **Ciclos** imposibles: validación por prefijo de `path` dentro de la transacción.
5. Nombre único **entre hermanas**, case-insensitive, con trim → los **dos** índices parciales de §1.3.
6. Nombre: máx 100, **sin patrón de caracteres** (tildes y `_` válidos).
7. Borrado de tablero: la asignación desaparece con la fila. Sin limpieza extra.
8. Cross-account → `403`; inexistente → `404`.
9. **No** hace falta `require_user_id` (D1: el scope es la cuenta) — pero sí registrar `created_by` cuando haya identidad.
10. Máximo de carpetas por cuenta: **50** técnico (I5). El aviso de >15 es de UI.
11. `GET /dashboards` no puede degradarse: índice por `folder_id`.
12. Las operaciones en lote (D8/D9) son **transaccionales**: con 1+N llamadas, una falla parcial deja la carpeta a medio llenar y el "Deshacer" deja de ser confiable. **Es el punto de negociación con FE.**

---

## 7. Convenciones del repo a cumplir

`apps/dashboards/` DDD (`api/views` → `services` → `domain/repositories` → `domain/models`),
DI por `container.py`, migración Alembic registrada, tests en `tests/apps/dashboards/`, plan
del cambio en `docs/plans/YYYY-MM-dd-<slug>.md`, `make check-code` + `make test` verdes.

Detalles de auth reutilizables ya presentes: `AUTH_FAILURE_RESPONSES` y `DASHBOARD_SCOPES`
estandarizan los responses; `resolve_user_id(auth)` para el `created_by`.

---

## 8. Migración

No hay backfill: **todo tablero arranca sin carpeta** (`folder_id = NULL`). El empty state de
carpetas y el onboarding del primer uso son parte del diseño de FE, no de una migración de datos.

---

## 9. Preguntas abiertas para BE

| # | Pregunta | Impacto |
|---|---|---|
| 1 | ¿`path` como `String` o extensión `ltree`? | `ltree` da operadores nativos; `String` no necesita extensión |
| 2 | ¿`subtree_count` calculado o materializado? | Con ≤50 carpetas el join alcanza; si crece, columna denormalizada |
| 3 | ¿El lote de D9 en un endpoint propio o reusando `PATCH /dashboards/folder`? | Afecta la transaccionalidad del punto 12 |
| 4 | ¿`ondelete` del `parent_id` en `RESTRICT` o `CASCADE`? | Propuesto `RESTRICT`: el servicio siempre reparenta antes, así que un `CASCADE` solo podría hacer daño silencioso |
