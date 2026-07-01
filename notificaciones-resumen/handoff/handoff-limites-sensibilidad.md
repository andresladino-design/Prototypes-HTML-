# Handoff — Detección de anomalías por serie (límites fijos vs. sistema adaptativo)

Fecha: 2026-07-01 (act. 1-jul pm)
Origen: `notificaciones-resumen/index.html` → paso **Series y valores** del diálogo de monitoreo (KPI "Conteo De Registros", COUNT_DISTINCT). Bloques: `.ns-ai*` (Análisis inteligente) + `#nsWrap` (`ns-*`), estado `NS_*` en JS.
Registro: **Interno (Operation Center)** — operador Simetrik configurando cómo el monitoreo detecta anomalías de un gráfico.
Patrón de presentación: **narrativa previa (IA) → colapsables inline** con modelo **configuración general + override por serie**.

> **Reescrito el 1-jul-2026.** Reemplaza el modelo anterior (slider 0–100 + severidad por dos bandas + grilla "POR SERIE" + selector de categoría). El viejo (`.sens-*`, `.cat-*`, `.tm-series-*`, `.tm-dialog-preview-card`) quedó **deprecado y eliminado**.
>
> **Ajustes 1-jul pm:** (a) se agregó la **narrativa "Análisis inteligente"** arriba (lo que Simetrik responde antes de monitorear, con límites sugeridos) + estado de **carga "Pensando…"** y **skeleton** en los colapsables; (b) **se quitó agregar/quitar serie** — siempre se muestran las 6; (c) **default = Límites fijos** (antes adaptativo); (d) la **simulación muestra un solo total** de alertas (sin discriminar tipo).

---

## 1. Contexto y objetivo

Un gráfico/KPI se descompone en varias **series** (por fuente: Banco_Occidente, PayU_Latam, ERP_SAP…). Antes de configurar, Simetrik entrega una **narrativa de análisis** (línea base + límites sugeridos). Luego el operador define **cómo se detecta una anomalía**.

**Pregunta rectora (por serie y por defecto):** *¿Cómo quieres detectar las anomalías?*

| Modo | Qué hace | Controles |
|---|---|---|
| **Límites fijos** *(default)* | Tú defines el mínimo y el máximo válidos; avisa si el valor sale de ahí | inputs mín/máx (activables por bound) + valor sugerido |
| **Sistema adaptativo** | Simetrik aprende el comportamiento normal y avisa de lo inusual | nivel de sensibilidad (Alta/Media/Baja) + opción "Agregar límites de seguridad" |

**Modelo de configuración = general + override:**
- **Límites generales de {métrica}** (card "Todas las categorías"): la configuración **base** que heredan todas las series.
- **Límites por serie**: cada serie hereda la base hasta que la editas; al editarla queda con su propia config. **Todo arranca en Límites fijos.**

Objetivo: que el operador entienda **qué gana con cada modo** y vea, con un dato real (simulación sobre el histórico), **cuántas alertas** generaría — sin caja negra: input → output visible en la gráfica y en el número.

## 2. Usuario y registro

- **Registro:** Interno / Op Center. Power user, alta tolerancia a densidad, uso recurrente.
- **Modo de uso:** revisar la narrativa, configurar el KPI (general) y personalizar solo las series que lo ameriten.
- **Dato clave al primer vistazo:** de cada serie, **cómo está detectando** (badge de modo) y **cuántas alertas** daría.
- **Primera versión = evangelizar:** enseñar el modelo mental (fijo vs adaptativo). La config es explicativa, no una tabla densa. La vista súper-colapsada a tabla queda para una iteración futura.

## 3. Estructura de la vista

```
[✦] Análisis inteligente                         ← narrativa (IA), ver §4
┌─ card tintada ────────────────────────────────┐
│ Media 15.4   Límite inf. sugerido 10   Límite sup. 24 │
│ Línea base estable y limpia - 30 días…          │
│ › Ver análisis detallado                        │
│ ── ⓘ Este análisis refleja el agregado de todas las categorías │
└─────────────────────────────────────────────────┘

Límites generales de Conteo De Registros          ← encabezado de sección
  ▸ [layers] Todas las categorías  [Límites fijos] mín 10 · máx 24

Límites por serie                     [ 6 series ] ← encabezado + badge outline
  ▸ Banco_Occidente   [Límites fijos] mín 10 · máx 24
  ▸ PayU_Latam        [Límites fijos] mín 10 · máx 24
  … (una fila por serie, siempre las 6)
```

- **Colapsables inline, una abierta a la vez** (global y series comparten la regla).
- Al abrir una fila, se despliega **la card de configuración** (§5) inline.
- El **badge de cada fila** refleja el modo efectivo: `Límites fijos` (ámbar) o `Sistema adaptativo` (azul). Al lado, un resumen: rango mín/máx (fijo) o sensibilidad (adaptativo).
- **Las series son fijas** (catálogo del KPI): no hay agregar ni quitar; siempre se muestran todas. El contador es un **badge outline** (`{N} series`).

## 4. Análisis inteligente (narrativa) + carga

Antes de los colapsables, Simetrik muestra su lectura del histórico (portado de `config-system-kpi`, adaptado a vanilla, **sin gráfica** — la gráfica vive en cada colapsable).

- **Header** "Análisis inteligente" (indigo + ícono sparkle gradiente), fuera de la card.
- **Card tintada** con: **stats** (Media · Límite inferior sugerido · Límite superior sugerido) → **descripción** ("Línea base estable y limpia - 30 días…") → toggle **"Ver análisis detallado"** (colapsable) que despliega **Tendencia · Estacionalidad · Valores atípicos · Brechas de datos** → divisor → **footer** "ⓘ Este análisis refleja el agregado de todas las categorías".

**Estado de carga (al entrar a Series y valores):**
- El análisis entra en **"Pensando…"**: spinner + pasos que aparecen uno a uno (*Consultando datos históricos · Calculando línea base · Detectando patrones · Identificando atípicos · Generando narrativa*), el último con ícono gradiente, los previos con dot. El botón "Pensando…" colapsa/expande los pasos.
- Mientras "Pensando…", **los colapsables (`#nsWrap`) muestran un skeleton** (filas con shimmer) en vez del contenido real.
- Al terminar (~4–5 s en el prototipo), se **revela la narrativa** y se **renderizan los colapsables reales** (mismo instante).
- En prod: la narrativa, los sugeridos y el conteo los provee el BE; el "Pensando…" refleja la latencia real del análisis.

## 5. La card de configuración (global y por serie, mismo template)

Orden de la información (de arriba a abajo):

1. **Gráfica · últimos 30 días** (título pequeño + leyenda). **Se muestra completa** (histórico), sin marca "AHORA" ni tramo proyectado.
   - **Por serie:** línea del valor + **banda "rango esperado"** (solo en adaptativo) + **líneas de límite fijo** (en fijo, o si hay límites de seguridad).
   - **Global ("Todas las categorías"):** **todas las series superpuestas** (líneas tenues) — es el agregado. No dibuja banda (series de distinta escala); sí líneas de límite si aplica.
2. **Pregunta:** `¿Cómo quieres detectar las anomalías (por defecto / de esta serie)?` → dos radios: **Límites fijos** *(default)* / **Sistema adaptativo**.
3. **Panel según el modo:**
   - *Límites fijos:* grid **Límite inferior / superior**, cada uno con **checkbox** (incluir ese bound) + input + **chip azul "Valor sugerido: N"** (clic aplica; se oculta si ya coincide).
   - *Sistema adaptativo:* segmented **Alta / Media (recomendada) / Baja** + checkbox **"Agregar límites de seguridad"** que revela el grid de límites (mín/máx que avisan sí o sí).
4. **Caja de resultado (blanca, unificada):**
   - Texto contextual del aviso: `Te avisamos solo cuando la serie se salga del rango que definiste…` (varía por modo/seguridad).
   - Separador sutil.
   - **Simulación = un solo número:** `{N} avisos en los últimos 30 días`. **Sin discriminar** tipo (ya no hay "fuera de límites" / "comportamiento inusual" por separado): es el **total de veces que se levantaría una alerta** con la config actual. Se recalcula en vivo.

> La caja de resultado no lleva caption redundante ni fondo azul: el aviso hace de introducción y el número va debajo, en fondo blanco.

## 6. Arquitectura de componentes / clases

| Mock (prototipo) | Componente desyk | Notas |
|---|---|---|
| `.ns-ai` / `.ns-ai-head` / `.ns-ai-title` / `.ns-ai-card` / `.ns-ai-foot` | `Card` (tintada) + header | narrativa "Análisis inteligente" |
| `.ds-an-stats` / `.ds-an-stat*` | stat tiles | Media / Límite inf. / Límite sup. sugeridos |
| `.ds-an-desc` + `.ds-an-detail-toggle` (`.ds-an-detail-chev`) + `.ds-an-detail-body` (`.ds-an-section*`) | texto + `Collapsible` | descripción + "Ver análisis detallado" + secciones |
| `.ds-think` (`.ds-think-trigger` / `-spinner` / `-steps` / `-step` / `-dot`) | loader de pasos | estado "Pensando…" (`nsAiThink`) |
| `.ns-skel` / `.ns-skel-bar` | skeleton (shimmer) | placeholder de `#nsWrap` durante la carga (`nsShowSkeleton`) |
| `#nsWrap` | contenedor de la sección | render por JS (`nsInit` → `nsRenderList`) |
| `.ns-secth` + `#nsCnt` | encabezado + `Badge` outline | "Límites generales de {métrica}" · "Límites por serie" `{N} series`. Sin mayúsculas sostenidas. |
| `.ns-acc` / `.ns-acc-item` / `.ns-acc-hd` / `.ns-acc-body` | `Accordion` | colapsable; una abierta a la vez (`nsToggle`) |
| `.ns-acc-item.ns-gl` | item destacado | la card "Todas las categorías" (fondo tenue) |
| `.ns-badge` (`.adapt` / `.fijo`) | `Badge` | modo de detección |
| `.ns-radio` (×2) | `RadioCard` | Límites fijos / Sistema adaptativo (`nsSetMode`) |
| `.ns-seg` | `SegmentedControl` | Alta / Media / Baja (`nsSetLevel`) |
| `.ns-check` | `Checkbox` | "Agregar límites de seguridad" (`nsToggleSafety`) |
| `.ns-lim` (grid) | `Checkbox` + `Input` numérico | bound on/off (`nsSetBoundOn`) + valor (`nsSetLim`) |
| `.ns-limsug` | `Chip` (clic) | valor sugerido (`nsApplySug`) |
| `svg.ns-chart` | gráfico custom (SVG) | render `nsDraw`; línea/banda/límites, sin AHORA |
| `.ns-alert` (+ `.ns-alert-body` / `.ns-impact-row` con 1 tile) | `Card` neutra | aviso contextual + **total** de alertas, fondo blanco |

**Modelo de datos (fuente única en el prototipo):**

```
NS_GLOBAL = { mode:'fijo'|'adaptativo', level, safety, fixedLo, fixedHi, loOn, hiOn, sug:{lo,hi} }  // default: mode 'fijo'
NS_SERIES[] = { id, name, data:number[], sug:{lo,hi},
                customized:bool,   // false = hereda NS_GLOBAL (todas inician false)
                cfg:{...} }        // su config propia cuando customized
```

**Lógica clave:**
- **Herencia:** una serie con `customized=false` usa `NS_GLOBAL` (`nsView`). La primera edición la "forkea" (`nsBeforeEdit`).
- **Simulación (número único):** por serie, sobre TODA la ventana (sin corte "AHORA"). Se cuenta cada punto que dispararía alerta: fijo/seguridad → fuera de `[lo,hi]` activos; adaptativo → `|v − baseline| > margen(nivel)`. El total = suma. El global agrega el conteo de todas las series con su propio baseline. (Los puntos rojo/ámbar en la gráfica siguen distinguiendo visualmente el origen, pero el número es uno solo.)
- Todo (badges, resúmenes, gráfica, simulación) se re-renderiza desde el mismo estado.

## 7. Estados

- **Carga:** narrativa en "Pensando…" (pasos) + `#nsWrap` en **skeleton**. Al terminar → narrativa + colapsables reales.
- **Inicial (post-carga):** "Todas las categorías" y las 6 series en **Límites fijos** (mín 10 · máx 24), todas heredando el global; contador `6 series`.
- **Serie heredando:** badge del modo del global; al editar pasa a personalizada (sin badge extra; el override se refleja en su resumen/gráfica).
- **Global expandido:** todas las series superpuestas + simulación agregada.
- **Bound apagado:** input atenuado e inerte (conserva valor); ese límite no marca ni se dibuja.
- **Validación:** valor no numérico / `lower ≥ upper` con ambos activos → error + microcopy (pendiente de cablear).

## 8. Copy (glosario aplicado)

> Glosario Op Center: **monitoreo** (no "agente"/"Agente IA"), **incidente**, **señal**, **KPI**, **Tablero**. Sin em-dashes. Sin mayúsculas sostenidas en títulos.

- Narrativa: título `Análisis inteligente`; desc `Línea base estable y limpia - 30 días de observaciones de baja dispersión, sin brechas ni valores atípicos. Una línea base simple para anclar el monitoreo.`; toggle `Ver análisis detallado`; footer `Este análisis refleja el agregado de todas las categorías.`; pasos de carga (ver §4).
- Encabezados: `Límites generales de {métrica}` · `Límites por serie` + badge `{N} series`.
- Pregunta: `¿Cómo quieres detectar las anomalías (por defecto)?` (global) / `…de esta serie?` (serie).
- Radios: **Límites fijos** — `Tú defines el mínimo y el máximo válidos.` · **Sistema adaptativo** — `Simetrik aprende lo normal y avisa de lo inusual.`
- Sensibilidad: `Alta` (`Detecta hasta cambios chicos`) · `Media` (`Recomendada`) · `Baja` (`Solo lo muy fuera de lo normal`).
- Seguridad: `Agregar límites de seguridad` — `Un mínimo/máximo que avisa sí o sí, aunque el sistema lo vea normal. Para valores que jamás deberían pasar.`
- Límites: `Límite inferior` / `Límite superior` · chip `Valor sugerido: N`.
- Aviso (por modo): fijo → `Te avisamos solo cuando la serie se salga del rango que definiste. Predecible y bajo tu control.` · adaptativo → `Te avisamos cuando la serie se comporte distinto a lo habitual (sensibilidad {nivel}). Se ajusta solo.` · adaptativo+seguridad → `…y siempre que cruce tus límites de seguridad.` (global: "cada serie").
- **Simulación (número único):** `{N} avisos en los últimos 30 días`.

## 9. Microinteracciones

| Interacción | Detalle |
|---|---|
| Entrar a "Series y valores" | narrativa en "Pensando…" (pasos animados) + skeleton en colapsables; al terminar, reveal + render real |
| Ver análisis detallado | despliega/colapsa las secciones (chevron rota) |
| Abrir colapsable | cierra los demás; despliega la card; render de gráfica + simulación |
| Elegir modo / nivel / seguridad | re-render de panel, gráfica, aviso y total en vivo |
| Editar límite / toggle bound | redibuja banda/línea y recalcula el total; chip sugerido se muestra/oculta |

Durations canónicas: 120 / 200 / 320 ms ease-out. Skeleton para carga; spinner solo en el loader "Pensando…". Light mode.

## 10. Mapeo BADS / preguntas para ingeniería

- **Narrativa + sugeridos + baseline:** los provee el BE (análisis del histórico). El "Pensando…" refleja esa latencia; hoy **mockeado**.
- **Sistema adaptativo** → detección de patrón de BADS (`TRIGGER` / `TRAJECTORY` / `NEW_SERIES`); el **nivel** (Alta/Media/Baja) mapea a un parámetro real del detector → **confirmar valores con BE**.
- **Límites fijos / de seguridad** → umbral duro del usuario (condición adicional OR sobre el adaptativo; modelo Anodot).
- **Severidad** (`URGENT` / `REQUIRES_ATTENTION`) sigue **system-assigned** (no la elige el usuario). La UI ya no la discrimina en la simulación (solo total).
- **Simulación (total)** requiere que el BE devuelva el conteo de disparos por config sobre la ventana; **misma ventana** (30 días) para serie, banda y conteo.
- **Herencia:** override adaptativo por-serie es poco común (Splunk lo prohíbe); si se restringe, el override por serie podría limitarse a límites duros. Decisión de producto pendiente.

**Endpoint esperado (borrador):** `GET/PUT /monitoring/{chartId}/detection` con `analysis` (narrativa + sugeridos), `general` (config base) + `series[]` (`{id, override?}`); `data`, `band`, `suggested`, `signals` read-only del BE.

## 11. Investigación que respalda el diseño (1-jul)

- **Patrón dominante en monitoreo** (Datadog, New Relic, Dynatrace): una config declarativa + el motor la instancia por serie; override por excepción. La lista de series es de **inspección**.
- **Adaptativo + límite duro coexisten** (Anodot) → "sistema adaptativo + límites de seguridad".
- **UX (NN/g):** para editar config compleja de varios ítems, se eligió **colapsables inline (una abierta)** + **default global** (el default enseña el modelo mental) para una v1 que debe evangelizar.
- **Diferenciador de mercado:** análisis narrativo previo + simulación de impacto en vivo. Se mantienen.

## 12. Checklist pre-implementación

- [ ] **Narrativa "Análisis inteligente"** arriba: header + card (stats sugeridos + descripción + "Ver análisis detallado" + footer). Sin gráfica propia.
- [ ] **Carga:** estado "Pensando…" (pasos) + **skeleton** en los colapsables; al terminar, reveal narrativa + render real.
- [ ] Dos secciones tituladas (sin uppercase): **Límites generales de {métrica}** + **Límites por serie** (badge outline `{N} series`).
- [ ] Colapsables inline, una abierta a la vez (global + series). **Series fijas** (sin agregar/quitar).
- [ ] Card de config compartida: gráfica completa (sin AHORA) → pregunta modo → panel (fijo/adaptativo) → caja blanca aviso + **total único**.
- [ ] **Default = Límites fijos** (global y todas las series).
- [ ] Modo **Límites fijos** (mín/máx con on/off por bound + valor sugerido) y **Sistema adaptativo** (Alta/Media/Baja + límites de seguridad).
- [ ] Card "Todas las categorías" = base heredable; gráfica con series superpuestas + simulación agregada.
- [ ] Simulación = **un solo número** ("avisos en los últimos 30 días"), sin discriminar tipo.
- [ ] Glosario ("monitoreo", no "agente"), sin em-dashes, tokens desyk, 120/200/320 ms, A11y AA.
- [ ] BE: narrativa + banda + simulación + sugeridos reales (hoy mockeados); mapeo de nivel → parámetro del detector.

## 13. Prototipo ↔ repo real (`fe-solutions-mf`)

> **La feature YA existe** en el repo. Este prototipo **rediseña** el paso de límites/series del diálogo actual, **no es greenfield**. Stack: React + TS, `@simetrikinc/desyk-components`, **zustand** (solo modales/estado local), **@tanstack/react-query** (server state), sin react-hook-form. Microfrontend (Module Federation, rsbuild). CSS scoped a `#solutions-app`. i18n por namespace (es/en/pt).

**Ubicación:** `src/oc/features/anomalies/` (Operation Center). El diálogo de configuración vive en `components/AnomalyMonitoringConfig/`.

### Archivos clave
| Qué | Ruta |
|---|---|
| Diálogo de config (wizard: Programación → Notificaciones → métricas/series) | `components/AnomalyMonitoringConfig/AnomalyMonitoringConfig.tsx` |
| Detalle por KPI (baseline + narrativa + secciones colapsables) | `components/AnomalyMonitoringConfig/SystemKpiDetailView.tsx` |
| **Narrativa IA + "Pensando…"** | `components/AnomalyMonitoringConfig/AiReasoningSteps.tsx`, `AiCollectingLoader.tsx` |
| Input de límite (formateo `Intl`) | `components/AnomalyMonitoringConfig/components/ThresholdInput/ThresholdInput.tsx` |
| Radio de modo (patrón card) | `components/MonitoringConfigForm/components/MonitoringOptionCard/MonitoringOptionCard.tsx` |
| Notificaciones (email/slack) | `components/AnomalyMonitoringConfig/NotificationsSection`, `SlackChannelCard.tsx` |
| Form de monitoreo de ingesta (config-system-kpi) | `components/MonitoringConfigForm/` (`sections/*`) |
| Servicios | `services/anomalies/monitoringConfig` (config KPI), `services/anomalies/badsProxy` (baseline/preview + narrativa), `services/dashboards/notificationConfig` |
| Store | `features/anomalies/store/index.ts` (zustand: modales + analyzing) |
| Wrappers de portal (Shadow DOM en OC Box) | `shared/components/desyk-components-with-portals` (`Solutions*`) |

### Mapeo componente prototipo → real
| Prototipo (`ns-*` / clase) | desyk / componente real | Nota |
|---|---|---|
| Wizard del diálogo | `DialogNavigation` vía `SolutionsDialogNavigation` | ya en `AnomalyMonitoringConfig` |
| Colapsables (`.ns-acc`, `.ds-analysis`) | `Collapsible` / `Accordion` (`type=single`) | patrón `AiSection` en `SystemKpiDetailView` |
| Radios fijo/adaptativo (`.ns-radio`) | `RadioGroup`/`RadioGroupItem` (patrón `MonitoringOptionCard`) | no existe "RadioCard" en desyk |
| Segmented sensibilidad (`.ns-seg`) | `Tabs` o `ToggleGroup` | no existe "SegmentedControl" |
| Inputs de límite (`.ns-lim`) | `Input` + wrapper `ThresholdInput` | reusar el existente |
| Chip valor sugerido (`.ns-limsug`) | `Badge`/`Button` chip | valor de baseline (p5/p95) |
| Badges de modo (`.ns-badge`) | `Badge variant="outline"` | |
| Contador (`#nsCnt`) | `Badge variant="outline"` | |
| Skeleton (`.ns-skel`) | `Skeleton` | |
| Aviso (`.ns-alert`) | `Alert` / `Card` | |
| Gráfica (`svg.ns-chart`) | **recharts** (`ReferenceLine`=límite fijo, `ReferenceArea`=banda) | **no** SVG a mano |
| Switch/checkbox, Select, toasts | `Switch`/`Checkbox`, `Select`, `sonner` | |

### API desyk verificada (paquete `@simetrikinc/desyk-components` instalado)
Exports y variantes reales (import por subpath, p. ej. `from "@simetrikinc/desyk-components/badge"`):
- **accordion**: `Accordion` (prop `type: "single" | "multiple"`, `collapsible`), `AccordionItem` (**`variant: "rounded" | "simple"`**), `AccordionTrigger`, `AccordionContent`, `AccordionTitle`, `AccordionActions`, `AccordionTitleSlot`.
- **collapsible**: `Collapsible`, `CollapsibleTrigger`, `CollapsibleContent` (para el patrón "Análisis inteligente"/`AiSection`).
- **radio-group**: `RadioGroup` (`RadioGroupProps`), `RadioGroupItem` (`value/id/disabled/onClick`). No hay `RadioCard` → envolver como `MonitoringOptionCard`.
- **tabs**: `Tabs`, `TabsList`/`TabsTrigger` (variantes `size: "default" | "lg"`, `shape: "circle" | "square"`), `TabsContent`.
- **toggle-group**: `ToggleGroup` (`type single|multiple`, **`variant: "default" | "outline"`**, `size`, `joined`), `ToggleGroupItem`. Opción para el segmented Alta/Media/Baja.
- **badge**: `Badge` (**`variant: "default" | "destructive" | "outline" | "success" | "warning" | "info" | "ai" | "draft"`**). Modo fijo → `warning`; adaptativo → `info`/`ai`; contador → `outline`.
- **alert**: `Alert` (**`variant: "default" | "destructive" | "success" | "warning" | "info" | "ai"`**) + `AlertTitle`/`AlertDescription`/`AlertContent`/`AlertClose`. Para la caja de aviso.
- **input**: `Input` (`variant: "default" | "error"`) → usar con el wrapper `ThresholdInput` (formateo `Intl`).
- **checkbox**: `Checkbox` (Radix; `checked`/`onCheckedChange`). **switch**: `Switch` (`id`, `disabled`, `checked`/`onCheckedChange`).
- **skeleton**: `Skeleton` (`className`) para el loader de los colapsables.
- **chart**: existe `@simetrikinc/desyk-components/chart` (wrapper sobre recharts), pero en anomalías las gráficas se arman **directo con recharts** (`ReferenceLine`/`ReferenceArea`); confirmar con FE si migrar al wrapper desyk.
- **dialog-navigation**: `DialogNavigation*` (sidebar + content items) — es el wizard actual; usar los wrappers `Solutions*` por el Shadow DOM del OC Box.

> Verificado contra el paquete instalado en `fe-solutions-mf/node_modules/@simetrikinc/desyk-components/dist` (revisar versión al implementar). No existen en desyk: `RadioCard`, `SegmentedControl` (usar RadioGroup+wrapper y Tabs/ToggleGroup).

### Qué YA existe vs. qué cambia el prototipo
- **Narrativa "Análisis inteligente" + "Pensando…" → YA EXISTE** (`AiReasoningSteps` + `AiCollectingLoader`; baseline `KpiNarrative` con `seasonality/trend/data_gaps/outliers/overall_assessment` multilingüe, y `baseline.{mean,stddev,p5,p95,ci_*}`). El prototipo solo **alinea copy/layout**: header, "Ver análisis detallado", footer "agregado de todas las categorías", y los **límites sugeridos** salen de `p5`/`p95`/`mean`.
- **Skeleton de carga en los colapsables → NUEVO/menor** (usar `Skeleton`).
- **"Límites fijos vs Sistema adaptativo"** → mapea al **tri-estado de límite** que ya maneja el repo: `number` (fijo) · `null` (adaptativo) · `{mode:"off"}` (apagado). El prototipo lo vuelve una **pregunta explícita con 2 radios**. Default = fijo.
- **Colapsables por serie (general + override)** → hoy es `MetricPanelSection` + filas de threshold (`kpi_configs[].thresholds[]` con `series_value`). El prototipo propone **Collapsible por serie** con "Todas las categorías" como base heredable.
- **Simulación = total único → NUEVO**: requiere que BADS devuelva el **conteo de disparos por config** sobre la ventana (hoy no existe explícito). Sin discriminar tipo.
- **Series fijas (sin agregar/quitar)** → coherente con `series_column_ids` del KPI (el catálogo lo define el KPI, no el usuario).

### Tipos reales a tocar
- `services/anomalies/monitoringConfig/types.ts` → `AnomalyMonitoringConfig` (`kpi_configs[].thresholds[] {operator, value, series_value}`, `days_of_week`, `granularity`, `series_column_ids`).
- `services/anomalies/badsProxy/types.ts` → `BaselinePreviewResult` / `KpiBaselineResponse` (`baseline` + `KpiNarrative`).
- `services/dashboards/notificationConfig/types.ts` → `NotificationConfig` (email/slack/in-app + locale).

### Notas de implementación
- **Sin react-hook-form**: estado con `useState` + hooks (`useScheduleForm`, `useThresholdRules`, `useNotificationsForm`) o el patrón section-descriptor (`useMonitoringConfigForm`); validación manual + Zod en el payload al guardar.
- Usar los **wrappers `Solutions*`** (portal) por el Shadow DOM del OC Box.
- **i18n**: crear namespace + `handle.i18nNs` + `locales/{es,en,pt}`.
- **Severidad** sigue system-assigned; la simulación de total no la discrimina (consistente con la UI nueva).

### Preguntas abiertas para BE / producto
1. **Conteo de simulación** (total de disparos por config sobre la ventana) — ¿lo expone BADS?
2. Mapeo de **nivel adaptativo** (Alta/Media/Baja) → parámetro real del detector.
3. **Sugeridos por serie** desde baseline (`p5`/`p95`) — ¿por serie o solo agregado?
4. ¿El override adaptativo **por serie** se permite, o se restringe a límites duros? (Splunk lo prohíbe; ver §10/§11.)
