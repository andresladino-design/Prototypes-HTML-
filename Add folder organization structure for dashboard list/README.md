# Carpetas en la lista de tableros — SWAT-577

Organización por carpetas para el panel de Tableros del Centro de operaciones.
Los usuarios acumulan tableros (159 en la cuenta de referencia) en una lista plana e infinita;
el buscador exige recordar el nombre. Este proyecto diseña el mecanismo de **reconocimiento**.

🔗 [SWAT-577 en Linear](https://linear.app/simetrik/issue/SWAT-577/enhancement-dashboards-add-folderorganization-structure-for-dashboard)
**Última actualización:** 2026-08-03 · **Estado:** 🟡 En diseño (etapa 6 de 8)

## Cómo verlo

| Prototipo | Qué es | Local |
|-----------|--------|-------|
| `prototypes/00-baseline-tableros.html` | **Estado actual (antes).** Réplica del panel en producción, sin carpetas. Punto de comparación del handoff. | abrir el archivo en el navegador |
| `prototypes/index.html` | **Prototipo con carpetas.** Switch A/B (acordeón vs drill-down), toggle antes/después, 6 escenarios y las 9 interacciones. | abrir el archivo en el navegador |

## Estructura

```
plans/      → un plan por etapa (empezar por plans/00-indice.md)
handoff/    → documentos para el equipo (exploración, decisiones, benchmark, handoff FE/BE)
design.md   → sistema de diseño del prototipo, derivado de desyk
design/     → tokens.css + tailwind.desyk.js extraídos de desyk
prototypes/ → los HTML
.ohana/     → user flows en Moka
```

## Estado por etapa

| # | Etapa | Entregable | Estado |
|---|-------|-----------|--------|
| 0 | Exploración FE / BE | `handoff/00-exploracion-fe-be.md` | ✅ |
| 0.5 | Decisiones de modelo (D1–D7) | `handoff/01-decisiones.md` | ✅ |
| 1 | Benchmark de interacción (I1–I6) | `handoff/01-benchmark.md` | ✅ |
| 2 | Sistema de diseño desde desyk | `design.md` + `design/` | ✅ |
| 3 | Vista espejo del panel actual | `prototypes/00-baseline-tableros.html` | ✅ |
| 4 | User flows | `.ohana/flow.json` (7 flows + sitemap) + `handoff/04-userflows.md` | ✅ |
| 5 | User stories UX | `handoff/05-user-stories.md` (8 historias + revisión heurística) | ✅ |
| 6 | Prototipo con carpetas | `prototypes/index.html` (A/B + antes/después) | ✅ |
| 7 | Handoff FE + BE | `handoff/07-*.md` | ⬜ |
| 8 | Tickets en Linear | sub-issues de SWAT-577 | ⬜ |

## Decisiones tomadas

Carpetas **por cuenta** · **un solo nivel** · pertenencia **exclusiva** · eliminar carpeta **desagrupa** (nunca borra tableros) ·
mover por **menú `⋮` + drag** · carpetas **dentro** de la sección "Tableros" · el orden A→Z aplica en cada nivel.

Detalle y razones en [`handoff/01-decisiones.md`](handoff/01-decisiones.md).

## Stack

Tailwind CSS (CDN) · Alpine.js · Lucide Icons · tokens de desyk (`design/tokens.css`) · sin build.

## Changelog

### 2026-08-03
- Exploración de `fe-solutions-mf` (@ `8aebc1879`) y `op-center-backend` (@ `8cc5bc3b`): no existe concepto de carpeta; precedentes en Favoritos y en Almacenamiento.
- Cerradas las decisiones de modelo D1–D7 y las de interacción I1–I6.
- `design.md` + tokens extraídos de `@simetrikinc/desyk-components@1.30.0-0`.
- Baseline HTML del panel actual con 6 estados.
- 7 user flows (F1–F7) + sitemap en Moka, con la anatomía de las pantallas clave.
- 8 user stories UX con criterios verificables, métricas, telemetría y revisión heurística (3 críticos incorporados).
- Prototipo con carpetas: variantes A/B, toggle antes/después, 6 escenarios, drag & drop, deshacer y los 3 fixes de a11y.
