# Ops Roadmap — Anomaly Management UX

Roadmap UX del Operation Center v2.8 (Anomaly Management). Cada carpeta corresponde a un tema del backlog priorizado.

## Leyenda de colores (priorización)

| Color | Prioridad | Items |
|---|---|---|
| 🟢 Verde | P1 — siguiente en cola | 2, 5.1, 5.2, 5.3, 5.4, 10 |
| 🟠 Naranja | P2 — medio plazo | 1, 7, 9 |
| 🟣 Morado | P3 — requiere research | 3 |
| 🔵 Azul | P4 — más adelante / requiere research | 4, 6, 8 |
| 🔴 Rojo | Parent / "start research" | 5, 6, 10 |

## Tabla de priorización (Impacto × Esfuerzo)

| # | Tema | Impacto | Esfuerzo | Neto | Color | Notas |
|---|---|---|---|---|---|---|
| 1 | Prender/apagar sys-kpi | 2 | 1 | 2 | 🟠 | Toggle en sección RoI |
| 2 | KPIs Visual Pendiente Avanzados | 5 | 3 | 15 | 🟢 | |
| 3 | Umbral relativo (%) | 3 | 2 | 10 | 🟣 | Start research, user prod data |
| 4 | Refactor Navegación | 4 | inf | — | 🔵 | Start research |
| 5 | MVP reglas de notificación | 4 | 3 | 12 | 🔴 | Parent (5.1–5.4) |
| 5.1 | Parametrizar breach_pct en signals | — | — | — | 🟢 | |
| 5.2 | Parametrizar severity de Incidente | — | — | — | 🟢 | |
| 5.3 | Seleccionar Signals / Incident / ambos | — | — | — | 🟢 | |
| 5.4 | Mejora visual notificaciones Slack (Block Kit) | — | — | — | 🟢 | |
| 6 | Notificación tipo "reporte" consolidado / grupo | 5 | 5 | 25 | 🔵 | Start research |
| 7 | Add dashboard filter in Config list | 3 | 1 | 3 | 🟠 | |
| 8 | Add view of configured KPIs (anomalies) | 2 | 2 | 4 | 🔵 | |
| 9 | Favoritos: mostrar incidentes en tableros relevantes | 3 | 2 | 6 | 🟠 | Orden de favoritos en filtros |
| 10 | Support notifications for System KPIs | 5 | 3 | 15 | 🟢 | |

## Fuentes consultadas

- **Brain**: `~/Simetrik/ProductEngineeringBrain/versions/v2.8/operation-center/funcionalidades/anomalias/`
  - `Definicion - Anomalias.md` (21 casos de uso)
  - `Arquitectura - Anomalias.md` (5 servicios: AMS, KPISs, BADS, Brain, AVA)
- **Linear**: proyecto Operation Center (team Swat AI)
