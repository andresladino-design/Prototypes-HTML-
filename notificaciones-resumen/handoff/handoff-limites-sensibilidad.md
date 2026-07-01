# Handoff — Detección de anomalías por serie (límites fijos vs. sistema adaptativo)

Fecha: 2026-07-01
Origen: `notificaciones-resumen/index.html` → paso **Series y valores** del diálogo de monitoreo (KPI "Conteo De Registros", COUNT_DISTINCT). Bloque `#nsWrap` (clases `ns-*`, estado `NS_*` en JS).
Registro: **Interno (Operation Center)** — operador Simetrik configurando cómo el monitoreo detecta anomalías de un gráfico.
Patrón de presentación: **colapsables inline** con modelo **configuración general + override por serie**.

> **Reescrito completo el 1-jul-2026.** Este handoff reemplaza el modelo anterior (slider de sensibilidad 0–100 + severidad por dos bandas + grilla "POR SERIE" + selector de categoría sobre la gráfica). Origen del rediseño: Granola 1-jul "Configuración de alertas — límites vs. sensibilidad adaptativa" y "…diseño de interfaz con collapsables", + investigación de patrones (ver §11) + iteración validada en prototipo. El modelo viejo (`.sens-*`, `.cat-*`, `.tm-series-*`, `.tm-dialog-preview-card`) quedó **deprecado**.

---

## 1. Contexto y objetivo

Un gráfico/KPI se descompone en varias **series** (por fuente: Banco_Occidente, PayU_Latam, ERP_SAP…). El operador define **cómo se detecta una anomalía** en cada serie. Ya no es "una perilla de sensibilidad": es una pregunta explícita con dos caminos.

**Pregunta rectora (por serie y por defecto):** *¿Cómo quieres detectar las anomalías?*

| Modo | Qué hace | Controles |
|---|---|---|
| **Límites fijos** | Tú defines el mínimo y el máximo válidos; avisa si el valor sale de ahí | inputs mín/máx (activables por bound) + valor sugerido |
| **Sistema adaptativo** | Simetrik aprende el comportamiento normal y avisa de lo inusual | nivel de sensibilidad (Alta/Media/Baja) + opción "Agregar límites de seguridad" |

**Modelo de configuración = general + override:**
- **Límites generales de {métrica}** (card "Todas las categorías"): la configuración **base** que heredan todas las series.
- **Límites por serie**: cada serie hereda la base hasta que la configuras; al editarla queda con su propia config. Una serie recién agregada entra **"Sin configurar"**.

Objetivo: que el operador entienda **qué gana con cada modo** y vea, con un dato real (simulación sobre el histórico), cuántos avisos generaría — sin caja negra: input → output visible en la gráfica y en los números.

## 2. Usuario y registro

- **Registro:** Interno / Op Center. Power user, alta tolerancia a densidad, uso recurrente.
- **Modo de uso:** configurar el KPI una vez (config general) y personalizar solo las series que lo ameriten.
- **Dato clave al primer vistazo:** de cada serie, **cómo está detectando** (badge de modo) y **cuántos avisos** daría.
- **Primera versión = evangelizar:** hay que enseñar el modelo mental (adaptativo vs fijo). Por eso la config es explicativa, no una tabla densa. La vista súper-colapsada a tabla queda para una iteración futura (usuarios expertos).

## 3. Estructura de la vista (`#nsWrap`)

```
Límites generales de Conteo De Registros            ← encabezado de sección
  ▸ [layers] Todas las categorías  [Sistema adaptativo] sens. media   ← colapsable (config base)

Límites por serie                        [ 6 de 6 series ]  ← encabezado + badge outline (contador)
  ▸ Banco_Occidente   [Sistema adaptativo] sens. media          🗑
  ▸ PayU_Latam        [Límites fijos] mín 2 · máx 9             🗑
  ▸ ERP_SAP           [Sin configurar]                          🗑
  … (una fila por serie)
  [ + Agregar serie ]                    ← solo si quedan series en el catálogo
```

- **Colapsables inline, una abierta a la vez** (abrir una cierra las demás; global y series comparten esa regla).
- Al abrir una fila, se despliega **la card de configuración** (§5) inline.
- El **badge de cada fila** refleja el modo efectivo: `Sistema adaptativo` (azul), `Límites fijos` (ámbar) o `Sin configurar` (outline punteado). Al lado, un resumen: sensibilidad (adaptativo) o rango mín/máx (fijo).

## 4. Agregar / quitar series

- **Catálogo fijo** de N series (en el prototipo, 6). El contador ("Límites por serie") es un **badge outline**: `{activas} de {total} series`.
- **Quitar** (🗑 por fila): saca la serie del monitoreo; vuelve al catálogo disponible. Sin límite mínimo (se pueden quitar todas).
- **Agregar** (botón `+ Agregar serie`, dashed): aparece **solo si hay series disponibles**; abre un menú con las no agregadas. Si están todas, el botón no aparece.
- Al agregar, la serie entra **"Sin configurar"** y **se abre automáticamente** para configurarla. Queda "Sin configurar" hasta que el usuario elige un modo (cualquier edición la marca configurada).

## 5. La card de configuración (global y por serie, mismo template)

Orden de la información (de arriba a abajo):

1. **Gráfica · últimos 30 días** (título pequeño + leyenda). **Se muestra completa** (histórico), sin marca "AHORA" ni tramo proyectado.
   - **Por serie:** línea del valor + **banda "rango esperado"** (solo en modo adaptativo) + **líneas de límite fijo** (en modo fijo, o si hay límites de seguridad).
   - **Global ("Todas las categorías"):** **todas las series superpuestas** (líneas tenues) — comunica que es el agregado. No dibuja banda (series de distinta escala); sí las líneas de límite si aplica.
2. **Pregunta:** `¿Cómo quieres detectar las anomalías (por defecto / de esta serie)?` → dos radios: **Límites fijos** / **Sistema adaptativo**.
3. **Panel según el modo:**
   - *Límites fijos:* grid de **Límite inferior / superior**, cada uno con **checkbox** (incluir ese bound) + input numérico + **chip azul "Valor sugerido: N"** (clic para aplicar; se oculta si el valor ya coincide).
   - *Sistema adaptativo:* segmented **Alta / Media (recomendada) / Baja** + checkbox **"Agregar límites de seguridad"** que revela el mismo grid de límites (mín/máx que avisan sí o sí).
4. **Caja de resultado (blanca, unificada)** — antes eran dos bloques, ahora uno:
   - Texto contextual: `Te avisamos cuando la serie se comporte distinto a lo habitual (sensibilidad media). Se ajusta solo.` (varía por modo/seguridad).
   - Separador sutil.
   - **Simulación** (3 números inline): `avisos en total` · `fuera de límites` (rojo) · `comportamiento inusual` (ámbar). Se recalcula en vivo.

> La caja de resultado ya **no** lleva el caption "Con esta configuración… habrías recibido" ni fondo azul: el texto del aviso hace de introducción y los números van debajo, en fondo blanco.

## 6. Arquitectura de componentes / clases

| Mock (prototipo) | Componente desyk | Notas |
|---|---|---|
| `#nsWrap` | contenedor de la sección | render por JS (`nsInit` → `nsRenderList`) |
| `.ns-secth` + `#nsCnt` | encabezado de sección + `Badge` outline | "Límites generales de {métrica}" · "Límites por serie" `{n de N series}`. **Sin mayúsculas sostenidas.** |
| `.ns-acc` / `.ns-acc-item` / `.ns-acc-hd` / `.ns-acc-body` | `Accordion` | colapsable; una abierta a la vez (`nsToggle`) |
| `.ns-acc-item.ns-gl` | item destacado | la card "Todas las categorías" (fondo tenue) |
| `.ns-acc-toprow` + `.ns-acc-del` | fila + `IconButton` (`trash-2`) | quitar serie (`nsRemoveSeries`) |
| `.ns-badge` (`.adapt` / `.fijo` / `.unset`) | `Badge` | modo de detección o "Sin configurar" |
| `.ns-addwrap` / `.ns-add-btn` / `.ns-add-menu` | `Button` (dashed) + `DropdownMenu` | agregar serie (`nsAddSeries`) |
| `.ns-radio` (×2) | `RadioCard` | Límites fijos / Sistema adaptativo (`nsSetMode`) |
| `.ns-seg` | `SegmentedControl` | Alta / Media / Baja (`nsSetLevel`) |
| `.ns-check` | `Checkbox` | "Agregar límites de seguridad" (`nsToggleSafety`) |
| `.ns-lim` (grid) | `Checkbox` + `Input` numérico | bound on/off (`nsSetBoundOn`) + valor (`nsSetLim`) |
| `.ns-limsug` | `Chip` (clic) | valor sugerido (`nsApplySug`); se oculta si ya coincide |
| `svg.ns-chart` | gráfico custom (SVG) | render `nsDraw`; línea/banda/límites, sin AHORA |
| `.ns-alert` (+ `.ns-alert-body` / `.ns-impact-row`) | `Card` neutra | aviso contextual + simulación, en **fondo blanco** |

**Modelo de datos (fuente única en el prototipo):**

```
NS_GLOBAL = { mode:'adaptativo'|'fijo', level:'alta'|'media'|'baja', safety:bool,
              fixedLo, fixedHi, loOn, hiOn, sug:{lo,hi} }        // config base
NS_SERIES[] = { id, name, data:number[], sug:{lo,hi},
                active:bool,        // está en el monitoreo (agregada)
                configured:bool,    // false = "Sin configurar"
                customized:bool,    // false = hereda NS_GLOBAL
                cfg:{...} }         // su config propia cuando customized
```

**Lógica clave:**
- **Herencia:** una serie con `customized=false` muestra/usa `NS_GLOBAL` (`nsView`). La primera edición la "forkea" (`nsBeforeEdit`: copia el global y marca `customized=true` + `configured=true`).
- **Sin configurar:** `configured=false` → badge "Sin configurar", sin resumen; no cuenta en la simulación agregada del global.
- **Simulación:** por serie, sobre TODA la ventana (ya no hay corte "AHORA"). Adaptativo: outlier si `|v − baseline| > margen(nivel)`; fijo/seguridad: fuera de `[lo,hi]` activos. El global agrega los conteos de las series configuradas, cada una con su propio baseline.
- Todo (badges, resúmenes, gráfica, simulación) se re-renderiza desde el mismo estado.

## 7. Estados

- **Inicial:** "Todas las categorías" adaptativo/media; las series iniciales configuradas (heredando); contador `N de N`.
- **Serie heredando:** badge del modo del global; al editar pasa a personalizada.
- **Serie sin configurar:** badge outline "Sin configurar"; al abrir muestra la card (preview con la base) para configurarla.
- **Global expandido:** todas las series superpuestas + simulación agregada + explicación de que es la base.
- **Bound apagado:** input atenuado e inerte (conserva valor); ese límite no marca ni se dibuja.
- **Sin series disponibles:** el botón "Agregar serie" no aparece. **Todas quitadas:** lista vacía, botón muestra las N.
- **Validación:** valor no numérico / `lower ≥ upper` con ambos activos → error + microcopy (pendiente de cablear en el prototipo).

## 8. Copy (glosario aplicado)

> Glosario Op Center: **monitoreo** (no "agente"/"Agente IA"), **incidente**, **señal**, **KPI**, **Tablero**. Sin em-dashes. Sin mayúsculas sostenidas en títulos.

- Encabezados: `Límites generales de {métrica}` · `Límites por serie` + badge `{n} de {N} series`.
- Card "Todas las categorías": badge de modo + resumen. Gráfica: `Todas las categorías · últimos 30 días`, leyenda `Series` (+ `Límite fijo` si aplica).
- Pregunta: `¿Cómo quieres detectar las anomalías (por defecto)?` (global) / `…de esta serie?` (serie).
- Radios: **Límites fijos** — `Tú defines el mínimo y el máximo válidos.` · **Sistema adaptativo** — `Simetrik aprende lo normal y avisa de lo inusual.`
- Sensibilidad: `Alta` (`Detecta hasta cambios chicos`) · `Media` (`Recomendada`) · `Baja` (`Solo lo muy fuera de lo normal`).
- Seguridad: `Agregar límites de seguridad` — `Un mínimo/máximo que avisa sí o sí, aunque el sistema lo vea normal. Para valores que jamás deberían pasar.`
- Límites: `Límite inferior` / `Límite superior` · chip `Valor sugerido: N`.
- Aviso (por modo):
  - fijo: `Te avisamos solo cuando la serie se salga del rango que definiste. Predecible y bajo tu control.`
  - adaptativo: `Te avisamos cuando la serie se comporte distinto a lo habitual (sensibilidad {nivel}). Se ajusta solo.`
  - adaptativo + seguridad: `…y siempre que cruce tus límites de seguridad.`
  - (global: "cada serie" en vez de "la serie").
- Simulación: `{N} avisos en total` · `{X} fuera de límites` · `{Y} comportamiento inusual`.

## 9. Microinteracciones

| Interacción | Detalle |
|---|---|
| Abrir colapsable | cierra los demás; despliega la card; render de gráfica + simulación |
| Elegir modo / nivel / seguridad | re-render de panel, gráfica, aviso y simulación en vivo |
| Editar límite / toggle bound | redibuja banda/línea y recalcula simulación; chip sugerido se muestra/oculta |
| Agregar serie | entra "Sin configurar" y se abre automáticamente |
| Quitar serie | sale de la lista; actualiza contador y botón de agregar |

Durations canónicas: 120 / 200 / 320 ms ease-out. Sin spinners; skeleton. Light mode.

## 10. Mapeo BADS / preguntas para ingeniería

- **Sistema adaptativo** → detección de patrón de BADS (`TRIGGER` / `TRAJECTORY` / `NEW_SERIES`). El **nivel** (Alta/Media/Baja) debe mapear a un parámetro real del detector (ancho de banda / umbral) → **confirmar valores por nivel con BE**.
- **Límites fijos** y **límites de seguridad** → umbral duro del usuario (condición adicional OR sobre el adaptativo). Coincide con el modelo Anodot (adaptativo + hard limit apilados).
- **Severidad** (`URGENT` / `REQUIRES_ATTENTION`) sigue siendo **system-assigned** (no la elige el usuario). Confirmar si el modo/nivel influye.
- **Banda "rango esperado"** dibujada y **simulación** ("habrías recibido N") requieren que el BE devuelva la banda + el conteo por config sobre la ventana → hoy **mockeado**.
- **Herencia:** una serie sin config propia hereda la general; el override por-serie con adaptativo es poco común en la industria (Splunk lo prohíbe) — si se restringe, el override por serie podría limitarse a **límites duros**. Decisión de producto pendiente.

**Endpoint esperado (borrador):** `GET/PUT /monitoring/{chartId}/detection` con `general` (config base) + `series[]` (`{id, active, configured, override?}`); `data`, `band`, `suggested`, `signals` read-only del BE. Misma ventana (30 días) para serie, banda y conteo.

## 11. Investigación que respalda el diseño (1-jul)

- **Patrón dominante en monitoreo** (Datadog, New Relic, Dynatrace): una config declarativa + el motor instancia por serie automáticamente; override **por excepción**. La lista de series es de **inspección**, no de edición masiva inline.
- **Adaptativo + límite duro coexisten** como condiciones apilables (Anodot) → nuestro "sistema adaptativo + límites de seguridad".
- **UX (NN/g):** para editar config compleja de muchos ítems, evitar accordion "pesado"; se eligió **colapsables inline con una sola abierta** + **default global** (el default enseña el modelo mental) por ser lo más claro para una v1 que debe evangelizar.
- **Diferenciador de mercado:** simulación de impacto en vivo ("con esta config habrías recibido N"). Se mantiene.

## 12. Checklist pre-implementación

- [ ] Dos secciones tituladas (sin uppercase): **Límites generales de {métrica}** + **Límites por serie** (contador en badge outline).
- [ ] Colapsables inline, una abierta a la vez (global + series).
- [ ] Card de config compartida: gráfica completa (sin AHORA) → pregunta modo → panel (fijo/adaptativo) → caja blanca aviso+simulación.
- [ ] Modo **Límites fijos** (mín/máx con on/off por bound + valor sugerido en chip).
- [ ] Modo **Sistema adaptativo** (Alta/Media/Baja + "Agregar límites de seguridad").
- [ ] Card "Todas las categorías" = base heredable; gráfica con **todas las series superpuestas** + **simulación agregada** + explicación.
- [ ] Herencia general → serie; edición marca personalizada.
- [ ] Estado **"Sin configurar"** para series agregadas; agregar abre la card.
- [ ] **Agregar / quitar serie** (catálogo, botón dashed condicionado, papelera por fila).
- [ ] Aviso + simulación **unificados** en fondo blanco (sin caption redundante).
- [ ] Glosario ("monitoreo", no "agente"), sin em-dashes, tokens desyk, 120/200/320 ms, A11y AA.
- [ ] BE: banda + simulación + sugeridos + señales reales (hoy mockeados); mapeo de nivel → parámetro del detector.
