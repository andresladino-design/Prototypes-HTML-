# 10. Support notifications for System KPIs

**Prioridad**: 🟢 P1 (verde) — *aunque el header del item aparece en rojo en el roadmap*
**Impacto**: 5 · **Esfuerzo**: 3 · **Neto**: 15

## Qué se necesita

Habilitar **canal de notificación para System KPIs** — los KPIs que el sistema crea automáticamente en cascada sobre el árbol de dependencias hoy no tienen notificación dirigida.

## Estado en Linear

### Milestone activo: M2.5 Config de System KPIs

Todos asignados a Andres y en Phase 3.

| Issue | Título | Status | Nota |
|---|---|---|---|
| **SWAT-535** | [E2.2] Parametrización de system KPIs | **In Progress** | Urgent · panel central de la épica |
| **SWAT-536** | [E2.2] Sugerencias del agente con resumen NL e insights históricos | **In Progress** | Urgent · LLMNarrativeService en prod (SWAT-703 Done) |
| **SWAT-537** | [E2.2] Activar/desactivar system KPIs por fuente | **In Progress** | Ver también item 1 |
| **SWAT-538** | [E2.2] Template de System KPIs en tableros | **In Progress** | System KPIs como primitiva de viz |
| SWAT-805 | [UX] Panel de sugerencias del agente en detalle del system KPI | **In Progress** | Andres · estados completos |

### Infra entregada en M2.5

| Issue | Título | Status |
|---|---|---|
| SWAT-1235 | [BADS] M2.5 Slice 1 — Registro directo de System KPIs + ResourceProfile | Done |
| SWAT-1304 | [BADS] POST /system-kpis: paridad con CreateKpiRequest | Done |
| SWAT-1250 | [fe-solutions-mf] Tab System KPI: lista + panel detalle | Done |
| SWAT-1308 | Fix: timezone descartado silenciosamente en POST /system-kpis | Done |
| SWAT-1425 | BADS preview baseline: multi-metric + consolidated narrative + kpi_archetype | Done |
| SWAT-1347 | Hipótesis incidente: exponer límite roto + breach_pct por category | Done |

### Gap específico de "notificaciones"

- Los templates SWAT-883 (signal) y SWAT-884 (incident) son **genéricos** — no distinguen system vs user KPI
- No hay issue específico para **routing/filtering de notificaciones de system KPIs**
- Pregunta: ¿el usuario quiere notificación por system KPI o solo por el incident agrupado que resulta?

## Contexto Brain

- Épica DOE16 (Detección IA — cascada de system KPIs sobre árbol de dependencias)
- Épica DOE17 (Config de alertas por usuario) — RFC Complete
- Épica DOE24 (Notificaciones externas) — RFC Complete
- Documentación: `Definicion - Anomalias.md` (21 casos de uso) + `Arquitectura - Anomalias.md`

## Gap UX

- ¿El usuario configura notificación por **system KPI individual** o por **fuente (RoI)**?
- Default razonable: notificación al **owner del recurso** sin opt-in explícito (porque la cascada es automática)
- Riesgo de **ruido**: una cascada puede crear ~5 system KPIs × 5 fuentes = 25 monitoreos. Notificar todo es overload.
- Relación con item 6 (digest) — system KPIs son el caso de uso ideal para consolidación
