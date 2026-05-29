# 6. Notificación tipo "reporte" consolidado o grupo

**Prioridad**: 🔵 P4 (azul)
**Impacto**: 5 · **Esfuerzo**: 5 · **Neto**: 25
**Nota original**: *"start research, user prod data to land better feedback"*

## Qué se necesita

Una notificación **consolidada / digest** en lugar de una por evento. Por ejemplo, "resumen de 8 incidentes del día" en lugar de 8 Slacks separados.

## Estado en Linear

### Antecedentes directos

| Issue | Título | Status | Nota |
|---|---|---|---|
| **SWAT-563** | [Épica 8.2] Reglas de envío | **Backlog** | M8 — *"Reglas de cuándo enviar notificaciones, agrupación de notificaciones y configuración de silencios/mute"* |
| SWAT-705 | [BADS][Épica] SignalGroupingStrategy pluggable + v0 con LLM | Todo | Agrupación de signals con LLM |
| SWAT-791 | [BADS] Incident timeline endpoint — audit events como vista cronológica | Backlog | Vista timeline tipo Traversal |

### Notification center actual (relacionado)

| Issue | Título | Status |
|---|---|---|
| SWAT-1264 | [notification-center] Excluir notificaciones archivadas del listado por defecto | Done |
| SWAT-1352 | [notifications-fe] Click en notificación — confirmar shape + fallback por tipo | Backlog |
| SWAT-1007 | [FE] Handler SSE para notificación async de template publicado | Done |

## Research necesario

> *"start research, user prod data to land better feedback"*

- ¿Qué cadencia? (cada hora, diaria, semanal)
- ¿Por canal? (Slack tolera burst, email pide digest)
- ¿Agrupado por qué? (workspace, resource, problem category, severity)
- ¿Cuántos incidentes por día tiene un account promedio en prod?
- Mute/snooze global vs per-resource

## Contexto Brain

- Épica DOE24 cubre Slack/Email/Webhooks/Pusher — pero **un evento = una notificación**
- Épica DOE27 (Smart Rules, **Blocked**) anticipa este tipo de lógica
- `SignalGroupingStrategy` en BADS (SWAT-705) puede ser cimiento técnico para agrupación

## Preguntas abiertas

1. ¿Es un **canal nuevo** (digest channel) o un **modo** del canal existente?
2. ¿Quién decide el contenido del digest — LLM o template fijo?
3. ¿El usuario configura el digest o es automático cuando supera N incidentes/hora?
