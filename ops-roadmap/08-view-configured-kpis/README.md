# 8. Add view of configured KPIs (anomalies)

**Prioridad**: 🔵 P4 (azul)
**Impacto**: 2 · **Esfuerzo**: 2 · **Neto**: 4

## Qué se necesita

Vista dedicada para ver **todos los KPIs configurados** para monitoreo de anomalías (user-defined + system KPIs), con búsqueda, filtros y acciones bulk.

## Estado en Linear

### La épica padre fue **cancelada** — pero la necesidad sigue

| Issue | Título | Status | Nota |
|---|---|---|---|
| **SWAT-534** | [E2.1 Visibilidad KPI] Lista de todos los KPIs monitoreados incluyendo system KPIs | **Canceled** | Andres · cancelado 2026-04-27 |
| SWAT-822 | [BE] Endpoint list KPIs por account + filtros + export | Canceled | Sub-issue de 534 |
| SWAT-823 | [FE] Implementación de la lista de KPIs monitoreados | Canceled | Sub-issue de 534 |

### Lo que sí existe hoy

| Issue | Título | Status | Nota |
|---|---|---|---|
| SWAT-1250 | [fe-solutions-mf] Tab System KPI: lista de fuentes + panel de detalle con Preparación | Done | Lista parcial — solo System KPI dentro de modo Config |
| SWAT-415 | [UI] Source of interest y KPIs de sistema en modal de configuración de anomalías | Done | Visibilidad dentro del modal |
| SWAT-226 | [BE-4] Endpoint GET /charts/{chart_id}/anomaly-config/readiness | Done | Readiness por chart |
| SWAT-196 | Historia 2: Visibilidad del aprendizaje del KPI tras el registro | Done | Readiness inicial |

## Contexto Brain

- Épica DOE17 (Configuración de alertas por usuario en KPIs, datasets, widgets) — RFC Complete
- Épica 2.1 (Visibilidad KPI) — fue cancelada en M2 pero la necesidad de **visibilidad cross-chart de KPIs configurados** persiste

## Gap UX

- Decidir si es:
  - **Página dedicada** `/operation-center/anomalies/kpis` (lo que era SWAT-534)
  - **Vista dentro del modal de configuración** existente (SWAT-415 ya cubre parte)
  - **Tab del config mode** (lo que hizo SWAT-1250 para System KPI)
- Acciones bulk: activar/desactivar/silenciar múltiples
- Export CSV (estaba en scope original de SWAT-822)
