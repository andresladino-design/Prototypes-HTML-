# 9. Favoritos: mostrar fácilmente incidentes en tableros relevantes al usuario

**Prioridad**: 🟠 P2 (naranja)
**Impacto**: 3 · **Esfuerzo**: 2 · **Neto**: 6
**Nota original**: *"En filtros por dashboards (incidents, config), mostrar dashboards en orden de favoritos"*

## Qué se necesita

Cuando el usuario filtra por dashboard en la lista de incidentes (o en config), los **dashboards favoritos aparecen primero** — leveraging el sistema de favoritos ya existente.

## Estado en Linear

### Sistema de favoritos ya existe (todo Done)

| Issue | Título | Status | Nota |
|---|---|---|---|
| SWAT-762 | [Dashboard - Favoritos] Sistema de favoritos de tableros | Done | Persistencia cross-device, límite 15, ⭐ siempre visible, drag & drop |
| SWAT-764 | [Favoritos] Sección FAVORITOS en sidebar con empty state | Done | Sección arriba de TABLEROS |
| SWAT-881 | [Favoritos] Alinear UX/UI a patrón de Pendientes (pin zone + arrastre) | Done | Consistencia visual con Pendientes |
| SWAT-891 | [Dashboard Favoritos] Mejoras y fixes post-release | Done | Label "Favoritos" + número |

### Lista de incidentes

| Issue | Título | Status | Nota |
|---|---|---|---|
| SWAT-530 | [E1.5] Lista navegable de incidentes | Done | Lista principal de incidentes |
| SWAT-693 | [UX/FE] Rediseño panel izquierdo anomalías | Done | Filtros del panel |
| SWAT-1018 | Mejoras en la vista de incidentes | Done | Polish |
| SWAT-558 | [Épica 7.3] Contextualización de incidentes con metadata de tableros | Backlog | M7 — relacionar incidents a su dashboard de origen |

### Gap

- No hay issue específico para "orden por favoritos en filtros"
- API de favoritos ya está → debería ser **only-FE** consumir `?favorite=true` o ordenar por `is_favorite` desc

## Contexto Brain

- Épica DOE18 (Centro de anomalías — hub central) — RFC Complete
- DOE17 (Config de alertas por usuario) — RFC Complete

## Gap UX

- Sección "Favoritos" arriba en el dropdown de filtro
- Empty state si el usuario no tiene favoritos
- Aplicar mismo patrón en **dos lugares**: filtros de Incidents y filtros de Config
