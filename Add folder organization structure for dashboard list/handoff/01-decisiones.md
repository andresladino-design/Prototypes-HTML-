# Decisiones de producto y diseño — Carpetas en la lista de tableros (SWAT-577)

**Fechas:** D1–D7 el 2026-08-03 (antes de prototipar) · **D8 y D9 el 2026-08-04, tras probar el prototipo**
· **D2, D6 y D10 revisadas el 2026-08-14** · **D12–D15 abiertas el 2026-08-14**
· **D17–D20 el 2026-08-18, desde el feedback del prototipo en Ohana (Etapa 9)**
**Decidido por:** Andrés Ladino (UX) con la exploración técnica de [`00-exploracion-fe-be.md`](00-exploracion-fe-be.md)
**Estado:** cerradas, **menos D20**, que espera confirmación de BE. D17 quedó cerrada el
2026-08-18 (mecanismo y valores confirmados). Cambiar D1 o D3 después de la Etapa 7 implica
rehacer el modelo de BE.

> D8 y D9 salieron de **usar** el prototipo, no de analizarlo. D8 además **revierte** una decisión previa mía
> ("la carpeta nace vacía"). Quedan registradas acá con lo que reemplazan, para que el handoff no arrastre
> la versión anterior.
>
> **🔄 Tres revisiones del 2026-08-14.** El equipo pidió subcarpetas (**D2**) y recortar el alcance a
> tableros (**D10**); revisar el BE reveló además que **D6** no podía apoyarse en una FK. Las tres
> se reescriben abajo **conservando la decisión anterior y su razón**, porque en los tres casos la razón
> original sigue siendo la restricción que condiciona el diseño actual. No se reescribe la historia:
> se registra el cambio.

---

## Tabla resumen

| # | Decisión | Resultado | Costo de revertir |
|---|----------|-----------|-------------------|
| **D1** | Scope de las carpetas | **Por cuenta** (compartidas) | 🔴 Alto — modelo BE + migración |
| **D2** 🔄 | Profundidad | **3 niveles de carpeta** *(antes: un solo nivel)* | 🔴 Alto — `parent_id` + `path` en BE |
| **D3** | Pertenencia | **Exclusiva** (un tablero, una carpeta) | 🔴 Alto — modelo BE + modelo mental |
| **D4** | Convivencia con Favoritos / Pendientes | Carpetas **dentro** de "Tableros"; las otras dos secciones intactas | 🟢 Bajo |
| **D5** | Alcance del orden A→Z | Aplica en **cada nivel** | 🟢 Bajo |
| **D6** 🔄 | Eliminar carpeta | **Disuelve un nivel**: el contenido sube a la madre *(antes: a la raíz vía `ON DELETE SET NULL`)* | 🔴 Alto (que no elimine tableros es criterio del issue) |
| **D7** | Mover un tablero | **Menú `⋮` primario + drag como atajo**, ambos en la v1 | 🟡 Medio |
| **D8** | Crear carpeta | **2 pasos: elegir tableros → ponerle nombre.** Al crear, la carpeta se revela con scroll + resalte | 🟡 Medio |
| **D9** | Llenar una carpeta existente | **"Agregar tableros"** con selección múltiple: botón punteado en la carpeta vacía + ítem en el menú `⋮` | 🟢 Bajo |
| **D11** | Patrón de panel | **«Panel de recursos del OC»**: 9 slots en orden fijo. Eje **artefacto vs. evento** deriva fila, ancho, paginación y tipo de membresía | 🟢 Bajo |
| ~~**SD-8**~~ | ~~«Favoritos» vs «Fijados»~~ | ⛔ Fuera de alcance con D10 revisada (era sobre el panel de Pendientes) | — |
| ~~**SD-7**~~ | ~~Conciliaciones ya agrupadas~~ | ⛔ Fuera de alcance con D10 revisada | — |
| **D10** 🔄 | Alcance | **Solo Tableros** *(antes: transversal a las 4 entidades)* | 🟢 Bajo — se recorta, no se migra |
| **D12** ✨ | Secciones colapsables | Las 4 secciones del panel colapsan; se persiste lo **colapsado** | 🟢 Bajo |
| **D13** ✨ | Chevron de carpeta | El **icono** lleva el estado (`folder` ↔ `folder-open`); sin chevron | 🟢 Bajo |
| **D14** ↗️ | Ancho útil de la fila | **Extraída a un issue aparte** — no depende de carpetas | 🟢 Bajo |
| **D15** ✨ | Agrupamiento server-side | El árbol **no** se resuelve en cliente: la lista es paginada de 20 con `search`/`sort` en BE | 🔴 Alto — condiciona todo el contrato de API |
| **D16** ✨ | Forma de navegar | **Árbol in-place.** Se descarta el drill-down por niveles | 🟡 Medio |
| **D17** ✅ | Ancho del panel | **Tres anchos fijos: `sm` 288 · `md` 384 · `lg` 480**, persistidos. Arrastrar el borde, sombreando la franja del delta | 🟢 Bajo |
| **D18** ✨ | Contador de subcarpeta | **Sale de la fila.** El total se muda al `title` y al `aria-label` (0px). +20px por fila de carpeta | 🟢 Bajo |
| ~~**D19**~~ | ~~Acordeón exclusivo~~ | ⛔ **Descartada** — sacada del plan el 2026-08-18. D12 sigue: secciones independientes | — |
| **D20** 🟡 | Permisos de carpeta | **Solo quien la creó** puede renombrar, mover o eliminar. `oc:manage_access` es el **escape**. **Revierte D1.b** · a confirmar con BE | 🟡 Medio — agrega comprobación de autoría |

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

## D2 🔄 — Anidamiento hasta **3 niveles** de carpeta

**Revisada el 2026-08-14.** Antes: *«carpetas planas, sin subcarpetas en el MVP»*.

**Decisión:** 3 niveles de carpeta (`Adquirencia › Visa › Contracargos`). Los tableros
cuelgan de cualquiera de ellos y **no cuentan como nivel**.

**Por qué cambió:** el equipo pidió subcarpetas. El doc original ya había dejado la puerta
abierta — *«anidar más adelante es aditivo; quitar la anidación sería una migración»* — así
que no hay contradicción de modelo, es la escalación prevista.

### La razón original de D2 no desapareció

Es lo más importante de esta revisión. D2 argumentaba carpetas planas porque **el panel
tiene 240px útiles** (`w-72` con `px-3` dos veces: en el `<aside>` y en el cuerpo de la
sección) **y los nombres reales ya se truncan hoy**:

```
Adquirencia_2026_06_04_conciliacion_visa     ← 40 caracteres
Adquirencia_2026_06_04_conciliacion_master
```

Esa restricción es exactamente la que obliga a las **tres mitigaciones** del diseño actual.
Si alguien las revierte por parecer arbitrarias, el anidamiento se vuelve inusable:

| Mitigación | Qué pasa sin ella |
|---|---|
| Indentación de **12px** por nivel (no los 19px del acordeón original) | en el nivel 3 el nombre baja a ~120px |
| **Truncado al medio** fijando el último segmento | se pierde la cola, que es lo que desambigua `_visa` de `_master` |
| **Tope de 3 niveles** | la profundidad se vuelve ilimitada y el `path` del BE, de largo impredecible |

Presupuesto resultante — peor caso permitido:

| | nivel 1 | nivel 2 | nivel 3 |
|---|---|---|---|
| Nombre de carpeta | 182px | 170px | **158px** |
| Nombre de tablero dentro | 190px | 178px | **166px** |

**Por qué 3 y no «sin tope»:** se evaluó profundidad libre y se descartó al revisar el BE.
Con tope, el `path` materializado tiene largo acotado, el `CHECK` de profundidad es trivial
y las consultas de subárbol son predecibles. Sin tope, todo eso queda abierto. El tope
**abarata el backend**, no solo ordena la UI.

**Consecuencias:**

1. **BE:** `parent_id` (self-FK) + `path` materializado. Ver [`07-handoff-be.md`](07-handoff-be.md).
2. **Ciclos:** una carpeta no puede colgar de su propio subárbol → guarda por prefijo de `path`.
3. **`MoveToFolderDialog` deja de ser una lista simple y pasa a ser un árbol con ruta** — con anidamiento puede haber tres carpetas llamadas «2026», y el nombre solo no alcanza.
4. **Unicidad de nombre pasa a ser entre hermanas**, no global: `Adquirencia / 2026` y `Cierre contable / 2026` conviven (ver I6 y el gotcha de Postgres en el handoff de BE).
5. **Nueva operación: mover una carpeta.** No existía. Endpoint propio + su flujo (F10).
6. **Revelar una carpeta implica abrir toda la cadena de ancestros**, no solo la hoja.
7. **Sin breadcrumb en el sidebar** — el árbol in-place no navega, expande (D16).

**Grafana como precedente sigue aplicando, en el otro sentido:** anidó y arrastró
incompatibilidades con features que asumían un nivel ([#124158](https://github.com/grafana/grafana/issues/124158)).
La lección que queda es el **contador**: si un número puede significar «directos» o
«subárbol» según el contexto, se rompe. Acá se define una sola vez — siempre subárbol,
con desglose en el `title`.

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

## D6 🔄 — Eliminar una carpeta **disuelve un nivel**; nunca elimina tableros

**Revisada el 2026-08-14.** Antes: *«sus tableros vuelven a la lista de sueltos»* vía `ON DELETE SET NULL`.

**Decisión:** al eliminar una carpeta, su contenido —tableros **y subcarpetas**— sube a la
**carpeta madre**. Si la carpeta era de primer nivel, sube a la lista de sueltos (que es el
mismo comportamiento de antes, ahora como caso particular).

**Por qué cambió:** con anidamiento, mandar todo a la raíz **teletransporta** los tableros de
una subcarpeta profunda al primer nivel. El usuario que elimina «Visa» espera que sus tableros
queden en «Adquirencia», no sueltos entre 111 más. Subir un nivel es lo que la metáfora de
carpeta promete.

**Consecuencia técnica — la que más importa:** `ON DELETE SET NULL` **ya no implementa el
feature**. Reparentar es lógica de servicio, en una transacción:

```
1. UPDATE dashboards        SET folder_id = <madre>              WHERE folder_id = <id>
2. UPDATE dashboard_folders SET parent_id = <madre>, path = …    WHERE parent_id = <id>
3. DELETE FROM dashboard_folders                                 WHERE id = <id>
```

La FK se conserva como **red de seguridad** (si algo borra la fila por fuera del servicio, los
tableros no se van con ella), no como el mecanismo. Perdimos la garantía «lo hace el motor de
base de datos», así que **el test de que eliminar no borra tableros pasa a ser obligatorio**
en la suite de BE, no opcional.

**Consecuencias de producto:**

1. **Copy del diálogo (el punto más delicado del feature):** tiene que decir el número **y a dónde va**.
   > **¿Eliminar carpeta?**
   > Se eliminará la carpeta «Visa». Sus **8 tableros y 1 subcarpeta** suben a «Adquirencia»; **no se eliminan**.
2. "Quitar de la carpeta" (F3) tampoco elimina nada y no lleva diálogo de confirmación — es reversible y de bajo riesgo, con toast + "Deshacer".
3. El "Deshacer" tiene que restaurar **tres cosas**: la carpeta, el `parent_id` de sus hijas y el `folder_id` de sus tableros.
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

---

## D10 🔄 — **Solo Tableros** (revierte el alcance transversal)

**Revisada el 2026-08-14.** Antes: *«una carpeta, cuatro entidades»* (ver el registro completo más abajo).

**Decisión:** las carpetas son **solo del panel de Tableros**.

- **Datasets** conserva su lista plana. El tab existe en producción y **no se toca**: sin carpetas, sin «Nueva carpeta», sin «Mover a carpeta» en el menú. Sirve además como control: verifica que el feature no lo afectó.
- **Anomalías** y **Pendientes** quedan fuera por completo. Sus tabs siguen siendo chrome del OC, sin vista implementada en el prototipo.

**Consecuencias:**

1. La tabla vuelve a llamarse **`dashboard_folders`**, no `folders`. El componente se queda en **`features/dashboards/`**, no pasa a `shared/`.
2. **No hace falta** la tabla puente `folder_external_items` ni la coordinación con el equipo del datahub — era el entregable más caro y desaparece.
3. La membresía **heredada** (el diseño para anomalías) deja de aplicar. Era la parte más interesante del alcance transversal y queda como registro, no como entregable.
4. El copy destructivo cuenta **solo tableros y subcarpetas** (ver D6), no entidades mixtas.
5. El wizard (D8) deja de parametrizarse por entidad: siempre dice «Elige los tableros».
6. **SD-1, SD-2, SD-7 y SD-8 quedan fuera de alcance** — todas eran del alcance transversal.
7. Los flujos **F9 (tableros + datasets)** y **F10 (anomalías por carpeta)** se **borraron del board** de Moka. Sus números se reutilizaron para los flujos de anidamiento.
8. `06-organizacion-transversal.md` y `02-benchmark-transversal.md` se **conservan como registro** de la exploración, marcados como descartados.

**Qué sobrevive del alcance transversal:** el **patrón de panel** (D11, los 9 slots) se derivó
comparando los cuatro paneles del OC. Ese análisis sigue siendo válido y útil aunque el feature
ya no los toque: describe la anatomía real del panel de Tableros y dónde entra lo nuevo (slot 7).

---

### 📁 Registro de la decisión anterior (2026-08-04 → 2026-08-14)

*Se conserva porque documenta un diseño que costó y del que puede volver a servir la
idea de membresía heredada si el alcance se reabre.*

**Fecha:** 2026-08-04 · **Origen:** feedback al prototipo.
**Detalle completo:** [`06-organizacion-transversal.md`](06-organizacion-transversal.md) *(descartado)*

**Qué pasó:** el feedback señaló que el contexto de SWAT-577 era más chico que el problema — *"lo que toca lograr es una organización para las diferentes entidades, principalmente tableros y datasets… deberíamos ver si lo hacemos de forma transversal, como ya lo hiciste para anomalías"*.

**Decisión:** una sola tabla `folders` por cuenta, **sin `entity_type`**. "Adquirencia" es UNA carpeta y cada vista muestra lo suyo: el tab Tableros sus 24 tableros, el tab Datasets sus 8 datasets, la vista de Anomalías sus incidentes.

**La membresía tiene dos formas, y esa es la clave del diseño:**

- **Declarada** (Tableros, Datasets): el usuario mueve el ítem. Columna `folder_id` en cada tabla.
- **Heredada** (Anomalías, Pendientes): el evento hereda la carpeta del recurso al que apunta. **No se persiste** — se resuelve en la query, si no quedaría desincronizada cuando el tablero cambie de carpeta.

**Por qué heredada y no declarada para los streams:** nadie puede archivar a mano un incidente que todavía no ocurrió, y si lo archivara, el siguiente incidente del mismo gráfico volvería a quedar sin clasificar. El vínculo ya existe en el modelo (`anomaly_signals.chart_id`, `anomaly_incident_entities.resource_id + resource_type`), así que el usuario organiza **una vez** sobre tableros y datasets y obtiene gratis "las anomalías de Adquirencia" — **incluidas las que aún no existen**.

**Consecuencias:**

1. La tabla se llama `folders`, no `dashboard_folders`. El componente nace en `shared/`, no en `features/dashboards/`.
2. **D3 se reinterpreta:** la exclusividad es **por entidad** (un tablero en una carpeta, un dataset en una carpeta). La carpeta **sí** mezcla entidades — eso es el objetivo.
3. El copy destructivo debe contar por entidad: *"24 tableros y 8 datasets volverán a sus listas"*.
4. El wizard de creación (D8) se parametriza por entidad: "Elige los tableros" / "Elige los datasets".
5. **Corrección del 2026-08-04:** el reparto no es "2 declaradas + 2 heredadas" sino **3 + 1**. El panel de Pendientes lista **conciliaciones** (título "Conciliaciones", buscador, sección de fijadas — misma anatomía que Tableros), así que la conciliación entra a la carpeta de forma **declarada** y el pendiente hereda de ella. Anomalías es el único stream.
6. **Pendientes necesita un modelo extra:** su recurso ancla (la conciliación) vive en el **datahub**, no en `op-center-backend`, así que no admite una columna `folder_id`. Requiere tabla puente `folder_external_items`. Es el último entregable y necesita coordinación con otro equipo.

**Orden de entrega:** Tableros → Datasets → Anomalías → Pendientes.

**Nota de proceso:** recomendé dejar anomalías y pendientes con **filtros guardados** en vez de carpetas, porque son streams. La decisión fue incluirlos con carpetas, y el diseño de herencia es la forma de cumplirlo sin pedirle al usuario que clasifique eventos a mano. Queda **SD-1** abierta: si además se quiere archivar un incidente puntual manualmente.

---

## D12 ✨ — Las cuatro secciones del panel colapsan

**Fecha:** 2026-08-14

**Decisión:** `Configuraciones pendientes`, `Favoritos`, `Tableros` y `Sin carpeta` llevan
chevron y colapsan. El estado persiste en `localStorage`, en una **clave distinta** a la de
las carpetas expandidas.

**Razón:** el hallazgo #3 del benchmark decía que colapsar carpetas no alcanza — con 4 carpetas
y 111 sueltos quedan ~115 filas. Colapsar **secciones** ataca eso directamente: cerrar Pendientes
y Favoritos devuelve 13 filas, y cerrar «Sin carpeta» otras 20. De 59 filas visibles a 26.

**Detalle que importa:** se persiste **lo colapsado**, no lo abierto. Así el default de toda
sección es «abierta», y una sección nueva no aparece cerrada solo por no estar en la lista
guardada. Con la lógica invertida, agregar una quinta sección la mostraría colapsada a todos
los usuarios existentes.

**Jerarquía:** el chevron de sección queda en `text-muted-foreground` y el label mantiene su
registro (`text-xs font-medium`), así que sigue leyéndose por encima de la fila de carpeta
(`text-sm font-medium foreground`). Y aparece una distinción útil: **chevron = sección del
sistema · icono con estado = carpeta del usuario** (ver D13).

**Consecuencia:** durante la búsqueda «Tableros» pasa a ser «Resultados» y el toggle se
deshabilita — ahí no es una sección sino el resultado de una consulta.

---

## D13 ✨ — El icono de carpeta absorbe el chevron

**Fecha:** 2026-08-14

**Decisión:** la fila de carpeta **no lleva chevron**. El propio icono indica el estado:
`folder` cerrada ↔ `folder-open` abierta.

**Razón:** son 16px por fila y un elemento menos que procesar al escanear, en un panel donde
el ancho es el recurso escaso (ver D2). Es el patrón del sidebar de Finder.

**Lo que se conserva:** `aria-expanded` sigue en el botón, así que la semántica para lectores
de pantalla no cambia — lo que se fue es solo el glifo.

**Dónde NO se aplica, deliberadamente:**

| Lugar | Por qué conserva chevron |
|---|---|
| Encabezados de sección (D12) | no tienen icono que pueda cargar el estado |

**Riesgo abierto:** `folder` y `folder-open` se distinguen menos que un chevron a 14px. Queda
como pregunta **D13** del panel de demo: *¿se lee el estado sin el chevron?* Si la respuesta es
que no, la alternativa a evaluar es el patrón de Notion — icono en reposo, chevron en hover, en
el mismo slot y a costo cero de ancho.

---

## D14 ↗️ — El ancho útil de la fila se va a un issue aparte

**Fecha:** 2026-08-14

**Decisión:** el **truncado al medio** y los **botones de fila en hover** se extraen de SWAT-577
y se documentan como mejora independiente:
[`ancho-util-lista-tableros/`](../../ancho-util-lista-tableros/).

**Razón:** ninguno de los dos depende de carpetas. Los dos arreglan un problema que **ya existe
hoy en producción**: el `⋮` reserva 20px invisibles en cada fila, y el truncado al final corta
justo por donde los nombres se distinguen. Meterlos en SWAT-577 los ataría a un feature más
grande y más lento.

**Consecuencia de proceso, y hay que decirla en el ticket:** el prototipo los tiene **activos**,
así que parte de la mejora visual que se ve ahí **no la entrega SWAT-577**. Sin esa nota, la demo
promete más que el ticket.

**Recomendación de secuencia:** abrir el issue de D14 **antes**. Es solo FE, un componente, y
deja la fila con más ancho disponible justo cuando el anidamiento va a empezar a consumirlo.

---

## D15 ✨ — El agrupamiento se resuelve **server-side**

**Fecha:** 2026-08-14 · **Origen:** revisión de `op-center-backend` @ `8cc5bc3b` y `fe-solutions-mf` @ `8aebc1879`

**Decisión:** el árbol **no** se construye en el cliente. El BE expone las carpetas completas
con sus contadores, y los tableros paginados por carpeta.

**Por qué:** verificado en código, no supuesto.

| Hallazgo | Fuente |
|---|---|
| `DASHBOARDS_PAGE_SIZE = 20` + `useInfiniteQuery` + `IntersectionObserver` | `DashboardList.tsx:117` |
| `page_size` con tope duro `le=100` | `utils/common/dependencies/pagination.py:8` |
| `search`, `sort_by`, `sort_order` server-side | `api/views/dashboards.py:68-106` |

Con 155 tableros y tope de 100 por página, **no existe un «traer todo»**. Cualquier diseño que
asuma la lista completa en memoria —contador de subárbol, orden global, árbol completo— no es
implementable.

> ⚠️ **El prototipo hace exactamente eso.** Construye `treeRows` recorriendo los 159 tableros en
> memoria y calcula los contadores en cliente. Es válido como exploración de interacción y **no
> es implementable tal cual**. Es el riesgo #1 del handoff: se ve implementable y no lo es.

**Contrato:** carpetas completas sin paginar (son pocas, I5) + tableros paginados por carpeta,
pedidos **al expandir**. Detalle en [`07-handoff-be.md`](07-handoff-be.md).

**Nota:** este riesgo **ya estaba escrito** en [`00-exploracion-fe-be.md`](00-exploracion-fe-be.md) §5.1
desde el 2026-08-03. Se perdió de vista al diseñar el anidamiento. Queda como D15 para que no
vuelva a pasar.

---

## D16 ✨ — Árbol in-place; se descarta el drill-down

**Fecha:** 2026-08-14 · **Cierra I4** y el A/B de la Etapa 6.

**Decisión:** el panel expande el árbol **en el mismo lugar**. Se descarta la navegación por
niveles con breadcrumb, que se había prototipado como variante B.

**Razón:** el gesto más frecuente del panel es **cambiar de tablero**, y el drill-down le suma
clics justo a eso — para saltar de un tablero de «Adquirencia / Visa» a otro de «Cierre contable»
hay que subir dos niveles y bajar dos. El árbol in-place lo hace en un clic. Es el mismo
argumento que ya había dado el benchmark (I4); el A/B se armó para ponerlo a prueba y la
conclusión se sostuvo.

**El trade-off que se acepta a cambio:** el drill-down tenía una ventaja real que el in-place no
puede igualar — **el nombre nunca pierde ancho**, porque siempre ves el nivel actual sin indentar.
El in-place paga **12px por nivel**. Se acepta porque las tres mitigaciones de D2 lo dejan en un
peor caso de 158px, y porque el costo de navegación se paga en **cada** cambio de tablero mientras
el costo de ancho se paga solo en el nivel más profundo.

**Consecuencias:**

1. **Sin breadcrumb** en el sidebar. El único breadcrumb del feature es la **ruta** en los
   resultados de búsqueda (I3) y en el chip del header del tablero abierto.
2. **El chevron solo existe en los encabezados de sección** (D12). En la fila de carpeta el icono
   lleva el estado (D13). Ya no hay un lugar donde el chevron signifique «entrar».
3. Se elimina del prototipo el switch A/B y ~100 líneas de la variante B.
4. **Divergencia deliberada con Almacenamiento**, que sí navega por niveles. Es la misma
   divergencia que I3 ya había asumido para la búsqueda: el panel de Tableros es una lista de
   trabajo, no un explorador de archivos.

**Puerta abierta:** si la telemetría mostrara que muchas cuentas llegan al tope de 3 niveles y el
ancho se vuelve un problema real, el drill-down vuelve a estar sobre la mesa — pero como
alternativa, no como complemento. Tener las dos formas de navegar el mismo árbol sería peor que
cualquiera de las dos.

---

## D17 🟡 — Tres anchos fijos de panel: `sm` 288 · `md` 384 · `lg` 480

**Fecha:** 2026-08-18 · **Origen:** `cmt_mst640rv` de la revisión en Ohana ·
**Estado: ✅ CERRADA el 2026-08-18.** Mecanismo decidido (arrastrar el borde, sombreando la
franja del delta) y **los tres valores confirmados: 288 · 384 · 480.**
Queda **re-sincronizar D2/D13/D16, I4, `design.md` y `07-handoff-fe` §4**.

**Estado en producción, verificado:** el panel **no** es redimensionable. `w-72 min-w-72` fijo
(`OcContentLayout.tsx:171`), sin handle ni preferencia de ancho.

**Decisión propuesta:** el ancho pasa a ser una **preferencia del usuario** con tres valores
fijos, persistida en `localStorage`.

### Por qué esos tres números

No se eligieron: cada uno responde a una pregunta. Es la cuenta de D2 parametrizada, y a 288px
reproduce exacto sus números — que es la prueba de que es la misma cuenta.

| | px | Clase | Qué pregunta responde |
|---|---|---|---|
| `sm` | **288** | `w-72` | Lo de hoy. Es el **default**: elegirlo no cambia nada de producción. |
| `md` | **384** | `w-96` | **El anidamiento deja de costar ancho.** Un tablero en el nivel 3 pasa a 262px, 60px *más* que un tablero suelto a `sm` (202px). |
| `lg` | **480** | `w-[30rem]` | **El peor caso real entra entero** hasta el nivel 3: 45 caracteres ≈ 329px. |

Presupuesto para el nombre, por tamaño y nivel:

| | `sm` 288 | `md` 384 | `lg` 480 |
|---|---|---|---|
| Tablero suelto | 202px · 27c | 298px · 40c | 394px · 54c ✓ |
| Carpeta nivel 1 / 2 / 3 | 202 / 190 / **178** | 298 / 286 / **274** | 394 / 382 / **370** ✓ |
| Tablero dentro, nivel 1 / 2 / 3 | 190 / 178 / **166** | 286 / 274 / **262** | 382 / 370 / **358** ✓ |

✓ = entra el nombre más largo sin truncar. **Solo `lg` lo logra en todos los niveles.**

> Las filas de carpeta ya **no descuentan contador** (D18), así que una carpeta y un tablero a
> la misma indentación miden lo mismo. La tabla de D2 (182/170/158) se calculó **con** contador
> — de ahí los +20px.

> **⚠️ Corrección a D2.** El peor caso son **45 caracteres**, no 40:
> `Adquirencia_2026_06_04_conciliacion_master_v2`. D2 se calibró contra
> `Adquirencia_2026_06_04_conciliacion_visa` (40), que es un peor caso optimista — el propio
> generador de nombres del producto pone sufijos `_v2` y `_master`. **Esto hay que corregir en
> D2 pase lo que pase con D17.**

**Se descartó la propuesta de arranque del plan (288/360/440):** 360 y 440 no salían de ningún
criterio, y 440 se queda **3px corto** para el peor caso al nivel 3 — habría prometido algo que
no cumple.

### Mecanismo — ✅ A · arrastrar el borde (decidido el 2026-08-18)

El comentario pedía dos cosas a la vez («explorar un **resize**» y «medidas **fijas**»), así que
se prototiparon las dos:

| | Cómo | A favor | En contra |
|---|---|---|---|
| **A** ✅ | Handle de arrastre en el borde, con **snap** a los tres valores | Cuesta **0px** del header. Es un resize de verdad. | Hay que descubrir el borde. |
| **B** ⛔ | Control discreto **S/M/L** en el header del panel | Se descubre solo. Lectura literal del comentario. | Se come ~72px del **slot 1**, y **obliga a interpretar `S/M/L`**. |

**Por qué se cayó B, y de paso el rótulo:** `S/M/L` es vocabulario de diseñador. No le dice al
usuario **hasta dónde va a llegar el panel**, que es la única pregunta que tiene mientras
arrastra. La primera versión de A tenía el mismo defecto en otro lugar: un badge que escribía
«MD · 384px» durante el arrastre. Escribir el tamaño es admitir que no se ve.

**El feedback correcto es espacial, no textual.** Al arrastrar se sombrea **solo la franja que
el panel gana o devuelve**, y una línea azul de 2px marca dónde va a quedar el borde. Las tres
paradas quedan marcadas con líneas tenues.

**Se sombrea el delta, no el panel entero** — segunda corrección de Andrés. Pintar los 288px
completos tapa la lista que el usuario está leyendo, y de paso resalta lo que no importa: la
pregunta no es «cuánto va a medir» sino **«cuánto gano»**. La franja arranca en el borde actual
y termina en el destino, así que funciona en los dos sentidos: creciendo se pinta en azul lo
que se suma; encogiendo, en gris lo que se devuelve al contenido. Con el destino igual al
tamaño de partida la franja mide 0 y no se dibuja nada, que es la lectura correcta.

Dos cosas más se resuelven solas con esto:

1. **El snap deja de sentirse como un bug.** El panel no sigue al cursor —salta entre tres
   valores— y antes eso se leía como que la interfaz no responde. Ahora lo que se mueve es la
   zona, y el salto se lee como intención.
2. **Las medidas fijas se enseñan sin nombrarlas.** Ver tres paradas posibles comunica «hay
   tres anchos» mejor que tres letras.

El rótulo se eliminó de todas partes de cara al usuario: badge de arrastre, tooltip del riel
colapsado y `aria-label` del separador (ahí el número lo dan `aria-valuenow`/`min`/`max`, que
es lo que corresponde al patrón).

Paridad por teclado con `role="separator"` + flechas (patrón WAI-ARIA *window splitter*),
mismo criterio que **D7** con el drag. Durante el arrastre se suprime la selección de texto:
sin eso el gesto va seleccionando los nombres de la lista al pasar.

> **Crédito donde va:** esto lo corrigió Andrés al revisar el prototipo. La versión que yo
> había hecho pasaba el problema del control B (nombrar el tamaño) al mecanismo A en vez de
> resolverlo.

### Persistencia

Clave propia — `oc_sidebar_width` en producción. **No se unifican** las tres claves de
preferencia: producción ya persiste el colapso en `oc_sidebar_collapsed` con su propia clave
(`OcContentLayout.tsx:19`), así que el ancho va en paralelo. Unificarlas sería migrar algo que
ya funciona a cambio de nada.

### Interacción con el colapso automático: ya estaba resuelta

No hubo que inventar nada. `restoreIfNoAutoCollapse()` (`OcContentLayout.tsx:86`) ya separa la
**preferencia del usuario** de los **motivos de colapso automático** (viewport angosto, panel
lateral abierto, modo edición de datasets) y restaura cuando el motivo desaparece. El ancho se
cuelga del mismo mecanismo:

**Gana el colapso, y al reexpandir se recupera el tamaño elegido.**

### 🔴 Hallazgo colateral, y pesa más que D17

**El umbral de colapso mide el contenedor, no la ventana.** `COLLAPSE_WIDTH_THRESHOLD = 1200`
(`:56`) se compara contra `entry.contentRect.width` del contenedor del OC (`:127`), y
`contentRect` **excluye el padding** — o sea que del ancho de ventana ya se descontaron el nav
de plataforma y el `px-6`.

Con el nav en 256px, el colapso se dispara alrededor de los **1504px de ventana**: **en un
portátil de 1440px el panel arranca colapsado y el árbol de carpetas no se ve.**

**Pendiente de verificar:** el nav de plataforma no vive en `fe-solutions-mf`, así que los
256px son el supuesto del prototipo. El número exacto cambia; la dirección no. Si se confirma,
esto le pega a la premisa de **D2** y **D16**, que asumen el panel expandido — y hay que
resolverlo **antes** de discutir 384 vs 480.

**Consecuencias si se aprueba:**

1. **FE:** `OcContentLayout` pasa de clase fija a ancho por preferencia. Es el único archivo.
2. **Nada de BE.** No toca modelo, API ni permisos.
3. **Costo a validar:** a `lg` en 1920px el grid de 2 columnas del tablero baja a ~543px por
   gráfico. Es el argumento más fuerte para que el default siga en `sm`.
4. **Probablemente no es de SWAT-577.** Beneficia al panel exista o no el feature de carpetas,
   igual que **D14** — y es la **tercera palanca de ancho** del mismo problema. Recomendación:
   que las tres viajen juntas en `ancho-util-lista-tableros/`.

---

## D18 ✨ — El contador del subárbol sale de la fila de carpeta

**Fecha:** 2026-08-18 · **Origen:** `cmt_mst64r43` («QUitar este contador») · **Cierra ③.**

**Decisión: el contador se quita de la fila.** El total del subárbol **no desaparece del
producto** — se muda al `title` y al `aria-label`, que cuestan 0px de ancho.

> **Corrección de rumbo.** La primera versión de D18 decidió lo contrario: que el contador se
> quedaba, porque el motivo del comentario era *ancho* y ② devolvía 96px donde el contador
> devolvía 20. **Ese razonamiento contestaba una pregunta que nadie hizo.** El comentario era
> una instrucción («quitar este contador»); el motivo explicaba *por qué*, no *si*. Convertir un
> «por qué» en un «si o no» y resolverlo con una resta fue un error de lectura, no una decisión
> de diseño. Queda registrado porque el razonamiento de la resta sigue siendo válido para lo que
> sí decidía: que **quitarlo no era la forma de recuperar ancho**. Pero se quita igual, porque el
> ancho no era la única razón para quitarlo.

### Qué gana la fila

| | Con contador (D2) | Sin contador | |
|---|---|---|---|
| Carpeta nivel 1 | 182px | **202px** | +20 |
| Carpeta nivel 2 | 170px | **190px** | +20 |
| Carpeta nivel 3 | **158px** | **178px** | +20 |

Y aparece una propiedad que antes no estaba: **una carpeta y un tablero a la misma indentación
miden exactamente lo mismo.** La fila deja de tener dos presupuestos distintos según el tipo,
lo que hace la tabla de D17 más simple de razonar.

Sumado a ② en `lg`, la carpeta de nivel 3 pasa de **158px a 370px**.

### Lo que se pierde, y hay que decirlo

**Una carpeta cerrada ya no dice cuánto tiene adentro.** Era la única señal de volumen sin
expandir, y es justo el caso donde más servía: decidir si vale la pena abrirla.

Mitigación: el total sigue en el `title` (hover) y en el `aria-label` (teclado y lector de
pantalla). No es equivalente — un dato que exige un gesto no es un dato que se escanea.

**A validar en la próxima revisión:** si al recorrer el panel se extraña saber el volumen de una
carpeta cerrada. Si se extraña, la salida **no** es volver al contador en todas las filas, sino
mostrarlo **solo en carpetas colapsadas** — con la carpeta abierta el número es redundante
porque los hijos ya están a la vista.

### Lo que NO cambia de D2

La **definición** del contador sigue intacta para donde sí se muestre (`title`, `aria-label`):
**total del subárbol**, con desglose «directos · en total» cuando hay hijas. La lección de
Grafana ([#124158](https://github.com/grafana/grafana/issues/124158)) sigue en pie: un número
que significa una cosa u otra según el contexto se rompe. Acá se define una sola vez.

**Los contadores de sección no se tocan:** «Tableros» (slot 1), «Configuraciones pendientes
(8)», «Favoritos (5/15)» y «Sin carpeta» existen en producción y no son de lo que hablaba el
comentario, que estaba anclado en el `span` de una fila de carpeta.

---

## ~~D19~~ ⛔ — Acordeón exclusivo entre secciones: descartada

**Fecha:** 2026-08-18 · **Origen:** `cmt_mst69j96` · **Sacada del plan por Andrés.**

No se diseña. **D12 se mantiene:** las cuatro secciones del panel colapsan de forma
**independiente**, y las carpetas del árbol también.

Queda el registro porque el comentario sigue `open` en Ohana, y conviene que esté escrito por
qué no se hizo. Los riesgos que se habían identificado —y que ya no hay que resolver— eran que
«Tableros» es la sección principal y un acordeón exclusivo la cerraría para mostrar 5 atajos,
y que entre carpetas chocaría con **I2** (estado persistido) y con «revelar después de actuar».

---

## D20 🟡 — Solo quien creó la carpeta puede renombrarla, moverla o eliminarla

**Fecha:** 2026-08-18 · **Origen:** `cmt_mst66vz6` («¿solo elimino las carpetas que yo creo?») ·
**Revierte D1.b** · **Estado: a confirmar con BE.**

**Decisión:** la autoría gobierna las tres acciones que cambian **la carpeta misma**.
`oc:manage_access` funciona como **escape**.

| Acción | ¿Restringida? | Por qué |
|---|---|---|
| Renombrar carpeta | ✅ solo el autor | Cambia cómo la ven todos |
| Mover carpeta a… | ✅ solo el autor | Idem, y reordena el árbol de otros |
| Eliminar carpeta | ✅ solo el autor | Disuelve un nivel (D6) |
| **Agregar tableros** | ❌ libre | Una carpeta es una **ubicación compartida** (D1): llenarla es colaborativo |
| **Nueva subcarpeta** | ❌ libre | La subcarpeta que yo creo **es mía**, así que la puedo gestionar |
| Mover / quitar un tablero | ❌ libre | Lo gobierna la regla del tablero (`hasAccess`), no la carpeta |

La línea que separa las dos mitades: **restringir lo que altera la carpeta de otro, no lo que
la usa.** Sin eso, «solo el autor» se vuelve un candado que impide colaborar en la ubicación
compartida que D1 definió.

### El escape, que es la parte que hace viable a (b)

**`oc:manage_access` puede gestionar cualquier carpeta.** No es una política paralela: es la
salida al problema que hacía inaceptable a (b) a secas.

> Si solo el creador puede eliminar, la carpeta de alguien que **se fue del equipo** queda
> inmanejable **para siempre**.

Reusa un permiso que **ya existe** y ya gobierna «Gestionar acceso», así que no hay modelo
nuevo ni un estado «carpeta abandonada» que mantener. El prototipo lo modela con una carpeta
huérfana real (`2025`, creada por alguien marcado `inactive`) y un toggle para simular el
permiso.

### El copy cambia con el motivo

No alcanza un mensaje único, porque las dos situaciones ofrecen salidas distintas:

| Caso | Mensaje |
|---|---|
| La creó alguien que **sigue** en la cuenta | *«Solo María, que creó esta carpeta, puede renombrarla, moverla o eliminarla.»* |
| La creó alguien que **se fue** | *«Lucía ya no está en la cuenta. Solo alguien que gestione accesos puede renombrarla, moverla o eliminarla.»* |

Mandar a «pedirle a Lucía» cuando Lucía no está sería un callejón sin salida. **Un mensaje
de permisos tiene que nombrar la salida, no solo la puerta cerrada.**

### Dónde vive la autoría — y dónde NO

**No va en la fila.** Un «creada por María» visible gastaría exactamente el ancho que **D17**
acaba de recuperar; poner las dos decisiones juntas en el mismo sprint y que una se coma a la
otra sería incoherente. Vive en tres lugares que cuestan **0px**:

1. El **`title`** de la fila (`Adquirencia / Visa · creada por María`).
2. El **`aria-label`** del `treeitem`, para que con teclado tampoco haya que abrir el menú.
3. El **pie del menú `⋮`**, una sola vez y no como tooltip por ítem: tres tooltips que dicen
   lo mismo es ruido, y un tooltip no se lee con teclado. Va con `role="note"` junto a los
   `aria-disabled`.

**Los ítems se deshabilitan, no se ocultan** — mismo criterio que el tope de 3 niveles:
esconder una acción que existe en otras carpetas deja al usuario buscándola.

### Dos trampas que el prototipo cierra

1. **Una carpeta recién creada tiene que ser gestionable por quien la creó.** Si `createdBy` no
   se asigna al crear, la creás y no la podés ni renombrar. Hay **cuatro** rutas de creación en
   el proto y las cuatro lo asignan.
2. **«Deshacer» un borrado restaura al autor original, no a quien deshace.** Si no, eliminar +
   deshacer sería una forma de **apropiarse de la carpeta de otro** — un escalamiento de
   privilegios por la puerta de atrás.

### La tensión con D1.b, explícita

D1.b decía *«no se introduce un permiso nuevo»*, y argumentaba que ninguna acción de carpetas
es destructiva porque todo tiene «Deshacer». **D20 respeta la letra y rompe el espíritu:** no
introduce un permiso nuevo (reusa `oc:manage_access`), pero **sí agrega una comprobación de
autoría que hoy no existe**.

Lo que habilitó el cambio: **D6 debilitó la premisa.** Eliminar ya no lo garantiza el motor de
base de datos (`ON DELETE SET NULL`), es lógica de servicio que reparenta antes de borrar. La
reversibilidad dejó de ser gratis.

**Consecuencias:**

1. **BE:** el dato ya existe (`created_by`, §1.1 del handoff BE). Falta **devolverlo en el
   listado** —hoy no viaja— y **validar en el endpoint**, no solo en la vista: un permiso que
   solo vive en el FE no es un permiso.
2. **FE:** el menú de carpeta y las cuatro rutas de creación.
3. **A confirmar con BE:** que `oc:manage_access` sea el override correcto, y si la validación
   de autoría vive en el servicio o en la política de acceso existente.
4. **Drag & drop:** D7 hace del drag un alias de «Mover a». Las carpetas no son arrastrables en
   el proto, así que no hay inconsistencia hoy — **pero si se agrega, tiene que respetar D20.**

---

## Alcance de la v1 — qué NO entra

| Fuera de alcance | Razón | ¿Reversible? |
|------------------|-------|--------------|
| **Más de 3 niveles** de anidamiento | D2 revisada — el tope abarata el `path` del BE | Sí, aditivo |
| Carpetas en **Datasets, Anomalías y Pendientes** | D10 revisada | Sí, aditivo |
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
