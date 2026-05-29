# 5.2 Parametrizar severity de Incidente

**Prioridad**: 🟢 P1 (verde) — sub-item de [5. Reglas de notificación MVP](../README.md)

## Qué se necesita

Que el usuario pueda **filtrar notificaciones por severity** del incidente (ej. solo `URGENT`, o `URGENT + HIGH`).

## Estado en Linear

### Infra interna (Done)

| Issue | Título | Status | Nota |
|---|---|---|---|
| SWAT-650 | [BADS] Enum Incident Severity | Done | Enum estable en Pulsar — `URGENT`, `HIGH`, etc. |
| SWAT-1437 | Scoring engine treats missing baseline as zeroed features — severity matrix mis-labels | Backlog | Issue de calidad del severity |

### BADS ya publica severity como enum estable

Wire-format del evento incident incluye `severity: "URGENT"`, lo cual permite filtrar de forma segura en UI.

### Gap UX (no hay issue abierto)

- No hay issue de **filtrado por severity en config de notificación**
- Hoy el usuario recibe todo sin discriminar severity

## Contexto Brain

- Épica DOE24 (Notificaciones externas) — RFC Complete
- Épica DOE18 (Centro de anomalías) ya filtra por severity en la lista — falta replicar en config de notificación

## Preguntas abiertas

1. ¿Solo notifica `URGENT`? ¿`URGENT + HIGH`? ¿Multi-select?
2. ¿Aplica también a signals (que no tienen severity, solo `breach_type`)?
3. Default sugerido (¿todos? ¿solo URGENT?)
