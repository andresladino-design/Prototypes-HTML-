# Notificaciones Resumen

Prototipo de configuración de **notificaciones**, **ventana de monitoreo** y **métricas de gráficos** (K Cast) para el monitoreo inteligente de Operation Center.

**Última actualización:** 2026-06-30
**Estado:** 🟢 Activo

## Cómo verlo

- Online: https://andresladino-design.github.io/Prototypes-HTML-/notificaciones-resumen/
- Local: abrir `index.html` en el navegador

## Qué incluye

### Vista de Anomalías (tab superior "Anomalías")
- **Alertas (en el KPI):** el diálogo del gráfico configura *Alertas* (señales), no incidentes. "Historial" → **"Alertas levantadas"** (con columna ¿Notificada?).
- **Filtros de Gestión:** multiselect dentro de cada categoría (combina con **`o`**), entre categorías con **`Y`**; **filtros guardados** reutilizables; sin filtro de Severidad (hasta que sea configurable).
- **Notificaciones de incidentes = paquetes de reglas:** lista de tarjetas; cada paquete tiene scope ("Notifícame incidentes sobre…"), momento del ciclo de vida (al crearse / al confirmarse), updates y canales. Un incidente se evalúa contra todos los paquetes activos.
- **Resumen consolidado:** sección propia en el nav (1×día), reutiliza filtros.

### Diálogo de monitoreo del KPI
- **¿Cuándo notificar?** — control con slider animado (*Todo el tiempo* vs *Solo al cierre*) y resumen visual de la ventana de monitoreo; se habilita solo al activar un canal (Email/Slack).
- **3 modos de hard limit** por bound (on/off + valor sugerido) en user KPIs, replicando el patrón de system KPIs.
- **Sensibilidad** configurable (nula/media/alta) a nivel de KPI.
- Tabs segmentadas e iconografía unificada.
- Archivos de apoyo: `templates.html`, `slack-alternativas.html`, `slack-blockkit*.json`.
- Spec de plantillas Slack del agente (default/compact/ultra-compact): `slack-templates-agente.README.md`.

## Stack

- Tailwind CSS (CDN)
- Alpine.js (parcial — el diálogo de monitoreo usa vanilla JS)
- Lucide Icons
- desyk tokens

## Changelog

### 2026-06-30
- **Vista de Anomalías** con filtros multiselect (O dentro de categoría / Y entre categorías) + **filtros guardados**; quitado el filtro de Severidad.
- **Notificaciones de incidentes** reconstruidas como **paquetes de reglas** (lista de tarjetas + editor): scope "Notifícame incidentes sobre…", momento del ciclo de vida, updates, canales. Quitados los checkboxes de severidad/responsable/etiquetado y la sección "Qué incluir".
- **Resumen consolidado** movido a **sección propia** en el nav de Configuración.
- Handoff enumerado: `handoff/handoff-anomalias-filtros-notificaciones.md`. Plan: `plan-notificaciones-paquetes-30jun.md`.
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
