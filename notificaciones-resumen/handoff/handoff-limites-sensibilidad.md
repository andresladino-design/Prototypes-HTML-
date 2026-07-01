# Handoff — Sensibilidad y Límites del gráfico (slider + severidad por bandas)

Fecha: 2026-06-26
Origen: `notificaciones-resumen/index.html` → paso **Series y valores** del diálogo de monitoreo (prototipo validado). Bloques: gráfica `#sens-chart` + editor de límites contextual `#cat-limits` + slider `.sens-card` + grilla `#series-block` (POR SERIE).
Registro: **Interno (Operation Center)** — operador Simetrik calibrando cómo el monitoreo evalúa un gráfico (KPI "Conteo De Registros", COUNT_DISTINCT).
Patrón de presentación: **Centro de control vertical** — gráfica con selector de categoría → límites de esa categoría → slider de sensibilidad → grilla de todas las series.

> **Reescrito el 26-jun:** este handoff reemplaza el modelo anterior (segmented Nula/Media/Alta + franja azul). El rediseño (sesión 25-jun, 4:42 PM) unifica **severidad = sensibilidad** y cambia el control a un **slider continuo**.

> **Actualización 30-jun (pm) — design review con ingeniería:**
> - **Título de la sección** (`#sens-title`): **"Sensibilidad de detección"** (antes solo "Sensibilidad"; la palabra sola no comunicaba el espectro umbral↔adaptativo).
> - **Reencuadre de los extremos del slider.** "Nula" confundía (se leía como "mutear el sistema"). Escala nueva: izq **"Solo mi umbral"** · centro **"Media"** · der **"Detección adaptativa"**. El copy contextual (`#sens-sub`) explica el espectro: izq = *alerta de umbral fija, solo avisa cuando el valor sale de tus límites, el sistema no agrega nada*; der = *el sistema decide qué es anómalo según el patrón histórico, sin esperar al límite; no marca todo, solo lo inusual*.
> - **Valor sugerido en los límites de categoría** (`#catlim-lower`/`#catlim-upper`): muestran "Valor sugerido: X" (clic para aplicar), se ocultan cuando el valor ya coincide (comentario Ohana).
> - **Fix de la representación al 100%.** La banda de atención antes llegaba al **centro** (`mark = semi·(1−frac)` → 0 en 100%), dando la idea de que "cualquier punto se notifica". Ahora se conserva un **núcleo normal** (`CORE = 0.30`): `mark = semi·(1 − frac·(1−CORE))`, mínimo `semi·0.30`. Aun al máximo queda una franja central sin marcar — coherente con que la detección adaptativa no marca todo punto. Verificable en el mini-dashboard de impacto (al 100% siguen quedando puntos normales).
> - El glosario de cara al usuario **no usa "nula"**.

> **Actualización de layout (26-jun pm):**
> - **Gráfica + impacto + límites + sensibilidad en UNA sola card** (`.tm-dialog-preview-card`, blanca con borde), separadas por **divisores**. El bloque de límites+sensibilidad (`.cat-config-box`) es ahora una **sección inferior** de esa card, no una card aparte. Razón: lo que se edita en límites/sensibilidad **impacta la gráfica de arriba**, así que se leen como una unidad.
> - **Impacto = mini-dashboard** (no la frase de antes): bajo la gráfica, un caption + **3 tiles** (avisos / urgentes / de atención) con números grandes que cambian al mover el slider. Reemplaza el footer `.sens-impact`.
> - **Sensibilidad** dentro de la sección va en **card gris suave** (`muted/0.5`, sin borde); los **límites** quedan sobre el blanco de la card.
> - **Header de límites = "Límites de {nombre de la métrica}"** (dinámico; toma `#dlg-content-title`, o el nombre de la serie al enfocar), con el **mismo estilo** que el título de la gráfica (13.5px/500/#1F1B2E, sin uppercase) — ya no el textito en mayúsculas.

---

## 1. Contexto y objetivo

Define **qué tan grave** es cada desviación de un gráfico y **qué la dispara**, con un modelo de **dos bandas** (severidad = sensibilidad, son lo mismo):

| Banda | La define | Severidad | Color |
|---|---|---|---|
| **Exterior (dura)** | Los **límites** del usuario (mín/máx) | `URGENT` | Rojo |
| **Interior (atención)** | La **sensibilidad** (qué tan adentro del límite empieza a importar) | `REQUIRES_ATTENTION` | Amarillo |

- Lo que **supera el límite** → siempre rojo / urgente.
- Lo que cae en la **banda amarilla interior** → de atención.
- La sensibilidad es un **multiplicador del límite**: el slider cierra la banda amarilla desde los bordes hacia el centro. `0%` → no hay amarillo (solo el límite duro). `100%` → todo el interior es amarillo.

Todo opera **por categoría**: el KPI agregado ("Todas las categorías") y cada serie (fuente). El selector de la gráfica manda: al elegir una categoría, debajo aparecen **sus** límites + **su** slider y la gráfica muestra **su** serie.

Objetivo: que el operador calibre el monitoreo con una sola perilla continua entendiendo, con un dato real, cuántas veces le habríamos avisado (y de qué severidad) en la ventana histórica.

## 2. Usuario y registro

- **Registro:** Interno / Op Center. Power user recurrente, alta tolerancia a densidad.
- **Modo de uso:** ajuste fino por KPI; compara el efecto de mover la perilla contra el histórico antes de guardar.
- **Dato clave al primer vistazo:** ¿cuántas señales generaría esta config y de qué severidad?

## 3. Historias de usuario

**HU-1 — Graduar la sensibilidad con una perilla continua y ver su impacto**
> Como operador, quiero mover un slider de sensibilidad y ver en vivo, sobre la gráfica y con un dato real, cuántas señales urgentes y de atención generaría, para calibrar sin recibir ruido ni perderme desviaciones.
- **Slider continuo 0–100%** (escala Nula · Media · Alta) con readout de %. Reemplaza el segmented de 3 opciones.
- Al moverlo: la **banda amarilla** crece/se cierra hacia el centro, los puntos se re-clasifican y el **mini-dashboard de impacto** se recalcula.
- **Mini-dashboard de impacto** (debajo de la gráfica, no en el footer del slider): caption `Con esta sensibilidad, en los últimos 30 días habrías recibido:` + **3 tiles** con número grande — **avisos en total** · **urgentes** (rojo) · **de atención** (ámbar). Los números cambian en vivo al mover el slider (mucho más legible que la frase anterior). _Insight de la sesión 26-jun: el impacto enterrado en una frase no se leía como "lo que estoy configurando"._

**HU-2 — Definir los límites duros (banda roja) por bound, activables**
> Como operador, quiero fijar el límite inferior y superior, activarlos/desactivarlos por separado, para monitorear solo los bordes que importan.
- Dos inputs (inferior / superior) + **checkbox on/off** por bound. Al apagar uno: input atenuado e inerte (conserva valor) y **ese lado del gráfico desaparece** — se quitan su zona roja, su banda amarilla, su línea de límite y su umbral; los puntos de ese lado dejan de marcarse.
- Editar un input **redibuja la banda roja** de la gráfica en vivo. El monitoreo propone un **valor sugerido** (hint).

**HU-3 — Ajustar todo por categoría sin perder el contexto del gráfico (centro de control)**
> Como operador, quiero que al elegir una categoría en el selector de la gráfica, debajo aparezcan sus límites y su sensibilidad, sin tener que hacer scroll y perder la gráfica.
- El **selector de categoría** (sobre la gráfica) manda: cambia la serie graficada, el editor de límites y el slider, todo en su sitio.
- Cada categoría **recuerda su propia sensibilidad y límites**. Herencia: una serie sin ajuste propio **usa el % del global** ("Todas"); al moverla, queda como override.

**HU-4 — Graduar la sensibilidad de cada serie sin entrar a cada una**
> Como operador, quiero ajustar la sensibilidad de varias series de un vistazo desde la lista.
- En la grilla **POR SERIE** (visible solo en "Todas las categorías"), cada fila tiene un **pill de %** que abre un **mini-slider en popover**. Mover = override de esa serie. El pill muestra el % efectivo y marca si **hereda** el global.

**HU-5 — Enfocar una serie y volver**
> Como operador, quiero saltar al detalle de una serie desde la lista, y tener una salida clara para volver.
- Cada fila tiene un **botón de acceso rápido** (ícono `maximize-2`) que enfoca esa serie: la gráfica + límites + slider cambian a ella y la grilla se oculta.
- **Volver (chip con ✕):** al enfocar una serie, el selector de la gráfica la muestra como chip con una **✕** (oculta el chevron). Clic en la ✕ → vuelve a "Todas las categorías" (reaparece la grilla) sin abrir el menú. El botón sigue abriendo el menú para saltar directo a otra serie.

## 4. Arquitectura de componentes desyk

| Mock (prototipo) | Componente desyk | Notas |
|---|---|---|
| `#sens-chart` (SVG render JS) | gráfico custom (SVG) | dibuja zonas rojo/amarillo, líneas de límite y umbral, serie y puntos clasificados |
| `.cat-select` / `.cat-menu` | `Select` / `DropdownMenu` | selector de categoría sobre la gráfica; "Todas las categorías" + una opción por serie, con check en la activa. Con una serie enfocada muestra un **chip con ✕** (`.cat-clear`) para volver a "Todas" |
| `.sens-slider` (`input[range]`) | `Slider` | 0–100, continuo; pista ámbar; thumb con borde `--primary` |
| `.sens-row` + `.sens-pct` | row de control | ícono `gauge` + título/sub dinámico + readout `%` a la derecha; dentro de la **card gris** (`muted/0.5`) de sensibilidad |
| `.sens-kpi-wrap` / `.sens-kpi` (×3) | mini-dashboard (stat tiles) | caption + 3 tiles (avisos / urgentes / de atención); número 17px; vive **debajo de la gráfica**, dentro de la card de comportamiento. Reemplaza `.sens-impact` |
| `.tm-dialog-preview-card` (contenedor) | `Card` (blanca, borde) | **una sola card** que envuelve: gráfica → mini-dashboard → (divisor) límites → (divisor) sensibilidad gris |
| `.cat-config-box` | sección dentro de la card | límites + sensibilidad como sección inferior, separada de la gráfica por `border-top`. No es card propia |
| `#cat-limits` (`.tm-limits-block`) | bloque de campos | editor de límites; **header = "Límites de {métrica/serie}"** con estilo de título (13.5/500), no uppercase |
| `.tm-limit-field` + `.tm-limit-check` | `Checkbox` + grupo de campo | on/off por bound; `is-off` atenúa el input |
| `.tm-limit-input` | `Input` (numérico, `tabular-nums`) | edita el límite; redibuja la banda en vivo |
| `#series-block` / `.tm-series-grid` | grid (table-like) | POR SERIE; visible **solo en "Todas"** |
| `.tm-series-sens` (pill + popover) | `Button` + `Popover` + `Slider` | sensibilidad por serie inline; pill muestra % efectivo / "hereda" |
| `.tm-series-focus` | `IconButton` (`maximize-2`) | enfoca la serie |
| `.tm-series-del` | `IconButton` (`trash-2`) | quita la serie del override por-serie |

**Modelo de datos (fuente única en el prototipo, `DS_AN_CATS`):**

```
type Category = {
  id: string                  // 'all' | resource_id
  name: string                // 'Todas las categorías' | 'Banco_Occidente' | ...
  isAggregate?: boolean
  values: number[]            // serie de la ventana (del BE)
  lower: number; upper: number
  lowerOn: boolean; upperOn: boolean   // on/off por bound (off → extiende al extremo de datos)
  sens?: number               // 0..100; undefined = hereda el global ("all")
}
```

**Lógica clave (del prototipo):**
- `mark = semiAncho * (1 - frac)` donde `frac = sens/100`. Anomalía: `|v - centro| > semiAncho` → **rojo**; `mark < |v - centro| ≤ semiAncho` → **amarillo**.
- `sensPctFor(cat)` = `cat.sens` si existe, si no el `sens` del global, si no 50 (herencia).
- Bound off (`lowerOn`/`upperOn` = false) → ese lado **no se dibuja** (sin zona/línea/umbral) y sus puntos no se clasifican. El eje Y se ajusta a los datos + solo los límites activos.
- **Borde suave:** sobre cada línea de límite activa con banda amarilla, una franja de gradiente (~16px) funde rojo↔amarillo (`<linearGradient>` con stops por tokens).
- **Ejes:** valores en Y (ticks redondos + gridlines punteadas) y fechas rotadas en X, 1:1 con los puntos.
- El selector, el editor de límites, el slider, la grilla y la gráfica **leen/escriben el mismo modelo** (siempre sincronizados).

## 5. Estados

- **Loading:** skeleton de la gráfica + editor de límites + slider (no spinner).
- **Inicial:** categoría = "Todas las categorías", slider 50%, ambos límites activos con valor sugerido, grilla POR SERIE visible.
- **Categoría = serie:** gráfica/límites/slider de esa serie; **grilla oculta**; el selector muestra chip con ✕ para volver.
- **Serie heredando global:** el pill de % va atenuado ("hereda"); el popover dice "Hereda el global. Mover para personalizar."
- **Bound apagado:** input atenuado e inerte (conserva valor); ese lado de la banda desaparece.
- **Error de validación:** valor no numérico / inferior ≥ superior → borde `destructive` + microcopy.

## 6. Copy completo (glosario aplicado)

> Glosario Op Center: **monitoreo** (no "agente"/"Agente IA"), **incidente**, **señal**, **KPI**, **Tablero**. Severidades = enums del sistema (`URGENT` / `REQUIRES_ATTENTION`); en copy de usuario: "urgente" / "de atención".

**Gráfica**
- Título: `Comportamiento del KPI · últimos 30 días`
- Leyenda: `Fuera de límites · urgente` (rojo) · `Zona de atención · medio` (amarillo)

**Mini-dashboard de impacto** (debajo de la gráfica)
- Caption: `Con esta sensibilidad, en los últimos 30 días habrías recibido:`
- Tiles: `{N}` `avisos en total` · `{X}` `urgentes` (rojo) · `{Y}` `de atención` (ámbar)

**Sensibilidad** (slider, en card gris)
- Título: `Sensibilidad` · readout `{pct}%`
- Sub (por rango): `0%` → `Funciona como umbral fijo: solo avisa cuando el valor supera el límite que definiste.` · `1–66%` → `Avisa al acercarse al límite, pasado un umbral intermedio.` · `67–100%` → `Avisa ante cualquier desviación inusual, sin esperar al límite.`
- Escala: `Nula` · `Media` · `Alta`

**Límites**
- Header (dinámico): `Límites de {nombre de la métrica}` en agregado (toma `#dlg-content-title`, p. ej. `Límites de Conteo De Registros`); al enfocar una serie, `Límites de {serie}` (p. ej. `Límites de Banco_Occidente`)
- Labels: `Límite inferior` · `Límite superior`
- Hint sugerido (global): `Valor sugerido: <N>`

**Pill de sensibilidad por serie**
- Pill: `{pct}%`
- Popover: título `Sensibilidad`, valor `{pct}%`, pie `Hereda el global. Mover para personalizar.` / `Personalizada para esta serie.`

## 7. Microinteracciones

| Interacción | Detalle |
|---|---|
| Mover slider | re-render de bandas + puntos + contador en vivo |
| Cambiar categoría (selector) | gráfica, límites y slider cambian a la categoría; grilla muestra/oculta |
| Apagar bound | input → `opacity .45` + inerte, transición `120ms`; banda redibuja |
| Editar límite | banda roja redibuja en vivo; sincroniza la fila de la grilla |
| Abrir pill de serie | popover con mini-slider (`200ms ease-out`); cierra al clic fuera |
| Enfocar serie | gráfica/límites/slider cambian a la serie; grilla se oculta |

Durations canónicas: 120 / 200 / 320 ms ease-out. Sin spinners; skeleton.

## 8. AI integration

- El **valor sugerido** de cada límite y la **serie/ventana** los provee el monitoreo (BADS). La UI deja claro que el sugerido viene del monitoreo (hint), y el override es manual.
- La **sensibilidad** modula qué tan adentro del límite el monitoreo llama "de atención". No badges "AI", no sparkles.
- Empty/contexto: el bloque "Análisis inteligente" (paso Fuente) resume la línea base del agregado. (Se evaluó mostrar una narrativa por serie al enfocar y se descartó: no va en esta versión.)

## 9. Endpoints esperados

`GET /monitoring/{chartId}/sensitivity` →
```json
{
  "windowDays": 30,
  "categories": [
    {
      "id": "all", "name": "Todas las categorías", "isAggregate": true,
      "sensitivity": 50,
      "limits": {
        "lower": { "value": 1, "enabled": true, "suggested": 25.20 },
        "upper": { "value": 20, "enabled": true, "suggested": 79.00 }
      },
      "series": [ { "t": "2026-04-01", "value": 12 }, "… ventana" ],
      "signals": { "urgent": 6, "attention": 2 }
    },
    {
      "id": "79008", "name": "Banco_Occidente",
      "sensitivity": null,
      "limits": { "lower": { "value": 8.4, "enabled": true }, "upper": { "value": 25, "enabled": true } },
      "series": [ "… " ]
    }
  ]
}
```
`PUT /monitoring/{chartId}/sensitivity` con el shape de config (por categoría: `sensitivity` + `limits` con on/off). `series`, `signals` y `suggested` son **read-only** (los provee el monitoreo / BE).

> **Severidad derivada de las bandas (no campo aparte):** dado `limits` + `sensitivity` por categoría, el BE clasifica cada punto de la ventana: fuera del límite → `URGENT`; dentro de la banda de atención → `REQUIRES_ATTENTION`. `signals.urgent/attention` alimentan el contador. `sensitivity: null` ⇒ heredar el global.
> **Misma ventana** para serie, conteo y marcado (30 días) — evita el desfase histórico 7d/30d.

## 10. Edge cases y validaciones

- Valor no numérico o vacío con bound activo → error, bloquea guardar.
- `lower >= upper` (ambos activos) → error de coherencia.
- Ambos bounds apagados → permitido (sin banda roja); con sensibilidad 0% no hay monitoreo efectivo: advertir al guardar.
- Recalcular `suggested` (nuevo aprendizaje) con override activo → mantener override; actualizar el sugerido mostrado.
- Serie con `sensitivity: null` → muestra el % heredado; al editar pasa a override.
- Muchas series → la grilla hace scroll; el popover del pill no debe quedar cortado (abrir hacia arriba en las últimas filas — pendiente).

## 11. Test cases sugeridos

1. Mover el slider re-clasifica puntos (rojo/amarillo) y actualiza el contador `N — X urgentes · Y de atención` en vivo.
2. Editar un límite redibuja la banda roja y sincroniza la fila de la grilla; y viceversa.
3. Apagar un bound atenúa el input, lo vuelve inerte, conserva valor y **quita ese lado del gráfico** (zona, línea, umbral, marcado).
4. Cambiar de categoría en el selector mueve gráfica + límites + slider y muestra/oculta la grilla.
5. Cada categoría recuerda su % y límites; una serie sin override hereda el global.
6. El pill de % por serie abre el popover; mover el mini-slider personaliza esa serie (deja de "heredar").
7. El botón de foco enfoca la serie (grilla oculta); el selector muestra chip con ✕ y al hacer clic vuelve a "Todas" (grilla visible) sin abrir el menú.
8. `lower >= upper` con ambos activos dispara error de coherencia.

## 12. Tokens utilizados

`--primary` (thumb del slider, foco input, check de categoría) · `--primary-text` (readout %, pill) · `--warning` (banda amarilla, pista del slider, severidad media) · `--destructive` (banda roja, línea de límite, severidad urgente) · `--border-default` (inputs, cards, popover) · `muted-foreground` (labels, escala) · `text-primary`. Radius: `9–11px` inputs/cards, `8px` botones, `999px` slider/thumb.

## 13. Checklist pre-PR

- [ ] Slider continuo (`Slider` desyk) reemplaza el segmented; escala Nula/Media/Alta + readout %
- [ ] Coloreado invertido: rojo = fuera de límites · amarillo = zona de atención (anillo interior)
- [ ] Severidad derivada de las bandas (urgente / de atención), no de un campo suelto
- [ ] Selector de categoría manda: gráfica + límites + slider + visibilidad de grilla
- [ ] Sensibilidad y límites **por categoría** con herencia del global
- [ ] Pill de % + popover por serie en la grilla (visible solo en "Todas")
- [ ] Botón de foco por serie; grilla oculta al enfocar; **chip con ✕ en el selector para volver a "Todas"**
- [ ] Límites con on/off por bound; off → **se quita ese lado del gráfico** (zona/línea/umbral/marcado)
- [x] Borde suave (gradiente rojo↔amarillo) sobre cada límite activo con banda amarilla
- [x] Ejes: valores en Y (+ gridlines) y fechas rotadas en X
- [ ] **Impacto = mini-dashboard** (3 tiles: avisos / urgentes / de atención) debajo de la gráfica, números en vivo — reemplaza el footer `.sens-impact`
- [ ] **Una sola card** envuelve gráfica + impacto + límites + sensibilidad, separadas por divisores; sensibilidad en **card gris** (`muted/0.5`)
- [ ] Header de límites = **"Límites de {métrica/serie}"** (dinámico), con estilo de título (no uppercase)
- [ ] Glosario: "monitoreo" (no "agente"), "incidente", "señal", "KPI"
- [ ] Microinteracciones 120/200/320 ms ease-out · light mode · A11y (labels, foco, contraste AA)
- [ ] Pendiente: que el popover del pill no se corte en las últimas filas; **Fase 5** (límites como % relativos). Nota: la **narrativa por serie** se probó y se descartó (no va en esta versión).
