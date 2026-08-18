# SWAT-577 — Carpetas en la lista de tableros · Índice de planes

**Issue:** [SWAT-577](https://linear.app/simetrik/issue/SWAT-577/enhancement-dashboards-add-folderorganization-structure-for-dashboard) · Backlog · High · Operation Center · Swat AI
**Proyecto local:** `Add folder organization structure for dashboard list/`
**Exploración técnica base:** [`handoff/00-exploracion-fe-be.md`](../handoff/00-exploracion-fe-be.md) ✅

---

## El problema, en una línea

Los usuarios del OC acumulan **tableros** en una lista plana e infinita;
el buscador exige **recordar** el nombre. Necesitamos un mecanismo de **reconocimiento**: agrupar por carpetas.

> **⚠️ El alcance se recortó y la profundidad se abrió (2026-08-14).** Dos cambios que
> revierten decisiones anteriores:
>
> 1. **Solo Tableros.** Se descarta el sistema transversal a las 4 entidades que se había
>    ampliado el 2026-08-04. Datasets conserva su lista plana; Anomalías y Pendientes
>    quedan fuera. Ver **D10 (revisada)**.
> 2. **Anidamiento hasta 3 niveles**, revirtiendo «un solo nivel». Ver **D2 (revisada)**.
>
> Lo diseñado antes **sobrevive casi todo**: la tabla BE vuelve a ser específica de tableros
> y suma `parent_id`; el componente se queda en `features/dashboards`; se caen los
> entregables por entidad y entran los de anidamiento.

## Objetivos

- **Experiencia:** bajar el tiempo para encontrar un tablero reduciendo carga cognitiva (Ley de Miller: chunks de 5–9 en vez de una lista de 155).
- **UX:** dar un camino de navegación **además** del buscador — reconocer antes que recordar.
- **UI:** 100 % desyk, siguiendo los patrones de producto ya establecidos de crear / editar / eliminar, con flujos de **una tarea a la vez**.

## Criterios (del issue + del brief de UX)

| # | Criterio | Etapa donde se resuelve |
|---|----------|------------------------|
| C1 | Crear, renombrar y borrar carpetas (borrar = disolver, nunca eliminar tableros) | 4, 6, 7 |
| C2 | Agregar tableros a una carpeta | 4, 6, 7 |
| C3 | Quitar un tablero de la carpeta sin eliminarlo | 4, 6, 7 |
| C4 | Las carpetas tienen **más jerarquía visual** que los tableros sueltos | 2, 6 |
| C5 | El buscador devuelve resultados de **cualquier** carpeta | 4, 6, 7 |
| C6 | UI alineada al desyk y a los patrones de crear/editar/eliminar | 2, 6 |
| C7 | Un flujo por tarea; sin acciones múltiples que confundan | 4, 6 |
| C8 | Documentado para usuario final | 7, 8 |

---

## Etapas — se abordan **una a una**

| # | Etapa | Entregable | Estado |
|---|-------|-----------|--------|
| 0 | Exploración FE / BE | `handoff/00-exploracion-fe-be.md` | ✅ Hecha |
| 0.5 | Decisiones de modelo (D1–D7) | `handoff/01-decisiones.md` | ✅ Cerradas · D2 y D6 revisadas |
| 1 | [Benchmark acotado](01-benchmark.md) | `handoff/01-benchmark.md` — I1–I6 resueltas | ✅ Hecha · I4 revisada |
| 2 | [design.md desde desyk](02-design-md-desyk.md) | `design.md` + `design/tokens.css` + `design/tailwind.desyk.js` | ✅ Hecha |
| 3 | [Vista espejo HTML del panel actual](03-vista-espejo-html.md) | `prototypes/00-baseline-tableros.html` | ✅ Hecha — falta revisión visual lado a lado |
| 4 | [User flows en Moka](04-userflows.md) | flows + sitemap en `.ohana/flow.json` + `handoff/04-userflows.md` | ✅ Hecha · reescrita en 6.8 |
| 5 | [User stories UX](05-user-stories.md) | `handoff/05-user-stories.md` — 8 historias + revisión heurística | ✅ Hecha — **desactualizada**, ver 7 |
| 6 | [Prototipo HTML con carpetas](06-prototipo-carpetas.md) | `prototypes/index.html` (antes/después) | ✅ Hecha · **el A/B se cerró: ganó in-place (D16)** |
| ~~6.5~~ | ~~Alcance transversal (D10)~~ | `handoff/06-organizacion-transversal.md` | ⛔ **Descartada** (D10 revisada) — se conserva como registro |
| ~~6.5b~~ | ~~Benchmark transversal (T1–T6)~~ | `handoff/02-benchmark-transversal.md` | ⛔ **Descartada** — se conserva como registro |
| ~~6.5c~~ | ~~Flujos transversales F9, F10~~ | `.ohana/flow.json` | ⛔ **Revertida**: los flujos se borraron del board |
| 6.6 | Anidamiento hasta 3 niveles en el prototipo | `prototypes/index.html` — árbol, mover carpeta, ciclos, tope | ✅ Hecha |
| 6.7 | Secciones colapsables del panel | `prototypes/index.html` — Pendientes · Favoritos · Tableros · Sin carpeta | ✅ Hecha |
| 6.8 | Flujos reescritos al alcance real | F9–F12 nuevos + F1/F5/F6/F7 + sitemap corregidos | ✅ Hecha |
| 7 | [Handoff FE + BE](07-handoff-fe-be.md) | `handoff/07-handoff-fe.md` · `handoff/07-handoff-be.md` · `handoff/07-antes-despues.md` | ✅ Hecha — falta la revisión visual y las capturas |
| 8 | [Tickets en Linear](08-linear.md) | sub-issues colgando de SWAT-577 | ⬜ |
| **9** | [**Feedback del prototipo**](09-feedback-prototipo.md) | 5 hallazgos de la revisión en Ohana → D17–D20 | 🔄 **Feedback cerrado** — ②③④ resueltos, ①⑤ fuera. Falta re-sincronizar flujos y handoff |

**Dependencias reales:** 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8.
La única que se puede adelantar en paralelo es la 3 (vista espejo), porque replica lo que **ya existe**.

> **La Etapa 7 se escribió el 2026-08-14** e incluye el contrato de agrupamiento
> server-side (D15), que no existía cuando se planeó. Lo que queda abierto de ella son
> **las capturas antes/después** y la revisión visual contra el baseline.
>
> Antes de la Etapa 8 hay que revisar `handoff/05-user-stories.md`: se escribió con
> D2 = un nivel y D10 = transversal.
>
> **Y antes de la 8 va la [Etapa 9](09-feedback-prototipo.md):** la revisión del prototipo
> dejó 5 hallazgos, uno de los cuales —**el resize del panel**— reabre el presupuesto de
> ancho del que dependen D2, D13, D14 y D16. Cerrar tickets antes de resolver eso sería
> estimar sobre números que van a cambiar.
>
> **Al 2026-08-18:** ② quedó resuelto en el prototipo como **D17** (propuesta: falta elegir
> mecanismo), ③ se cerró como **D18** sin quitar el contador, y ⑤ se descartó. **D2 arrastra
> un error que hay que corregir igual:** su peor caso son 45 caracteres, no 40. Y salió un
> hallazgo que pesa más que ②: el **umbral de colapso mide el contenedor, no la ventana**, así
> que en un portátil de 1440px el panel arranca colapsado y el árbol no se ve.

---

## Decisiones de modelo

Cerradas el 2026-08-03 · **D2, D6 y D10 revisadas el 2026-08-14**.
Registro completo con razones y consecuencias: [`handoff/01-decisiones.md`](../handoff/01-decisiones.md)

| # | Decisión | Resultado |
|---|----------|-----------|
| **D1** | Scope | **Por cuenta** (compartidas). Habilita columna `folder_id` en `dashboards`. Sin permiso nuevo: mismo umbral que crear un tablero. |
| **D2** 🔄 | Profundidad | **3 niveles de carpeta** (`Adquirencia › Visa › Contracargos`); los tableros cuelgan de cualquiera y no cuentan como nivel. *Antes: un solo nivel.* La razón original de D2 sigue viva y es la que condiciona el diseño — ver abajo. |
| **D3** | Pertenencia | **Exclusiva** — un tablero, una carpeta. "Mover a carpeta", nunca "agregar a". |
| **D4** | Convivencia | Carpetas **dentro** de "Tableros". Favoritos y Pendientes intactos. Un tablero puede ser favorito **y** estar en una carpeta. |
| **D5** | Orden A→Z | El toggle existente aplica en **cada nivel**. Sin control nuevo. |
| **D6** 🔄 | Eliminar carpeta | **Disuelve un nivel**: tableros y subcarpetas suben a la carpeta madre, no a la raíz. *Antes: `ON DELETE SET NULL`.* Ya no es una FK — es lógica de servicio que reparenta antes de borrar. |
| **D7** | Mover | **Menú `⋮` primario + drag como atajo**, ambos en la v1. Paridad por teclado obligatoria. |
| **D8** | Crear carpeta | **Wizard de 2 pasos** (elegir tableros → nombre) con resumen de lo que se guarda, y la carpeta se **revela** al crearse. |
| **D9** | Llenar carpeta existente | **"Agregar tableros"** con selección múltiple: botón punteado en la carpeta vacía + ítem en el menú `⋮` de la carpeta. |
| **D10** 🔄 | Alcance | **Solo Tableros.** Datasets conserva su lista plana (el tab existe en producción y no se toca); Anomalías y Pendientes quedan fuera. *Antes: transversal a las 4 entidades con tabla `folders` compartida.* |
| **D12** ✨ | Secciones colapsables | Las 4 secciones del panel (Pendientes · Favoritos · Tableros · Sin carpeta) colapsan. Se persiste **lo colapsado**, no lo abierto, para que el default de toda sección sea «abierta». Clave de `localStorage` aparte. |
| **D13** ✨ | Chevron de carpeta | **El icono absorbe el chevron**: `folder` cerrada ↔ `folder-open` abierta. Un elemento menos y 16px recuperados. `aria-expanded` se conserva. |
| **D14** ↗️ | Ancho útil de la fila | **Extraída a un issue aparte** — no depende de carpetas. Ver [`ancho-util-lista-tableros/`](../../ancho-util-lista-tableros/). |
| **D15** ✨ | Agrupamiento server-side | **El árbol no se puede resolver en cliente.** La lista es paginada (`DASHBOARDS_PAGE_SIZE = 20`, scroll infinito) con `search` y `sort` server-side y tope duro de 100/página. Contrato requerido en la Etapa 7. |
| **D16** ✨ | Forma de navegar | **Árbol in-place.** Se descarta el drill-down por niveles: el gesto más frecuente es cambiar de tablero y navegar le suma clics justo a eso. Cierra I4. |
| **D17** 🟡 | Ancho del panel | **Tres anchos fijos: `sm` 288 · `md` 384 · `lg` 480**, persistidos por usuario. Cada valor está derivado de una pregunta, no elegido. **Mecanismo decidido:** arrastrar el borde, dibujando en azul la zona que va a ocupar — el rótulo `S/M/L` se descartó porque no dice hasta dónde llega el panel. Faltan de confirmar los tres valores. |
| **D18** ✨ | Contador de subcarpeta | **Se queda.** Quitarlo devolvía 20px; D17 devuelve 96 sin perder información. |
| ~~**D19**~~ | ~~Acordeón exclusivo~~ | ⛔ **Descartada** el 2026-08-18. D12 sigue igual: secciones independientes. |
| **D20** 🟡 | Permisos de carpeta | **Solo quien la creó** puede renombrar, mover o eliminar; `oc:manage_access` es el escape para las huérfanas. Agregar tableros y crear subcarpetas quedan libres — la carpeta es una ubicación compartida. **Revierte D1.b · a confirmar con BE.** |

### Por qué D2 conserva su razón original

D2 argumentaba carpetas planas porque **el panel mide 240px útiles y los nombres reales ya se truncan**
(`Adquirencia_2026_06_04_conciliacion_visa` son 40 caracteres). Esa restricción **no desapareció** al
abrir el anidamiento: es exactamente la que obliga a las tres mitigaciones del diseño actual.

| Mitigación | Sin ella |
|---|---|
| Indentación de **12px** por nivel (no 19) | al nivel 3 el nombre baja a ~120px |
| **Truncado al medio** fijando el último segmento | se pierde la cola, que es lo que desambigua |
| **Tope de 3 niveles** | la profundidad se vuelve ilimitada y el `path` del BE, impredecible |

Peor caso permitido hoy: **158px** para una carpeta de nivel 3, **166px** para un tablero dentro de ella.

**Fuera de alcance de la v1:** más de 3 niveles · etiquetas · permisos por carpeta · carpetas personales · multi-selección **como modo del panel** (sí existe dentro del wizard, D8) · orden manual de carpetas · colores de carpeta · carpetas en Datasets.

## Decisiones de interacción

Cerradas el 2026-08-03 · **I4 revisada el 2026-08-14**.
Registro con evidencia: [`handoff/01-benchmark.md`](../handoff/01-benchmark.md)

| # | Resultado |
|---|-----------|
| **I1** | Botón icono `FolderPlus` + tooltip en el **header de la sección "Tableros"**, junto al toggle A→Z. Deshabilitado durante la búsqueda. «Nueva subcarpeta» vive en el menú `⋮` de la carpeta, deshabilitado al llegar al tope de 3. |
| **I2** | **Colapsadas** por defecto · se revela **toda la cadena de ancestros** del tablero activo · estado persistido en `localStorage` · con una sola carpeta, expandida. |
| **I3** | **Segunda línea en la fila** con la **ruta completa** (`Adquirencia / Visa`), clickable para revelar la carpeta. Carpetas que coinciden, primero — y la ruta también es buscable. Divergencia deliberada con Almacenamiento: la búsqueda **no** se acota a la carpeta. |
| **I4** ✅🔄 | **Cerrada: árbol in-place** (D16). Mismo `text-sm` que un tablero + **`font-medium`** + icono de carpeta con estado (D13, **sin chevron**) + contador del **subárbol** + hijos indentados **12px** con guía de 1px. Sin fuente mayor, sin mayúsculas, sin color de acento. |
| **I5** | Sin tope duro de cantidad. Objetivo 7 ± 2 · aviso suave > 15 · máximo técnico 50. Lo que se vigila es el **% de tableros sueltos**, no el número de carpetas. |
| **I6** | Componente propio en `features/dashboards` sobre `DashboardNameField`. **No** se reusa el validador de Almacenamiento. Sí se reusa el léxico. **Unicidad entre hermanas**, no global: `Adquirencia / 2026` y `Cierre contable / 2026` conviven. |

### ⚠️ Hallazgos que hay que arrastrar a todas las etapas

1. **La validación de nombres de Almacenamiento rechaza tildes y `_`** (`/^[a-zA-Z0-9- ]+$/`): "Conciliación diaria" y "Tesorería" no pasan. Las carpetas de tableros usan las reglas de nombre de **tablero** (máx 100, sin patrón).
2. **En Almacenamiento "Eliminar carpeta" borra el contenido; acá disuelve.** Mismo botón, consecuencia opuesta. El copy debe **romper activamente** la expectativa: *"Sus 8 tableros y 1 subcarpeta suben a «Adquirencia»; no se eliminan."*
3. **Colapsar carpetas no alcanza:** con 4 carpetas + 111 sueltos quedan ~115 filas. La métrica que importa es **% de tableros dentro de una carpeta**. D12 (colapsar secciones) ayuda: baja de 59 a 26 filas visibles.
4. **El agrupamiento es server-side (D15).** Cualquier diseño que asuma la lista completa en memoria —contadores de subárbol, orden global, árbol completo— no es implementable. El prototipo lo hace en cliente **solo porque es un prototipo**.

---

## Convenciones del proyecto

- Carpetas: `prototypes/` (HTML) · `plans/` (estos planes) · `handoff/` (docs para el repo/equipo) · `design/` + `design.md` (sistema de diseño) · `.ohana/` (flows de Moka).
- Stack de prototipo: Tailwind CDN + Alpine.js + Lucide, tokens desyk vía `design/tokens.css`.
- Idioma de la UI y los docs: español. Glosario Simetrik obligatorio (**tablero**, no "dashboard", en el copy de cara al usuario).
- Demos con alternativas → switch A/B visible + nota para recoger feedback antes del handoff.
- **Los planes `01`–`06` no se reescriben** cuando una decisión cambia: documentan cómo se llegó a lo que existe. Las revisiones se registran acá y en `handoff/01-decisiones.md`.
