# 1. Permitir prender y apagar los sys-kpi

**Prioridad**: 🟠 P2 (naranja)
**Impacto**: 2 · **Esfuerzo**: 1 · **Neto**: 2
**Nota original**: *"add toggle en la seccion de RoI"*

## Qué se necesita

Toggle en la sección de Resource of Interest (RoI) para que el usuario pueda **activar/desactivar System KPIs por fuente** sin perder la configuración.

## Estado en Linear

| Issue | Título | Status | Nota |
|---|---|---|---|
| **SWAT-537** | [E2.2] Activar/desactivar system KPIs por fuente | **In Progress** | Asignado a Andres · Phase 3 · Milestone M3 Production Readiness I |
| SWAT-1250 | Tab System KPI: lista de fuentes + panel de detalle con Preparación | Done | UI base ya implementada |
| SWAT-1304 | POST /system-kpis: paridad con CreateKpiRequest | Done | BADS expone settings + per-series limits |
| SWAT-1308 | POST /system-kpis descarta timezone | Done | Bug fix |

## Contexto Brain

- Épica DOE16 (Detección IA y parametrización) cubre la exclusión de fuentes
- `ResourceProfile` introducido en M2.5 (Slice 1, SWAT-1235)
- La cascada automática (SWAT-517) crea system KPIs sobre todo el árbol de dependencias → este toggle permite excluir fuentes específicas (sandbox, dev, estacionalmente apagadas)

## Gap UX

- Diseñar UI del toggle en el contexto RoI del modal de configuración
- Copy: claridad sobre qué pasa con signals existentes al apagar (¿se descartan, se silencian, quedan en pausa?)
- Estado intermedio "pausado por usuario" vs "pausado por sistema"
