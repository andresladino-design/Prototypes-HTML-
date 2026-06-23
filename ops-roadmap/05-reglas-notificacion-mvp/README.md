# 5. Agregar MVP de "reglas de notificación"

**Prioridad**: 🔴 (rojo — parent / research)
**Impacto**: 4 · **Esfuerzo**: 3 · **Neto**: 12

## Qué se necesita

MVP de **reglas de notificación**: que el usuario pueda configurar cuándo, cómo y por qué canal recibe alertas de anomalías.

> Mock UX en progreso en el prototipo [`notificaciones-resumen/`](../../notificaciones-resumen/) (config de notificaciones, ventana de monitoreo, hard limits y Slack Block Kit). Basado en feedback de la reunión del 23-jun.

## Sub-temas (todos 🟢 P1)

- [`5.1-breach-pct/`](./5.1-breach-pct/README.md) — Parametrizar breach_pct en signals
- [`5.2-severity-incidente/`](./5.2-severity-incidente/README.md) — Parametrizar severity de Incidente
- [`5.3-signals-vs-incident/`](./5.3-signals-vs-incident/README.md) — Seleccionar Signals / Incident / ambos
- [`5.4-slack-block-kit/`](./5.4-slack-block-kit/README.md) — Mejora visual notificaciones Slack (Block Kit)

## Estado en Linear (epica padre)

| Issue | Título | Status | Nota |
|---|---|---|---|
| **SWAT-563** | [Épica 8.2] Reglas de envío | **Backlog** | Milestone M8 Gestión de notificaciones · *cuándo enviar, agrupación, silencios/mute* |
| SWAT-532 | [E1.6] Notificación por Slack | Done | Canal Slack ya entregado |
| SWAT-531 | [E1.6] Notificación por correo | Done | Canal email ya entregado |
| SWAT-355 | [FE] Configuración canal Slack en notificaciones | Done | UI básica ya existe |

## Contexto Brain

- Épica **DOE24** — Notificaciones externas (Slack, Email, Webhooks, Pusher) — RFC Complete
- Épica **DOE27** — Smart Rules (respuestas automatizadas) — **Blocked/diferido**
- Hoy la config de notificaciones vive en `AnomalyMonitoringConfig` (tab notificaciones) con campo dashboard/page/channels

## Por qué es rojo

Es un **paraguas**: el MVP requiere acordar el alcance y construir el modelo de "regla" (condiciones + acciones). Los sub-tickets 5.1–5.4 son los ladrillos concretos en verde para empezar.
