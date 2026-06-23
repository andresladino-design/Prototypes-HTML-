# 5.4 Mejora visual de notificaciones Slack (Block Kit)

**Prioridad**: 🟢 P1 (verde) — sub-item de [5. Reglas de notificación MVP](../README.md)
**Estado general**: ✅ **EN MARCHA** — es el item con más avance concreto

## Qué se necesita

Migrar las notificaciones de Slack de **texto plano / `mrkdwn`** a **Block Kit** (UI framework oficial de Slack: header, section, divider, actions, context, buttons).

## Assets de referencia (Block Kit)

- [`slack-blockkit.json`](./slack-blockkit.json) — Block Kit base de una alerta.
- [`slack-blockkit-carousel.json`](./slack-blockkit-carousel.json) — Variante con tarjetas/carrusel.
- [`slack-blockkit.README.md`](./slack-blockkit.README.md) — Notas de uso y parámetros.
- [`slack-alternativas.html`](./slack-alternativas.html) — Exploración visual de alternativas de layout.

> Pendiente: pedir a Santi Quintero los Block Kits del equipo de IA (Agent Factory) para alinear parámetros y consistencia.

## Estado en Linear

### Slice activo (SWAT-1381 — In Progress)

| Issue | Título | Status | Nota |
|---|---|---|---|
| **SWAT-1381** | notifications-backend: soportar Block Kit para envío de mensajes a Slack | **In Progress** | Iván Díaz · parent |
| SWAT-1382 | SWAT-1381-A: schema changes — `SlackBlock` + `SlackDeliveryConfig.blocks` | Backlog | ~1 SP |
| SWAT-1384 | SWAT-1381-B: provider Path B + error classification (4xx vs 5xx) | Done | ~2 SP |
| SWAT-1383 | notifications-backend: bump sphere — añadir `slack_blocks` a `DeliveryTaskEventData` | Done | Follow-up |
| SWAT-1386 | SWAT-1381-D: docs + BDD step defs + runbook | Done | `docs/SLACK_BLOCK_KIT.md` |
| SWAT-1398 | notifications-backend: activar pytest-bdd para scaffolds del Slice D | Backlog | Follow-up |

### Antecedentes (Slack ya integrado)

| Issue | Título | Status | Nota |
|---|---|---|---|
| SWAT-846 | [BE] Integración Slack API + routing de eventos + actions handler | Done | App con scopes, threads, actions (Tomar/Resolver/Silenciar) |
| SWAT-532 | [E1.6] Notificación por Slack (épica) | Done | Phase 1 entregado |
| SWAT-958 | [BE] Compartir incidente por email y Slack | Done | Acción manual de share |

## Contexto Brain

- Épica DOE24 (Notificaciones externas — Slack, Email, Webhooks, Pusher) — **RFC Complete**
- Patrón: un mensaje root por incidente + replies en thread para updates
- Action buttons: Tomar / Resolver / Silenciar

## Gap UX

- Definir el **layout de Block Kit** para signal y incident:
  - header (problem category + severity badge)
  - section (KPI name + breach details)
  - context (timestamp, workspace, ROI)
  - actions (Tomar / Ver detalle / Silenciar)
  - divider entre updates en el thread
- Validar contra plantillas reales de Slack (`https://app.slack.com/block-kit-builder`)
- Manejo de truncación si el mensaje excede `SLACK_MAX_BLOCKS`
