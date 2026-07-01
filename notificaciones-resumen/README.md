# Notificaciones Resumen

Prototipo de configuración de **notificaciones**, **ventana de monitoreo** y **métricas de gráficos** (K Cast) para el monitoreo inteligente de Operation Center.

**Última actualización:** 2026-07-01
**Estado:** 🟢 Activo

## Cómo verlo

- Online: https://andresladino-design.github.io/Prototypes-HTML-/notificaciones-resumen/
- Local: abrir `index.html` en el navegador

## Qué incluye

### Vista de Anomalías (tab superior "Anomalías")
- **Alertas (en el KPI):** el diálogo del gráfico configura *Alertas* (señales), no incidentes. "Historial" → **"Alertas levantadas"** (con columna ¿Notificada?).
- **Filtros de Gestión:** multiselect dentro de cada categoría (combina con **`o`**), entre categorías con **`Y`**; **filtros guardados** reutilizables; sin filtro de Severidad (hasta que sea configurable).
- **Notificaciones de incidentes = paquetes de reglas:** lista de tarjetas; cada paquete tiene alcance ("Entidades afectadas": tableros/recursos con `o` + tipo), momentos del ciclo de vida (al crearse / en observación / al confirmarse / al resolverse + updates) y canales. Un incidente se evalúa contra todos los paquetes activos.
- **Resumen consolidado:** modo de entrega **dentro del paquete** (1×día), sobre el mismo alcance y canales, con hora + zona + período t-n. Ya no es una sección propia del nav.

### Diálogo de monitoreo del KPI
- **Alertas · ¿Cuándo notificar?** — eje de timing de 3 estados (*Nunca* / *Solo al final* / *En tiempo real*); la barra de la ventana de monitoreo actúa de explicador (las notificaciones aparecen como marcadores a su hora). Los canales se exigen de forma reactiva al pasar de paso.
- **Series y valores · detección por serie** — narrativa "Análisis inteligente" (con carga "Pensando…") + configuración general + override por serie: **Límites fijos** vs **Sistema adaptativo** (Alta/Media/Baja + límites de seguridad), con simulación de alertas sobre el histórico.
- Tabs segmentadas e iconografía unificada.
- Archivos de apoyo: `templates.html`, `slack-alternativas.html`, `slack-blockkit*.json`.
- Spec de plantillas Slack del agente (default/compact/ultra-compact): `slack-templates-agente.README.md`.

## Stack

- Tailwind CSS (CDN)
- Alpine.js (parcial — el diálogo de monitoreo usa vanilla JS)
- Lucide Icons
- desyk tokens

## Changelog

### 2026-07-01
- **Detección de anomalías rediseñada por serie:** se reemplazó el slider de sensibilidad (nula/media/alta) por narrativa "Análisis inteligente" + configuración general + override por serie (**Límites fijos** vs **Sistema adaptativo**), con simulación de alertas.
- **Resumen consolidado** dejó de ser sección propia del nav: pasó a ser un **modo de entrega dentro del paquete** (mismo alcance y canales + período t-n), decisión del design review del 30-jun pm.
- **Handoff reorganizado en 3 estructuras** (por épica de ingeniería) en `handoff/`: filtros en vista de incidentes · configuración de detección en tableros/monitoreo · notificaciones + vista de Anomalías. Consolida los 5 handoffs previos y el plan del 30-jun (ambos preservados en el historial de git).

### 2026-06-30
- **Vista de Anomalías** con filtros multiselect (O dentro de categoría / Y entre categorías) + **filtros guardados**; quitado el filtro de Severidad.
- **Notificaciones de incidentes** reconstruidas como **paquetes de reglas** (lista de tarjetas + editor): scope "Notifícame incidentes sobre…", momento del ciclo de vida, updates, canales. Quitados los checkboxes de severidad/responsable/etiquetado y la sección "Qué incluir".
- **Resumen consolidado** movido a **sección propia** en el nav de Configuración.
- Handoff enumerado en `handoff/` (3 estructuras: filtros, config de detección, notificaciones + vista de Anomalías; ver `handoff/README.md`).
- Basado en la sesión Granola del 30-jun y comentarios de Ohana.

### 2026-06-25
- Slack: etiquetado por **user ID** (no `@nombre`) con helper de cómo obtenerlo.
- Sensibilidad **ligada a la gráfica** del KPI: banda de rango esperado que se angosta por nivel + anomalías en rojo; conteo derivado (no mock).
- Templates: cuerpo del incidente = **metadata del problem category** (sin texto de agente); Slack vertical recomendada; color por severidad; email con toggle con/sin gráfica; patrón "+N incidentes".
- Basado en feedback de la reunión del 25-jun.

### 2026-06-23
- Rediseño del bloque "¿Cuándo notificar?" (patrón `sens-row`) con slider animado y ventana de monitoreo como referencia visual.
- Tarjeta de timing deshabilitada hasta activar un canal.
- 3 modos de hard limit por bound en user KPIs.
- Tabs segmentadas; íconos consistentes.
- Basado en feedback de la reunión del 23-jun (notificaciones, métricas y templates).
