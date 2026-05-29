# 5.1 Parametrizar breach_pct en signals

**Prioridad**: 🟢 P1 (verde) — sub-item de [5. Reglas de notificación MVP](../README.md)

## Qué se necesita

Que el usuario pueda definir un **umbral mínimo de `breach_pct`** (qué tan lejos del límite está la señal) para disparar notificación. Hoy `breach_pct` se calcula internamente pero no es configurable como knob del usuario.

## Estado en Linear

### Infra interna (toda Done)

| Issue | Título | Status | Nota |
|---|---|---|---|
| SWAT-746 | [Feature] Scoring trivial para TRIGGERs en reconfirmación (`breach_pct` = minutos desde ventana) | Done | Sergio Lobo · Phase 1 |
| SWAT-867 | Enrich Trigger signal audit trail details and diagnostics matrix | Done | `breach_pct` transitions en audit |
| SWAT-1199 | BADS: incident hypothesis prompt produces hallucinated narratives — fix `breach_pct` semantics | Backlog | Stage testing 2026-05-06 |
| SWAT-1347 | Hipótesis: exponer límite roto + enseñar interpretación de `breach_pct` por category | Done | Camila / ops-center testing |
| SWAT-1437 | Scoring engine treats missing baseline as zeroed features — severity matrix mis-labels warming-up breaches | Backlog | Production Readiness I |

### Gap UX (no hay issue abierto)

- No existe issue para **exponer breach_pct como knob configurable** en el modal de monitoring config
- `breach_pct` hoy es derivado por categoría (Trigger / Trajectory hard / Trajectory adaptativo)
- Riesgo: si lo exponemos, ¿qué semántica se preserva por categoría?

## Contexto Brain

- Épica DOE16 (Detección IA y parametrización, **thresholds**) — aquí encaja
- `breach_pct` ya está documentado en el evento `anomaly.updated` (Pulsar)

## Preguntas abiertas

1. ¿El usuario configura % por KPI o global?
2. ¿Solo aplica a categoría `Trajectory hard` o también adaptativo?
3. UI: ¿slider, input, presets ("crítico" / "warning")?
4. Default value y safe-zone
