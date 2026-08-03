# SWAT-577 — Carpetas en la lista de tableros · Índice de planes

**Issue:** [SWAT-577](https://linear.app/simetrik/issue/SWAT-577/enhancement-dashboards-add-folderorganization-structure-for-dashboard) · Backlog · High · Operation Center · Swat AI
**Proyecto local:** `Add folder organization structure for dashboard list/`
**Exploración técnica base:** [`handoff/00-exploracion-fe-be.md`](../handoff/00-exploracion-fe-be.md) ✅

---

## El problema, en una línea

Los usuarios del OC acumulan tableros (155 en la cuenta de la captura) en una lista plana e infinita;
el buscador exige **recordar** el nombre. Necesitamos un mecanismo de **reconocimiento**: agrupar por carpetas.

## Objetivos

- **Experiencia:** bajar el tiempo para encontrar un tablero reduciendo carga cognitiva (Ley de Miller: chunks de 5–9 en vez de una lista de 155).
- **UX:** dar un camino de navegación **además** del buscador — reconocer antes que recordar.
- **UI:** 100 % desyk, siguiendo los patrones de producto ya establecidos de crear / editar / eliminar, con flujos de **una tarea a la vez**.

## Criterios (del issue + del brief de UX)

| # | Criterio | Etapa donde se resuelve |
|---|----------|------------------------|
| C1 | Crear, renombrar y borrar carpetas (borrar = desagrupar, nunca eliminar tableros) | 4, 6, 7 |
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
| 0.5 | Decisiones de modelo (D1–D7) | `handoff/01-decisiones.md` | ✅ Cerradas |
| 1 | [Benchmark acotado](01-benchmark.md) | `handoff/01-benchmark.md` — I1–I6 resueltas | ✅ Hecha |
| 2 | [design.md desde desyk](02-design-md-desyk.md) | `design.md` + `design/tokens.css` + `design/tailwind.desyk.js` | ✅ Hecha |
| 3 | [Vista espejo HTML del panel actual](03-vista-espejo-html.md) | `prototypes/00-baseline-tableros.html` | ✅ Hecha — falta revisión visual lado a lado |
| 4 | [User flows en Moka](04-userflows.md) | 7 flows + sitemap en `.ohana/flow.json` + `handoff/04-userflows.md` | ✅ Hecha |
| 5 | [User stories UX](05-user-stories.md) | `handoff/05-user-stories.md` — 8 historias + revisión heurística | ✅ Hecha |
| 6 | [Prototipo HTML con carpetas](06-prototipo-carpetas.md) | `prototypes/index.html` (A/B + antes/después) | ✅ Hecha — falta revisión visual |
| 7 | [Handoff FE + BE](07-handoff-fe-be.md) | `handoff/07-handoff-fe.md`, `handoff/07-handoff-be.md` | ⬜ |
| 8 | [Tickets en Linear](08-linear.md) | sub-issues por sistema colgando de SWAT-577 | ⬜ |

**Dependencias reales:** 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8.
La única que se puede adelantar en paralelo es la 3 (vista espejo), porque replica lo que **ya existe**.

---

## Decisiones de modelo — ✅ cerradas el 2026-08-03

Registro completo con razones y consecuencias: [`handoff/01-decisiones.md`](../handoff/01-decisiones.md)

| # | Decisión | Resultado |
|---|----------|-----------|
| **D1** | Scope | **Por cuenta** (compartidas). Habilita columna `folder_id` en `dashboards`. Sin permiso nuevo: mismo umbral que crear un tablero. |
| **D2** | Profundidad | **Un solo nivel.** Sin subcarpetas en el MVP. |
| **D3** | Pertenencia | **Exclusiva** — un tablero, una carpeta. "Mover a carpeta", nunca "agregar a". |
| **D4** | Convivencia | Carpetas **dentro** de "Tableros". Favoritos y Pendientes intactos. Un tablero puede ser favorito **y** estar en una carpeta. |
| **D5** | Orden A→Z | El toggle existente aplica en **cada nivel**. Sin control nuevo. |
| **D6** | Eliminar carpeta | **Desagrupa siempre** (`ON DELETE SET NULL`). El diálogo dice el número de tableros que vuelven a la lista. |
| **D7** | Mover | **Menú `⋮` primario + drag como atajo**, ambos en la v1. Paridad por teclado obligatoria. |
| **D8** | Crear carpeta | **Wizard de 2 pasos** (elegir tableros → nombre) con resumen de lo que se guarda, y la carpeta se **revela** al crearse. Revierte «la carpeta nace vacía» tras probar el prototipo. |

**Fuera de alcance de la v1:** anidación · etiquetas · permisos por carpeta · carpetas personales · multi-selección **como modo del panel** (sí existe dentro del wizard de creación, D8) · orden manual de carpetas · colores de carpeta.

## Decisiones de interacción — ✅ cerradas el 2026-08-03

Registro con evidencia: [`handoff/01-benchmark.md`](../handoff/01-benchmark.md)

| # | Resultado |
|---|-----------|
| **I1** | Botón icono `FolderPlus` + tooltip en el **header de la sección "Tableros"**, junto al toggle A→Z. Deshabilitado durante la búsqueda. Entrada secundaria dentro del selector de "Mover a carpeta". |
| **I2** | **Colapsadas** por defecto · se revela la carpeta del tablero activo · estado persistido en `localStorage` · con una sola carpeta, expandida. |
| **I3** | **Segunda línea en la fila** con icono + nombre de carpeta (`text-[11px] muted`), clickable para revelar la carpeta. Carpetas que coinciden, primero. Divergencia deliberada con Almacenamiento: la búsqueda **no** se acota a la carpeta. |
| **I4** | Mismo `text-sm` que un tablero + **`font-medium`** + icono + chevron + contador `11px` + hijos indentados 16px con guía de 1px. Sin fuente mayor, sin mayúsculas, sin color de acento. |
| **I5** | Sin tope duro. Objetivo 7 ± 2 · aviso suave > 15 · máximo técnico 50. Lo que se vigila es el **% de tableros sueltos**, no el número de carpetas. |
| **I6** | Componente propio en `features/dashboards` sobre `DashboardNameField`. **No** se reusa el validador de Almacenamiento. Sí se reusa el léxico. |

### ⚠️ Dos hallazgos del benchmark que hay que arrastrar a todas las etapas

1. **La validación de nombres de Almacenamiento rechaza tildes y `_`** (`/^[a-zA-Z0-9- ]+$/`): "Conciliación diaria" y "Tesorería" no pasan. Las carpetas de tableros usan las reglas de nombre de **tablero** (máx 100, sin patrón).
2. **En Almacenamiento "Eliminar carpeta" borra el contenido; acá desagrupa.** Mismo botón, consecuencia opuesta. El copy debe **romper activamente** la expectativa: *"Los 24 tableros que contiene volverán a la lista de tableros; no se eliminarán."*
3. **Colapsar carpetas no alcanza:** con 4 carpetas + 111 sueltos quedan ~115 filas. La métrica que importa es **% de tableros dentro de una carpeta**, y la primera mejora a desbloquear si la adopción se estanca es la **multi-selección**.

---

## Convenciones del proyecto

- Carpetas: `prototypes/` (HTML) · `plans/` (estos planes) · `handoff/` (docs para el repo/equipo) · `design/` + `design.md` (sistema de diseño) · `.ohana/` (flows de Moka).
- Stack de prototipo: Tailwind CDN + Alpine.js + Lucide, tokens desyk vía `design/tokens.css`.
- Idioma de la UI y los docs: español. Glosario Simetrik obligatorio (**tablero**, no "dashboard", en el copy de cara al usuario).
- Demos con alternativas → switch A/B visible + nota para recoger feedback antes del handoff.
