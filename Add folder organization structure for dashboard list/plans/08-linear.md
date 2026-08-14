# Etapa 8 — Tickets en Linear

**Objetivo:** dejar SWAT-577 listo para entrar a un ciclo, con sub-issues por sistema y el handoff linkeado.
**Entregable:** SWAT-577 actualizado + sub-issues creados + doc ligera con links.
**Precondición:** Etapa 7 (el handoff es el insumo de los tickets).

> **Actualizado el 2026-08-14.** La descomposición cambió por tres decisiones: **D2**
> (3 niveles de anidamiento → sub-issues nuevos de BE y FE), **D10** (solo Tableros →
> se caen los sub-issues por entidad) y **D15** (agrupamiento server-side → S4 sube de
> prioridad y cambia de forma). Además **D14 sale de este issue** y necesita su propio
> issue padre.

---

## Convención del equipo

Las épicas se documentan **ligeras**: el issue padre describe el problema y **lista los sistemas involucrados**, con links al handoff;
el detalle vive en el handoff, no copiado en Linear. Los sub-issues se abren **por sistema**.

---

## 0. Un issue aparte, primero

**D14 — ancho útil de la fila** (truncado al medio + botones en hover) se extrajo de
SWAT-577 porque no depende de carpetas y mejora la lista tal como está hoy.
Handoff: [`ancho-util-lista-tableros/`](../../ancho-util-lista-tableros/).

Conviene abrirlo **como issue independiente y antes** que las carpetas: es solo FE,
un componente, y deja la fila con más ancho disponible justo cuando el anidamiento
va a empezar a consumirlo. Si se hace después, se mide dos veces.

---

## 1. Actualizar SWAT-577 (el padre)

Agregar a la descripción, sin reescribir el reporte original:

- **Objetivo de UX** y las leyes que lo sustentan (Miller · reconocer > recordar).
- **Links:** prototipo en GitHub Pages · `handoff/07-handoff-fe.md` · `handoff/07-handoff-be.md` · `handoff/07-antes-despues.md` · flows de Moka.
- **Sistemas involucrados:**
  - `op-center-backend` — modelo con `parent_id` + `path`, migración, CRUD de carpetas, mover carpeta, filtro en `GET /dashboards`
  - `fe-solutions-mf` — panel de Tableros (árbol, diálogos, servicios, i18n)
  - QA — plan de pruebas
  - Contenido/soporte — documentación de usuario final (C8)
- **Decisiones tomadas** (D1–D15) en una tabla de una línea cada una, marcando las **revisadas** (D2, D6, D10) con su fecha.
- **Fuera de alcance de la v1**: más de 3 niveles · etiquetas · permisos por carpeta · carpetas personales · multi-selección como modo del panel · colores · **carpetas en Datasets**.
- **Nota de alcance:** SWAT-577 **no** entrega el truncado al medio ni los botones en hover; eso es el issue de D14. Sin esta nota, el prototipo promete más de lo que el ticket cubre.

## 2. Sub-issues propuestos

| # | Título | Sistema | Depende de |
|---|--------|---------|-----------|
| S1 | BE — Modelo + migración: `dashboard_folders` con `parent_id` y `path`, los **dos índices parciales** de unicidad y el `CHECK` de 3 niveles | op-center-backend | — |
| S2 | BE — CRUD de carpetas (`GET`/`POST`/`PATCH`/`DELETE /dashboards/folders`) con `direct_count` y `subtree_count` en **una query agregada** | op-center-backend | S1 |
| S3 | BE — Eliminar carpeta = **reparentar a la madre** en transacción (D6), devolviendo qué subió | op-center-backend | S1 |
| S3b | BE — **Mover carpeta** (`PATCH /folders/{id}/parent`): guarda de ciclos por prefijo de `path`, guarda de profundidad, y reescritura del `path` del subárbol | op-center-backend | S1 |
| S4 | BE — `GET /dashboards`: `folder_id` / `unfiled` + `folder{id,name,path}` en la respuesta, **sin romper `search`** | op-center-backend | S1 |
| S5 | FE — Servicios y schemas de carpetas (`services/dashboards/folders/`) | fe-solutions-mf | S2, S4 |
| S6 | FE — `FolderTree`: árbol aplanado por `depth`, carga **perezosa al expandir**, jerarquía visual, contador de subárbol | fe-solutions-mf | S5 |
| S6b | FE — Secciones colapsables del panel (D12), con clave de `localStorage` propia | fe-solutions-mf | — |
| S7 | FE — Crear carpeta y **subcarpeta** / renombrar / eliminar (diálogos + unicidad entre hermanas + tope de 3 + toasts) | fe-solutions-mf | S5 |
| S8 | FE — Mover tablero a carpeta / quitar (menú + optimistic update) | fe-solutions-mf | S5, S6 |
| S8b | FE — **Mover carpeta**: diálogo de destinos como árbol con ruta, destino «Primer nivel», y ocultar destinos inválidos por ciclo o tope | fe-solutions-mf | S3b, S6 |
| S9 | FE — Búsqueda cross-carpeta con la **ruta completa** como metadato del resultado | fe-solutions-mf | S5, S6 |
| S10 | FE — Empty states, onboarding de la primera carpeta y telemetría (con `depth`) | fe-solutions-mf | S6 |
| S11 | FE — i18n es/en/pt de las keys nuevas | fe-solutions-mf | S7, S8 |
| S12 | QA — Plan de pruebas (incluye «eliminar carpeta no borra tableros», ciclos, tope de 3, y **paginación con árbol**) | QA | S1–S11 |
| S13 | Doc — Ayuda para usuario final (C8) | Contenido | S6–S9 |

**Atajo válido si el ciclo aprieta:** S1+S2 pueden ser un solo sub-issue de BE, y S6b es
independiente de todo (se puede entregar suelto y temprano, da valor sin carpetas).

**Lo que NO se colapsa:**

- **S4** — es donde vive D15. Si se mezcla, la paginación con árbol se resuelve a la carrera.
- **S3b** — ciclos y profundidad son las dos formas de corromper el árbol.
- **S12** — QA tiene que probar explícitamente que eliminar no borra.

Cada sub-issue lleva: criterios de aceptación de su historia (Etapa 5), link al handoff correspondiente y link al prototipo.

## 3. Trazabilidad historia ↔ ticket

Tabla en el handoff: HU-01…HU-08 → sub-issues que la implementan → criterio C1…C8 que cierra.
Sirve para verificar que ningún criterio del issue quedó sin ticket.

> ⚠️ **Las historias de la Etapa 5 están desactualizadas.** Se escribieron con D2 = un
> nivel y D10 = transversal. Antes de armar esta matriz hay que revisarlas: faltan
> historias de subcarpeta, mover carpeta y colapsar secciones, y sobran las de datasets
> y anomalías.

## 4. Definition of done

- [ ] SWAT-577 actualizado con objetivo de UX, sistemas, decisiones (marcando las revisadas), links y fuera de alcance.
- [ ] Nota explícita de que D14 va en otro issue.
- [ ] Issue de D14 abierto y linkeado como relacionado.
- [ ] Sub-issues creados con label por sistema y estimación pedida a cada dev.
- [ ] Cada sub-issue linkea handoff + prototipo; ninguno repite el detalle del handoff.
- [ ] Matriz de trazabilidad HU ↔ ticket ↔ criterio, sin huecos, **con las historias ya revisadas**.
- [ ] Dependencias declaradas en Linear (blocked by / blocks).
- [ ] El prototipo publicado y accesible desde el issue.

## 5. Riesgos

- **Copiar el handoff dentro de Linear:** se desincroniza al primer cambio. Linear linkea; el handoff es la fuente.
- **Sub-issues por pantalla en vez de por sistema:** rompe la convención y complica la asignación.
- **Abrir tickets sin resolver D15:** S6 y S4 quedan acopladas de una forma que nadie declaró, y el árbol se implementa contra una lista paginada sin contrato.
- **Prometer en el ticket lo que se ve en el prototipo:** el prototipo incluye D14, que no entrega este issue.
