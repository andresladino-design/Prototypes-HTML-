# 2. Soportar KPIs de Visual de Pendiente Avanzados

**Prioridad**: 🟢 P1 (verde)
**Impacto**: 5 · **Esfuerzo**: 3 · **Neto**: 15

## Qué se necesita

Que el visual **Pendientes Avanzados** sea fuente válida para registrar KPIs / anomaly monitoring (hoy está excluido).

## Estado en Linear

### Visual ya existe (gráfico Pendientes Avanzados — Fase 2, Done)

| Issue | Título | Status |
|---|---|---|
| SWAT-381 | [E] Gráficos de pendiente en dashboards (parent) | Done |
| SWAT-324 | Nuevo tipo de gráfico: Pendientes Avanzados | Done |
| SWAT-379 | Gráfico de pendiente con configuración avanzada (opcional) | Done |
| SWAT-495 | Estructura visual: barras duales, %, ajustes, config inicial | Done |
| SWAT-514 | Configuración de rangos relativos del widget | **In Progress** (Felipe Duarte) |
| SWAT-1216 | Bug: error al crear la gráfica en tableros | Done (Urgent) |
| SWAT-1328 | Bug: Advanced Pendings — lado B sin no-conciliados | Done (Urgent) |

### KPI/anomaly monitoring sobre pending_kpi

| Issue | Título | Status | Nota |
|---|---|---|---|
| **SWAT-1433** | [FE] Smart Monitoring UI para charts `pending_kpi` | **In Progress** | Camila Herrera · M5 Reconciliación · **este es el ticket clave** |

## Gap

- `pending_kpi` está excluido de `MONITORING_SUPPORTED_TYPES` (`src/oc/features/anomalies/types/constants.ts:20`)
- `AnomalyMonitoringConfig.tsx` (~3857 líneas) asume `chartDetail.config.metrics`, pero `PendingKpiCustom` no tiene `metrics` ni columnas dinámicas
- Hay que rediseñar el modal de configuración para que entienda esta forma alterna del config

## Contexto Brain

- Funcionalidad de Pendientes en `funcionalidades/pendientes/`
- Anomalías sobre pendientes: Épica DOE16 (Detección IA) escenario aplicable a reconciliación
