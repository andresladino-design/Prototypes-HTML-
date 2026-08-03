# Etapa 4 — User flows en Moka

**Objetivo:** definir cada tarea como un flujo lineal, verificable, de **una tarea a la vez** (criterio C7).
**Entregables:** flows en `.ohana/flow.json` + `handoff/04-userflows.md` (narrativa + decisiones de interacción).
**Precondición:** Etapas 1 y 2 cerradas.

> Ya existe un flow vacío llamado **"Create folders in dashboards"** en `.ohana/flow.json` con una pantalla `P1`.
> Se reusa como flujo F1 y se renombra.

---

## Los 7 flujos (uno por tarea, ni más ni menos)

| ID | Flujo | Criterio que cubre | Board |
|----|-------|-------------------|-------|
| **F1** | Crear carpeta (primera vez → empty state) | C1 | userflow |
| **F2** | Agregar tablero(s) a una carpeta | C2 | userflow |
| **F3** | Quitar un tablero de la carpeta (sin eliminarlo) | C3 | userflow |
| **F4** | Renombrar carpeta | C1 | userflow |
| **F5** | Eliminar carpeta → desagrupar sus tableros | C1, D6 | userflow |
| **F6** | Buscar con carpetas presentes (resultados cross-carpeta) | C5 | userflow |
| **F7** | Navegar / colapsar-expandir carpetas y abrir un tablero | C4 | userflow |

Además, un **sitemap** corto que sitúe el panel dentro del OC: `Centro de operaciones → Tableros → panel lateral (Tableros / Datasets)`, para que el flow no quede huérfano de contexto.

---

## Convenciones de Moka a respetar (de `.ohana/MOKA.md`)

- Cada userflow: **`start` → backbone lineal de izquierda a derecha → `end`**. Un `next` por pantalla.
- `decision` en diamante con **2 salidas ya resueltas**: Sí en verde continúa el backbone, No en rojo es una rama corta que reingresa o termina.
- Reintentos reales marcados con `dir:"back"`.
- Anatomía por pantalla: **regiones → secciones → componentes**. Los componentes deben ser los de desyk que quedaron en el `design.md` (Etapa 2) — no inventar componentes fuera del sistema.
- Empty states como **estado** (`variant:"empty"`), no como tipo de pantalla.
- No fijar `x`/`y`; expresar estructura y pedir layout.

---

## Detalle de los flujos (backbone propuesto)

### F1 — Crear carpeta
`start` → **Panel Tableros (sin carpetas)** → *decisión: ¿hay tableros?* → **Acción "Nueva carpeta"** → **Dialog nombre** → *decisión: ¿nombre válido y único?* (No → error inline, `dir:"back"`) → **Carpeta creada + toast** → `end`
Puntos a resolver acá: **dónde vive el disparador** de "Nueva carpeta" (header de la sección Tableros vs. menú del botón "Nuevo tablero" vs. menú contextual del vacío) y **si la carpeta nueva nace vacía** o pidiendo tableros en el mismo paso. Por C7: nace vacía, mover es otra tarea.

### F2 — Agregar tablero a carpeta
`start` → **Fila de tablero** → **Menú `⋮` → "Mover a carpeta"** → **Dialog selector de carpeta** (buscador si hay muchas; opción "Nueva carpeta" dentro del selector) → *decisión: ¿ya estaba en otra carpeta?* (Sí → confirmar el cambio, porque la carpeta es exclusiva según D3) → **Tablero movido + toast** → `end`
Rama alterna documentada como atajo, no como camino principal: **drag & drop** de la fila sobre la carpeta (D7).

### F3 — Quitar de la carpeta
`start` → **Fila dentro de una carpeta** → **Menú `⋮` → "Quitar de la carpeta"** → **Tablero vuelve a los sueltos + toast con "Deshacer"** → `end`
Sin diálogo de confirmación: es reversible y de bajo riesgo. El copy debe dejar claro que **no** elimina el tablero ("Quitar de la carpeta", nunca "Eliminar").

### F4 — Renombrar carpeta
`start` → **Fila de carpeta** → **Menú `⋮` → "Renombrar carpeta"** → **Dialog nombre precargado** → *decisión: ¿único?* (No → error inline) → **Renombrada + toast** → `end`

### F5 — Eliminar carpeta (desagrupar)
`start` → **Fila de carpeta** → **Menú `⋮` → "Eliminar carpeta"** → **AlertDialog destructivo**: "¿Eliminar carpeta? Se eliminará la carpeta «X». Los N tableros que contiene volverán a la lista de tableros; no se eliminarán." → *decisión: ¿confirma?* → **Carpeta eliminada, N tableros en sueltos + toast** → `end`
Este diálogo es **el punto más delicado del feature**: si el usuario cree que borra tableros, no usa carpetas. El copy se valida explícitamente.

### F6 — Buscar con carpetas
`start` → **Panel con carpetas** → **Escribe en "Buscar tablero"** → **Resultados aplanados cross-carpeta, cada fila con su carpeta como metadato** → *decisión: ¿hay resultados?* (No → empty state `noResults`) → **Abre un resultado** → `end`
A resolver: si al limpiar la búsqueda el panel **vuelve al estado de expansión previo** de las carpetas (debería) y si el resultado dentro de una carpeta la **revela expandida** al navegar hacia él.

### F7 — Navegar y colapsar
`start` → **Panel con carpetas (colapsadas por defecto)** → **Click en carpeta → expande** → **Click en tablero → se abre** → `end`
A resolver: **estado por defecto** (¿todas colapsadas, o recordar por usuario en `localStorage`/BE?) y comportamiento del toggle A→Z (D5).

---

## Actividades

1. Renombrar el flow existente a `F1 — Crear carpeta` y armar su backbone con las tools de intención (`ohana_flow_add_step`, `ohana_flow_add_branch`).
2. Crear F2–F7 como flows independientes del proyecto.
3. Poblar la anatomía de las pantallas clave (panel, dialogs) con **secciones y componentes desyk** del `design.md`.
4. Marcar los empty states con `variant:"empty"` (panel sin carpetas, carpeta vacía, búsqueda sin resultados).
5. Layout automático y revisión visual: ningún cruce de líneas, ningún fan de conexiones.
6. Escribir `handoff/04-userflows.md`: por flujo → objetivo, pasos, estados, decisiones de interacción tomadas, y qué queda por validar.

## Definition of done

- [ ] 7 flows + 1 sitemap en `.ohana/flow.json`, cada uno con `start` y `end`.
- [ ] Cada `decision` con sus 2 salidas resueltas (verde/rojo) y reintentos con `dir:"back"`.
- [ ] Empty states marcados como estado, no como pantalla.
- [ ] Todas las pantallas usan solo componentes que existen en el `design.md`.
- [ ] `handoff/04-userflows.md` cierra: disparador de "Nueva carpeta", exclusividad al mover, copy del diálogo destructivo, estado por defecto de expansión, comportamiento del sort y de la búsqueda.

## Riesgos

- **Flujos que se ramifican en árbol** en vez de backbone lineal: es la señal de que la tarea está haciendo dos cosas. Partirla.
- **Meter multi-selección** ("mover 10 tableros de una vez") en el MVP: choca de frente con C7. Anotarlo como mejora posterior con su razón.
- Diseñar la búsqueda como si fuera otra pantalla: es un **estado** del mismo panel.
