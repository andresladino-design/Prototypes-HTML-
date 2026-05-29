# 5.3 Seleccionar si Signals, Incident o ambos

**Prioridad**: 🟢 P1 (verde) — sub-item de [5. Reglas de notificación MVP](../README.md)

## Qué se necesita

Toggle/multi-select en la config de notificación para que el usuario elija **qué tipo de evento dispara la notificación**:
- solo `anomaly_signal` (ruido alto, más granular)
- solo `anomaly_incident` (agrupado, más contexto)
- ambos

## Estado en Linear

### Templates ya soportan ambos tipos (Done)

| Issue | Título | Status | Nota |
|---|---|---|---|
| SWAT-883 | [Notif] Template parametrizado para señal (signal) de anomalía | Done | `notification_type: anomaly_signal_active` |
| SWAT-884 | [Notif] Template parametrizado para incidente de anomalía | Done | `notification_type: anomaly_incident_opened` |
| SWAT-936 | Notification type: anomaly_signal (email body template) | Done | MJML body |
| SWAT-526 | [E1.5] Creación automática de incidente con problem category | Done | Incidentes agrupan signals por categoría |

### Gap UX (no hay issue abierto)

- Hoy el sistema **emite ambas notificaciones siempre**
- No hay control de usuario para silenciar uno u otro
- En la práctica genera **doble ruido** (signal + incident del mismo evento)

## Contexto Brain

- Definición Anomalías: **incidents tienen mayor jerarquía que signals** y son el foco de gestión operativa diaria
- Decisión: signals son secundarios → default debería ser **solo incidents**
- Pero el usuario power-user puede querer signals para visibilidad temprana

## Preguntas abiertas

1. Default: ¿solo incidents o ambos?
2. ¿Aplica por canal? (ej. Slack=solo incidents, email=ambos)
3. ¿Aplica por KPI o global?
4. Copy: "Notifícame de…" con 2 checkboxes
