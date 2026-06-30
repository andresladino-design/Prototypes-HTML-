# Handoff — Anomalías: filtros, paquetes de notificación y resumen

**Prototipo:** `notificaciones-resumen/index.html` → vista de **Anomalías** (tab superior "Anomalías").
**Fuente:** sesión Granola **30-jun-2026** + comentarios de Ohana del mismo día.
**Plan:** `plan-notificaciones-paquetes-30jun.md`.
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
- **Unificar construcción de títulos** de notificaciones/templates.
