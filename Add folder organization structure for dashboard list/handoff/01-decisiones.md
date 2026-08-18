# Decisiones de producto y diseño — Carpetas en la lista de tableros (SWAT-577)

**Fechas:** D1–D7 el 2026-08-03 (antes de prototipar) · **D8 y D9 el 2026-08-04, tras probar el prototipo**
· **D2, D6 y D10 revisadas el 2026-08-14** · **D12–D15 abiertas el 2026-08-14**
**Decidido por:** Andrés Ladino (UX) con la exploración técnica de [`00-exploracion-fe-be.md`](00-exploracion-fe-be.md)
**Estado:** cerradas. Cambiar D1 o D3 después de la Etapa 7 implica rehacer el modelo de BE.

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
