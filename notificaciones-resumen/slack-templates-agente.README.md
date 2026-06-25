# Plantillas de notificación Slack — Detector de anomalías (Agent Factory)

Spec oficial de las **3 plantillas de Slack Block Kit** que devuelve el detector de anomalías de Agent Factory.
Fuente: Santiago Quintero (Advanced AI Engineer) — DM del **2026-06-23**.

> Estas son las plantillas **canónicas del agente** (notificación por ventana, agrupada por fuente).
> No confundir con el **resumen diario consolidado** (`slack-blockkit.README.md` / `templates.html`), que es otro mensaje.

## Selección de plantilla

Se elige por el header HTTP **`X-Slack-Template`**:

| Valor | Filosofía |
|---|---|
| `default` | La más verbosa: nombres de métrica completos, `*Incidente:*` por bloque, "Otras acciones" aparte. |
| `compact` | Agrupada por detector, con **resumen IA** + métricas abreviadas. |
| `ultra-compact` | Numbers-first, agrupada **por recurso**, **sin texto de IA**. |

Variante: **`build_attention_blocks`** = igual al `ultra-compact` pero con header `🔎 *<severidad> — <workspace>*`, **sin "Acción Recomendada" ni "Ventana"**.

## Contrato de datos (ejemplo: 3 incidentes en 2 fuentes, idioma `es`)

- **Workspace:** `Acme Payments` · **N incidentes** + **N fuentes de datos**
- Por **fuente:** nombre + `res_id` (ej. `res_001`) + URL a `/ur/resources/native/<res_id>/management`
- **Detectores:** `MISSING_FILES`, `VOLUME_VARIATION`, `UNEXPECTED_NULL_COLUMN` (cada uno con sus métricas propias)
- **Meta:** generado el `2026-06-23 09:00` · **Ventana** `06:00–09:00` · `ID: ntf_abc123` (por incidente: `ntf_abc123-1`, `-2`, `-3`)
- **Acción recomendada** (texto) · **Confianza** (ej. Alta)
- **Botones:** Crear caso de soporte (Zendesk) · `:eyes:` Marcar como visto · Marcar como falso positivo (Typeform)

## Diferencias clave

| | `ultra-compact` | `compact` | `default` |
|---|---|---|---|
| Agrupación | por recurso (métricas inline) | por detector + botón "Abrir origen" | por detector, `*Incidente:*` por bloque |
| Resumen IA | ❌ | ✅ "3 incidents across 2 sources" | ✅ |
| Métricas | `expected: 10 \| arrived: 7 \| missing: 3` | abreviadas (`expected_files`, `missing_count`) | nombre completo (`expected_number_of_files_today`) |
| Acciones | 3 botones en una fila | botones + sección falso-positivo + confianza | "Otras acciones" separadas + falso-positivo |
| Ventana en meta | ✅ | ✅ | ✅ |

## Cómo probar el render

1. Abrir el **Block Kit Builder**: https://app.slack.com/block-kit-builder
2. Pegar el array de bloques de la plantilla deseada (abajo).

---

## 1) `ultra-compact`

Numbers-first, agrupado por recurso, sin texto de IA.

```json
[
  { "type": "section", "text": { "type": "mrkdwn", "text": "🚨 *Acme Payments — 3 Incidentes (2 fuentes de datos)*" } },
  { "type": "context", "elements": [ { "type": "mrkdwn", "text": "2026-06-23 09:00  -  Ventana: 06:00–09:00  -  ID: `ntf_abc123`" } ] },
  { "type": "context", "elements": [ { "type": "mrkdwn", "text": "*Acción Recomendada:* Contact the data provider to resend missing files." } ] },
  { "type": "divider" },
  { "type": "section", "text": { "type": "mrkdwn", "text": "▸ *<https://app.simetrik.com/ur/resources/native/res_001/management|Daily Settlements>* (res_001)" } },
  { "type": "context", "elements": [ { "type": "mrkdwn", "text": "`MISSING_FILES`  expected: 10  |  arrived: 7  |  missing: 3\n`VOLUME_VARIATION`  expected_rows: 1000000  |  arrived_rows: 580000  |  variation: -42" } ] },
  { "type": "section", "text": { "type": "mrkdwn", "text": "▸ *<https://app.simetrik.com/ur/resources/native/res_002/management|Card Transactions>* (res_002)" } },
  { "type": "context", "elements": [ { "type": "mrkdwn", "text": "`UNEXPECTED_NULL_COLUMN`  columns_monitored: 12  |  amount: null 35% (threshold 2%)  |  currency: null 18% (threshold 1%)" } ] },
  { "type": "divider" },
  { "type": "actions", "elements": [
    { "type": "button", "text": { "type": "plain_text", "text": "Crear caso de soporte", "emoji": true }, "url": "https://simetriksoporte.zendesk.com/...", "value": "create_ticket" },
    { "type": "button", "text": { "type": "plain_text", "text": ":eyes: Marcar como visto", "emoji": true }, "action_id": "mark_as_seen", "value": "ntf_abc123" },
    { "type": "button", "text": { "type": "plain_text", "text": "Marcar como falso positivo", "emoji": true }, "url": "https://simetrik-customersuccess.typeform.com/to/T0cduQBa", "value": "false_positive" }
  ] }
]
```

> `build_attention_blocks` es igual salvo el header `🔎 *<severidad> — <workspace>*`, sin "Acción Recomendada" ni "Ventana".

---

## 2) `compact`

Agrupado con resumen IA + métricas abreviadas por detector.

```json
[
  { "type": "section", "text": { "type": "mrkdwn", "text": "🚨 *Acme Payments — 3 Incidentes (2 fuentes de datos)*" } },
  { "type": "context", "elements": [ { "type": "mrkdwn", "text": "`MISSING_FILES`  `UNEXPECTED_NULL_COLUMN`  `VOLUME_VARIATION`" } ] },
  { "type": "section", "text": { "type": "mrkdwn", "text": "*Resumen:*\n3 incidents across 2 sources." } },
  { "type": "context", "elements": [ { "type": "mrkdwn", "text": "Generado el:: 2026-06-23 09:00  -  Ventana:: 06:00–09:00  -  ID de Notificación:: ntf_abc123" } ] },
  { "type": "section", "text": { "type": "mrkdwn", "text": "*Acción Recomendada:* Contact the data provider to resend missing files." } },
  { "type": "divider" },
  { "type": "section", "text": { "type": "mrkdwn", "text": "*Fuentes de datos afectadas (2)*" } },
  { "type": "section", "text": { "type": "mrkdwn", "text": "*Daily Settlements - ID: res_001*" }, "accessory": { "type": "button", "text": { "type": "plain_text", "text": "Abrir origen", "emoji": true }, "url": "https://app.simetrik.com/ur/resources/native/res_001/management", "value": "open_origin" } },
  { "type": "context", "elements": [ { "type": "mrkdwn", "text": "`MISSING_FILES`  |  *ID:* `ntf_abc123-1`\nexpected_files: 10  |  arrived_files: 7  |  missing_count: 3" } ] },
  { "type": "section", "text": { "type": "mrkdwn", "text": "*Daily Settlements - ID: res_001*" }, "accessory": { "type": "button", "text": { "type": "plain_text", "text": "Abrir origen", "emoji": true }, "url": "https://app.simetrik.com/ur/resources/native/res_001/management", "value": "open_origin" } },
  { "type": "context", "elements": [ { "type": "mrkdwn", "text": "`VOLUME_VARIATION`  |  *ID:* `ntf_abc123-2`\nexpected_rows: 1000000  |  arrived_rows: 580000  |  percentage: -42" } ] },
  { "type": "section", "text": { "type": "mrkdwn", "text": "*Card Transactions - ID: res_002*" }, "accessory": { "type": "button", "text": { "type": "plain_text", "text": "Abrir origen", "emoji": true }, "url": "https://app.simetrik.com/ur/resources/native/res_002/management", "value": "open_origin" } },
  { "type": "context", "elements": [ { "type": "mrkdwn", "text": "`UNEXPECTED_NULL_COLUMN`  |  *ID:* `ntf_abc123-3`\ntotal_monitored: 12\ncolumn_name: amount  |  current_pct: 35  |  historical_threshold: 2\ncolumn_name: currency  |  current_pct: 18  |  historical_threshold: 1" } ] },
  { "type": "divider" },
  { "type": "actions", "elements": [
    { "type": "button", "text": { "type": "plain_text", "text": "Crear caso de soporte", "emoji": true }, "url": "https://simetriksoporte.zendesk.com/...", "value": "create_ticket" },
    { "type": "button", "text": { "type": "plain_text", "text": ":eyes: Marcar como visto", "emoji": true }, "action_id": "mark_as_seen", "value": "ntf_abc123" }
  ] },
  { "type": "divider" },
  { "type": "section", "text": { "type": "mrkdwn", "text": "*Marcar como falso positivo*\nSi esto es esperado, indícanos el motivo..." }, "accessory": { "type": "button", "text": { "type": "plain_text", "text": "Marcar como falso positivo", "emoji": true }, "url": "https://simetrik-customersuccess.typeform.com/to/T0cduQBa", "value": "false_positive" } },
  { "type": "context", "elements": [ { "type": "mrkdwn", "text": "Tip: Razones breves ayudan a ajustar alertas...  -  *Confianza:: Alta*" } ] }
]
```

---

## 3) `default`

La más verbosa (métricas con nombre completo, `*Incidente:*` por bloque, "Otras acciones" aparte).

```json
[
  { "type": "section", "text": { "type": "mrkdwn", "text": "🚨 *Acme Payments — 3 Incidentes (2 fuentes de datos)*" } },
  { "type": "context", "elements": [ { "type": "mrkdwn", "text": "`MISSING_FILES`  `UNEXPECTED_NULL_COLUMN`  `VOLUME_VARIATION`" } ] },
  { "type": "section", "text": { "type": "mrkdwn", "text": "*Resumen:*\n3 incidents across 2 sources." } },
  { "type": "context", "elements": [ { "type": "mrkdwn", "text": "Generado el:: 2026-06-23 09:00  -  Ventana:: 06:00–09:00\nID de Notificación:: ntf_abc123" } ] },
  { "type": "section", "text": { "type": "mrkdwn", "text": "*Acción Recomendada:* Contact the data provider to resend missing files." } },
  { "type": "divider" },
  { "type": "section", "text": { "type": "mrkdwn", "text": "*Fuentes de datos afectadas (2)*" } },
  { "type": "section", "text": { "type": "mrkdwn", "text": "*Daily Settlements - ID: res_001*\n*Incidente:* `MISSING_FILES`" }, "accessory": { "type": "button", "text": { "type": "plain_text", "text": "Abrir origen", "emoji": true }, "url": "https://app.simetrik.com/ur/resources/native/res_001/management", "value": "open_origin" } },
  { "type": "context", "elements": [ { "type": "mrkdwn", "text": "*ID de Notificación:* `ntf_abc123-1`\n\nexpected_number_of_files_today: 10  |  arrived_number_of_files_today: 7  |  missing_files_count: 3" } ] },
  { "type": "section", "text": { "type": "mrkdwn", "text": "*Daily Settlements - ID: res_001*\n*Incidente:* `VOLUME_VARIATION`" }, "accessory": { "type": "button", "text": { "type": "plain_text", "text": "Abrir origen", "emoji": true }, "url": "https://app.simetrik.com/ur/resources/native/res_001/management", "value": "open_origin" } },
  { "type": "context", "elements": [ { "type": "mrkdwn", "text": "*ID de Notificación:* `ntf_abc123-2`\n\nexpected_number_of_rows_today: 1000000  |  arrived_number_of_rows_today: 580000  |  volume_variation_percentage: -42" } ] },
  { "type": "section", "text": { "type": "mrkdwn", "text": "*Card Transactions - ID: res_002*\n*Incidente:* `UNEXPECTED_NULL_COLUMN`" }, "accessory": { "type": "button", "text": { "type": "plain_text", "text": "Abrir origen", "emoji": true }, "url": "https://app.simetrik.com/ur/resources/native/res_002/management", "value": "open_origin" } },
  { "type": "context", "elements": [ { "type": "mrkdwn", "text": "*ID de Notificación:* `ntf_abc123-3`\n\ntotal_columns_monitored: 12\ncolumn_name: amount  |  current_null_pct: 35  |  historical_null_threshold: 2\ncolumn_name: currency  |  current_null_pct: 18  |  historical_null_threshold: 1" } ] },
  { "type": "divider" },
  { "type": "section", "text": { "type": "mrkdwn", "text": "*Otras acciones*" } },
  { "type": "actions", "elements": [
    { "type": "button", "text": { "type": "plain_text", "text": "Crear caso de soporte", "emoji": true }, "url": "https://simetriksoporte.zendesk.com/...", "value": "create_ticket" },
    { "type": "button", "text": { "type": "plain_text", "text": ":eyes: Marcar como visto", "emoji": true }, "action_id": "mark_as_seen", "value": "ntf_abc123" }
  ] },
  { "type": "divider" },
  { "type": "section", "text": { "type": "mrkdwn", "text": "*Marcar como falso positivo*\nSi esto es esperado, indícanos el motivo..." }, "accessory": { "type": "button", "text": { "type": "plain_text", "text": "Marcar como falso positivo", "emoji": true }, "url": "https://simetrik-customersuccess.typeform.com/to/T0cduQBa", "value": "false_positive" } },
  { "type": "context", "elements": [ { "type": "mrkdwn", "text": "Tip: Razones breves ayudan a ajustar alertas...\n*Confianza:: Alta*" } ] }
]
```

---

## Notas de diseño / pendientes de alineación

- **Reaparece el concepto "Ventana"** (meta de todas las plantillas). En el diálogo de monitoreo (`index.html`) lo reemplazamos por "horario programado" por feedback de usuario. Decidir si se alinea el copy también acá.
- Texto mezclado **ES/EN** en los ejemplos (`3 incidents across 2 sources`, `Contact the data provider...`): el agente recibe `idioma: es` pero el resumen/acción vienen en inglés. Revisar con Agent Factory.
- Doble `::` en labels del `compact`/`default` (`Generado el::`, `Confianza::`) — probable typo del template del agente.
