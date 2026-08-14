# Antes → Después — Carpetas en la lista de tableros (SWAT-577)

Convención del equipo: los cambios se enumeran contra el **estado real de producción**,
no contra una versión idealizada.

**Referencias verificadas:** `fe-solutions-mf` @ `8aebc1879` · `op-center-backend` @ `8cc5bc3b`
**Baseline visual:** [`prototypes/00-baseline-tableros.html`](../prototypes/00-baseline-tableros.html) — replica el panel de hoy
**Después:** [`prototypes/index.html`](../prototypes/index.html) — el panel de demo trae un switch **«Antes / después»** para comparar en vivo

---

## 0. Cómo leer esta tabla

Tres columnas de origen, porque no todo lo que se ve en el prototipo lo entrega este issue:

| Marca | Significado |
|---|---|
| **577** | Lo entrega SWAT-577 |
| **D14** | Lo entrega el issue aparte de [ancho útil](../../ancho-util-lista-tableros/) — se ve en el prototipo pero **no es de este issue** |
| **—** | No cambia |

---

## 1. Panel de Tableros — estructura

| # | Antes (hoy en producción) | Después | Origen | Archivo real |
|---|---|---|---|---|
| 1 | Sección `Tableros (155)` = lista plana paginada de 20 en 20 | Árbol de hasta **3 niveles** + sueltos después, con carga perezosa al expandir | **577** | `DashboardList.tsx`, `DashboardSection.tsx` |
| 2 | Sin disparador de crear carpeta | Icono `FolderPlus` en el header de la sección, junto al toggle A→Z | **577** | `DashboardList.tsx` |
| 3 | Las 3 secciones del panel no colapsan | Las **4** colapsan (entra `Sin carpeta`) y persisten | **577** | `DashboardSection.tsx` |
| 4 | Separador de sueltos no existe (todo es «sueltos») | Separador `Sin carpeta` con contador, colapsable | **577** | `DashboardList.tsx` |
| 5 | Toggle A→Z ordena la lista plana | Ordena carpetas entre sí **y** tableros dentro de cada nivel | **577** | server-side |

## 2. Fila de tablero

| # | Antes | Después | Origen | Archivo real |
|---|---|---|---|---|
| 6 | Menú `⋮` con 5 acciones | + `Mover a carpeta` · + `Quitar de la carpeta` (esta solo si está en una) | **577** | `DashboardListItem.tsx` |
| 7 | No es arrastrable | Drag source hacia carpetas (`DASHBOARD_TO_FOLDER_MIME`) | **577** | `DashboardListItem.tsx` |
| 8 | En búsqueda, la fila no dice dónde está | Segunda línea con la **ruta completa** (`Adquirencia / Visa`), clickable | **577** | `DashboardListItem.tsx` |
| 9 | Nombre truncado al final: `Adquirencia_2026_06_04_c…` | Truncado **al medio**: `Adquirencia_2026_06_04_conciliacion…_visa` | **D14** | `DashboardListItem.tsx` |
| 10 | El `⋮` reserva 20px invisibles en toda fila | El contenedor de acciones arranca en `w-0` y se abre en hover/focus | **D14** | `DashboardListItem.tsx` |

## 3. Fila de carpeta (nueva)

| # | Antes | Después | Origen |
|---|---|---|---|
| 11 | — | Fila de **32px**: icono con estado + nombre `font-medium` + `subtree_count` + `⋮` | **577** |
| 12 | — | **Sin chevron** — el icono lleva el estado (`folder` ↔ `folder-open`) · D13 | **577** |
| 13 | — | Hijos indentados **12px** con guía vertical de 1px | **577** |
| 14 | — | Menú `⋮`: `Agregar tableros` · `Nueva subcarpeta` · `Renombrar` · `Mover carpeta a…` · `Eliminar` | **577** |

## 4. Diálogos

| # | Antes | Después | Origen |
|---|---|---|---|
| 15 | — | `CreateFolderWizard` de 2 pasos, con `Dentro de: <ruta>` si hay madre | **577** |
| 16 | — | `MoveToFolderDialog` como **árbol con ruta** (no lista simple) + destino `Primer nivel` | **577** |
| 17 | — | `DeleteFolderDialog` diciendo **a dónde sube** el contenido | **577** |
| 18 | — | `DashboardPicker` compartido, **tope de 10 filas visibles** + scroll | **577** |

## 5. Contratos de datos

| # | Antes | Después | Origen | Archivo real |
|---|---|---|---|---|
| 19 | `dashboardItemSchema` sin carpeta | + `folder: { id, name, path } \| null` | **577** | `services/dashboards/dashboards/schemas.ts` |
| 20 | `GET /dashboards` sin filtro de carpeta | + `folder_id` · + `unfiled` | **577** | `api/views/dashboards.py` |
| 21 | No existe endpoint de carpetas | `GET/POST/PATCH/DELETE /dashboards/folders` + `PATCH /folders/{id}/parent` | **577** | `apps/dashboards/api/views/` |
| 22 | No existe entidad carpeta | Tabla `dashboard_folders` con `parent_id` + `path` + 2 índices parciales + `CHECK` de profundidad | **577** | migración Alembic |
| 23 | `dashboards` sin `folder_id` | + columna `folder_id` (FK, `SET NULL` como red de seguridad) | **577** | `domain/models/dashboard.py` |

## 6. Lo que NO cambia

| # | Qué | Por qué |
|---|---|---|
| 24 | Tab **Datasets** | D10 revisada: las carpetas son solo de Tableros. Sirve como control de que el feature no lo afectó |
| 25 | Sección **Favoritos** | D4. Un tablero puede ser favorito **y** estar en una carpeta — son cosas distintas: favorito = atajo, carpeta = ubicación |
| 26 | Sección **Configuraciones pendientes** | D4. Solo gana el chevron de colapsar (#3) |
| 27 | Vistas de **Anomalías** y **Pendientes** | D10 revisada. Sus tabs siguen siendo chrome del OC |
| 28 | Paginación e scroll infinito | Se conserva **por carpeta**. No se reemplaza: D15 lo confirma como restricción |
| 29 | Validación de nombre de tablero | Las carpetas reusan sus reglas (máx 100, sin patrón) |

---

## 7. Los cambios que más riesgo de regresión tienen

Puestos aparte porque son los que QA debe mirar primero:

| Riesgo | Qué se rompería | Cómo verificarlo |
|---|---|---|
| **La búsqueda deja de cruzar carpetas** | C5, criterio explícito del issue | Buscar un término que esté en 3 carpetas distintas y en sueltos → los 4 aparecen |
| **Eliminar carpeta borra tableros** | Criterio explícito del issue. Con D6 revisada ya no lo garantiza el motor de BD, es lógica de servicio | `count(*) FROM dashboards` no cambia al eliminar carpetas de cada nivel |
| **El contador miente** | Al anidar, un número que significa «directos» en un lugar y «subárbol» en otro | Carpeta con 16 directos y 8 en una hija debe mostrar **24** |
| **El árbol se rompe en la página 2** | D15: si alguien resuelve el agrupamiento en cliente | Carpeta con >20 tableros, scrollear dentro de ella |
| **Ciclo o exceso de profundidad** | Árbol corrupto | Mover una carpeta de altura 2 a un nivel 1 → debe rechazarse |
| **Favoritos y carpetas se pelean el drop** | Arrastrar un tablero activa los dos drop targets | Arrastrar desde Tableros hacia Favoritos y hacia una carpeta |

---

## 8. Capturas

> ⬜ **Pendiente.** Falta la revisión visual lado a lado contra el baseline (Etapas 3 y 6
> quedaron con esa tarea abierta). Cada fila de las tablas 1–4 debería llevar su par de
> capturas antes/después tomadas del prototipo.
>
> Mientras eso no esté, la comparación se hace en vivo: abrir
> [`prototypes/index.html`](../prototypes/index.html) y usar el switch **«Antes / después»**
> del panel de demo.
