# Decisiones de producto y diseño — Carpetas en la lista de tableros (SWAT-577)

**Fecha:** 2026-08-03
**Decidido por:** Andrés Ladino (UX) con la exploración técnica de [`00-exploracion-fe-be.md`](00-exploracion-fe-be.md)
**Estado:** cerradas. Cambiar cualquiera de D1, D2 o D3 después de la Etapa 7 implica rehacer el modelo de BE.

---

## Tabla resumen

| # | Decisión | Resultado | Costo de revertir |
|---|----------|-----------|-------------------|
| **D1** | Scope de las carpetas | **Por cuenta** (compartidas) | 🔴 Alto — modelo BE + migración |
| **D2** | Profundidad | **Un solo nivel** | 🟡 Medio — anidar es aditivo |
| **D3** | Pertenencia | **Exclusiva** (un tablero, una carpeta) | 🔴 Alto — modelo BE + modelo mental |
| **D4** | Convivencia con Favoritos / Pendientes | Carpetas **dentro** de "Tableros"; las otras dos secciones intactas | 🟢 Bajo |
| **D5** | Alcance del orden A→Z | Aplica en **cada nivel** | 🟢 Bajo |
| **D6** | Eliminar carpeta | **Desagrupa siempre**; nunca elimina tableros | 🔴 Alto (es criterio del issue, no negociable) |
| **D7** | Mover un tablero | **Menú `⋮` primario + drag como atajo**, ambos en la v1 | 🟡 Medio |
| **D8** | Crear carpeta | **2 pasos: elegir tableros → ponerle nombre.** Al crear, la carpeta se revela con scroll + resalte | 🟡 Medio |
| **D9** | Llenar una carpeta existente | **"Agregar tableros"** con selección múltiple: botón punteado en la carpeta vacía + ítem en el menú `⋮` | 🟢 Bajo |

---

## D1 — Las carpetas son **por cuenta**

**Decisión:** una sola estructura de carpetas por cuenta, visible para todos los usuarios de esa cuenta.

**Razón:** el issue describe el problema como *"All dashboards from all users in an account are listed in a flat, infinite list"* — el desorden es **de la cuenta**. Si las carpetas fueran por usuario (como Favoritos), cada uno de los N usuarios tendría que volver a organizar los mismos 155 tableros, y una carpeta que solo ve su autor es más una "vista personal" que una carpeta. Los tableros ya son entidades de cuenta (`account_id` + `access_type` + ACL), así que la carpeta hereda el mismo scope que la cosa que organiza.

**Consecuencias:**

1. **BE:** habilita la opción más simple — columna `folder_id` en `dashboards` con `ON DELETE SET NULL` (ver D3 y D6). No hace falta tabla puente ni `user_id`.
2. **Cualquier usuario con acceso a Tableros puede mover un tablero de otro.** Es aceptable porque **ninguna acción de carpetas es destructiva** (D6) y todo tiene "Deshacer". Se registra `created_by` en la carpeta para trazabilidad.
3. **D1.b — permisos:** no se introduce un permiso nuevo. Crear / renombrar / eliminar carpeta usa el **mismo umbral que crear un tablero** hoy. *(A confirmar con BE en la Etapa 7; si el equipo prefiere atarlo a `oc:manage_access`, es un cambio de una línea en la vista, no del modelo.)*
4. **Tableros sin acceso dentro de una carpeta:** se siguen viendo atenuados y no navegables, exactamente como hoy en la lista plana (`has_access: false` → `opacity-60`). El contador de la carpeta los incluye. **No hay fuga de información nueva**: el nombre de esos tableros ya es visible hoy en la lista.

**Descartado:** por usuario (no resuelve el problema como equipo) · híbrido en la v1 (dos modelos coexistiendo antes de validar el primero).
**Puerta abierta:** carpetas personales como capa aparte ("Mis vistas") en una versión futura; el modelo por cuenta no la bloquea.

---

## D2 — Un solo nivel de carpetas

**Decisión:** carpetas planas. Sin subcarpetas en el MVP.

**Razón:** el panel mide ~280 px; al tercer nivel de indentación el nombre del tablero deja de ser legible — y los nombres reales son largos (`Adquirencia_2026_06_04_...`, ya truncados hoy). Ley de Miller: el objetivo es chunks reconocibles, no una jerarquía profunda. Grafana operó con carpetas planas durante años antes de anidar. Y anidar más adelante es **aditivo**; quitar la anidación sería una migración.

**Consecuencias:** sin breadcrumb en el sidebar · query de un nivel · el `MoveToFolderDialog` es una lista simple, no un árbol · si una cuenta creara 30 carpetas volvería a tener una lista larga → se define un máximo razonable de carpetas en la Etapa 5.

---

## D3 — Un tablero vive en **una sola** carpeta

**Decisión:** pertenencia exclusiva. Mover a otra carpeta lo saca de la anterior.

**Razón:** la palabra "carpeta" ya promete exclusividad, y el issue pide explícitamente la metáfora de explorador de archivos. La alternativa (etiquetas) obliga a que el mismo tablero aparezca repetido en el sidebar, lo cual **empeora** el problema que venimos a resolver: más filas para escanear, no menos. Técnicamente, exclusiva = columna `folder_id`, el modelo más barato.

**Consecuencias:**

1. Un tablero que pertenece a dos contextos debe elegir uno. Se compensa con **Favoritos** (atajo transversal, ya existe) y con la **búsqueda cross-carpeta** (C5).
2. Al mover un tablero que ya estaba en otra carpeta, el flujo F2 **confirma el cambio** en vez de asumirlo.
3. El copy nunca dice "agregar a" (sugiere acumulación) sino **"Mover a carpeta"**.

**Descartado:** etiquetas múltiples. Si aparece la necesidad real, se diseña como feature aparte con su propio nombre y su propia UI — no como variante de carpetas.

---

## D4 — Las carpetas viven dentro de la sección "Tableros"

**Decisión:** el panel conserva sus tres secciones (`Configuraciones pendientes`, `Favoritos`, `Tableros`). Las carpetas son un nivel **dentro** de "Tableros"; las otras dos no cambian en nada.

**Razón:** si una carpeta se pintara como header de sección competiría visualmente con "Favoritos" y el usuario dejaría de distinguir qué es una sección del sistema y qué una carpeta propia. La jerarquía queda: **header de sección** > **carpeta** > **fila de tablero**.

**Consecuencias:** un tablero puede ser favorito **y** estar en una carpeta — son cosas distintas: *favorito = atajo*, *carpeta = ubicación*. Los favoritos se siguen mostrando arriba, sin indicar su carpeta (no aporta en un atajo de 5 ítems). Los tableros sueltos van **después** de las carpetas, sin indentación, tal como se ven hoy.

---

## D5 — El orden A→Z aplica en cada nivel

**Decisión:** el toggle existente (`ArrowDownAZ` / `ArrowUpZA`) ordena las carpetas entre sí **y** los tableros dentro de cada carpeta **y** los sueltos. Un solo control, sin UI nueva.

**Razón:** es el comportamiento que el usuario ya conoce, aplicado recursivamente; un segundo control ("ordenar carpetas" vs. "ordenar tableros") sería la clase de complejidad que el criterio C7 pide evitar.

**Consecuencia:** el orden manual de carpetas (`order`) queda como endpoint opcional en BE, no como feature de la v1.

---

## D6 — Eliminar una carpeta desagrupa; nunca elimina tableros

**Decisión:** criterio explícito del issue. Al eliminar una carpeta, sus tableros vuelven a la lista de sueltos.

**Consecuencias:**

1. **BE:** `ON DELETE SET NULL` — el desagrupado lo garantiza el motor de base de datos, no la lógica de aplicación.
2. **Copy del diálogo (el punto más delicado del feature):** tiene que decir el número.
   > **¿Eliminar carpeta?**
   > Se eliminará la carpeta «Adquirencia». Los **24 tableros** que contiene volverán a la lista de tableros; no se eliminarán.
3. "Quitar de la carpeta" (F3) tampoco elimina nada y no lleva diálogo de confirmación — es reversible y de bajo riesgo, con toast + "Deshacer".
4. El lenguaje nunca mezcla los dos verbos: **"Eliminar carpeta"** ≠ **"Eliminar tablero"**. Si el usuario confunde ambos, no usa carpetas.

---

## D7 — Menú `⋮` primario + drag & drop como atajo, ambos en la v1

**Decisión:** "Mover a carpeta" en el menú de la fila (y en el click derecho, que comparte los mismos ítems) es la vía principal. Arrastrar la fila sobre una carpeta es un atajo equivalente, disponible desde la v1.

**Razón:** el menú es la ruta accesible por teclado y la que funciona con 155 tableros y carpetas colapsadas. El drag es más rápido para quien lo descubre, y **la infra ya existe en este mismo panel** (`useDashboardCrossDrag` con MIME types + `useHtml5Sortable` + optimistic updates con rollback, hoy usados por Favoritos), así que el costo incremental es bajo.

**Consecuencias / lo que hay que resolver en el diseño:**

1. **Drop en carpeta colapsada:** debe funcionar sin expandirla (highlight de la fila de carpeta + drop directo). Opcional: expandir en hover tras ~700 ms.
2. **Autoscroll** del panel mientras se arrastra hacia una carpeta fuera del viewport.
3. **MIME nuevo** (`DASHBOARD_TO_FOLDER_MIME`) para no chocar con los de favoritos; una fila arrastrada no debe activar el drop target de Favoritos y el de carpetas a la vez.
4. **Paridad obligatoria:** todo lo que se logre arrastrando tiene que poder lograrse por menú y teclado. El drag es atajo, nunca requisito.
5. Si en la implementación el drag amenaza el alcance, **se corta el drag, no el menú** — y se documenta como v1.1.

---

---

## D8 — Crear una carpeta es un flujo de **2 pasos**: elegir tableros → ponerle nombre

**Fecha:** 2026-08-03 (posterior a las pruebas del prototipo)
**Revierte:** la decisión previa de que "la carpeta nace vacía y mover es otra tarea".

**Qué pasó:** al probar el prototipo apareció una sensación de flujo roto. En palabras de Andrés:

> *"cuando creo una carpeta se cierra el modal y quedé buscando dónde se creó. Cuando creo una carpeta nueva primero quiero seleccionar los tableros que quiero dentro y luego con un botón siguiente agregar el nombre, para que cuando la cree me quede claro qué hice y qué estoy guardando."*

**Dos problemas distintos, ambos reales:**

1. **Orientación.** Al cerrar el diálogo, la carpeta nueva aparecía en su lugar alfabético entre 4 carpetas y 100 sueltos. El toast decía "Carpeta creada" pero no mostraba **dónde**. El usuario quedaba buscando su propio resultado.
2. **Sentido de la acción.** Una carpeta vacía no es un resultado: es una promesa. La confirmación no comunicaba nada verificable, así que la acción se sentía sin consecuencia.

**Decisión:**

- **Paso 1 — Elige los tableros:** buscador + lista con checkboxes, **los tableros sin carpeta primero** (son los que urge ordenar), y los que ya están en otra carpeta muestran cuál. Botón "Siguiente".
- **Paso 2 — Ponle nombre:** el campo de nombre **más un resumen de lo que se va a guardar** ("Se creará con 12 tableros" + los primeros 4 + "y 8 más") y un enlace para volver a cambiar la selección. El botón dice **"Crear con 12 tableros"**, no "Crear".
- **Crear vacía sigue siendo posible:** con 0 seleccionados el paso 2 dice "Se creará vacía" y el botón dice "Crear vacía".
- **Al crear, la carpeta se revela:** entra expandida, **se hace scroll hasta ella** y se resalta ~2s. El mismo tratamiento se aplica al mover un tablero y al renombrar.
- El toast lleva **Deshacer**, que revierte la creación **y** devuelve cada tablero a donde estaba.

**Por qué no rompe C7 ("un flujo por tarea"):** la tarea del usuario nunca fue "crear un contenedor vacío" — es **"agrupar estos tableros"**. Dos pasos de una misma tarea es un patrón de producto, no dos tareas. Y el producto ya lo usa: `CreateConnectionWizard` y `TemplateFormDialog/steps` en el OC, con el componente `stepper` de desyk. Mi decisión anterior aplicaba C7 al pie de la letra y terminaba contra su propio objetivo.

**Consecuencia sobre el alcance:** la **selección múltiple entra a la v1, pero solo dentro del wizard de creación** — no como modo de selección del panel. Eso resuelve buena parte de PA-14 (los 100 sueltos) sin agregar una capa de modo a la navegación principal: ordenar 30 tableros de una vez es crear una carpeta, no 30 operaciones de mover.

**Consecuencia para BE:** `POST /dashboards/folders` acepta opcionalmente `dashboard_ids: UUID[]` para crear y asignar en una sola transacción. Sin eso, el FE tendría que hacer 1 + N llamadas y una falla parcial dejaría la carpeta a medio llenar.

---

---

## D9 — "Agregar tableros": selección múltiple sobre una carpeta que ya existe

**Fecha:** 2026-08-04 · **Origen:** pruebas del prototipo.

**Pedido:** *"cuando la carpeta esté vacía, muéstrame un botón outline punteado para agregar tableros; al dar clic me aparece el modal para seleccionar los que quiero añadir."*

**Decisión:**

- La carpeta vacía muestra un **botón outline punteado** del alto de una fila (32px) con `⊕ Agregar tableros`, dentro de la carpeta. Reemplaza el texto pasivo anterior, que describía el mecanismo ("mueve tableros desde su menú") en vez de ofrecer la acción.
- El botón abre **el mismo selector múltiple del paso 1 del wizard** (D8), en modo "agregar a esta carpeta": buscador, checkboxes, sueltos primero, y los que ya están en otra carpeta muestran cuál. El botón de confirmación dice **"Agregar 12 tableros"**.
- Los tableros que **ya están en esa carpeta** se excluyen de la lista: el objetivo es agregar, no revisar.
- Si alguno venía de otra carpeta, el toast lo dice (*"3 tableros agregados a «X» · 1 salió de otra carpeta"*) — D3 sigue siendo exclusiva.
- **La misma acción vive en el menú `⋮` de la carpeta**, no solo en el estado vacío. Sin eso, al agregar el primer tablero desaparecería la única vía de agregar varios y el usuario volvería a mover de a uno. *(Esta parte no estaba en el pedido; se agregó para no dejar el hueco. Es trivial de quitar si se prefiere solo el estado vacío.)*

**Consecuencia:** cierra **PA-14**. Ordenar 30 tableros es una operación tanto al crear la carpeta como después. La multi-selección **como modo del panel** sigue fuera de alcance y ya no hace falta.

**Para BE:** el endpoint de mover necesita aceptar lote — `PATCH /dashboards/folder` con `{ dashboard_ids: UUID[], folder_id }` — o bien reusar `POST /dashboards/folders/{id}/dashboards`. Con N llamadas sueltas, una falla parcial deja la operación a medias y el "Deshacer" deja de ser confiable.

---

## Alcance de la v1 — qué NO entra

| Fuera de alcance | Razón | ¿Reversible? |
|------------------|-------|--------------|
| Subcarpetas anidadas | D2 | Sí, aditivo |
| Etiquetas / pertenencia múltiple | D3 | Es otro feature |
| Permisos propios por carpeta | D1.b — no se introduce permiso nuevo | Sí |
| Carpetas personales ("Mis vistas") | D1 — capa futura | Sí |
| Multi-selección **como modo del panel** | Criterio C7. Nota: sí existe **dentro del wizard de creación** (D8) | Sí, aditivo |
| Orden manual de carpetas (drag entre carpetas) | D5 — el A→Z alcanza | Sí |
| Colores / iconos personalizados de carpeta | No resuelve encontrabilidad; suma decisiones | Sí |

---

## Qué queda por decidir (ya no es modelo de datos, es interacción)

Estas se resuelven con el **benchmark acotado** de la Etapa 1 y se cierran en los flujos (Etapa 4):

| # | Pregunta abierta |
|---|------------------|
| I1 | ¿Dónde vive el disparador de **"Nueva carpeta"**: header de la sección Tableros, menú junto a "Nuevo tablero", o menú contextual del vacío? |
| I2 | ¿Las carpetas arrancan **colapsadas** por defecto? ¿Se recuerda el estado por usuario (`localStorage`)? |
| I3 | ¿Cómo se muestra la carpeta en un **resultado de búsqueda**: chip, texto secundario en la fila, o agrupado por carpeta? |
| I4 | ¿Qué palancas exactas dan la **jerarquía visual** de la carpeta (peso, icono, contador, indentación) sin romper la densidad del panel? |
| I5 | ¿Cuántas carpetas son "demasiadas" y hay que sugerir un máximo? |
| I6 | ¿Se **reusa** el `FolderNameDialog` de Almacenamiento o se crea uno propio en `features/dashboards`? |
