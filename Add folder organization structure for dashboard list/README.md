# Organización por carpetas en el Centro de operaciones — SWAT-577

Carpetas **anidables hasta 3 niveles** en el panel de **Tableros** del OC, por cuenta.
Los usuarios acumulan tableros (159 en la cuenta de referencia) en una lista plana e infinita;
el buscador exige recordar el nombre. Este proyecto diseña el mecanismo de **reconocimiento**.

🔗 [SWAT-577 en Linear](https://linear.app/simetrik/issue/SWAT-577/enhancement-dashboards-add-folderorganization-structure-for-dashboard)
**Última actualización:** 2026-08-14 · **Estado:** 🟢 Handoff escrito · falta revisión visual y capturas

> **Dos cambios de alcance del 2026-08-14.** El sistema **transversal a 4 entidades** que se había
> ampliado el 2026-08-04 se **descartó**: las carpetas son solo de Tableros (D10). Y se abrió el
> **anidamiento a 3 niveles**, revirtiendo «un solo nivel» (D2). El changelog de abajo conserva
> lo que se exploró.

## Cómo verlo

| Prototipo | Qué es | Local |
|-----------|--------|-------|
| `prototypes/00-baseline-tableros.html` | **Estado actual (antes).** Réplica del panel en producción, sin carpetas. Punto de comparación del handoff. | abrir el archivo en el navegador |
| `prototypes/index.html` | **Prototipo de carpetas.** Árbol in-place de 3 niveles, mover carpeta, secciones colapsables, toggle antes/después y 7 escenarios. | abrir el archivo en el navegador |

> ⚠️ **El prototipo construye el árbol en cliente.** Producción pagina de 20 en 20 con orden y
> búsqueda server-side, así que **no es implementable tal cual** — el contrato correcto está en
> [`handoff/07-handoff-be.md`](handoff/07-handoff-be.md) (D15). Todo lo demás sí se replica.
>
> ⚠️ **Parte de la mejora visual no es de este issue.** El truncado al medio y los botones de fila
> en hover son un entregable aparte: [`../ancho-util-lista-tableros/`](../ancho-util-lista-tableros/).

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
| 0.5 | Decisiones de modelo | `handoff/01-decisiones.md` (D1–D15) | ✅ |
| 1 | Benchmark de interacción (I1–I6) | `handoff/01-benchmark.md` | ✅ |
| 2 | Sistema de diseño desde desyk | `design.md` + `design/` | ✅ |
| 3 | Vista espejo del panel actual | `prototypes/00-baseline-tableros.html` | ✅ |
| 4 | User flows | `.ohana/flow.json` (**12 flows + sitemap**) + `handoff/04-userflows.md` | ✅ |
| 5 | User stories UX | `handoff/05-user-stories.md` (11 historias + revisión heurística) | ✅ |
| 6 | Prototipo con carpetas | `prototypes/index.html` (A/B + antes/después) | ✅ |
| 6.6 | Anidamiento de 3 niveles | árbol, mover carpeta, ciclos, tope | ✅ |
| 6.7 | Secciones colapsables | las 4 del panel, persistidas | ✅ |
| ~~6.5~~ | ~~Alcance transversal (D10)~~ | ⛔ descartado — se conserva como registro | — |
| 7 | Handoff FE + BE | `handoff/07-handoff-fe.md` · `07-handoff-be.md` · `07-antes-despues.md` | ✅ falta capturas |
| 8 | Tickets en Linear | sub-issues de SWAT-577 | ⬜ |

## Decisiones tomadas

Carpetas **por cuenta** · **hasta 3 niveles** de anidamiento · pertenencia **exclusiva** ·
eliminar carpeta **disuelve un nivel** (el contenido sube a la madre, nunca se borra) ·
mover por **menú `⋮` + drag** · carpetas **dentro** de la sección "Tableros" · el orden A→Z aplica en cada nivel ·
**crear es un wizard de 2 pasos** (elegir tableros → nombre) y **"Agregar tableros"** llena una carpeta existente con selección múltiple ·
las **4 secciones del panel colapsan** · el **icono de carpeta lleva el estado** (sin chevron) · **árbol in-place**, sin drill-down ·
el **agrupamiento se resuelve server-side**.

**Solo Tableros (D10 revisada):** Datasets conserva su lista plana y sirve como control de que el
feature no lo afectó. Anomalías y Pendientes quedan fuera.

**Tres mitigaciones que no son cosméticas** — el panel tiene 240px útiles y los nombres reales ya
se truncan, así que el anidamiento solo funciona con indentación de **12px** por nivel, **truncado
al medio** y **tope de 3**. Peor caso: 158px para una carpeta de nivel 3. Ver D2.

Detalle y razones en [`handoff/01-decisiones.md`](handoff/01-decisiones.md).


---

### 2026-08-14 — recorte de alcance, anidamiento y handoff

- **D10 revertida:** las carpetas son **solo de Tableros**. Se quitaron del prototipo las vistas de Anomalías y Pendientes (~640 líneas), y Datasets volvió a lista plana. Los flujos F9/F10 del alcance transversal se borraron del board.
- **D2 revertida:** **anidamiento hasta 3 niveles**. Entran mover una carpeta, guarda de ciclos, unicidad entre hermanas y el tope validado en UI y BE.
- **D6 revisada:** eliminar una carpeta **disuelve un nivel** — el contenido sube a la madre, no a la raíz. Y dejó de ser una FK: es lógica de servicio, así que el test de que no borra tableros pasa a ser obligatorio.
- **D12/D13 nuevas:** las 4 secciones del panel colapsan; el icono de carpeta absorbe el chevron.
- **D15 nueva, y es la que más peso tiene:** revisar el BE mostró que la lista es paginada de 20 con `search`/`sort` server-side y tope de 100. **El árbol no se puede resolver en cliente.** El riesgo ya estaba escrito en la exploración §5.1 y se había perdido de vista.
- **D14 extraída:** el truncado al medio y los botones en hover se van a [`../ancho-util-lista-tableros/`](../ancho-util-lista-tableros/) — arreglan un problema que ya existe hoy y no dependen de carpetas.
- **D16 · el A/B se cerró: gana el árbol in-place.** Se descartó el drill-down por niveles y se quitó del prototipo (~100 líneas). El gesto más frecuente es cambiar de tablero y navegar le suma clics justo a eso. El trade-off aceptado: el in-place paga 12px de indentación por nivel, algo que el drill-down no pagaba.
- **Etapa 7 escrita** (no existía): handoff de FE, de BE y el antes/después contra producción.
- **Rendimiento del prototipo:** el árbol pasó de 60 recorridos de la colección por render a 3 (~13.000 accesos a 657); con el árbol abierto los clics se bloqueaban.

## Stack

Tailwind CSS (CDN) · Alpine.js · Lucide Icons · tokens de desyk (`design/tokens.css`) · sin build.

## Changelog

### 2026-08-04 — patrón unificado de panel (D11)
- Los tres paneles divergían en **10 de 10 slots** (ancho 288 vs 425, buscador h-9 vs h-10 vs inexistente, el contador en tres lugares distintos). Documentado el patrón **«Panel de recursos del OC»** con 9 slots en orden fijo en `design.md`.
- **El eje que ordena todo: artefacto vs. evento.** Es el mismo criterio que decide la membresía de carpeta (D10): un artefacto se declara, un evento hereda. Y también deriva la unidad de fila (32px vs card), el ancho, el fin de lista (scroll vs paginación) y si existe acción de crear. Una entidad nueva se clasifica una vez y lo demás sale solo.
- **Unificado lo accidental:** contador como badge junto al título en los tres · **buscador nuevo en Anomalías** ("Buscar por recurso") · buscador a `h-10` en los tres · Anomalías pasa a una card con `border-r` como los otros dos.
- **Documentado como regla lo semántico**, en vez de forzarlo: fila, ancho y paginación se derivan del eje.
- Abiertas: **SD-8** ("Favoritos" en Tableros vs "Fijados" en Pendientes: mismo mecanismo, dos nombres) y si Pendientes debería tener acción primaria.

### 2026-08-04 — vistas replicadas de las capturas reales
- **SD-7 (nueva):** el panel de Conciliaciones **ya está agrupado por dataset** (con badge `clickhouse` y conteos), y cada fila lleva badge **AVZ/STD**. Si la carpeta entrara como nivel extra habría **dos jerarquías compitiendo** en 288px. Implementado como **toggle «Agrupar por: Dataset | Carpeta»** — un solo nivel a la vez.
- **Detalle de anomalía completo:** narrativa con chips inline, meta en columnas (Estado · Severidad · Tableros impactados · **Carpeta heredada**), los tres colapsables (Hallazgos · Recomendaciones · Proceso de análisis) con el disclaimer de IA, barra de acciones, y los tabs **abajo en una card aparte** (Impacto potencial · Evidencia · Línea de tiempo).
- **Paginación al pie** del panel de anomalías: `1 - 20 de 3054 incidencias`. Con 3054, filtrar por carpeta no es cosmético: es 153 páginas contra 1.
- Panel de Pendientes con contador, fijadas (grip + workspace + AVZ/STD) y tarjetas de resumen Lado A / Lado B con sus tiles.

### 2026-08-04 — vistas reales de Anomalías y Pendientes
> ⛔ *Revertido el 2026-08-14 (D10). Se conserva como registro de lo que se exploró.*
- **Corrección del modelo:** el reparto no es "2 declaradas + 2 heredadas" sino **3 + 1**. El panel de Pendientes no lista pendientes: lista **conciliaciones**, con buscador y sección de fijadas — la misma anatomía que Tableros. Así que la conciliación se organiza de forma **declarada** y el pendiente hereda de ella. **Anomalías es el único stream.**
- **Vista de Anomalías reconstruida contra el código:** es **master-detail**, no una lista a ancho completo. Panel con los 3 tabs reales (Gestión / Configuración / Alertas, donde solo el activo muestra su label), fila `Filtrar · Ordenar · Guardados`, barra de filtros activos, y `AnomalyCard` con su anatomía real (título `{categoría} - {tipo}: {recurso}`, badge de estado, "Tableros afectados", antigüedad y origen). La carpeta entra como categoría del popover y como chip.
- **Vista de Pendientes nueva:** panel "Conciliaciones" con filtro de espacio, buscador, fijadas y **carpetas declaradas** sobre las conciliaciones.
- Los 6 estados reales de incidente con sus badges (En observación, Abierto, En investigación, Confirmado, Resuelto, Cerrado automático).

### 2026-08-04 — prototipo transversal
> ⛔ *Revertido el 2026-08-14 (D10). Se conserva como registro de lo que se exploró.*
- **Tabs Tableros | Datasets funcionales** con la MISMA carpeta: «Adquirencia» muestra 24 tableros en un tab y 8 datasets en el otro. El contador es **por vista**, no global.
- **Vista de Anomalías** con filtro por carpeta **heredada**: ningún incidente se archivó a mano; la carpeta se resuelve desde el recurso al que apunta, y cada fila la muestra como metadato clickable que lleva a la carpeta.
- **Wizard con selector de entidad** en el paso 1 (F9): se puede armar una carpeta con tableros y datasets en una sola pasada. El resumen y los toasts desglosan por entidad.
- **Copy destructivo por entidad:** «Los 24 tableros y 8 datasets que contiene volverán a sus listas» — «32 ítems» no diría qué se está tocando.
- Icono por tipo en las filas (benchmark T2: Metabase mezcla tipos pero siempre con icono).

### 2026-08-04 — benchmark y flujos del alcance transversal
> ⛔ *Revertido el 2026-08-14 (D10). Se conserva como registro de lo que se exploró.*
- **Benchmark transversal** (`handoff/02-benchmark-transversal.md`): el modelo de D10 es el **patrón dominante**. Grafana mete dashboards y reglas de alerta en la misma carpeta y la navega **con tabs por tipo**; Metabase hace que los eventos de una timeline aparezcan solos en los gráficos de su colección (**herencia por co-locación**); Datadog usa tags en vez de carpetas para monitores (el contrafactual). **Nadie obliga a archivar eventos a mano.**
- Cierra **SD-1** (no archivar incidentes a mano), **SD-2** (filtro antes que agrupación), **SD-3** (el filtro guardado sí puede incluir carpeta — `filters` es JSONB, sin migración), **SD-5** ("carpeta" se mantiene: es el término de Grafana para esta mezcla) y **SD-6**.
- Flujos nuevos: **F9** (una carpeta con tableros y datasets, con el contador por vista y el copy destructivo por entidad) y **F10** (anomalías de una carpeta por herencia). F1–F8 quedan marcados como **agnósticos de la entidad**. Sitemap ampliado a las cuatro vistas.

### 2026-08-04 — alcance transversal
> ⛔ *Revertido el 2026-08-14 (D10). Se conserva como registro de lo que se exploró.*
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
