# User flows — Carpetas en la lista de tableros (SWAT-577)

**Fecha:** 2026-08-03
**Boards en Moka:** `.ohana/flow.json` — 7 user flows + 1 sitemap
**Decisiones que los gobiernan:** [`01-decisiones.md`](01-decisiones.md) (D1–D7) · [`01-benchmark.md`](01-benchmark.md) (I1–I6)

Cada flujo es **una tarea** con un backbone lineal (criterio C7). Ningún flujo hace dos cosas.

| Board | Pantallas | Cubre |
|-------|-----------|-------|
| F1 — Crear una carpeta (2 pasos) | 8 | C1 |
| F2 — Mover un tablero a una carpeta | 9 | C2 |
| F3 — Quitar un tablero de la carpeta | 7 | C3 |
| F4 — Renombrar una carpeta | 8 | C1 |
| F5 — Eliminar una carpeta (desagrupar) | 8 | C1, D6 |
| F6 — Buscar un tablero con carpetas presentes | 7 | C5 |
| F7 — Navegar y colapsar carpetas | 5 | C4 |
| Sitemap — Dónde viven las carpetas | 13 | contexto |

---

## F1 — Crear una carpeta

```
Inicio → Panel Tableros · aún sin carpetas ⟨empty⟩
       → Paso 1 · Elige los tableros ⟨dialog⟩ ──Siguiente──▶ Paso 2 · Ponle nombre ⟨dialog⟩
       → ¿Nombre válido y único? ─Sí→ Carpeta creada con sus tableros · se revela → Fin
                                 └No→ Error inline ⟨dialog⟩ ⤸ vuelve al paso 2
```

- **Disparador (I1):** botón icono `FolderPlus` con tooltip en el **header de la sección "Tableros"**, a la izquierda del toggle A→Z. El slot ya existe en el código (`DashboardSection.headerAction`).
- **Dos pasos, una sola tarea (D8).** La tarea del usuario no es "crear un contenedor vacío" sino **"agrupar estos tableros"**. Paso 1 elige, paso 2 nombra y **muestra qué se está guardando**. Precedentes en el producto: `CreateConnectionWizard` y `TemplateFormDialog/steps`, con el `stepper` de desyk.
- **Al crear, la carpeta se revela:** entra expandida, scroll hasta ella y resalte de ~2s. Sin esto el usuario queda buscando su propio resultado entre 4 carpetas y 100 sueltos — fue el hallazgo de las pruebas.
- **Crear vacía sigue siendo posible** (0 seleccionados → "Crear vacía"), y el resumen lo dice.
- **Validación:** `trim` · mín 1 · **máx 100** · **sin restricción de caracteres** — las reglas de nombre de *tablero*, no las de Almacenamiento (que rechaza tildes).
- **Empty state del feature:** el panel sin carpetas es el primer contacto (HU-08). Lleva CTA de texto completo, no solo el icono — mitiga el riesgo de Fitts de un target de 28 px.
- Crear queda **deshabilitado durante la búsqueda**, igual que en Almacenamiento.

## F2 — Mover un tablero a una carpeta

```
Inicio → Panel con carpetas → Menú del tablero ⟨modal⟩ → Mover a carpeta · selector ⟨dialog⟩
       → ¿El tablero está sin carpeta? ─Sí→ Tablero movido + toast «Deshacer» → Fin
                                       └No→ Confirmar cambio de carpeta ⟨dialog⟩ ─→ movido
       └─(atajo)→ Arrastrar la fila sobre la carpeta ─→ movido
```

- **Pregunta formulada para que el "Sí" sea el backbone.** Si el tablero ya estaba en otra carpeta, se **confirma el cambio** — D3 hace la pertenencia exclusiva, así que mover significa *sacar de donde estaba*.
- **Copy:** "Mover a carpeta", nunca "Agregar a" (sugeriría acumulación).
- **Selector:** lista simple (D2 descartó la anidación → sin árbol ni breadcrumb) + buscador solo si hay más de 7 carpetas + entrada "＋ Nueva carpeta" (I1 secundario).
- **El drag es un atajo, nunca requisito** (D7). Debe funcionar con la carpeta **colapsada** y con autoscroll del panel.
- El menú pasa de 5 a 6 ítems → verificar Hick en el prototipo.

## F3 — Quitar un tablero de la carpeta

```
Inicio → Panel · carpeta expandida → Menú del tablero ⟨modal⟩
       → Vuelve a «Sin carpeta» + toast con Deshacer
       → ¿Usa Deshacer? ─Sí→ El tablero vuelve a la carpeta → Fin
                         └No→ Fin
```

- **Sin diálogo de confirmación:** es reversible y de bajo riesgo. La red de seguridad es el "Deshacer" del toast.
- **Copy:** "Quitar de la carpeta". La palabra "Eliminar" no aparece en ningún lugar de este flujo.

## F4 — Renombrar una carpeta

```
Inicio → Panel · con carpetas → Menú de la carpeta ⟨modal⟩ → Renombrar carpeta (nombre precargado) ⟨dialog⟩
       → ¿Nombre único? ─Sí→ Carpeta renombrada + toast → Fin
                         └No→ Error inline · 409 ⟨dialog⟩ ⤸ vuelve al diálogo
```

- Mismo diálogo que F1 en modo `rename`, con el valor precargado y seleccionado.
- El **409 del servidor** se muestra **inline en el diálogo**, además del toast — el patrón que ya usa el rename de tableros.

## F5 — Eliminar una carpeta (desagrupar)

```
Inicio → Panel · carpeta con 24 tableros → Menú de la carpeta ⟨modal⟩
       → ¿Eliminar carpeta? ⟨AlertDialog⟩
       → ¿Confirma? ─Sí→ Carpeta eliminada · los 24 tableros vuelven a la lista + toast → Fin
                     └No→ Sin cambios → Fin
```

**Este es el punto más delicado del feature.** En Almacenamiento, "Eliminar carpeta" **sí borra el contenido** y el diálogo lo advierte contando descendientes. Acá hace lo contrario, así que el copy tiene que **romper activamente** esa expectativa:

> **¿Eliminar carpeta?**
> Se eliminará la carpeta «Adquirencia». Los **24 tableros** que contiene volverán a la lista de tableros; **no se eliminarán**.

- `AlertDialog`, no `Dialog`: no se descarta clickeando fuera.
- Si falla, `Alert variant="destructive"` **dentro** del diálogo (no toast).
- En BE lo garantiza `ON DELETE SET NULL` — el desagrupado lo hace el motor de base de datos, no la lógica de aplicación.

## F6 — Buscar un tablero con carpetas presentes

```
Inicio → Panel · con carpetas → Resultados aplanados (cruzan todas las carpetas)
       → ¿Hay resultados? ─Sí→ Abre el resultado · se revela su carpeta → Fin
                           └No→ Sin resultados para «xyz» ⟨empty⟩ → Fin
```

- **La búsqueda cruza todas las carpetas (C5).** Divergencia deliberada con Almacenamiento, que acota la búsqueda a la carpeta actual y lo indica con un badge "en: X".
- Cada resultado lleva su carpeta como **segunda línea** de la fila (I3), clickable para revelar la carpeta. Los tableros sin carpeta no muestran segunda línea.
- Las **carpetas que coinciden** con el término se listan primero.
- Sigue siendo server-side con **debounce de 300 ms**, como hoy.

## F7 — Navegar y colapsar carpetas

```
Inicio → Panel · carpetas colapsadas por defecto → Carpeta expandida (estado persistido)
       → Tablero abierto · fila activa → Fin
```

- **Colapsadas por defecto**, salvo la carpeta del **tablero activo**, que se revela expandida (I2).
- El estado de expansión se **persiste en `localStorage`** por (cuenta, usuario). Colapsar todo en cada recarga se lee como un bug.
- Los **tableros sueltos van después** de las carpetas y **sin indentar**: así la carpeta gana jerarquía sin degradar al suelto.
- **Invariante:** la fila de carpeta mide 32 px igual que un tablero. Si el contador la empuja a 40 px, se pierde una fila visible por carpeta.

## Sitemap — Dónde viven las carpetas

```
Centro de operaciones
├── Tableros
│   ├── Panel lateral de tableros
│   │   ├── Configuraciones pendientes
│   │   ├── Favoritos
│   │   ├── Carpetas · NUEVO ──── Tableros de la carpeta
│   │   └── Tableros sin carpeta
│   └── Tablero abierto
├── Anomalías · Pendientes · Almacenamiento · Asientos contables
```

Deja claro el alcance: **las carpetas son un nivel dentro del panel de Tableros** (D4). "Configuraciones pendientes" y "Favoritos" no cambian.

---

## Decisiones de interacción que estos flujos cierran

| Tema | Resolución |
|------|-----------|
| Disparador de crear | Header de la sección "Tableros" (icono + tooltip) + entrada secundaria en el selector de mover |
| Carpeta nueva | **Wizard de 2 pasos**: elegir tableros → nombrar. Puede crearse vacía, pero no es el camino principal (D8) |
| Exclusividad al mover | Si ya estaba en otra carpeta, se **confirma** el cambio |
| Confirmación al quitar | **No** lleva diálogo; lleva toast con "Deshacer" |
| Copy destructivo | Dice el **número** de tableros que vuelven a la lista y que **no se eliminarán** |
| Expansión por defecto | Colapsado + revelar la del tablero activo + persistir en `localStorage` |
| Búsqueda | Cruza carpetas, carpeta como 2ª línea, carpetas coincidentes primero |
| Drag & drop | Atajo con paridad obligatoria por menú y teclado |

## Lo que estos flujos NO cubren (y por qué)

- **Multi-selección como modo del panel** ("marcar 12 filas y moverlas"): choca con C7. **Pero sí existe dentro del wizard de creación** (D8), que es donde resuelve el problema de los 100 sueltos sin agregar un modo a la navegación.
- **Reordenar carpetas a mano:** D5 resolvió el orden con el toggle A→Z existente.
- **Subcarpetas** (D2), **etiquetas** (D3), **permisos por carpeta** (D1.b).

## Nota de proceso

Los boards se construyeron con las tools de intención de Moka hasta detectar que **los writes concurrentes al mismo `flow.json` se pierden** (dos nodos desaparecieron sin error). El resto de la estructura se escribió en un único write al archivo — la vía que `MOKA.md` contempla — y luego se reordenó con `ohana_flow_layout` flujo por flujo. Validado después: 64 pantallas, 63 edges, sin huérfanos, sin edges roto, todas con posición, cada userflow con su `start` y su `end`.
