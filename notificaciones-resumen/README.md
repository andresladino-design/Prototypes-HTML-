# Notificaciones Resumen

Prototipo de configuración de **notificaciones**, **ventana de monitoreo** y **métricas de gráficos** (K Cast) para el monitoreo inteligente de Operation Center.

**Última actualización:** 2026-06-23
**Estado:** 🟢 Activo

## Cómo verlo

- Online: https://andresladino-design.github.io/Prototypes-HTML-/notificaciones-resumen/
- Local: abrir `index.html` en el navegador

## Qué incluye

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

### 2026-06-23
- Rediseño del bloque "¿Cuándo notificar?" (patrón `sens-row`) con slider animado y ventana de monitoreo como referencia visual.
- Tarjeta de timing deshabilitada hasta activar un canal.
- 3 modos de hard limit por bound en user KPIs.
- Tabs segmentadas; íconos consistentes.
- Basado en feedback de la reunión del 23-jun (notificaciones, métricas y templates).
