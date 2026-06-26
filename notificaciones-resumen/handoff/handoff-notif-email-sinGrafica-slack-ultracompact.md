# Handoff — Notificación de Resumen diario: Email (sin gráfica) + Slack Block Kit (ultra-compact)

Fecha: 2026-06-26
Origen: `notificaciones-resumen/templates.html` (prototipo validado). Dos plantillas: columna **Email · "Sin gráfica"** y columna **Slack · Block Kit · ultra-compact**.
Registro: **Op Center** — notificación saliente del Centro de Operaciones a quien configuró el monitoreo en su Espacio de trabajo.
Patrón de presentación: **lista de incidentes agrupada/escaneable**, generada 1:1 desde el JSON del detector (BADS).

> **Punto de entrada (wording 26-jun):** el resumen se activa desde el botón **"Resumen de incidentes"** (label corto, ícono `mails`) en la vista de monitoreo. Su popover aclara el alcance —**"de este tablero"**— y la hora configurable —**"Todos los días, a la hora que elijas"** (sin "cada mañana")—. El resumen **no lo genera una IA**: reutiliza los textos ya generados de cada incidente (no introducir copy de "agente/IA").

> **Regla base (no negociable):** el contenido sale **1:1 del `bads_payload`** del endpoint de incidentes. Texto **verbatim**; la única transformación permitida es **elegir idioma** (`es`/`en`/`pt`) y **resolver los marcadores `[n]`** con `references[]`. No se genera ni reescribe texto, no se fabrican campos. Todo lo que envió Santiago (3 plantillas vía `X-Slack-Template`, acciones a nivel mensaje, `mark_as_seen`, header `x-slack-responsible`) queda **fuera de este alcance**.

---

## 1. Contexto y objetivo

El detector de anomalías (BADS) genera incidentes (`status: OPEN`). El **Resumen diario** consolida los incidentes abiertos del día anterior y los entrega por **Email** y/o **Slack** según la config de notificación del KPI.

Objetivo de estas dos plantillas: que el operador, de un vistazo, sepa **qué fuentes tienen incidentes abiertos, de qué severidad y categoría**, y pueda abrir/accionar sin salir del canal.

- **Email sin gráfica:** la variante **más segura de entregar** (no depende de render de imagen). Tarjeta por incidente con narrativa + acciones. Es el fallback canónico del email.
- **Slack ultra-compact:** la variante **más densa/escaneable** de Slack. Una línea por incidente (título) + tags. Sin summary ni botones por incidente.

## 2. Usuario y registro

- **Registro:** Op Center. Receptor = operador de la cuenta / Espacio de trabajo que activó el monitoreo. Uso recurrente (diario), lectura rápida, alta tolerancia a densidad.
- **Modo de interacción:** escanear → identificar lo urgente → abrir el incidente o crear ticket.
- **Dato clave al primer vistazo:** ¿cuántos incidentes urgentes hay y en qué fuentes?

## 3. Historias de usuario

**HU-1 — Escanear el resumen del día**
> Como operador, quiero recibir un resumen diario con los incidentes abiertos agrupados por fuente y por severidad, para saber en segundos qué requiere mi atención sin abrir el producto.

**HU-2 — Confiar en el dato (auditable)**
> Como operador, quiero ver la narrativa del detector tal cual, con su categoría, severidad y confianza, para confiar en el número sin sospechar que se "inventó" un resumen.

**HU-3 — Accionar desde el canal**
> Como operador, quiero abrir el incidente o crear un ticket de soporte directo desde la notificación (Email), para no perder tiempo navegando.
> *(En ultra-compact la acción es abrir el incidente desde el título; los botones por incidente viven en la variante `default`, fuera de este handoff.)*

## 4. Alcance de este handoff

| Incluye | NO incluye (otro handoff) |
|---|---|
| Email **sin gráfica** | Email **con gráfica** (depende de render PNG server-side, pendiente) |
| Slack **ultra-compact** | Slack `default` / `compact` |
| Estructura + mapeo de campos desde el JSON | La **vista modal** ("ver todos") |
| Copy chrome (glosario) + estados | Config de notificación (canal + `slack_id`) → ya en `handoff-notificaciones-canales.md` |

---

## 5. Anatomía, parser y relación con cada canal

### 5.1 Flujo end-to-end (del JSON a la notificación)

Separar **3 cosas**: el **QUÉ** (`bads_payload`), el **A QUIÉN/DÓNDE** (config: canal + `slack_id`), el **CÓMO se ve** (MJML / Block Kit). El detector no sabe de Email/Slack; Email/Slack no saben del `bads_payload`. En el medio, el **servicio de notificaciones** parsea y renderiza por canal.

```
[1] Detector BADS  ─▶  [2] JSON bads_payload  ─▶  [3] Servicio notif. (parsea)  ─▶  ├─ [4a] MJML       ─▶  [5a] Cliente de correo
    genera incidente       status: OPEN,             parse(payload, lang)            └─ [4b] Block Kit  ─▶  [5b] Slack
    emite evento           findings, actions         + render por canal
                                                            ▲
                                                Config del KPI: canal + slack_id
```

1. **Se genera el incidente** — el detector (`workflow_type: ingestion_analysis`) crea los `findings` con IA, arma el `bads_payload` (`schema_version 1.7`), persiste el incidente (`status: OPEN`) y emite un evento (`event_type: com.simetrik.bads.incident.escalated` / `.enriched`).
2. **Sale como JSON** — dos vías: **push** (el evento dispara la notificación de **KPI** en tiempo real) y **pull** (`GET results[]` filtrando `OPEN` + día, para el **resumen**).
3. **El servicio de notificaciones parsea** — backend, **no** el front ni el cliente de correo/Slack. Lee la config (canal + `slack_id`), toma el `bads_payload`, elige idioma, resuelve `[n]`, agrupa por recurso y produce un **modelo normalizado** (§5.2).
4. **Render por canal** (mismo parseo, distinto renderer): **Email** → MJML; **Slack** → Block Kit (ultra-compact).
5. **Envío al destino** — **Email**: notification center / SMTP (sin imagen en la variante sin gráfica). **Slack**: `chat.postMessage` con `channel` + etiqueta `slack_id` (ambos de la config).

> Aplica igual a las **dos** notificaciones del JSON: **KPI** (1 incidente, evento) y **resumen** (N incidentes, `results[]` filtrado). Solo cambia cuántos incidentes entran al parser.

### 5.2 El parser (compartido, agnóstico de canal)

Una sola función `parseIncidents()` consume el JSON y entrega un modelo normalizado; luego cada canal **renderiza** desde ese modelo. Único punto donde se toca el texto: elegir idioma y resolver `[n]`.

```js
function resolveRefs(text, refs = []) {                 // [1][2] -> resource_name (verbatim salvo esto)
  return text.replace(/\[(\d+)\]/g, (_, id) => {
    const r = refs.find(x => x.ref_id === id);
    return r?.resource_ref ? r.resource_ref.resource_name : ''; // action_ref -> fuera del texto
  });
}

function parseIncidents(results, lang, day) {
  return results
    .filter(i => i.status === 'OPEN'
      && i.bads_payload.scope.coverage_dates.includes(day))   // resumen: OPEN + día
    .map(i => {
      const p = i.bads_payload, f = p.findings[0], ref = p.scope.resource_refs[0];
      return {
        resource:   { name: ref.resource_name, type: ref.resource_type }, // id NO se muestra
        title:      resolveRefs(f.title[lang],   f.references),  // verbatim
        summary:    resolveRefs(f.summary[lang], f.references),  // verbatim (solo Email)
        severity:   f.severity,                 // URGENT | REQUIRES_ATTENTION
        category:   f.problem_category,         // MISSING_FILE | VOLUME_VARIATION | ...
        confidence: f.confidence,               // 0..1
        hypothesis: p.hypothesis?.confidence,   // INDICATIVE | PROBABLE | CONFIRMED (solo Email)
        coverageDate: p.scope.coverage_dates[0],
        detectedAt:   i.executed_at,
        affectedDashboards: i.affected_dashboards_count,
        actions: p.recommended_actions          // solo las que traen action_ref con label
          .sort((a, b) => a.priority - b.priority)
          .flatMap(a => a.references.filter(r => r.action_ref))
          .map(r => ({ label: r.action_ref.label[lang], type: r.action_ref.action_type,
                       target: r.action_ref.target, body: r.action_ref.body?.[lang] })),
      };
    });
}

// luego, por canal:
//   renderEmailSinGrafica(groupByResource(model))   -> MJML
//   renderSlackUltraCompact(model)                  -> Block Kit
```

**Idioma:** `es` / `en` / `pt` según preferencia del usuario (fallback `en`).

### 5.3 Qué usa cada canal del modelo (relación parser ↔ notificación)

El parser es uno solo; cada plantilla **toma un subconjunto** del modelo:

| Campo del modelo (← JSON) | Email **sin gráfica** | Slack **ultra-compact** |
|---|---|---|
| `resource.name` (← `resource_name`) | encabezado de grupo | dentro del `title` (no se repite) |
| `resource.type` (← `resource_type`) | sub del grupo | — |
| `title` (← `title[lang]`) | título de la tarjeta | `section` (puede ir como link) |
| `summary` (← `summary[lang]`) | **cuerpo (narrativa)** | — (no se usa) |
| `severity` (← `severity`) | badge | tag de color en el `context` |
| `category` (← `problem_category`) | chip | `context` |
| `confidence` (← `confidence`) | texto | `context` |
| `hypothesis` (← `hypothesis.confidence`) | texto | — |
| `coverageDate` (← `coverage_dates[0]`) | línea de timestamp | opcional |
| `detectedAt` (← `executed_at`) | "Detectado…" | — |
| `affectedDashboards` (← `affected_dashboards_count`) | chip "afecta N tableros" | — |
| `actions` (← `recommended_actions`) | **botones** (§8) | — (ultra no lleva botones; el title-link cubre "Abrir") |
| conteos (count por `severity`) | stats (3 tarjetas) | `context` del header |

> Lectura rápida: **Email sin gráfica** usa casi todo el modelo (narrativa + acciones + impacto). **Slack ultra-compact** usa el mínimo: `title` + `category` + `severity` + `confidence`.

---

## 6. Plantilla A — Email (sin gráfica)

Tecnología: **MJML** (registrado en el notification center). Estructura fija (componentización con loop sobre incidentes); solo se parametrizan textos y enlaces.

### Estructura (de arriba a abajo)
1. **Barra de marca:** logo Simetrik + "Centro de Operaciones". *(chrome, fijo)*
2. **H1:** "Resumen diario". **Intro:** "Incidentes abiertos (status OPEN), agrupados por la fuente de datos afectada."
3. **Stats (3 tarjetas):** `count(URGENT)` · `count(REQUIRES_ATTENTION)` · `count(fuentes)`.
4. **Label de sección:** "INCIDENTES POR FUENTE".
5. **Por cada fuente** (`scope.resource_refs`): encabezado = `resource_name`; sub = `resource_type`.
   **Por cada `finding` de esa fuente** → una tarjeta:
   - Badge de **severidad** (`URGENT`/`REQUIRES_ATTENTION`) + chip de **categoría** (`problem_category`).
   - **Título** (`title`, verbatim).
   - **Narrativa** (`summary`, verbatim) ← este es el cuerpo; **no hay gráfica** en esta variante.
   - **Confianza:** `confidence` numérico + `hypothesis.confidence` enum.
   - Chip **"afecta N tableros"** si `affected_dashboards_count > 0`.
   - **Botones** = `recommended_actions[]` (ver §8).
   - **Timestamp:** `executed_at`.
6. **"+N incidentes más, ver todos en el Centro de Operaciones"** (manejo de volumen, top-N).
7. **Disclaimer** + **footer** (motivo del envío + link "Centro de Operaciones › Resumen diario").

### Reglas email
- **Sin SVG ni JS** (los clientes los bloquean). Esta variante no lleva imagen, por eso es la segura.
- Todo el cuerpo entendible en **texto plano** (muchos clientes bloquean imágenes/estilos).
- **Light only** (los emails no tienen dark mode confiable; no mezclar).
- Las métricas (esperados/llegaron/faltan/%) **viven dentro de `summary`** — no hay campos discretos; **no** parsear la narrativa con regex para fabricar chips.

---

## 7. Plantilla B — Slack Block Kit (ultra-compact)

Tecnología: **Slack Block Kit** (`blocks[]`). Las mismas blocks sirven en mensaje o modal; aquí va como **mensaje** (la notificación se envía, no se abre).

### Estructura
1. **`section`** (header): `🚨 *Resumen diario · N incidentes abiertos (M fuentes)*`.
2. **`context`** (conteo): `*X* URGENT  ·  *Y* REQUIRES_ATTENTION`.
3. **`divider`**.
4. **Por cada `finding`** (lista plana, incidente primero):
   - **`section`** = el **incidente**: `*title*` (verbatim). El título puede ir como **link** al incidente: `*<{go_to.target_url}|{title}>*` si hay una acción `go_to`.
   - **`context`** = tags: `` `problem_category` · {severity} · {confidence} ``.
   - **Sin** `summary`, **sin** botones por incidente (eso es `default`).

### Block Kit JSON (esqueleto, verbatim desde el JSON)
```json
[
  { "type": "section", "text": { "type": "mrkdwn", "text": "🚨 *Resumen diario · 4 incidentes abiertos (4 fuentes)*" } },
  { "type": "context", "elements": [{ "type": "mrkdwn", "text": "*2* URGENT   ·   *2* REQUIRES_ATTENTION" }] },
  { "type": "divider" },

  { "type": "section", "text": { "type": "mrkdwn", "text": "*URGENTE: 28 archivos faltantes (100% de lo esperado) detectados en source-1-payments-merchant el 2026-06-22*" } },
  { "type": "context", "elements": [{ "type": "mrkdwn", "text": "`MISSING_FILES` · URGENT · 0.85" }] }
  // … una pareja section+context por cada finding …
]
```
> El recurso **no se repite** en el `context`: ya va dentro del `title` al resolver `[1]`. La severidad va como tag de color (rojo/ámbar), sin badge (Block Kit no tiene pill de color nativo).

### Notas Slack
- ⚠️ **Sin imagen** en v1 (la generación de imagen en Slack quedó marcada como riesgo, pendiente con Iván). El `summary` no se usa en ultra-compact, así que no aplica.
- Etiquetado (si la config lo pide): se arroba a la persona por su `slack_id` (viene de la config: canal + ID), no por `@nombre`.

---

## 8. Botones / acciones (solo Email en este handoff)

Salen de `recommended_actions[]`. Solo pinta botón la acción que trae `action_ref.label`; las que solo traen `resource_ref` (ej. `REVIEW_DATA_SOURCE`) **no** pintan botón. Orden por `priority`.

| Opción (`label.es`) | `action_type` | Comportamiento |
|---|---|---|
| **Abrir** | `go_to` | abre el `target` (deep link `app.simetrik.com/...`) |
| **Crear ticket** | `create_support_ticket` | abre flujo de ticket con `body[lang]` prellenado |
| **Enviar mensaje** | `send_message` | redacta al proveedor con `body[lang]` prellenado |

Universo completo en el JSON: solo esas 3. (ultra-compact omite botones; el título-link cubre el "abrir".)

---

## 9. Copy completo (glosario aplicado)

Chrome (lo único que NO viene del JSON). Glosario Op Center aplicado, sin em-dashes:

| Slot | Copy |
|---|---|
| Asunto email | `Tu resumen diario · Centro de Operaciones` |
| H1 | `Resumen diario` |
| Intro | `Incidentes abiertos (status OPEN), agrupados por la fuente de datos afectada.` |
| Stats labels | `URGENT` · `REQUIRES_ATTENTION` · `Fuentes afectadas` |
| Sección | `INCIDENTES POR FUENTE` |
| Impacto | `afecta N tableros` *(no "dashboards")* |
| Volumen | `+N incidentes más, ver todos en el Centro de Operaciones` |
| Footer | `Recibes este resumen porque el monitoreo de anomalías está activo en tu cuenta. Ajusta el horario o desactívalo en Centro de Operaciones › Resumen diario.` |
| Header Slack | `🚨 Resumen diario · N incidentes abiertos (M fuentes)` |

> **Fix pendiente en el prototipo:** `templates.html` dice "afecta 1 dashboard" → debe ser **tablero** (glosario).
> **Severidad** se muestra como enum crudo (`URGENT`/`REQUIRES_ATTENTION`): aceptable en Op Center (técnico). Si se decide localizar, mapear (`URGENT`→"Urgente", `REQUIRES_ATTENTION`→"Requiere atención") en una sola capa, no en la narrativa.
> Los **títulos y narrativas** son verbatim del detector y **sí** contienen em-dashes / mayúsculas; eso es del payload, no se edita.

---

## 10. Estados

| Estado | Email sin gráfica | Slack ultra-compact |
|---|---|---|
| **0 incidentes OPEN del día** | No enviar (o variante "Sin novedades hoy" si producto lo pide) | Igual |
| **1 incidente** | 1 fuente, 1 tarjeta | header "1 incidente (1 fuente)" + 1 línea |
| **Muchos** (la cuenta tiene miles) | top-N tarjetas + "+N más, ver todos" | top-N líneas + "+N más" |
| **Fuente con varios `findings`** | varias tarjetas bajo la misma fuente | varias líneas seguidas (lista plana) |
| **Sin `recommended_actions` con label** | tarjeta sin botones (solo "Abrir incidente" si hay `go_to`) | n/a (ultra no lleva botones) |
| **`coverage_dates` vacío** | usar `executed_at` como fecha; no romper | igual |
| **Idioma faltante** | fallback `en` | fallback `en` |

---

## 11. Endpoint esperado

- **Lista de incidentes** (paginada): `results[]`, cada item = un incidente con `bads_payload` (`schema_version 1.7`).
- Filtro para el resumen: `status = OPEN` + `coverage_dates` incluye el día anterior.
- El total puede ser de **miles** (`pagination_data.totalItems` ej. 2415); por eso top-N + "+N más".
- Cada `recommended_actions[].action_ref` trae `target` (para construir la URL) y `body[lang]` (para `create_support_ticket` / `send_message`).

## 12. Edge cases y validaciones

- **Título muy largo** (ultra): truncar visualmente a 1 línea (CSS ellipsis); **no** reescribir el texto.
- **Resource duplicado**: nunca repetir `resource_name` en el `context` de ultra (ya va en el title).
- **`affected_dashboards_count = 0`**: ocultar el chip de impacto.
- **Acciones sin `label`**: no renderizar botón (no inventar "Tablero/Ver incidente").
- **Imagen Slack**: bloqueada en v1 (no incluir `image` blocks).
- **Email sin estilos** (cliente los bloquea): el contenido debe leerse igual.
- **Números dentro del `summary`**: no extraer con regex para chips; mostrar la narrativa tal cual.

## 13. Test cases sugeridos

1. **Happy path Email:** 4 incidentes / 3-4 fuentes, mezcla `URGENT` + `REQUIRES_ATTENTION`, con y sin `affected_dashboards_count`. Verificar verbatim de `title`/`summary` y `[n]` resueltos.
2. **Happy path Slack ultra:** mismos datos, una línea por incidente, conteo del header correcto, sin botones, sin imagen.
3. **Volumen:** 50 incidentes → top-N + "+N más" en ambos.
4. **Acciones:** incidente con `CONTACT_INTERNAL_SUPPORT` (Crear ticket con body) vs uno con solo `REVIEW_DATA_SOURCE` (sin botón).
5. **i18n:** `lang = es/en/pt` y fallback.
6. **Email texto plano:** desactivar imágenes/estilos y confirmar legibilidad.

## 14. Checklist pre-PR

- [ ] Contenido **1:1 del `bads_payload`** (title/summary/labels verbatim); única transformación: idioma + resolver `[n]`.
- [ ] **Sin chrome de Santiago** (sin `X-Slack-Template`, sin acciones a nivel mensaje, sin `mark_as_seen`, sin `x-slack-responsible`).
- [ ] **Glosario** aplicado en chrome (`tablero`, `Fuente`, `Incidente`, `Espacio de trabajo`); sin em-dashes en copy propio.
- [ ] `resource_id` **no** visible (solo en URL/target).
- [ ] Botones solo desde `recommended_actions` con `label`; orden por `priority`.
- [ ] **ultra-compact**: sin summary, sin botones, sin imagen; severidad como tag de color.
- [ ] **Email sin gráfica**: sin SVG/JS; legible en texto plano; light only.
- [ ] Estados: 0 incidentes (no enviar), 1, muchos (top-N).
- [ ] A11y email: jerarquía semántica, contraste, `alt` no aplica (sin imágenes en esta variante).
- [ ] Conteos del header = count real de la lista.

---

## Anexo — Ejemplo real (1 incidente del `bads_payload`, recortado)

```json
{
  "status": "OPEN",
  "executed_at": "2026-06-22T23:50:03Z",
  "affected_dashboards_count": 1,
  "bads_payload": {
    "scope": {
      "resource_refs": [{ "resource_id": "80133", "resource_type": "native", "resource_name": "source-1-payments-merchant" }],
      "coverage_dates": ["2026-06-22"]
    },
    "severity": "URGENT",
    "findings": [{
      "problem_category": "MISSING_FILE",
      "severity": "URGENT",
      "confidence": 0.85,
      "title":   { "es": "URGENTE: 28 archivos faltantes (100% de lo esperado) detectados en [1] el 2026-06-22" },
      "summary": { "es": "El detector MISSING_FILES (confianza ALTA) determinó que los 28 archivos esperados … contactar al soporte de Simetrik …" },
      "references": [{ "ref_id": "1", "resource_ref": { "resource_id": "80133", "resource_name": "source-1-payments-merchant" } }]
    }],
    "hypothesis": { "confidence": "PROBABLE" },
    "recommended_actions": [{
      "action": "CONTACT_INTERNAL_SUPPORT", "priority": 0,
      "references": [{ "ref_id": "29", "action_ref": {
        "action_type": "create_support_ticket",
        "label": { "es": "Crear ticket" },
        "target": { "resource_id": "80133", "resource_type": "native" },
        "body":  { "es": "Incidente …: 28 archivos no llegaron …" }
      }}]
    }]
  }
}
```
