# Organización por carpetas en el Centro de operaciones — SWAT-577

Sistema de organización **transversal** a las entidades del OC: Tableros, Datasets, Anomalías y Pendientes,
con una carpeta compartida por cuenta. Arranca por el panel de Tableros.
Los usuarios acumulan tableros (159 en la cuenta de referencia) en una lista plana e infinita;
el buscador exige recordar el nombre. Este proyecto diseña el mecanismo de **reconocimiento**.

🔗 [SWAT-577 en Linear](https://linear.app/simetrik/issue/SWAT-577/enhancement-dashboards-add-folderorganization-structure-for-dashboard)
**Última actualización:** 2026-08-04 · **Estado:** 🟡 En diseño · alcance ampliado a 4 entidades (D10)

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
| 4 | User flows | `.ohana/flow.json` (8 flows + sitemap) + `handoff/04-userflows.md` | ✅ |
| 5 | User stories UX | `handoff/05-user-stories.md` (8 historias + revisión heurística) | ✅ |
| 6 | Prototipo con carpetas | `prototypes/index.html` (A/B + antes/después) | ✅ |
| 7 | Handoff FE + BE | `handoff/07-*.md` | ⬜ |
| 8 | Tickets en Linear | sub-issues de SWAT-577 | ⬜ |

## Decisiones tomadas

Carpetas **por cuenta** · **un solo nivel** · pertenencia **exclusiva** · eliminar carpeta **desagrupa** (nunca borra tableros) ·
mover por **menú `⋮` + drag** · carpetas **dentro** de la sección "Tableros" · el orden A→Z aplica en cada nivel ·
**crear es un wizard de 2 pasos** (elegir tableros → nombre) y **"Agregar tableros"** llena una carpeta existente con selección múltiple.

**Transversal (D10):** una tabla `folders` compartida. Membresía **declarada** en tableros y datasets (`folder_id`),
**heredada** en anomalías y pendientes (del recurso al que apuntan, resuelta en query). Orden de entrega:
Tableros → Datasets → Anomalías → Pendientes.

Detalle y razones en [`handoff/01-decisiones.md`](handoff/01-decisiones.md).

## Stack

Tailwind CSS (CDN) · Alpine.js · Lucide Icons · tokens de desyk (`design/tokens.css`) · sin build.

## Changelog

### 2026-08-04 — alcance transversal
- **D10** · El sistema pasa a ser **transversal a las 4 entidades** del OC con una carpeta compartida por cuenta. La tabla BE se vuelve genérica (`folders`) y el componente nace en `shared/`.
- **Membresía declarada vs heredada:** tableros y datasets se mueven a mano; anomalías y pendientes **heredan** la carpeta del recurso al que apuntan, así que se organiza una vez y las anomalías futuras quedan clasificadas solas.
- **Pendientes es el caso difícil:** su conciliación ancla vive en el **datahub**, no en `op-center-backend` → necesita tabla puente. Va último.
- Precedente encontrado: `IncidentSavedFilter` es *"named, account-shared"* — confirma D1.

### 2026-08-04 — feedback de las pruebas del prototipo
- **D8** · Crear carpeta pasa a wizard de **2 pasos** (elegir tableros → nombre con resumen de lo que se guarda). Revierte "la carpeta nace vacía": en pruebas, el diálogo se cerraba y el usuario quedaba buscando el resultado.
- **Orientación** · al crear, mover, agregar o renombrar, la carpeta se **revela**: expandida, con scroll hasta ella y resalte de ~2s.
- **D9** · La carpeta vacía muestra un **botón outline punteado** `⊕ Agregar tableros` que abre el selector múltiple; la misma acción está en el menú `⋮` de la carpeta. **Cierra PA-14.**
- Nuevo flow **F8** en Moka + tres requisitos de transaccionalidad para BE (`dashboard_ids[]` al crear, mover en lote, y devolver el `folder_id` anterior para poder deshacer).

### 2026-08-03
- Exploración de `fe-solutions-mf` (@ `8aebc1879`) y `op-center-backend` (@ `8cc5bc3b`): no existe concepto de carpeta; precedentes en Favoritos y en Almacenamiento.
- Cerradas las decisiones de modelo D1–D7 y las de interacción I1–I6.
- `design.md` + tokens extraídos de `@simetrikinc/desyk-components@1.30.0-0`.
- Baseline HTML del panel actual con 6 estados.
- 7 user flows (F1–F7) + sitemap en Moka, con la anatomía de las pantallas clave.
- 8 user stories UX con criterios verificables, métricas, telemetría y revisión heurística (3 críticos incorporados).
- Prototipo con carpetas: variantes A/B, toggle antes/después, 6 escenarios, drag & drop, deshacer y los 3 fixes de a11y.
