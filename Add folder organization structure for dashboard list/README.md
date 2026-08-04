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
| `prototypes/index.html` | **Prototipo transversal.** Tabs Tableros/Datasets con la misma carpeta, vista de Anomalías con filtro por carpeta heredada, switch A/B, toggle antes/después y 6 escenarios. | abrir el archivo en el navegador |

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
| 4 | User flows | `.ohana/flow.json` (**10 flows + sitemap**, 91 pantallas) + `handoff/04-userflows.md` | ✅ |
| 5 | User stories UX | `handoff/05-user-stories.md` (8 historias + revisión heurística) | ✅ |
| 6 | Prototipo con carpetas | `prototypes/index.html` (A/B + antes/después) | ✅ |
| 6.6 | Prototipo transversal | Datasets + Anomalías por carpeta en el mismo prototipo | ✅ |
| 7 | Handoff FE + BE | `handoff/07-*.md` | ⬜ |
| 8 | Tickets en Linear | sub-issues de SWAT-577 | ⬜ |

## Decisiones tomadas

Carpetas **por cuenta** · **un solo nivel** · pertenencia **exclusiva** · eliminar carpeta **desagrupa** (nunca borra tableros) ·
mover por **menú `⋮` + drag** · carpetas **dentro** de la sección "Tableros" · el orden A→Z aplica en cada nivel ·
**crear es un wizard de 2 pasos** (elegir tableros → nombre) y **"Agregar tableros"** llena una carpeta existente con selección múltiple.

**Transversal (D10):** una tabla `folders` compartida, con reparto **3 + 1**. Membresía **declarada** en las tres
listas de recursos organizables — tableros, datasets y **conciliaciones** (el panel de Pendientes las lista) — y
**heredada** en anomalías, el único stream. Orden de entrega: Tableros → Datasets → Anomalías → Pendientes.

Detalle y razones en [`handoff/01-decisiones.md`](handoff/01-decisiones.md).

## Stack

Tailwind CSS (CDN) · Alpine.js · Lucide Icons · tokens de desyk (`design/tokens.css`) · sin build.

## Changelog

### 2026-08-04 — vistas replicadas de las capturas reales
- **SD-7 (nueva):** el panel de Conciliaciones **ya está agrupado por dataset** (con badge `clickhouse` y conteos), y cada fila lleva badge **AVZ/STD**. Si la carpeta entrara como nivel extra habría **dos jerarquías compitiendo** en 288px. Implementado como **toggle «Agrupar por: Dataset | Carpeta»** — un solo nivel a la vez.
- **Detalle de anomalía completo:** narrativa con chips inline, meta en columnas (Estado · Severidad · Tableros impactados · **Carpeta heredada**), los tres colapsables (Hallazgos · Recomendaciones · Proceso de análisis) con el disclaimer de IA, barra de acciones, y los tabs **abajo en una card aparte** (Impacto potencial · Evidencia · Línea de tiempo).
- **Paginación al pie** del panel de anomalías: `1 - 20 de 3054 incidencias`. Con 3054, filtrar por carpeta no es cosmético: es 153 páginas contra 1.
- Panel de Pendientes con contador, fijadas (grip + workspace + AVZ/STD) y tarjetas de resumen Lado A / Lado B con sus tiles.

### 2026-08-04 — vistas reales de Anomalías y Pendientes
- **Corrección del modelo:** el reparto no es "2 declaradas + 2 heredadas" sino **3 + 1**. El panel de Pendientes no lista pendientes: lista **conciliaciones**, con buscador y sección de fijadas — la misma anatomía que Tableros. Así que la conciliación se organiza de forma **declarada** y el pendiente hereda de ella. **Anomalías es el único stream.**
- **Vista de Anomalías reconstruida contra el código:** es **master-detail**, no una lista a ancho completo. Panel con los 3 tabs reales (Gestión / Configuración / Alertas, donde solo el activo muestra su label), fila `Filtrar · Ordenar · Guardados`, barra de filtros activos, y `AnomalyCard` con su anatomía real (título `{categoría} - {tipo}: {recurso}`, badge de estado, "Tableros afectados", antigüedad y origen). La carpeta entra como categoría del popover y como chip.
- **Vista de Pendientes nueva:** panel "Conciliaciones" con filtro de espacio, buscador, fijadas y **carpetas declaradas** sobre las conciliaciones.
- Los 6 estados reales de incidente con sus badges (En observación, Abierto, En investigación, Confirmado, Resuelto, Cerrado automático).

### 2026-08-04 — prototipo transversal
- **Tabs Tableros | Datasets funcionales** con la MISMA carpeta: «Adquirencia» muestra 24 tableros en un tab y 8 datasets en el otro. El contador es **por vista**, no global.
- **Vista de Anomalías** con filtro por carpeta **heredada**: ningún incidente se archivó a mano; la carpeta se resuelve desde el recurso al que apunta, y cada fila la muestra como metadato clickable que lleva a la carpeta.
- **Wizard con selector de entidad** en el paso 1 (F9): se puede armar una carpeta con tableros y datasets en una sola pasada. El resumen y los toasts desglosan por entidad.
- **Copy destructivo por entidad:** «Los 24 tableros y 8 datasets que contiene volverán a sus listas» — «32 ítems» no diría qué se está tocando.
- Icono por tipo en las filas (benchmark T2: Metabase mezcla tipos pero siempre con icono).

### 2026-08-04 — benchmark y flujos del alcance transversal
- **Benchmark transversal** (`handoff/02-benchmark-transversal.md`): el modelo de D10 es el **patrón dominante**. Grafana mete dashboards y reglas de alerta en la misma carpeta y la navega **con tabs por tipo**; Metabase hace que los eventos de una timeline aparezcan solos en los gráficos de su colección (**herencia por co-locación**); Datadog usa tags en vez de carpetas para monitores (el contrafactual). **Nadie obliga a archivar eventos a mano.**
- Cierra **SD-1** (no archivar incidentes a mano), **SD-2** (filtro antes que agrupación), **SD-3** (el filtro guardado sí puede incluir carpeta — `filters` es JSONB, sin migración), **SD-5** ("carpeta" se mantiene: es el término de Grafana para esta mezcla) y **SD-6**.
- Flujos nuevos: **F9** (una carpeta con tableros y datasets, con el contador por vista y el copy destructivo por entidad) y **F10** (anomalías de una carpeta por herencia). F1–F8 quedan marcados como **agnósticos de la entidad**. Sitemap ampliado a las cuatro vistas.

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
