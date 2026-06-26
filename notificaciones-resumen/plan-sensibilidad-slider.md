# Plan — Rediseño de la UI de Sensibilidad (slider + severidad unificada)

Fecha: 2026-06-25
Origen: sesión Granola "Configuración de sensibilidad y umbrales de severidad — slider parametrizable y aplicación por serie" (25-jun, 4:42 PM) + capturas del estado actual del producto.
Archivo a evolucionar: `index.html` (sección `.sens-card` + `#sens-chart` + `.tm-limits-block` + por-serie). Doc relacionado: `handoff/handoff-limites-sensibilidad.md`.

> **Regla del repo:** este es el copy de cara al usuario — **no usar el concepto de "agente"/"Agente IA"**; usar "monitoreo" o voz pasiva.

---

## 1. Concepto central — severidad = sensibilidad

Hoy "severidad del incidente" (URGENT / REQUIRES_ATTENTION) y "sensibilidad" (Nula/Media/Alta) viven separadas, pero son la **misma idea**. Se unifican en un modelo de **dos bandas**:

| Banda | Qué la define | Severidad | Color |
|---|---|---|---|
| **Exterior (dura)** | Los **hard limits** del usuario (mín/máx) | **URGENT** | Rojo |
| **Interior (amarilla)** | La **sensibilidad** (qué tan adentro de los límites empieza a importar) | **REQUIRES_ATTENTION** | Amarillo |

- Lo que **supera el hard limit** → siempre **rojo / urgente**.
- Lo que cae en la **banda amarilla interior** → **medio / requires attention**.
- La pregunta de la sensibilidad es literal: *"¿te notifico sobre lo amarillo o no?"* — y el slider la responde de forma continua.

**La sensibilidad es un multiplicador de los hard limits:**
- Slider en **0** → banda amarilla nula; solo existe el hard limit rojo (= "sensibilidad nula" de hoy).
- Slider hacia la **derecha** → la banda amarilla **se cierra desde los bordes hacia el centro**; todo lo que cae en esa zona pasa a contar como medio (amarillo).

---

## 2. Decisiones de diseño (de la sesión)

1. **Switch (Nula/Media/Alta) → SLIDER continuo**, 100% parametrizable (ej. 0–100% o "80%", "50%"). Reemplaza el segmented de 3 opciones.
2. **Coloreado invertido en la gráfica:**
   - Hoy se sombrea la zona de **adentro** (banda rosa entre mín/máx).
   - Nuevo: zona de **afuera = ROJA** (anomalías urgentes, ahí caen los puntos rojos); al mover el slider, la zona **interior = AMARILLA** crece hacia el centro y captura puntos amarillos. **Gradiente** rojo↔amarillo.
3. **Slider ligado a la gráfica y a los límites** (no en contenedor aparte). Orden de interacción: **gráfico → límites → (abajo) slider de sensibilidad**. Nunca sensibilidad antes que límites.
4. **Por serie + global:** el slider aplica a nivel **global de la métrica** y **por serie**. Al cambiar de serie en la gráfica, el control viaja con ella (no perder el gráfico de contexto al hacer scroll).
5. **Dos tamaños del control:**
   - **Grande/explicativo** (con "en los últimos 30 días te habríamos avisado N veces") → solo para la **serie enfocada / principal**.
   - **Resumido** → dentro del bloque "Por serie".
6. **Foco/zoom en una serie:** poder entrar a una serie → oculta el resto, mueve la gráfica a esa serie, abre el slider grande y muestra la **narrativa específica de esa serie** (hoy solo se muestra la del Total).
7. **Contador conectado:** "habría disparado N veces (últimos 30 días)" se recalcula al mover el slider y distingue **rojo (urgente)** vs **amarillo (medio)**.
8. **Compatibilidad a futuro:** el diseño debe servir tanto para **hard limits absolutos** como para **% relativos** (ej. "subida >20% vs. los últimos 5–10 valores"). Por ahora se mantiene absoluto, sin cerrar la puerta a relativos.

---

## 3. Estado actual vs. objetivo (gaps de las capturas)

| # | Hoy | Falta para la nueva interacción |
|---|---|---|
| 1 | Inputs de límite + segmented Nula/Media/Alta | **Slider continuo** de sensibilidad |
| 2 | Banda sombreada **adentro** (rosa) | Coloreado **invertido**: afuera rojo / adentro amarillo + gradiente |
| 3 | Gráfica arriba, límites/POR SERIE abajo (scroll) | **Todo junto** ("centro de control"); el control viaja al cambiar de serie |
| 4 | POR SERIE = solo inputs mín/máx | **Slider por serie** (resumido) + global |
| 5 | Sin foco/zoom | **Entrar a una serie** → slider grande + narrativa de la serie |
| 6 | Narrativa solo del Total | **Narrativa por serie** al enfocar |
| 7 | Contador atado a "límites manuales" | Contador atado al **slider**, separando rojo vs amarillo |

Se conserva lo ya pulido: el **loader** de Análisis inteligente ("Pensando… → Consultando datos históricos → Calculando línea base" + borde con gradiente) y el bloque de límites sugeridos.

---

## 4. Plan de implementación (por fases)

> Cada fase es demoable de forma independiente. Orden pensado para mostrar valor temprano (el "momento ajá" del slider) antes de la reorganización estructural.

### Fase 1 — Slider + coloreado invertido (serie/global enfocada)
- Reemplazar el segmented `.bgroup` por un **slider continuo** (0–100%).
- Modelo: banda roja = hard limits (fija); banda amarilla = `semiAncho * sliderFrac` desde el borde hacia el centro.
- **Invertir el render del chart** (`#sens-chart` / `renderSensChart`): rojo afuera, amarillo adentro, gradiente entre ambos; puntos rojos (fuera del límite) y amarillos (en la banda media).
- Conectar el **contador** al slider, separando conteo rojo (urgente) vs amarillo (medio).
- Mantener "en los últimos 30 días te habríamos avisado N veces".

### Fase 2 — Centro de control (unir gráfica + límites + slider)
- Reorganizar el layout: **gráfica → límites → slider** en un solo bloque visualmente conectado.
- Al cambiar de serie en el dropdown de la gráfica, **los límites y el slider se actualizan en su sitio** (sin perder la gráfica de contexto / sin scroll que la saque de vista).

### Fase 3 — Sensibilidad por serie + global
- Slider a nivel **global** (Todas las categorías) y **por serie**.
- En el bloque "Por serie", **versión resumida** del slider por fila (junto a los inputs mín/máx).
- Herencia: una serie sin override usa la configuración global (modo adaptativo puro como hoy).

### Fase 4 — Foco/zoom en una serie
- Acción para **enfocar una serie** (desde la gráfica o desde la lista): oculta el resto, mueve la gráfica a esa serie y abre el **slider grande + narrativa específica de la serie**.
- Transición natural (entrar/salir del foco).

### Fase 5 — Compatibilidad con % relativos (futuro / no bloqueante)
- Permitir definir límites como **% relativo** (ej. ">20% vs. últimos N valores) además de absolutos, reusando el mismo slider/coloreado.

---

## 5. Decisiones pendientes (confirmar antes de construir)

1. **Geometría del slider:** ¿un único slider que cierra la banda amarilla **simétricamente** desde ambos bordes, o **control por lado** (inferior/superior independientes)? La sesión sugiere uno solo que cierra hacia adentro — confirmar.
2. **Sentido y escala:** ¿0% = sin banda amarilla y 100% = banda amarilla ocupa casi todo el rango interior? ¿Mostramos el valor como % o como valor absoluto del umbral?
3. **¿"Notificar lo amarillo" es implícito o un toggle aparte?** La sesión lo dejó como que el slider ya implica notificar lo amarillo (REQUIRES_ATTENTION). Confirmar si hace falta un switch separado.
4. **Foco por serie (Fase 4):** ¿entrar al foco desde un botón en la fila de la serie, desde el punto en la gráfica, o ambos?
5. **Persistencia global↔serie:** al tener override por serie, ¿cómo se comunica "esta serie no sigue al global"? (chip "personalizada" / botón "volver al global").

---

## 6. Impacto en lo ya construido (prototipo actual)

- **Se reemplaza** el segmented `.bgroup` (Nula/Media/Alta) y la lógica `applySens` / `selSens` por el slider y su render.
- **Se reescribe** `renderSensChart` para el coloreado invertido (rojo afuera / amarillo adentro / gradiente). `SENS_FRAC` pasa de 3 niveles fijos a un valor continuo del slider.
- **Se mantiene** que los inputs de límite controlan la banda (hecho hoy) — ahora la banda es la **roja/dura**, y el slider define la **amarilla** sobre ella.
- La **gráfica de "Vista previa de configuración"** (anomalías marcadas, hecho hoy) se alinea con el coloreado nuevo.
- El handoff `handoff-limites-sensibilidad.md` se actualiza al cerrar el rediseño.

---

## 7. Aparte (no es de sensibilidad, anotado en la sesión)
- **Bug de enums de severidad** en el JSON: llegan a veces en minúscula / mayúscula / con underscore — revisar que use los enums correctos (puede ser data vieja de develop).
- **Templates Slack:** confirmado que se prefieren **links** (dashboard / resource / cliente) en vez de los botones de menú del template.
