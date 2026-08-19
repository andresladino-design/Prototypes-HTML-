# User flows — Carpetas en la lista de tableros (SWAT-577)

**Fecha:** 2026-08-03 · **reescrito el 2026-08-14** · **actualizado el 2026-08-19 (D17 · D18 · D20)**
**Boards en Moka:** `.ohana/flow.json` — 13 user flows + 1 sitemap · todos enlazados al prototipo
**Decisiones que los gobiernan:** [`01-decisiones.md`](../design-record/01-decisiones.md) · [`01-benchmark.md`](../design-record/02-benchmark.md) (I1–I6)

> **🔄 Reescrito el 2026-08-14.** Dos reversiones cambiaron el set de flujos:
>
> - **D10 → solo Tableros.** Se **borraron del board** los dos flujos del alcance transversal:
>   *F9 — Una carpeta con tableros y datasets* y *F10 — Ver las anomalías de una carpeta*.
>   Ya no describen el producto. Sus números se reutilizaron.
> - **D2 → 3 niveles de anidamiento.** Entraron cuatro flujos nuevos y se corrigieron cuatro
>   existentes que afirmaban cosas ya falsas.

> **🔄 Actualizado el 2026-08-19** con el feedback del prototipo (Etapa 9):
>
> - **D20 → permisos por autoría.** Cuatro flujos ganan una **rama nueva**: qué pasa cuando
>   **no sos quien creó la carpeta**. Antes esa rama no existía porque D1.b había aplazado la
>   política. Y entra **F13** para el caso de la carpeta huérfana.
> - **D17 → el ancho del panel es una preferencia.** F7 suma el gesto de redimensionar.
> - **D18 → el contador sale de la fila.** Se cae un invariante que F7 afirmaba.

Cada flujo es **una tarea** con un backbone lineal (criterio C7). Ningún flujo hace dos cosas.

| Board | Pantallas | Cubre |
|-------|-----------|-------|
| F1 — Crear una carpeta (2 pasos) | 8 | C1 |
| F2 — Mover un tablero a una carpeta | 9 | C2 |
| F3 — Quitar un tablero de la carpeta | 7 | C3 |
| F4 — Renombrar una carpeta 🔄 | 8 + rama | C1, **D20** |
| F5 — Eliminar una carpeta (**disolver un nivel**) 🔄 | 8 + rama | C1, D6, **D20** |
| F6 — Buscar un tablero · **resultados con ruta** | 7 | C5 |
| F7 — Navegar, redimensionar y colapsar **el árbol** 🔄 | 5 + 1 | C4, **D17** |
| F8 — Agregar tableros a una carpeta existente | 7 | C2 |
| **F9 — Crear una subcarpeta** ✨ | 9 | D2 |
| **F10 — Mover una carpeta a otra** ✨🔄 | 8 + rama | D2, **D20** |
| **F11 — Eliminar una carpeta con subcarpetas** ✨🔄 | 7 + rama | D2, D6, **D20** |
| **F12 — Colapsar las secciones del panel** ✨ | 6 | D12 |
| **F13 — Carpeta huérfana · el escape por admin** ✨ | 7 | **D20** |
| Sitemap — Dónde viven las carpetas (solo Tableros) | 14 | contexto |

🔄 = cambió el 2026-08-19. **La «rama» es siempre la misma:** el gate de autoría de D20, que
entra igual en los cuatro flujos que alteran una carpeta.

> **F8 nació de las pruebas del prototipo**, no del análisis inicial. Ver D9 en [`01-decisiones.md`](../design-record/01-decisiones.md).

---

## Los cuatro flujos nuevos

### F9 — Crear una subcarpeta

`Panel` → `⋮ de la carpeta` → `Nueva subcarpeta` → **paso 1** elegir tableros → **paso 2**
nombre con `Dentro de: Adquirencia / Visa` → decisión **¿nombre único entre hermanas?**

- La decisión **no** es «¿nombre único?» sino **«¿único entre hermanas?»** — `Adquirencia / 2026`
  y `Cierre contable / 2026` conviven (D2, consecuencia 4).
- Al crearse se abre **toda la cadena de ancestros**, no solo la carpeta nueva.
- En el nivel 3 el ítem del menú está **deshabilitado con etiqueta `máx 3`**, no oculto.

### F10 — Mover una carpeta a otra

`Panel` → `⋮` → `Mover carpeta a…` → diálogo con **árbol de destinos y ruta** → decisión
**¿el destino cuelga de la propia carpeta?**

- La rama negativa es **«no ofrecido»**, no «error»: el subárbol propio simplemente **no aparece**
  en la lista. Prevenir por ausencia en vez de dejar elegir y después fallar.
- Lo mismo con el tope: un destino donde el subárbol no cabría tampoco se lista.
- El diálogo incluye destino **`Primer nivel`** — sin él no habría forma de sacar una carpeta de su madre.
- 🔄 **Rama nueva (D20):** «Mover carpeta a…» está deshabilitado si no la creaste. Nota de
  consistencia: **D7 hace del drag un alias de «Mover a»**, así que si alguna vez se implementa el
  drag de carpetas **tiene que respetar el mismo gate**. Hoy las carpetas no son arrastrables, así
  que no hay conflicto — pero es una trampa fácil de pisar después.

### F11 — Eliminar una carpeta con subcarpetas

`Panel` → `⋮` → `Eliminar carpeta` → alert dialog → decisión **¿confirma?**

- El punto del flujo es el copy: **«Sus 8 tableros y 1 subcarpeta suben a "Adquirencia"»**.
  No a la raíz (D6 revisada).
- El «Deshacer» restaura **cuatro** cosas: la carpeta, el `parent_id` de sus hijas, el
  `folder_id` de sus tableros y —🔄 desde D20— el **`created_by` original**.
- 🔄 **Rama nueva (D20):** el mismo gate de autoría que F5.

### F12 — Colapsar las secciones del panel

`59 filas` → colapsar Pendientes y Favoritos → `46` → colapsar Sin carpeta → `26` →
recargar → **el estado persiste**.

- Los números son los del prototipo, no estimaciones.
- Cierra el hallazgo #3 del benchmark: colapsar carpetas no alcanzaba, colapsar **secciones** sí mueve la aguja.

### F13 — Carpeta huérfana · el escape por admin ✨

```
Inicio → Panel · carpeta «2025», la creó alguien que ya no está en la cuenta
       → Menú ⋮ ⟨modal⟩ · Renombrar / Mover / Eliminar DESHABILITADOS
       → ¿Tengo oc:manage_access? ─No→ Pie del menú: «Lucía ya no está en la cuenta.
       │                                Solo alguien que gestione accesos puede…» → Fin
       └Sí→ Los tres ítems habilitados · sigue por F4 / F10 / F11 → Fin
```

- **Es el flujo que justifica el escape.** Sin `oc:manage_access` como override, la carpeta de
  alguien que se fue del equipo queda **inmanejable para siempre**.
- **El copy es distinto al del caso normal, y es el punto del flujo.** Con un autor activo se
  puede decir «pedile a María». Con una huérfana no hay a quién pedirle: hay que **nombrar la
  salida real**, no la puerta cerrada.
- No hay estado «carpeta abandonada» ni migración de autoría. La huérfana **no se detecta ni se
  marca** — simplemente su autor está inactivo, y el override ya existe.
- **Lo que NO hace:** reasignar la autoría. Quien tiene el permiso actúa sobre la carpeta, no se
  convierte en su dueño. Reasignar sería un feature aparte.

---

## El gate de D20 — la rama que entra en F4, F5, F10 y F11

Se describe **una vez** acá porque es idéntica en los cuatro; en cada flujo se referencia.

```
Menú ⋮ de la carpeta → ¿la creé yo, o tengo oc:manage_access?
   ├─Sí→ el flujo continúa normal
   └─No→ Renombrar / Mover / Eliminar DESHABILITADOS
         + motivo al pie del menú → Fin (sin cambios)
```

| | |
|---|---|
| **Gated** | Renombrar · Mover a… · Eliminar |
| **Libre** | Agregar tableros · Nueva subcarpeta · mover un tablero |

La línea es **restringir lo que altera la carpeta de otro, no lo que la usa.** Si crear una
subcarpeta requiriera ser dueño de la madre, «solo el autor» se volvería un candado sobre la
ubicación compartida que definió D1.

**Decisiones de flujo que esto fija:**

- **Se deshabilita, no se oculta.** Mismo criterio que el tope de 3 niveles: esconder una acción
  que existe en otras carpetas deja al usuario buscándola.
- **La rama muere en «Fin», no en un error.** No hay diálogo, no hay toast: el usuario nunca
  llega a intentar la acción. Es prevención por estado, igual que los destinos no ofrecidos de F10.
- **El motivo va una vez al pie del menú**, no como tooltip por ítem: tres tooltips que dicen lo
  mismo es ruido, y un tooltip no se lee con teclado.
- **La autoría no se muestra en la fila.** Iría contra D17. Vive en el `title`, el `aria-label` y
  el pie del menú — los tres cuestan 0px.
- ⚠️ **Hay un camino que no pasa por el menú:** el **click derecho** sobre la fila abre el mismo
  menú contextual, y el teclado puede disparar la acción. **La guarda tiene que estar en el
  handler, no solo en el `disabled`.**

---

## Los cuatro flujos corregidos

| Flujo | Qué afirmaba y era falso | Ahora |
|---|---|---|
| **F1** | «Ya existe una carpeta con este nombre» (global) | El error es **entre hermanas** |
| **F5** | «los 24 tableros vuelven a la lista» | **Disuelve un nivel**: suben a la madre |
| **F6** | «se revela su carpeta» | Se revela su **ruta completa** |
| **F7** | Acordeón de un nivel | **Árbol**; expandir abre toda la cadena de ancestros |

Y en el **Sitemap** se borraron `Datasets en carpetas`, `Anomalías por carpeta (heredada)` y
`Pendientes por carpeta (vía datahub)`; entró `Subcarpetas · hasta 3 niveles`.

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
- **Selector:** **árbol de destinos con ruta** (D2 abrió la anidación) + buscador si hay más de 5 carpetas + destino «Primer nivel» + entrada "＋ Nueva carpeta" (I1 secundario).
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
- 🔄 **Rama nueva (D20):** si no creaste la carpeta, «Renombrar» está **deshabilitado** y el
  diálogo nunca se abre. Ver [«El gate de D20»](#el-gate-de-d20--la-rama-que-entra-en-f4-f5-f10-y-f11).

## F5 — Eliminar una carpeta (disolver un nivel)

```
Inicio → Panel · carpeta con contenido → Menú de la carpeta ⟨modal⟩
       → ¿Eliminar carpeta? ⟨AlertDialog⟩
       → ¿Confirma? ─Sí→ Carpeta disuelta · el contenido sube UN nivel + toast → Fin
                     └No→ Sin cambios · la carpeta y su subárbol siguen igual → Fin
```

**Este es el punto más delicado del feature.** En Almacenamiento, "Eliminar carpeta" **sí borra el contenido** y el diálogo lo advierte contando descendientes. Acá hace lo contrario, así que el copy tiene que **romper activamente** esa expectativa:

> **¿Eliminar carpeta?**
> Se eliminará la carpeta «Visa». Sus **8 tableros y 1 subcarpeta** suben a «Adquirencia»; **no se eliminan**.

- `AlertDialog`, no `Dialog`: no se descarta clickeando fuera.
- Si falla, `Alert variant="destructive"` **dentro** del diálogo (no toast).
- **El contenido sube a la madre, no a la raíz** (D6 revisada). Si la carpeta era de primer nivel, sí queda suelto — mismo comportamiento de antes, ahora como caso particular.
- ⚠️ **En BE ya no lo garantiza `ON DELETE SET NULL`.** Reparentar es lógica de servicio en una transacción, así que el test de que no borra tableros pasa a ser obligatorio. Ver [`handoff/02-backend.md`](02-backend.md) §3.
- Con subcarpetas, el caso completo está en **F11**.
- 🔄 **Rama nueva (D20):** solo quien creó la carpeta puede eliminarla. Y hay una razón extra
  para que el gate exista acá: **D6 debilitó la premisa de D1.b.** El argumento para no pedir
  permiso era que todo tenía «Deshacer» — pero eliminar ya no lo garantiza el motor de base de
  datos, es lógica de servicio. La reversibilidad dejó de ser gratis.
- 🔄 **Y una guarda que el flujo no tenía:** «Deshacer» restaura al **autor original**, no a quien
  deshace. Si no, eliminar + deshacer sería una forma de apropiarse de la carpeta de otro.

## F6 — Buscar un tablero · resultados con ruta

```
Inicio → Panel · con el árbol → Resultados aplanados (cruzan todo el árbol)
       → ¿Hay resultados? ─Sí→ Abre el resultado · se revela su RUTA (Adquirencia / Visa) → Fin
                           └No→ Sin resultados para «xyz» ⟨empty⟩ → Fin
```

- **La búsqueda cruza todo el árbol (C5).** Divergencia deliberada con Almacenamiento, que acota la búsqueda a la carpeta actual y lo indica con un badge "en: X".
- Cada resultado lleva la **ruta completa** como segunda línea (I3), clickable para revelar la carpeta. Los tableros sin carpeta no muestran segunda línea.
- **Con anidamiento la ruta es obligatoria, no un adorno:** puede haber tres carpetas «2026» y el nombre solo no desambigua. Requiere `folder.path` en la respuesta del BE.
- Las **carpetas que coinciden** se listan primero — y **la ruta también es buscable**: escribir «visa» encuentra la subcarpeta aunque el usuario recuerde la madre.
- Sigue siendo server-side con **debounce de 300 ms**, como hoy.

## F7 — Navegar y colapsar el árbol

```
Inicio → Panel · árbol con carpetas colapsadas → Subcarpeta expandida · se abre toda
       la cadena de ancestros (estado persistido) → Tablero abierto · fila activa → Fin
```

- **Colapsadas por defecto**, salvo la cadena del **tablero activo**, que se revela completa (I2).
- **Con anidamiento hay que abrir todos los ancestros, no solo la hoja:** expandir «Visa» sin expandir «Adquirencia» no revela nada.
- Sin chevron: el icono de carpeta lleva el estado (D13).
- El estado de expansión se **persiste en `localStorage`** por (cuenta, usuario). Colapsar todo en cada recarga se lee como un bug.
- Los **tableros sueltos van después** de las carpetas y **sin indentar**: así la carpeta gana jerarquía sin degradar al suelto.
- **Invariante:** la fila de carpeta mide 32 px igual que un tablero.
- 🔄 **Se cae media afirmación (D18).** El invariante decía «si el contador la empuja a 40px, se
  pierde una fila visible». **Ya no hay contador en la fila**, así que ese riesgo desapareció. El
  invariante de 32px se queda; el motivo era otro.
- ✨ **Paso nuevo (D17): redimensionar el panel.** Arrastrar el borde derecho, con snap a tres
  anchos fijos (288 · 384 · 480). Durante el arrastre se sombrea **solo la franja que se gana o
  devuelve** y las tres paradas quedan marcadas. Sin rótulo `S/M/L` — no le dice al usuario hasta
  dónde va a llegar el panel.
- **El ancho persiste** en `localStorage`, como el estado del árbol y el de las secciones. Tercera
  clave, no unificada: producción ya persiste el colapso con la suya.
- **Y convive con el colapso automático:** por debajo del umbral **gana el colapso**, y al volver a
  ensanchar se recupera el tamaño elegido. Reusa `restoreIfNoAutoCollapse`, que ya existe.

## F8 — Agregar tableros a una carpeta existente

```
Inicio → Panel · carpeta vacía ⟨empty⟩ ──⊕ Agregar tableros (o menú ⋮)──▶ Selector múltiple ⟨dialog⟩
       → ¿Seleccionó al menos un tablero? ─Sí→ N agregados · la carpeta se revela → Fin
                                          └No→ Botón deshabilitado ⤸ vuelve al selector
```

- **El estado vacío ofrece la acción, no la describe.** Botón **outline punteado** de 32px con `⊕ Agregar tableros`, dentro de la carpeta. Reemplaza el texto pasivo *"mueve tableros desde su menú de opciones"*.
- **Reusa el selector del paso 1 de F1** en modo "agregar a esta carpeta". Un solo componente, dos entradas.
- **Excluye los tableros que ya están en la carpeta destino:** el objetivo es agregar, no revisar.
- **La misma acción vive en el menú `⋮` de la carpeta.** Sin eso, al agregar el primer tablero desaparecería la única vía de agregar varios y el usuario volvería a mover de a uno.
- Si alguno venía de otra carpeta, el toast lo dice (*"1 salió de otra carpeta"*) — D3 sigue siendo exclusiva.
- **Deshacer devuelve cada tablero a su carpeta anterior**, no a "Sin carpeta".

**Cierra PA-14:** ordenar 30 tableros es una operación, tanto al crear la carpeta (F1) como después (F8).

## ⛔ F9 y F10 del alcance transversal — borrados del board

*Estaban acá: «Una carpeta con tableros y datasets» y «Ver las anomalías de una carpeta
(membresía heredada)». **D10 se revirtió el 2026-08-14** y ambos se borraron de
`.ohana/flow.json`, porque ya no describen el producto.*

*El diseño que documentaban —sobre todo la **membresía heredada**: que un incidente herede
la carpeta del recurso que monitorea, resuelto en query y no persistido— se conserva en
[`design-record/descartado/organizacion-transversal.md`](../design-record/descartado/organizacion-transversal.md), marcado como descartado.*

*Los números F9 y F10 ahora son los flujos de anidamiento (ver arriba).*

## Sitemap — Dónde viven las carpetas

```
Centro de operaciones
├── Tableros
│   ├── Panel lateral · tabs Tableros | Datasets  (Datasets SIN carpetas)
│   │   ├── Configuraciones pendientes
│   │   ├── Favoritos
│   │   ├── Carpetas · NUEVO · solo en Tableros
│   │   │   ├── Tableros de la carpeta
│   │   │   └── Subcarpetas · hasta 3 niveles
│   │   └── Tableros sin carpeta
│   └── Tablero abierto
├── Anomalías · Pendientes · Almacenamiento · Asientos contables
    └── (tabs del OC · fuera del alcance del feature)
```

Deja claro el alcance de **D10 revisada**: la carpeta vive en **un solo lugar**, el panel de
Tableros. El tab de Datasets sigue existiendo —está en producción— pero **sin carpetas**, y
sirve como control de que el feature no lo afectó. Anomalías y Pendientes quedan fuera.

---

## Decisiones de interacción que estos flujos cierran

| Tema | Resolución |
|------|-----------|
| Disparador de crear | Header de la sección "Tableros" (icono + tooltip) + entrada secundaria en el selector de mover |
| Carpeta nueva | **Wizard de 2 pasos**: elegir tableros → nombrar. Puede crearse vacía, pero no es el camino principal (D8) |
| Exclusividad al mover | Si ya estaba en otra carpeta, se **confirma** el cambio |
| Confirmación al quitar | **No** lleva diálogo; lleva toast con "Deshacer" |
| Llenar una carpeta existente | Botón punteado en la carpeta vacía + ítem en el menú `⋮`, con **selección múltiple** (D9) |
| Copy destructivo | Dice el **número** y **a dónde sube** el contenido; y que **no se elimina** |
| Expansión por defecto | Colapsado + revelar **toda la cadena** del tablero activo + persistir en `localStorage` |
| Búsqueda | Cruza el árbol, **ruta completa** como 2ª línea, carpetas coincidentes primero |
| Drag & drop | Atajo con paridad obligatoria por menú y teclado |
| Crear subcarpeta | Menú `⋮` de la carpeta; **deshabilitado con `máx 3`** en el nivel tope (D2) |
| Mover una carpeta | Diálogo con árbol de destinos y ruta; los inválidos por ciclo o tope **no se ofrecen** |
| Colapsar secciones | Las 4 del panel, persistiendo **lo colapsado** (D12) |
| Chevron de carpeta | No existe: el icono lleva el estado (D13) |
| **Contador de carpeta** | **No existe en la fila** (D18); el total del subárbol vive en el `title` y el `aria-label` |
| **Ancho del panel** | **Preferencia del usuario**: 3 anchos fijos, arrastrando el borde con snap y la franja del delta sombreada (D17) |
| **Permisos de carpeta** | **Solo quien la creó** renombra, mueve o elimina; `oc:manage_access` es el escape. Se **deshabilita**, no se oculta, y el motivo va al pie del menú (D20) |

## Lo que estos flujos NO cubren (y por qué)

- **Multi-selección como modo del panel** ("marcar 12 filas del sidebar y moverlas"): choca con C7. **Pero la selección múltiple sí existe** dentro del wizard de creación (D8, F1) y del "Agregar tableros" (D9, F8) — que es donde resuelve el problema de los 100 sueltos sin agregar un modo a la navegación principal.
- **Reordenar carpetas a mano:** D5 resolvió el orden con el toggle A→Z existente.
- **Más de 3 niveles** de anidamiento (D2 revisada), **etiquetas** (D3), **carpetas en Datasets/Anomalías/Pendientes** (D10 revisada).
- **Permisos por carpeta en el sentido de D1.b** —una ACL propia, con roles por carpeta— sigue
  fuera. **D20 no es eso:** es una comprobación de autoría sobre tres acciones, reusando un
  permiso que ya existe. No hay modelo de permisos nuevo.
- **Reasignar la autoría** de una carpeta (F13 la deja actuar, no cambiar de dueño).
- **El ancho útil de la fila** (truncado al medio, botones en hover) — es un issue aparte: [`ancho-util-lista-tableros/`](../../ancho-util-lista-tableros/). El prototipo lo tiene activo, así que no todo lo que se ve ahí lo entregan estos flujos. **Y D17 (el ancho del panel) es la tercera palanca del mismo issue**, aunque F7 la muestre.

## ⚠️ Estado del board vs. este documento

**Este documento está actualizado; el `flow.json` de Moka, al 2026-08-19, todavía no.**

Los boards viven en `.ohana/flow.json`, que está en el `.gitignore` (`**/.ohana/`), así que
**el board no viaja al repositorio** — este archivo es la fuente que el equipo consume. Cuando
se sincronice el board, lo que hay que agregar es:

| Flujo | Qué falta en el board |
|---|---|
| F4 · F5 · F10 · F11 | El nodo `decision` del gate de autoría + su rama negativa a `end` |
| F7 | El paso de redimensionar el panel |
| F13 | El flujo completo (7 nodos) |

Ninguna de esas ediciones cambia lo que dice este doc, que ya las describe.

## Nota de proceso

Los boards se construyeron con las tools de intención de Moka hasta detectar que **los writes concurrentes al mismo `flow.json` se pierden** (dos nodos desaparecieron sin error). El resto de la estructura se escribió en un único write al archivo — la vía que `MOKA.md` contempla — y luego se reordenó con `ohana_flow_layout` flujo por flujo. Validado después: 64 pantallas, 63 edges, sin huérfanos, sin edges roto, todas con posición, cada userflow con su `start` y su `end`.
