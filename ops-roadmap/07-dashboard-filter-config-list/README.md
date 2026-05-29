# 7. Add dashboard filter in Config list

**Prioridad**: 🟠 P2 (naranja)
**Impacto**: 3 · **Esfuerzo**: 1 · **Neto**: 3

## Qué se necesita

Agregar un **filtro por dashboard** en la lista de configuraciones (KPIs / monitoring configs). Hoy el usuario ve la lista completa sin poder acotar por dashboard.

## Estado en Linear

### Filtros existentes en tableros (referencia, todos Done)

| Issue | Título | Status | Nota |
|---|---|---|---|
| SWAT-90 | [Dashboards] Filtros por página para gráficas aplicados a datasets | Done | Filtros base de tableros |
| SWAT-725 | [Dashboard] Persistir valores de filtros por página | Done | Defaults + persistencia |
| SWAT-1131 | OC Tableros — Polish iterativo Wave 2 (filtros completos + edit-mode glow) | Done | Refinamiento UX |
| SWAT-1039 | E2E: dashboard page filters (11 tests, 9 filter types) | Done | Test coverage |

### Filtros en la lista de anomalías (referencia)

| Issue | Título | Status | Nota |
|---|---|---|---|
| SWAT-693 | [UX/FE] Rediseño del panel izquierdo de anomalías (tarjetas, estados y filtros) | Done | Andres · botón Filtrar |
| SWAT-698 | [FE] Filtros de la lista: mantener existentes + añadir filtro por tablero y por gráfico | **Duplicate** | Cancelado por duplicado |

### Gap

- No hay issue específico abierto para **filtro por dashboard en la Config List (KPIs)**
- Patrón ya existe en otros lados → reutilizable

## Contexto Brain

- Épica DOE17 (Configuración de alertas por usuario en KPIs, datasets, widgets) — RFC Complete
- Listas de config van a crecer (1 KPI por chart × N charts × N dashboards) → filtros son críticos para escala

## Gap UX

- Posición del filtro (top bar de la lista)
- Multi-select de dashboards
- Combinable con otros filtros (estado, recurso, tipo)
