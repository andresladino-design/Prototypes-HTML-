# 4. Refactor Navegación

**Prioridad**: 🔵 P4 (azul)
**Impacto**: 4 · **Esfuerzo**: inf · **Neto**: — (no calculable)
**Nota original**: *"start research, user prod data to land better feedback"*

## Qué se necesita

Refactor de la navegación del Operation Center. Esfuerzo = infinito porque el alcance no está acotado todavía.

## Estado en Linear

### Refactors recientes ya entregados

| Issue | Título | Status | Nota |
|---|---|---|---|
| SWAT-912 | Refactor OC sidebars: alinear Dashboards/Datasets, Pendientes y Anomalías con Storage | Done | Patrón base Storage unificado |
| SWAT-948 | [OC FF] Aplicar FF y configuración de módulos en los 4 tabs | Done | Top nav controlado por FF + permisos |
| SWAT-947 | [OC FF] Aplicar FF en sidebar y ruta de entrada del Operation Center | Done | Provider |
| SWAT-693 | [UX/FE] Rediseño del panel izquierdo de anomalías (tarjetas, estados y filtros) | Done | Andres · ya entregado |
| SWAT-1390 | [simetrik-web-component] RouterProvider: cargar oc-box/routes + initialEntries OC | Done | Web component apunta al OC |

### No hay un issue "refactor navegación" abierto

## Research necesario

> *"start research, user prod data to land better feedback"*

- ¿Qué fricciones de navegación está reportando el usuario en producción?
- ¿Es navegación entre módulos del OC (Tableros / Pendientes / Anomalías / Storage)?
- ¿O navegación dentro de Anomalías (incident → signal → KPI config → chart)?
- ¿Breadcrumbs faltantes?
- Heurísticas Nielsen: visibilidad del estado del sistema, "where am I"

## Contexto Brain

- `arquitectura/frontend/` puede tener decisiones previas de IA / navegación
- Tabs OC ya unificados con Storage como patrón base
