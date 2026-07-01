# Handoff — Anomalías: filtros, paquetes de notificación y resumen

**Prototipo:** `notificaciones-resumen/index.html` → vista de **Anomalías** (tab superior "Anomalías").
**Fuente:** sesiones Granola **30-jun-2026** (am: épicas y cambios de UI · **pm: design review con ingeniería/Sergio**) + comentarios de Ohana.
**Plan:** `plan-notificaciones-paquetes-30jun.md`.
**Historias de UX (complemento):** `handoff-anomalias-historias-ux.md` (5 HU con estados, criterios F/X, a11y).
**Regla del equipo:** *donde un cambio de UI no se enumere explícitamente, no se ejecuta en desarrollo.* Por eso este handoff lista **cada** cambio, incluso los chicos.

> ⚠️ Separar en épicas de ingeniería: **(1) Filtros**, **(2) Paquetes de notificación — incluye el resumen como modo de entrega**, **(4) Alertas por fuente**. Más la épica transversal de **fixes de UI**.

---

## 🔄 Actualización 30-jun (pm) — design review con ingeniería

Esta tanda **supersede** partes del documento. Donde haya conflicto, manda esta sección.

1. **Tablero + Recurso → un solo bloque "Entidades afectadas" (OR).** Eran entidades jerárquicas tratadas como filtros planos independientes: dejaban armar condiciones imposibles (un recurso que no pertenece al tablero elegido → nunca notifica). Ahora es **una sola categoría** que lista tableros y recursos juntos; **todo lo seleccionado se combina con `o`** (no compiten). Aplica en los filtros de Gestión **y** en el alcance del paquete. → reemplaza "Recurso/Tablero" separados de Épica 1 y Épica 2.
2. **Resumen consolidado deja de ser sección propia → es un MODO DE ENTREGA dentro del paquete.** El bloque "¿Cuándo quieres que te avisemos?" del editor tiene **dos entregas** sobre el mismo alcance: **Aviso por evento** (uno por cada evento, apenas ocurre) y **Resumen consolidado** (1×día). Se pueden activar las dos. El alcance y los canales se **heredan del grupo** (no se repiten filtros). → **anula la Épica 3** como sección independiente.
3. **Parámetro t-n (1 a 5) en el resumen + microcopy de período.** El corte del resumen siempre cierra el día anterior; la **hora solo define cuándo llega, no qué período cubre**. El selector "Qué período resume" (t-1 … t-5) cubre el **lag operativo** del cliente (operaciones a t-4, etc.): "hoy recibo lo que sigue abierto hasta hace n días".
4. **Filtro dinámico de fecha (t-n) en la lista de incidentes**, guardable. Rango **relativo** (Hoy, t-1 … t-5) que **se mueve solo cada día** (mañana muestra hasta el día siguiente sin tocar el calendario).
5. **Separar "¿qué incidentes te interesan?" (alcance) de "¿cuándo te avisamos?" (momento).** El **Estado** sale del alcance del paquete (se pisaba con el momento creado/confirmado). El alcance es solo entidades + tipo; el momento vive en la entrega "Aviso por evento".
6. **Slider de sensibilidad reencuadrado.** Se quita "nula" (se leía como "mutear"). Extremos: izq **"Solo mi umbral"** (alerta de umbral fija) ↔ der **"Detección adaptativa"** (el sistema decide qué es anómalo). **Fix del 100%:** la banda de atención **nunca llega al centro** (núcleo normal, `CORE=0.30`); aun al máximo no se pinta toda la gráfica, porque la detección adaptativa no marca "todo punto", solo lo inusual.
7. **Pendiente con Iván (notification center):** confirmar que el ID de usuario de Slack se soporta como **parámetro del template** antes de comprometer el etiquetado. Además: **2 templates** (creación vs updates) y **desacoplar en el listener** la lógica compartida entre tópicos de señales e incidentes.

---

## ÉPICA 1 — Filtros de la vista de Gestión

**Dónde:** Anomalías → Gestión → barra "Filtrar / Ordenar / Guardados".

### Cambios de UI (enumerados)
1. **Multiselect dentro de cada categoría.** Al abrir Entidades afectadas / Estado / Tipo, se pueden marcar **varios valores**. Cada opción muestra un **check** al elegirse; el submenú **no se cierra** (footer con "Limpiar" y "Listo").
2. **Lógica de combinación:** dentro de una categoría los valores se unen con **`o`** (OR); entre categorías distintas, con **`Y`** (AND). En los chips aplicados: el valor se lee `A o B`; entre chips aparece un conector **"Y"**.
3. **Quitar el filtro "Severidad".** Eliminado del menú. Motivo: no exponer severidad hasta que el usuario pueda **definir sus propios niveles**. (Vuelve cuando sea configurable.)
4. **Filtros que quedan:** **Entidades afectadas**, Estado, Tipo, Fecha (dinámica). *(30-jun pm: Recurso + Tablero se fusionaron en "Entidades afectadas", OR interno — ver changelog #1.)*
   - **Entidades afectadas** = tableros + recursos en una sola lista (con subtítulos "Tableros" / "Recursos"); todo lo elegido combina con `o`. Evita condiciones imposibles entre entidades jerárquicas.
   - **Tipo** = problem categories reales de BADS (Ingesta): Archivo faltante, Archivo fallido, Archivo vacío, Archivo duplicado, Variación de volumen.
   - **Fecha = rango dinámico** (no rango único estático): Hoy, t-1 … t-5 (y "Últimos 30 días"). Relativo a hoy, **se mueve solo cada día**; guardable. Valor único (reemplaza).
5. **Filtros guardados (recurrentes).** Botón **"Guardar filtro"** en el panel de chips → nombrar inline. Botón **"Guardados"** en la barra → menú con los filtros guardados (cargar / eliminar). Sin automatizaciones: solo guardar y reutilizar.

### Nota crítica para ingeniería
⚠️ **Producción HOY no soporta multiselect dentro de cada filtro.** Es un cambio nuevo de endpoints/UI. Documentarlo como tal. Según el equipo: casi 100% frontend + poco backend (Ayed puede apoyar).

---

## ÉPICA 2 — Paquetes de notificación de incidentes

**Dónde:** Anomalías → Configuración → **Notificaciones de incidentes**.

> **Cambio de paradigma:** ya **no** es un formulario único de config global. Es una **lista de paquetes (reglas)**. Un incidente se evalúa contra todos los paquetes **activos**; si coincide con varios, se notifica por cada vía. Cada usuario crea los suyos (quien configura, recibe).

### Cambios de UI (enumerados)
1. **Vista de lista plana** de todas las notificaciones configuradas. Cada tarjeta: nombre, resumen del alcance, toggle activo/inactivo, tags (momento · actualizaciones · canales) y acciones **Duplicar / Editar / Eliminar**. Botón **"Crear notificación"** arriba a la derecha.
   - **Empty state / first-run (activo, con forma):** en first-run el header se aligera (oculta subtítulo + botón de arriba) y el empty state lleva la explicación + el CTA. Contiene: **mini-diagrama** (notificación fantasma → wires → previews de **Email** y **Slack**, comunica "1 notificación llega por varios canales") + **plantillas para empezar** ("Incidentes confirmados de mis tableros", "Archivos faltantes o fallidos") que abren el editor **pre-llenado** + CTA primario **"Crear notificación"**. No es un "Sin resultados" plano.
   - El diagrama va dentro de un frame **"Vista previa"** (tintado + caption + `pointer-events:none`) para que se lea como ilustración, no como UI clickeable; las plantillas/CTA quedan fuera del frame.
   - **Motion pedagógico:** pulso de flujo (dashes en primario recorriendo los wires → enseña la dirección a los canales, loop 1.6s) + entrada escalonada (fade+rise, 320ms ease-out, delays 0/70/140/210/280ms). Solo transform/opacity/stroke-dashoffset; respeta `prefers-reduced-motion: reduce`.
   - 🎨 **Pendiente a futuro:** reemplazar el mini-diagrama por una **ilustración CSS más pulida** (hoy es un preview funcional interino).
   - **Duplicar** clona la configuración como una nueva notificación ("… (copia)") y abre el editor — implementa el *"me gusta esta config, me la copio"* de Granola.
   - ⚠️ **Sin concepto de dueño/equipo.** No hay separación "Mías / Del equipo" ni avatar de dueño. Se muestran todas las notificaciones configuradas en una lista; clonar es la vía para reutilizar una existente.
2. **Editor de paquete** (al crear/editar), con estos bloques **que no se interfieren** *(reestructurado 30-jun pm)*:
   - **Nombre** de la notificación.
   - **El alcance va en DOS bloques separados** (el Estado salió: se pisaba con el momento — changelog #5):
     - **Bloque 1 · "¿Qué entidades te interesan?"** → botón **"Agregar entidad"** (menú con buscador + lista de tableros/recursos, OR) + select **"aplica un filtro guardado"** (guardados / "Filtro actual de la vista" / "Todos mis incidentes"; al aplicarlo **solo se conservan Entidad y Tipo**, se descarta el Estado) + chip agrupado del alcance.
     - **Bloque 2 · "¿Qué tipos de incidente?"** → **chips seleccionables** (multiselect OR) de las 5 categorías de BADS. Vacío = todos los tipos.
   - **Bloque 3 · "¿Cuándo quieres que te avisemos?"** → dos **entregas** sobre el mismo alcance, combinables:
     - **Aviso por evento** (toggle): **momento(s) del ciclo de vida** del incidente, multiselección — **Cuando se cree** / **Cuando entre en observación** / **Cuando se confirme** / **Cuando se resuelva** + **Recibir actualizaciones** (toggle; reconfirmaciones, cambios de hipótesis, otros recursos afectados). *(Los estados del incidente se eligen aquí como momentos, no en el alcance, para no duplicarlos.)*
     - **Resumen consolidado** (toggle): **hora** + **zona horaria** (default 08:00 · CO Bogotá) + **"Qué período resume"** = **t-1 … t-5** con microcopy: *el corte siempre cierra el día anterior; la hora solo define cuándo llega, no qué período cubre*. 1×día, agrupa los incidentes del alcance.
   - **Canales** → mismo patrón que el "¿Dónde notificar?" del KPI: **tarjetas de canal activables** (Email / Slack) con toggle; Email → destinatarios; Slack → canales + **Etiquetar a personas por ID de usuario** (no `@nombre`; nota "Copiar id. de miembro"). **Aplican a ambas entregas.** Si el canal está apagado, no se notifica por ahí.
   - **Validación:** guarda solo si hay **≥1 entrega activa** (aviso por evento o resumen), en el aviso por evento **≥1 momento**, y **≥1 canal**.
   - Acciones: Cancelar / Guardar notificación.

### QUITADO del formulario anterior (no va)
- ❌ Checkbox **"Cuando la severidad sea alta"** (severidad pospuesta).
- ❌ Checkbox **"Cuando no tenga responsable asignado"** (fuera de scope ahora).
- ❌ Checkbox **"Cuando me etiquen"** → es **notificación de flujo de la app** ("te asignaron / te etiquetaron"), otro template, **otro feature**. No se configura aquí.
- ❌ Tarjeta **"Qué incluir en la notificación" (Hipótesis / Acción recomendada / Resumen / narrativa)** → eso va **directo en el template** (Block Kit / email), no es configurable por el usuario.
- ✅ **Resumen consolidado** *(actualizado 30-jun pm)*: NO sale a una sección aparte. Vive **dentro del editor**, como segunda **entrega** del Bloque 2 (ver arriba). Anula la decisión previa de "sección propia".

### Lógica (para ingeniería, no es de este prototipo)
- Incidente = evento. En cada evento (creación/update) se evalúan las reglas de todos los paquetes activos → match → notifica.
- Condiciones tipo filtro de Gmail; condiciones contradictorias → cero notificaciones (avisar visualmente si aplica).
- Anti-spam: por default, quien configura el paquete es quien recibe; agregar a terceros es explícito (en canales).

---

## ÉPICA 3 — Resumen consolidado · ~~sección propia~~ → ANULADA (ahora es modo del paquete)

> ⚠️ **Superseded el 30-jun pm.** En el design review con ingeniería (Sergio) se decidió **mover el resumen DENTRO del grupo de notificación**, porque como sección aparte obligaba a **repetir el filtro** y permitía resumir algo distinto a lo que se notifica en tiempo real. Ya **no** hay ítem de nav "Resumen consolidado" ni página independiente.
>
> El resumen vive como **segunda entrega** del editor de paquete (Épica 2, Bloque 2): mismo **alcance** y mismos **canales** heredados del grupo, + hora + zona + **t-n** (1…5) con microcopy de período. Ver changelog #2 y #3.

*(Esta épica se elimina del plan de ingeniería; su funcionalidad se absorbe en la Épica 2.)*

---

## ÉPICA 4 — Alertas por fuente (Ingesta de datos)

**Dónde:** En el **detalle del tablero** (Tableros → abrir tablero) → tab **"Ingesta de datos"** (junto a Calidad / Salud / Métricas). También accesible desde Anomalías → Configuración → Ingesta. Clic en una fuente → **modal** "Monitorear &lt;fuente&gt;" (`#sourceDialog`, overlay).

> Aquí se definen las **señales/alertas a nivel de fuente** (los thresholds que generan los `AnomalySignal` / problem categories que BADS luego agrupa en incidentes). Es el origen de los incidentes que las Épicas 1-3 filtran/notifican.

### Cambios de UI (enumerados)
1. **Grid de fuentes** (ya existía): cada fuente con "Activar monitoreo AI" / "Monitoreo activo". Ahora la tarjeta es **clickeable** → abre el detalle (reemplaza la grid; "Volver" regresa).
2. **Modal de detalle de fuente** (`#sourceDialog`, overlay) con **sidebar izquierdo de 2 ítems**: **Configuración** y **Alertas** (mismo patrón visual que el sidebar del diálogo del KPI, pero solo esos dos). Adaptado a vanilla desde `config-system-kpi/index.html` → `inline-source-detail`:
   - **Configuración** =
   - **Análisis inteligente** (colapsable): resumen + límites sugeridos (Media / inferior / superior). Estático.
   - **Ventana de tiempo**: llega a las · avisar si pasa de las · zona horaria → señal de **archivo faltante/tarde**.
   - **Cómo se monitorea**: radio *Igual todos los días* / *Por día de la semana* (este último marcado **Próx.**).
   - **Comportamiento de la fuente**: Cantidad de archivos (mín/máx + sugerencia) · Cantidad de registros (mín/máx) · **Otros comportamientos**: Archivos vacíos / duplicados / fallidos (switch + umbral %).
   - **Alertas** (2do ítem del sidebar) = **mismo patrón de 3 tarjetas que las Alertas del KPI**: ¿Cuándo notificar? (Nunca / Solo al final / En tiempo real + empty state + ventana de monitoreo, editar→Configuración) · ¿Dónde notificar? (Email/Slack + ID de Slack) · Idioma. Las funciones del patrón (`whenPick`, `renderWhen`, `toggleChannel`, `isChannelInvalid`/`showChannelWarning`) son **scope-aware** vía `data-notif-section` (un warning por sección, no chocan KPI vs fuente).
   - Footer: Salir / Guardar.

### Mapeo a BADS `problem_category`
| Sección del panel | señal / `problem_category` |
|---|---|
| Ventana de tiempo (llega/avisar) | `MISSING_FILE` |
| Cantidad de archivos / registros (mín/máx) | `VOLUME_VARIATION` |
| Otros comportamientos → Archivos vacíos | `UNEXPECTED_EMPTY_FILE` |
| Otros comportamientos → Archivos duplicados | `DUPLICATED_FILE` |
| Otros comportamientos → Archivos fallidos | `FAILED_FILE` |

### Fuera de este prototipo (vive completo en `config-system-kpi`)
Lo más pesado del original (Alpine) se marcó **Próx.** o se omitió: **config por día (tabs Lu→Do), grupos de archivos, y el "análisis inteligente" completo por métrica/día**. La versión fiel y completa está en `config-system-kpi/index.html`; acá quedó una adaptación vanilla con lo esencial.

---

## ÉPICA UI — Fixes de UI (ya aplicados, enumerar en Figma)

- "Historial" → **"Alertas levantadas"** (+ columna **"¿Notificada?"** por alerta).
- "Notificaciones" → **"Alertas"** en el diálogo del KPI.
- Botón **"Resumen de incidentes"** sacado de la tab de monitoreo del tablero (vive en Anomalías).
- Segmented de Anomalías: **Gestión · Alertas levantadas · Configuración** (activo muestra icono+texto; inactivo solo icono).
- Botón de **configuración** dentro de la vista de Anomalías.
- ⚠️ Revisar diferencias de la **tarjeta de incidente** (Gestión) vs producción → si las hay, van como fix de UI aparte.

---

## Fuera de scope (documentado)
- Notificaciones de **flujo de la app** (asignación/etiquetado).
- **Severidad** como filtro o condición (hasta que sea configurable).
- Preview "con esta config tendrías X notificaciones" (deprioritizado).

## Pendiente / a validar
- Visto bueno de **Cami** antes de entregar a **Edith**.
- Lógica de evaluación (tiempo real vs lote) — eng.
- ⚠️ Heredado: confirmación "al cierre de ventana" vs **workflow runner** (Iván).
- **Unificar construcción de títulos** de notificaciones/templates → se resuelve en la **respuesta del API** (cómo se arma el título del incidente), no es UI.

---

# Guía de implementación (BADS + fe-solutions-mf)

> Esta sección aterriza el prototipo contra el **modelo real de BADS** (Brain v2.8) y los **componentes desyk** del repo `fe-solutions-mf`. Objetivo: que el FE enlace a las entidades/eventos correctos y use los componentes canónicos.

## A. Contra qué datos se implementa (BADS)

Fuente: `ProductEngineeringBrain/versions/v2.8/operation-center/funcionalidades/anomalias/` (`Definicion`/`Arquitectura`).

**Dos entidades, dos vistas (no mezclar):**
- **AnomalySignal** (`anomaly_signal`) — señal atómica. Estados `ACTIVE`/`RESOLVED`; categorías `TRIGGER` / `TRAJECTORY` / `NEW_SERIES`. Es la "alerta/señal" del KPI.
- **Incident** (`incident`) — agrupa señales con causa raíz. **Esta vista (Anomalías → Gestión) y las notificaciones operan sobre INCIDENTES.**

**Incident — estados** (enlazar el filtro "Estado" a `incident.status`):
| Label UI (proto) | `incident.status` |
|---|---|
| En observación | `WATCHING` |
| Abierto | `OPEN` |
| Confirmado | `CONFIRMED` |
| Resuelto | `RESOLVED` |
| (terminales no mostrados) | `AUTO_CLOSED` · `USER_CLOSED` · `CLOSED` · `MERGED` |
(`UNDER_INVESTIGATION` reservado.)

**Severidad:** enum `URGENT` / `REQUIRES_ATTENTION`, **asignada por el workflow runner de BADS (D-13), NO configurable por el usuario** → por eso el filtro Severidad y la condición "severidad alta" se quitaron. Vuelven cuando exista severidad configurable.

**Filtro "Tipo" → `incident.problem_category`** (catálogo cerrado de Ingesta):
| Label UI | enum BADS |
|---|---|
| Archivo faltante | `MISSING_FILE` |
| Archivo fallido | `FAILED_FILE` |
| Archivo vacío | `UNEXPECTED_EMPTY_FILE` |
| Archivo duplicado | `DUPLICATED_FILE` |
| Variación de volumen | `VOLUME_VARIATION` |
- Los **nombres del catálogo** son exactos (Brain); los **constantes enum** `MISSING_FILE`/`FAILED_FILE`/`VOLUME_VARIATION` están inferidos del patrón (`UNEXPECTED_EMPTY_FILE`/`DUPLICATED_FILE` sí verbatim) → **confirmar string exacto con backend BADS**.
- `ALL_OK` es interno (auto-cierra el incidente) → **no se muestra**.
- Catálogos **Data Quality (M4), Conciliación (M5), Accounting (M10)** pendientes → el filtro Tipo hoy solo refleja Ingesta.

**Campos del incidente que el template usa** (no son config de usuario): `hypothesis`, `recommended_actions[]`, narrativa, `evidence_signal_ids`, `blast_radius` (recursos/tableros/charts impactados). → Por eso se quitó "Qué incluir": **el template del `problem_category` los arma server-side.**

## B. Motor de notificación (eventos) — para qué construye el FE

Flujo real: **`oc-bads-incident`** (Pulsar) → **op-center-backend** evalúa cada evento contra las **reglas activas** (nuestros "paquetes") → **`notifications-service`** → Sphere (**SES / Slack / Pusher in-app**).

- Cada **paquete = filtro (scope) + momento (evento del ciclo de vida) + updates + canales**. Evaluación tipo filtro de Gmail por evento.
- **Momento → eventos del incidente (multiselección):** "Cuando se cree" = creación (`OPEN`/`WATCHING`); "Cuando entre en observación" = `status_changed → WATCHING`/`UNDER_INVESTIGATION`; "Cuando se confirme" = `status_changed → CONFIRMED`; "Cuando se resuelva" = `status_changed → RESOLVED`. "Updates" = `status_changed`/reconfirmación/`MERGED`.
- Binding **N:M** (un incidente puede notificar por varios canales; un canal sirve a varias reglas).
- Backend ya define: **idempotencia** `X-Simetrik-Delivery-Id: {uuid}`, **retry** 3 intentos backoff (1s/5s/25s) Slack/webhook, **`webhook_delivery_log`**. El FE no maneja esto, pero el "qué se envía" debe calzar con el payload de `notifications-service` (contexto del incidente + recipients + channel config).

## C. Shape del "paquete" (regla de notificación) — guía FE

Estado que mantiene el prototipo *(modelo 30-jun pm: scope sin Estado; entregas realtime + digest)*:
```jsonc
{
  "id": "uuid",
  "name": "Incidentes de Adquirencia",
  "scope": [                       // SOLO entidades + tipo; ver lógica O/Y en D
    { "type": "Entidad", "value": "Adquirencia" },     // tablero o recurso → resolver a sus resources
    { "type": "Tipo",    "value": "Archivo faltante" } // → incident.problem_category IN [...]
  ],
  "realtime": {                    // entrega por evento (opcional)
    "enabled": true,
    "created": true, "watching": false, "confirmed": true, "resolved": false,  // momento(s) del ciclo de vida (≥1 si enabled)
    "updates": true                       // recibir status_changed posteriores
  },
  "digest": {                      // entrega consolidada 1×día (opcional) — mismo scope + canales
    "enabled": true,
    "hora": "08:00", "zona": "CO · Bogotá (GMT-5)",
    "tn": 4                              // período: cierra a t-n (1..5). Corte SIEMPRE día anterior; hora ≠ período
  },
  "channels": {                    // aplican a ambas entregas
    "emails":   ["ana.torres@simetrik.com"],          // SES
    "slack":    ["#incidentes-finops"],               // Slack webhook (canales)
    "mentions": ["U01ABC23DEF"]                        // Slack user IDs (no @nombre)
  },
  "active": true
}
```
- **Validación FE:** `realtime.enabled || digest.enabled`; si `realtime.enabled` → `created || watching || confirmed || resolved`; `channels.emails.length || channels.slack.length`.
- **`Entidad`** = tablero **o** recurso. El backend resuelve un tablero a sus resources; todos los `Entidad` del scope se combinan con **OR** entre sí (no jerárquico, no AND tablero∧recurso).

## D. Lógica de filtros (scope)
- **Dentro de una categoría: OR.** Entre categorías distintas: **AND.** → `entidad ∈ {tableros∪recursos} AND tipo ∈ {...}`.
- ⚠️ **Entidad NO se trata como jerarquía:** tablero y recurso van en la **misma** categoría con OR; nunca `tablero AND recurso` (generaba condiciones imposibles — fix 30-jun pm).
- **Fecha (lista de incidentes):** rango **relativo dinámico** (t-n), se recalcula cada día; persistir el offset, no la fecha absoluta.
- **Multiselect dentro de cada filtro: producción NO lo soporta hoy** → historia de eng (endpoints). ~100% FE + poco backend.
- **Filtros guardados**: entidad propia reutilizable (se referencian desde el scope del paquete).

## E. Mapeo a componentes desyk (`@simetrikinc/desyk-components`)
Refs: `fe-solutions-mf/.../skills/desyk/references/`.
| Patrón del proto | Componente desyk | Nota |
|---|---|---|
| Toggle on/off (activo, canal, updates, pausar) | **`Switch`** | reemplaza `.tm-notif-row-toggle`; usar `checked`/`onCheckedChange` + `role=switch` nativo |
| Tarjeta (paquete, config, canal) | **`Card`** (+ `CardHeader/Title/Content/Footer`) | |
| Dropdown (reutiliza filtro, incluir, zona horaria) | **`Select`** | |
| Chips de correos / canales / menciones | **`Combobox`** + render de chips | desyk **no** tiene token-input dedicado; Combobox con búsqueda + chips custom |
| Tabs de modo (Gestión/Alertas/Config) | **`Tabs`** o **`UnderlineTabs`** | |
| Checkbox (momento) | **`Checkbox`** | `checked: boolean \| "indeterminate"` |
| Botones (Crear, Guardar, Usar, Editar) | **`Button`** | variantes default/secondary/ghost/destructive; iconos con `size=icon-*` |
| Empty state / first-run | **`EmptyState`** (`EmptyStateTitle/Description/Content`) | reemplaza `.an-onb-*`; el diagrama va como contenido ilustrativo |
| Nota de ID de Slack | **`Alert` variant `info`** | reemplaza `.tm-notif-hint` |
| Aviso "regla no notifica nada" | **`Alert` variant `warning`** | reemplaza `.an-pkg-warn` |
| Estado/severidad como chip | **`Badge`** (variants success/warning/info/destructive) | |
| Menús de Filtrar/Ordenar/Guardados | **`Popover`** | |
| Tooltip de íconos | **`Tooltip`** | |

## F. Máquinas de estado (replicar el comportamiento del proto)
**Notificaciones de incidentes:**
`lista` ⇄ `editor`. Entradas al editor: Crear (vacío), Usar plantilla (pre-llenado), Editar (carga el paquete), Duplicar (clona "… (copia)" → editor). Guardar válido → vuelve a `lista`. Lista vacía → **empty state** (no "Sin resultados").

**Resumen consolidado (entrega del paquete, 30-jun pm):** ya no es una máquina de 3 estados aparte. Es un **toggle** dentro del editor (`digest.enabled`) que despliega su sub-form (hora · zona · t-n). Se guarda con el paquete; el card de la lista muestra su tag ("Resumen 08:00 · hasta hace 4 días (t-4)").

## G. Validaciones / edge cases
- **Regla que no notifica nada** (bloquear Guardar + `Alert warning`): exige **≥1 entrega activa** (aviso por evento o resumen); si aviso por evento, **≥1 momento** (created/watching/confirmed/resolved); **y ≥1 canal activo** (correo o Slack). Una mención sin canal de Slack no entrega.
- **Scope vacío** = "Todos mis incidentes" (válido, no es error).
- Canal con toggle **apagado** → no se leen sus destinatarios al guardar.
- Severidad: no exponer como filtro ni condición (system-assigned).

## H. Motion y a11y (specs)
- Durations canónicas **120 / 200 / 320 ms**, **ease-out exponential** `cubic-bezier(0.22,1,0.36,1)`. Solo `transform`/`opacity`/`stroke-dashoffset`.
- Empty states: **pulso de flujo** (dashes recorriendo los wires, enseña dirección incidente→canales) + entrada escalonada. **Diagrama `pointer-events:none`** (ilustración, no UI) dentro de frame "Vista previa".
- **`@media (prefers-reduced-motion: reduce)`** desactiva las animaciones.
- a11y: `Switch`/`Checkbox`/`Button` de desyk traen roles/aria; chips con `aria-label="Quitar"`; labels asociados (`for`/`id`) — pendiente en el proto, **obligatorio en la implementación**.
