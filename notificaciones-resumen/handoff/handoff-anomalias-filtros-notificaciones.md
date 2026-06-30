# Handoff — Anomalías: filtros, paquetes de notificación y resumen

**Prototipo:** `notificaciones-resumen/index.html` → vista de **Anomalías** (tab superior "Anomalías").
**Fuente:** sesión Granola **30-jun-2026** + comentarios de Ohana del mismo día.
**Plan:** `plan-notificaciones-paquetes-30jun.md`.
**Historias de UX (complemento):** `handoff-anomalias-historias-ux.md` (5 HU con estados, criterios F/X, a11y).
**Regla del equipo:** *donde un cambio de UI no se enumere explícitamente, no se ejecuta en desarrollo.* Por eso este handoff lista **cada** cambio, incluso los chicos.

> ⚠️ Separar en 3 épicas de ingeniería: **(1) Filtros**, **(2) Paquetes de notificación**, **(3) Resumen**. Más la épica transversal de **fixes de UI**.

---

## ÉPICA 1 — Filtros de la vista de Gestión

**Dónde:** Anomalías → Gestión → barra "Filtrar / Ordenar / Guardados".

### Cambios de UI (enumerados)
1. **Multiselect dentro de cada categoría.** Al abrir Recurso / Tablero / Estado / Tipo, se pueden marcar **varios valores**. Cada opción muestra un **check** al elegirse; el submenú **no se cierra** (footer con "Limpiar" y "Listo").
2. **Lógica de combinación:** dentro de una categoría los valores se unen con **`o`** (OR); entre categorías distintas, con **`Y`** (AND). En los chips aplicados: el valor se lee `A o B`; entre chips aparece un conector **"Y"**.
3. **Quitar el filtro "Severidad".** Eliminado del menú. Motivo: no exponer severidad hasta que el usuario pueda **definir sus propios niveles**. (Vuelve cuando sea configurable.)
4. **Filtros que quedan:** Recurso, Tablero, Estado, Tipo (+ Fecha como rango único, no multiselect).
   - **Tipo** = problem categories reales de BADS (Ingesta): Archivo faltante, Archivo fallido, Archivo vacío, Archivo duplicado, Variación de volumen.
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
2. **Editor de paquete** (al crear/editar), con estos bloques **que no se interfieren**:
   - **Nombre** de la notificación.
   - **Bloque 1 · "¿Qué incidentes te interesan?"** (alcance). Select **"Reutiliza un filtro"** (filtros guardados de la Épica 1 / "Filtro actual de la vista" / "Todos mis incidentes") + preview de chips de "Incidentes que coinciden" + link "Crear o editar filtros en la vista de incidentes". *El scope ES un filtro (suma de filtros).*
   - **Bloque 2 · "¿En qué punto de la vida del incidente quieres ser notificado?"** → 2 opciones: **Cuando se cree** / **Cuando se confirme**.
   - **Bloque 3 · "¿Recibir updates del incidente?"** → toggle (reconfirmaciones, cambios de hipótesis, otros recursos afectados).
   - **Canales** → mismo patrón que el "¿Dónde notificar?" del KPI: **tarjetas de canal activables** (Email / Slack) con toggle; Email → destinatarios; Slack → canales + **Etiquetar a personas por ID de usuario** (no `@nombre`; nota "Copiar id. de miembro"). Si el canal está apagado, no se notifica por ahí. Mismo patrón en el **Resumen consolidado**.
   - Acciones: Cancelar / Guardar notificación.

### QUITADO del formulario anterior (no va)
- ❌ Checkbox **"Cuando la severidad sea alta"** (severidad pospuesta).
- ❌ Checkbox **"Cuando no tenga responsable asignado"** (fuera de scope ahora).
- ❌ Checkbox **"Cuando me etiquen"** → es **notificación de flujo de la app** ("te asignaron / te etiquetaron"), otro template, **otro feature**. No se configura aquí.
- ❌ Tarjeta **"Qué incluir en la notificación" (Hipótesis / Acción recomendada / Resumen / narrativa)** → eso va **directo en el template** (Block Kit / email), no es configurable por el usuario.
- ❌ La tarjeta de **Resumen consolidado** sale de aquí → pasa a su propia sección (Épica 3).

### Lógica (para ingeniería, no es de este prototipo)
- Incidente = evento. En cada evento (creación/update) se evalúan las reglas de todos los paquetes activos → match → notifica.
- Condiciones tipo filtro de Gmail; condiciones contradictorias → cero notificaciones (avisar visualmente si aplica).
- Anti-spam: por default, quien configura el paquete es quien recibe; agregar a terceros es explícito (en canales).

---

## ÉPICA 3 — Resumen consolidado (sección propia)

**Dónde:** Anomalías → Configuración → **Resumen consolidado** (ítem nuevo en el nav, después de "Notificaciones de incidentes").

> Decisión de Ohana (cmt 0+1): el resumen **sale** del formulario de notificaciones y es **su propia sección**. Es distinto: las notificaciones llegan por evento; el resumen es **1×día**.

### Cambios de UI (enumerados)
1. **Nuevo ítem de nav** "Resumen consolidado" con su página.
2. **First-run (apagado por defecto):** estado vacío con intro + **mini-diagrama** (varias incidencias → agrupadas → un **Resumen** → enviado a **Email** y **Slack**) + botón **"Activar resumen diario"**. Al activar se revela la config; apagar el interruptor vuelve al estado inicial. 🎨 A futuro: ilustración CSS más pulida.
3. Config (al activar): **"¿Qué incidentes te interesan?"** (mismo patrón de scope que el paquete) + **Incluir** (solo abiertos y urgentes / todos); **"¿Cuándo llega?"** (hora + zona horaria, defaults 08:00 · CO Bogotá); **"¿Dónde notificar?"** (tarjetas Email/Slack + ID de Slack). Defaults ya puestos, no en cero.

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
- **Momento → eventos del incidente:** "Cuando se cree" = evento de creación (`WATCHING`); "Cuando se confirme" = `status_changed → CONFIRMED`. "Updates" = `status_changed`/reconfirmación/`MERGED`.
- Binding **N:M** (un incidente puede notificar por varios canales; un canal sirve a varias reglas).
- Backend ya define: **idempotencia** `X-Simetrik-Delivery-Id: {uuid}`, **retry** 3 intentos backoff (1s/5s/25s) Slack/webhook, **`webhook_delivery_log`**. El FE no maneja esto, pero el "qué se envía" debe calzar con el payload de `notifications-service` (contexto del incidente + recipients + channel config).

## C. Shape del "paquete" (regla de notificación) — guía FE

Estado que mantiene el prototipo (traducir a entidad de backend):
```jsonc
{
  "id": "uuid",
  "name": "Incidentes confirmados",
  "scope": [                       // suma de filtros; ver lógica O/Y en D
    { "type": "Estado", "value": "Confirmado" },   // → incident.status IN [...]
    { "type": "Tipo",   "value": "Archivo faltante" } // → incident.problem_category IN [...]
  ],
  "events": { "created": false, "confirmed": true },  // momento del ciclo de vida
  "updates": true,                                     // recibir status_changed posteriores
  "channels": {
    "emails":   ["ana.torres@simetrik.com"],          // SES
    "slack":    ["#incidentes-finops"],               // Slack webhook (canales)
    "mentions": ["@U01ABC23DEF"]                       // Slack user IDs (no @nombre)
  },
  "active": true
}
```
- **Resumen consolidado** es otra entidad/propiedad (1×día): `{ active, scope, include: "open_urgent"|"all", time, timezone, channels }`.

## D. Lógica de filtros (scope)
- **Dentro de una categoría: OR.** Entre categorías distintas: **AND.** → `recurso ∈ {...} AND tipo ∈ {...} AND estado ∈ {...}`.
- **Multiselect dentro de cada filtro: producción NO lo soporta hoy** → historia de eng (endpoints). ~100% FE + poco backend.
- **Filtros guardados**: entidad propia reutilizable (se referencian desde el scope del paquete y del resumen).

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

**Resumen consolidado (3 estados):**
`empty (apagado)` → *Activar* → `edit (formulario, defaults)` → *Guardar* → `saved (activo: resumen read-only + Editar + pausar)`.
- *Editar* (saved→edit), *Cancelar* (edit→saved si ya existía, si no →empty), *Pausar* (toggle off → empty).

## G. Validaciones / edge cases
- **Regla que no notifica nada** (bloquear Guardar + `Alert warning`): exige **≥1 momento** (created/confirmed) **y ≥1 canal activo** (correo o Slack). Una mención sin canal de Slack no entrega.
- **Scope vacío** = "Todos mis incidentes" (válido, no es error).
- Canal con toggle **apagado** → no se leen sus destinatarios al guardar.
- Severidad: no exponer como filtro ni condición (system-assigned).

## H. Motion y a11y (specs)
- Durations canónicas **120 / 200 / 320 ms**, **ease-out exponential** `cubic-bezier(0.22,1,0.36,1)`. Solo `transform`/`opacity`/`stroke-dashoffset`.
- Empty states: **pulso de flujo** (dashes recorriendo los wires, enseña dirección incidente→canales) + entrada escalonada. **Diagrama `pointer-events:none`** (ilustración, no UI) dentro de frame "Vista previa".
- **`@media (prefers-reduced-motion: reduce)`** desactiva las animaciones.
- a11y: `Switch`/`Checkbox`/`Button` de desyk traen roles/aria; chips con `aria-label="Quitar"`; labels asociados (`for`/`id`) — pendiente en el proto, **obligatorio en la implementación**.
