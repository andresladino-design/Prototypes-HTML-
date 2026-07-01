# Handoff 3 — Notificaciones de incidentes + vista de Anomalías (configuración y gestión)

**Prototipo:** `notificaciones-resumen/index.html` → vista de **Anomalías** → segmented **Configuración** (paquetes de notificación) y **Gestión** (lista de incidentes).
**Fuente:** sesiones Granola **30-jun-2026** (am: épicas y cambios de UI · **pm: design review con ingeniería/Sergio + Ohana**).
**Registro:** Interno — **Operation Center**. **Plataforma:** Desktop (shell de OC).
**Complementa:** Handoff 1 (filtros de la vista de Gestión) y Handoff 2 (detección/Alertas del KPI). Los **filtros guardados** que el editor de notificación reutiliza se crean en la vista de Gestión (Handoff 1).
**Regla del equipo (no negociable):** *donde un cambio de UI no se enumere explícitamente, no se ejecuta en desarrollo.* Por eso este handoff lista **cada** cambio, incluso los chicos.

> **Glosario obligatorio:** **monitoreo** (nunca "agente"/"Agente IA"/"IA" de cara al usuario), **incidente**, **señal/alerta**, **KPI**, **Tablero**, **Recurso**, **Entidad afectada**, **paquete/regla de notificación**, **entrega** (aviso por evento / resumen consolidado).

---

## 1. Cambio de paradigma

La configuración de notificaciones ya **no** es un formulario único de config global. Es una **lista de paquetes (reglas)** por usuario. Un incidente se evalúa contra todos los paquetes **activos**; si coincide con varios, se notifica por cada vía. Cada usuario crea los suyos: **quien configura, recibe**.

El **resumen consolidado** dejó de ser una sección/flujo aparte: ahora es un **modo de entrega dentro del paquete**, sobre el mismo alcance y los mismos canales. Ver la nota de deprecación de la Épica 3 al final.

### Changelog 30-jun (pm) — design review con ingeniería

Esta tanda **supersede** partes de los documentos previos. Donde haya conflicto, manda esta sección.

1. **Tablero + Recurso → un solo bloque "Entidades afectadas" (OR) — SOLO en el editor de notificación.** Eran entidades jerárquicas tratadas como filtros planos independientes: dejaban armar condiciones imposibles (un recurso que no pertenece al tablero elegido → nunca notifica). En el **alcance del paquete** se unifican en "Entidades afectadas" (tableros + recursos con `o`). Los filtros de la vista de **Gestión NO se tocan**: siguen con **Recurso** y **Tablero** separados (son features distintos; la lista es para navegar, no para definir una regla). Al **importar** un filtro guardado (o el filtro de la vista) al paquete, Tablero/Recurso se **colapsan** a Entidad automáticamente.
2. **Resumen consolidado deja de ser sección propia → es un modo de entrega dentro del paquete.** El bloque "¿Cuándo quieres que te avisemos?" del editor tiene **dos entregas** sobre el mismo alcance: **Aviso por evento** (uno por cada evento, apenas ocurre) y **Resumen consolidado** (1×día). Se pueden activar las dos. El alcance y los canales se **heredan del paquete** (no se repiten filtros). → **anula la Épica 3** como sección independiente.
3. **Parámetro t-n (1 a 5) en el resumen + microcopy de período.** El corte del resumen siempre cierra el día anterior; la **hora solo define cuándo llega, no qué período cubre**. El selector "Qué período resume" (t-1 … t-5) cubre el **lag operativo** del cliente (operaciones a t-4, etc.): "hoy recibo lo que sigue abierto hasta hace n días".
5. **Separar "¿qué incidentes te interesan?" (alcance) de "¿cuándo te avisamos?" (momento).** El **Estado** sale del alcance del paquete (se pisaba con el momento creado/confirmado). El alcance es solo entidades + tipo; el momento vive en la entrega "Aviso por evento".
7. **Pendiente con Iván (notification center):** confirmar que el ID de usuario de Slack se soporta como **parámetro del template** antes de comprometer el etiquetado. Además: **2 templates** (creación vs updates) y **desacoplar en el listener** la lógica compartida entre tópicos de señales e incidentes.

---

## 2. Épica · Paquetes de notificación de incidentes

**Dónde:** Anomalías → Configuración → **Notificaciones de incidentes**.

> Cada usuario crea sus paquetes. Un incidente = evento; en cada evento se evalúan las reglas de todos los paquetes activos → match → notifica. Anti-spam: por default, quien configura el paquete es quien recibe; agregar a terceros es explícito (en canales).

### Cambios de UI (enumerados)

**2.1 · Vista de lista plana** de todas las notificaciones configuradas. Cada tarjeta lleva: nombre, resumen del alcance, toggle activo/inactivo, tags de entrega (**"Por evento: al crearse, …"** · **con actualizaciones** · **"Resumen 08:00 · hasta hace 4 días (t-4)"** · canales) y acciones **Duplicar / Editar / Eliminar** (íconos en footer). Botón **"Crear notificación"** arriba a la derecha.

- **Inactiva:** tarjeta atenuada, toggle off.
- **Duplicar** clona la configuración como una nueva notificación ("… (copia)") y abre el editor. Implementa el *"me gusta esta config, me la copio"* de Granola.
- **Sin concepto de dueño/equipo.** No hay separación "Mías / Del equipo" ni avatar de dueño. Se muestran todas las notificaciones configuradas en una lista plana; clonar es la vía para reutilizar una existente.

**2.2 · Empty state / first-run (activo, con forma).** En first-run el header se aligera (oculta subtítulo + botón de arriba) y el empty state lleva la explicación + el CTA. **No es un "Sin resultados" plano.** Contiene:

- **Mini-diagrama** (notificación fantasma → wires → previews de **Email** y **Slack**), que comunica "1 notificación llega por varios canales".
- **Plantillas para empezar** ("Incidentes confirmados de mis tableros", "Archivos faltantes o fallidos") que abren el editor **pre-llenado**.
- CTA primario **"Crear notificación"**.
- El diagrama va dentro de un frame **"Vista previa"** (tintado + caption + `pointer-events:none`) para que se lea como ilustración, no como UI clickeable; las plantillas/CTA quedan **fuera** del frame.
- **Motion pedagógico:** pulso de flujo (dashes en primario recorriendo los wires → enseña la dirección hacia los canales, loop 1.6s) + entrada escalonada (fade+rise, 320 ms ease-out, delays 0/70/140/210/280 ms). Solo `transform`/`opacity`/`stroke-dashoffset`; respeta `prefers-reduced-motion: reduce`.
- **Pendiente a futuro:** reemplazar el mini-diagrama por una **ilustración CSS más pulida** (hoy es un preview funcional interino).

**2.3 · Editor de paquete** (al crear/editar), con estos bloques **que no se interfieren** *(reestructurado 30-jun pm)*:

- **Nombre** de la notificación.
- **El alcance va en DOS bloques separados** (el Estado salió: se pisaba con el momento — changelog #5):
  - **Bloque 1 · "¿Qué entidades te interesan?"** → botón **"Agregar entidad"** (menú con buscador + lista de tableros/recursos, OR) + **botón de ícono (bookmark) "Aplicar un filtro guardado"** (menú con los filtros guardados, mismo patrón que "Guardados" de Gestión; al aplicarlo **solo se conservan Entidad y Tipo**, y Tablero/Recurso se colapsan a Entidad) + chips agrupados por Tablero / Recurso (a todo el ancho, apilados; cuando hay ambos grupos se unen con un **conector "o" a la izquierda**, estilo join de query builder BI).
  - **Bloque 2 · "¿Qué tipos de incidente?"** → **chips seleccionables** (multiselect OR) de las 5 categorías de BADS. Vacío = todos los tipos.
- **Bloque 3 · "¿Cuándo quieres que te avisemos?"** → dos **entregas** sobre el mismo alcance, combinables:
  - **Aviso por evento** (toggle): **momento(s) del ciclo de vida** del incidente, multiselección — **Cuando se cree** / **Cuando entre en observación** / **Cuando se confirme** / **Cuando se resuelva** + **Recibir actualizaciones** (toggle; reconfirmaciones, cambios de hipótesis, otros recursos afectados). *(Los estados del incidente se eligen aquí como momentos, no en el alcance, para no duplicarlos.)*
  - **Resumen consolidado** (toggle): **hora** + **zona horaria** (default 08:00 · CO Bogotá) + **"Qué período resume"** = **t-1 … t-5** con microcopy: *el corte siempre cierra el día anterior; la hora solo define cuándo llega, no qué período cubre*. 1×día, agrupa los incidentes del alcance.
- **Canales** → mismo patrón que el "¿Dónde notificar?" del KPI: **tarjetas de canal activables** (Email / Slack) con toggle; Email → destinatarios; Slack → canales + **Etiquetar a personas por ID de usuario** (no `@nombre`; nota "Copiar id. de miembro"). **Aplican a ambas entregas.** Si el canal está apagado, no se notifica por ahí.
- **Validación (al Guardar):** **Nombre obligatorio** (borde rojo + mensaje inline si falta); **≥1 entrega activa** (aviso por evento o resumen); si aviso por evento, **≥1 momento**; **≥1 canal activo**; y **cada canal activo con destinatarios** (Email on → ≥1 correo; Slack on → ≥1 canal). Los faltantes se listan en una alerta (`.an-pkg-warn`, ámbar) con encabezado singular/plural. Alcance (entidades/tipo) es opcional (vacío = todos).
- **Acciones:** Cancelar / Guardar notificación.

**2.4 · QUITADO del formulario anterior (no va):**

- Checkbox **"Cuando la severidad sea alta"** (severidad pospuesta; la asigna BADS).
- Checkbox **"Cuando no tenga responsable asignado"** (fuera de scope ahora).
- Checkbox **"Cuando me etiqueten"** → es **notificación de flujo de la app** ("te asignaron / te etiquetaron"), otro template, **otro feature**. No se configura aquí.
- Tarjeta **"Qué incluir en la notificación" (Hipótesis / Acción recomendada / Resumen / narrativa)** → eso va **directo en el template** (Block Kit / email), no es configurable por el usuario.
- **Resumen consolidado** ya **no** sale a una sección aparte. Vive **dentro del editor**, como segunda **entrega** del Bloque 3. Anula la decisión previa de "sección propia".

**2.5 · Lógica (para ingeniería, no es de este prototipo):**

- Incidente = evento. En cada evento (creación/update) se evalúan las reglas de todos los paquetes activos → match → notifica.
- Condiciones tipo filtro de Gmail; condiciones contradictorias → cero notificaciones (avisar visualmente si aplica).
- Anti-spam: por default, quien configura el paquete es quien recibe; agregar a terceros es explícito (en canales).

---

## 3. Fixes de UI de la vista de Anomalías (ya aplicados, enumerar en Figma)

- "Historial" → **"Alertas levantadas"** (+ columna **"¿Notificada?"** por alerta).
- "Notificaciones" → **"Alertas"** en el diálogo del KPI.
- Botón **"Resumen de incidentes"** sacado de la tab de monitoreo del tablero (vive en Anomalías).
- Segmented de Anomalías: **Gestión · Alertas levantadas · Configuración** (activo muestra icono + texto; inactivo solo icono).
- Botón de **configuración** dentro de la vista de Anomalías.
- Revisar diferencias de la **tarjeta de incidente** (Gestión) vs producción → si las hay, van como fix de UI aparte.

---

## 4. Historias de UX

> Criterios marcados **[F]** = funcional (sí/no), **[X]** = de experiencia.
> **Persona base:** operador de Operation Center (analista/ops de Simetrik) que vigila incidentes de varios clientes a la vez. Uso frecuente, a menudo bajo presión. Su miedo: perderse algo importante o, al revés, ahogarse en ruido.

### HU-2 · Crear mi primera notificación (first-run, sin partir de cero)

**Usuario:** operador que nunca ha configurado notificaciones.
**Contexto:** llega a Configuración → Notificaciones de incidentes y no tiene nada; no quiere leer un manual.

**Historia:** como operador que entra por primera vez y no sabe qué se puede configurar, quiero **ver de qué se trata** y empezar desde una plantilla razonable, para tener una notificación útil en segundos y entender el modelo de paso.

**Estados de interfaz**
- **Vacío / first-run:** título + explicación corta + **"Vista previa"** (diagrama ilustrativo: una notificación → Email y Slack, no clickeable) + **plantillas** ("Incidentes confirmados", "Archivos faltantes o fallidos") + CTA **"Crear notificación"**. (No "Sin resultados".)
- **Desde plantilla:** abre el editor **pre-llenado** (nombre + alcance + momento) listo para ajustar.
- **Desde cero:** editor en blanco.
- **Guardado:** vuelve a la **lista** con la tarjeta ya creada.

**Interacción / motion:** en la vista previa, **pulso de flujo** por los wires enseña la dirección (incidente → canales); entrada escalonada. Respeta `prefers-reduced-motion`. El diagrama es ilustración (`pointer-events:none`), separado de plantillas/CTA (que sí son accionables).

**Criterios**
- **[F]** "Usar" plantilla pre-llena alcance + momento del editor.
- **[X]** El operador entiende, sin instrucciones, que **una notificación llega por varios canales**.
- **[X]** Nunca enfrenta un formulario en blanco como primera opción.

### HU-3 · Definir el alcance de una notificación ("¿qué incidentes te interesan?")

**Usuario:** operador que solo quiere enterarse de cierto subconjunto.
**Contexto:** le importan los incidentes confirmados de sus tableros; el resto es ruido.

**Historia:** como operador que no quiere recibir todo, quiero describir **qué incidentes me importan** combinando filtros (o reusando uno guardado), elegir **en qué momento** del ciclo de vida me avisan y **por dónde**, para recibir solo lo relevante y confiar en que no me llega spam ni se me escapa lo urgente.

**Estados de interfaz (editor)**
- **Bloque 1 · "¿Qué entidades te interesan?":** botón **Agregar entidad** (menú multiselect, inline) **o** botón bookmark "aplica un filtro guardado"; abajo "Tu alcance" como chips. Alcance vacío = "Todos mis incidentes".
- **Bloque 2 · "¿Qué tipos de incidente?":** chips seleccionables de las 5 categorías.
- **Bloque 3 · "¿Cuándo te avisamos?":** momento(s) del ciclo de vida (Cuando se cree / entre en observación / se confirme / se resuelva) + toggle "Recibir actualizaciones" + toggle "Resumen consolidado".
- **Canales:** tarjetas activables **Email** / **Slack**; Slack incluye **Etiquetar por ID de usuario** con su nota.
- **Inválido:** si no hay momento o no hay canal, **aviso** "Esta notificación no avisaría de ningún incidente" y no guarda.

**Criterios**
- **[F]** Momento ↔ eventos BADS (creación / `status_changed→CONFIRMED`); updates ↔ `status_changed` posteriores.
- **[F]** Canal apagado no se envía; mención por **ID de Slack** (no `@nombre`).
- **[F]** Guardar bloqueado si falta momento o canal.
- **[X]** El operador percibe el paquete como **una regla suya** ("a mí, esto, así").

**a11y:** toggles como `Switch` (rol/estado), checkboxes con label asociado, hint como `Alert info`.

### HU-4 · Mantener mis notificaciones (lista, editar, duplicar, pausar, eliminar)

**Usuario:** operador con varias reglas ya creadas.
**Contexto:** quiere ajustar una, clonar una parecida o pausar temporalmente sin perder la config.

**Historia:** como operador que ya tiene varias notificaciones, quiero verlas de un vistazo y **editar / duplicar / pausar / eliminar** cada una, para mantener mis avisos al día sin rehacer trabajo.

**Estados de interfaz**
- **Lista:** tarjeta por notificación con nombre, resumen del alcance, **toggle activo/inactivo**, tags (momento · actualizaciones · canales) y acciones **Duplicar · Editar · Eliminar** (íconos en footer).
- **Inactiva:** tarjeta atenuada, toggle off.
- **Duplicar:** crea "… (copia)" y abre el editor (clonar una existente es la vía para reutilizar).

**Criterios**
- **[F]** Toggle activa/pausa sin entrar al editor.
- **[F]** Duplicar copia alcance, momento, updates y canales.
- **[X]** "Me gusta esta config, me la copio" se resuelve en 1 clic (Granola).
- **[X]** Sin concepto de dueño/equipo: se ven todas las configuradas, en una lista plana.

### HU-5 · Recibir un resumen consolidado diario de una notificación

> **Reencuadrada 30-jun pm:** el resumen ya **no** es un objeto/flujo aparte. Es una **segunda entrega** dentro de una notificación (HU-3): el operador, en el mismo editor, activa "Resumen consolidado" sobre el **mismo alcance y canales** que ya definió, elige **hora** y **período (t-n)**. Puede tener aviso por evento, resumen, o ambos. Los estados empty→activar→form→saved de la versión anterior quedan obsoletos.

**Usuario:** operador que no quiere notificaciones sueltas todo el día.
**Contexto:** prefiere un único consolidado a una hora fija, sin volver a definir el filtro.

**Historia:** como operador que se satura con avisos sueltos, quiero un **único resumen al día** de los incidentes que me importan, a la hora que elija, para mantenerme al tanto sin interrupciones constantes.

**Estados de interfaz**
- Toggle **"Resumen consolidado"** dentro del Bloque 3 del editor; al activarlo despliega su sub-form (hora · zona · t-n) con **defaults** ya puestos (08:00, CO·Bogotá).
- El card de la lista muestra el tag del resumen ("Resumen 08:00 · hasta hace 4 días (t-4)").
- Pausar = apagar el toggle; se guarda con el paquete.

**Criterios**
- **[F]** El resumen es **distinto** de las notificaciones por evento: es **1×día** (no por `status_changed`).
- **[F]** Reutiliza el mismo alcance y los mismos canales del paquete (incl. ID de Slack); no se redefine.
- **[X]** El operador entiende, en la vista previa, que **muchas incidencias se agrupan en un solo aviso**.

### Notas transversales (todas las historias)

- **Glosario:** incidente, señal/alerta, tablero, KPI; **monitoreo** de cara al usuario (nunca "agente/IA").
- **Severidad** no se expone (la asigna BADS) hasta que sea configurable.
- **Desktop-only** (shell de Operation Center). Columna de lista de Anomalías ~384px; el detalle a la derecha.
- **Loading/empty/error** de datos reales: skeleton con forma (no spinner); empty states activos (ya definidos); error con mensaje que diga qué pasó y qué hacer.

> **Referencia (fuera de scope de este handoff):** **HU-1** (filtrar incidentes por varios valores y guardar ese filtro) vive en **Handoff 1** (filtros de la vista de Gestión). Los filtros guardados que HU-3 reutiliza se crean allí.

---

## 5. Plantillas del resumen (Email MJML + Slack Block Kit)

> **Origen:** `notificaciones-resumen/templates.html` (prototipo validado, 26-jun). Dos plantillas: **Email · "Sin gráfica"** (MJML) y **Slack · Block Kit · ultra-compact**, armadas **1:1 desde el JSON del detector (BADS)**.
> **Regla base (no negociable):** el contenido sale 1:1 del `bads_payload`. Texto **verbatim**; la única transformación permitida es **elegir idioma** (`es`/`en`/`pt`, fallback `en`) y **resolver los marcadores `[n]`** con `references[]`. No se genera ni reescribe texto, no se fabrican campos.
> El resumen **no lo genera una IA**: reutiliza los textos ya generados de cada incidente. No introducir copy de "agente/IA".

### 5.1 · Flujo end-to-end (del JSON a la notificación)

Separar tres cosas: el **QUÉ** (`bads_payload`), el **A QUIÉN/DÓNDE** (config: canal + `slack_id`), el **CÓMO se ve** (MJML / Block Kit). El detector no sabe de Email/Slack; Email/Slack no saben del `bads_payload`. En el medio, el **servicio de notificaciones** parsea y renderiza por canal.

```
[1] Detector BADS  ─▶  [2] JSON bads_payload  ─▶  [3] Servicio notif. (parsea)  ─▶  ├─ [4a] MJML       ─▶  [5a] Cliente de correo
    genera incidente       status: OPEN,             parse(payload, lang)            └─ [4b] Block Kit  ─▶  [5b] Slack
    emite evento           findings, actions         + render por canal
                                                            ▲
                                                Config del paquete: canal + slack_id
```

1. **Se genera el incidente** — el detector (`workflow_type: ingestion_analysis`) crea los `findings`, arma el `bads_payload` (`schema_version 1.7`), persiste el incidente (`status: OPEN`) y emite un evento.
2. **Sale como JSON** — dos vías: **push** (el evento dispara la notificación por evento en tiempo real) y **pull** (`GET results[]` filtrando `OPEN` + día, para el **resumen**).
3. **El servicio de notificaciones parsea** — backend, no el front ni el cliente. Lee la config, toma el `bads_payload`, elige idioma, resuelve `[n]`, agrupa por recurso y produce un modelo normalizado.
4. **Render por canal** (mismo parseo, distinto renderer): Email → MJML; Slack → Block Kit (ultra-compact).
5. **Envío al destino** — Email: notification center / SMTP (sin imagen en la variante sin gráfica). Slack: `chat.postMessage` con `channel` + etiqueta `slack_id`.

> Aplica igual a las dos notificaciones del JSON: por evento (1 incidente) y resumen (N incidentes, `results[]` filtrado). Solo cambia cuántos incidentes entran al parser.

### 5.2 · Parser compartido (agnóstico de canal) — snippet verbatim

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

**Qué usa cada canal del modelo:** Email **sin gráfica** usa casi todo (narrativa + acciones + impacto). Slack **ultra-compact** usa el mínimo: `title` + `category` + `severity` + `confidence`.

### 5.3 · Plantilla A — Email (sin gráfica, MJML)

Tecnología: **MJML** (registrado en el notification center). Estructura fija (loop sobre incidentes); solo se parametrizan textos y enlaces. Es la variante **más segura de entregar** (no depende de render de imagen); es el fallback canónico del email.

**Estructura (de arriba a abajo)**
1. **Barra de marca:** logo Simetrik + "Centro de Operaciones". *(chrome, fijo)*
2. **H1:** "Resumen diario". **Intro:** "Incidentes abiertos (status OPEN), agrupados por la fuente de datos afectada."
3. **Stats (3 tarjetas):** `count(URGENT)` · `count(REQUIRES_ATTENTION)` · `count(fuentes)`.
4. **Label de sección:** "INCIDENTES POR FUENTE".
5. **Por cada fuente** (`scope.resource_refs`): encabezado = `resource_name`; sub = `resource_type`. **Por cada `finding`** → una tarjeta con: badge de **severidad** + chip de **categoría**; **título** (verbatim); **narrativa** (`summary`, verbatim, es el cuerpo; no hay gráfica); **confianza** (`confidence` numérico + `hypothesis.confidence` enum); chip **"afecta N tableros"** si `affected_dashboards_count > 0`; **botones** (= `recommended_actions[]`, ver §5.5); **timestamp** (`executed_at`).
6. **"+N incidentes más, ver todos en el Centro de Operaciones"** (manejo de volumen, top-N).
7. **Disclaimer** + **footer** (motivo del envío + link "Centro de Operaciones › Resumen diario").

**Reglas email:** sin SVG ni JS (los clientes los bloquean); todo el cuerpo entendible en texto plano; **light only** (los emails no tienen dark mode confiable). Las métricas (esperados/llegaron/faltan/%) viven dentro de `summary`; **no** parsear la narrativa con regex para fabricar chips.

### 5.4 · Plantilla B — Slack Block Kit (ultra-compact)

Tecnología: **Slack Block Kit** (`blocks[]`), enviado como **mensaje**. Es la variante más densa/escaneable: una línea por incidente (título) + tags. Sin summary ni botones por incidente.

**Estructura**
1. **`section`** (header): `🚨 *Resumen diario · N incidentes abiertos (M fuentes)*`.
2. **`context`** (conteo): `*X* URGENT · *Y* REQUIRES_ATTENTION`.
3. **`divider`**.
4. **Por cada `finding`** (lista plana, incidente primero): **`section`** = el incidente (`*title*` verbatim; puede ir como link `*<{go_to.target_url}|{title}>*` si hay acción `go_to`); **`context`** = tags `` `problem_category` · {severity} · {confidence} ``. Sin `summary`, sin botones.

**Block Kit JSON (esqueleto, verbatim desde el JSON)**
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

**Notas Slack:** sin imagen en v1 (pendiente con Iván). Etiquetado (si la config lo pide): se arroba por `slack_id` (viene de la config), no por `@nombre`.

### 5.5 · Botones / acciones (solo Email)

Salen de `recommended_actions[]`. Solo pinta botón la acción que trae `action_ref.label`; las que solo traen `resource_ref` (ej. `REVIEW_DATA_SOURCE`) no pintan botón. Orden por `priority`.

| Opción (`label.es`) | `action_type` | Comportamiento |
|---|---|---|
| **Abrir** | `go_to` | abre el `target` (deep link `app.simetrik.com/...`) |
| **Crear ticket** | `create_support_ticket` | abre flujo de ticket con `body[lang]` prellenado |
| **Enviar mensaje** | `send_message` | redacta al proveedor con `body[lang]` prellenado |

(ultra-compact omite botones; el título-link cubre el "abrir".)

### 5.6 · Copy chrome (glosario aplicado)

Lo único que NO viene del JSON. Glosario Op Center, sin em-dashes:

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
> **Severidad** se muestra como enum crudo (`URGENT`/`REQUIRES_ATTENTION`): aceptable en Op Center. Si se localiza, mapear (`URGENT`→"Urgente", `REQUIRES_ATTENTION`→"Requiere atención") en una sola capa, no en la narrativa.
> Títulos y narrativas son verbatim del detector y **sí** contienen em-dashes / mayúsculas; eso es del payload, no se edita.

### 5.7 · Estados de las plantillas

| Estado | Email sin gráfica | Slack ultra-compact |
|---|---|---|
| **0 incidentes OPEN del día** | No enviar (o variante "Sin novedades hoy" si producto lo pide) | Igual |
| **1 incidente** | 1 fuente, 1 tarjeta | header "1 incidente (1 fuente)" + 1 línea |
| **Muchos** | top-N tarjetas + "+N más, ver todos" | top-N líneas + "+N más" |
| **Fuente con varios `findings`** | varias tarjetas bajo la misma fuente | varias líneas seguidas (lista plana) |
| **Sin `recommended_actions` con label** | tarjeta sin botones (solo "Abrir incidente" si hay `go_to`) | n/a |
| **`coverage_dates` vacío** | usar `executed_at` como fecha; no romper | igual |
| **Idioma faltante** | fallback `en` | fallback `en` |

### 5.8 · Anexo — Ejemplo real (1 incidente del `bads_payload`, recortado)

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

---

## 6. Guía de implementación

### 6.1 · Motor de notificación (§B) — eventos

Flujo real: **`oc-bads-incident`** (Pulsar) → **op-center-backend** evalúa cada evento contra las **reglas activas** (nuestros "paquetes") → **`notifications-service`** → Sphere (**SES / Slack / Pusher in-app**).

- Cada **paquete = filtro (scope) + momento (evento del ciclo de vida) + updates + canales**. Evaluación tipo filtro de Gmail por evento.
- **Momento → eventos del incidente (multiselección):** "Cuando se cree" = creación (`OPEN`/`WATCHING`); "Cuando entre en observación" = `status_changed → WATCHING`/`UNDER_INVESTIGATION`; "Cuando se confirme" = `status_changed → CONFIRMED`; "Cuando se resuelva" = `status_changed → RESOLVED`. "Updates" = `status_changed`/reconfirmación/`MERGED`.
- Binding **N:M** (un incidente puede notificar por varios canales; un canal sirve a varias reglas).
- Backend ya define: **idempotencia** `X-Simetrik-Delivery-Id: {uuid}`, **retry** 3 intentos backoff (1s/5s/25s) Slack/webhook, **`webhook_delivery_log`**. El FE no maneja esto, pero el "qué se envía" debe calzar con el payload de `notifications-service`.

### 6.2 · Shape del "paquete" (§C) — guía FE

Estado que mantiene el prototipo *(modelo 30-jun pm: scope sin Estado; entregas realtime + digest)*:
```jsonc
{
  "id": "uuid",
  "name": "Incidentes de Adquirencia",
  "scope": [                       // SOLO entidades + tipo; ver lógica O/Y
    { "type": "Entidad", "value": "Adquirencia" },     // tablero o recurso → resolver a sus resources
    { "type": "Tipo",    "value": "Archivo faltante" } // → incident.problem_category IN [...]
  ],
  "realtime": {                    // entrega por evento (opcional)
    "enabled": true,
    "created": true, "watching": false, "confirmed": true, "resolved": false,  // momento(s) del ciclo de vida (≥1 si enabled)
    "updates": true                       // recibir status_changed posteriores
  },
  "digest": {                      // entrega consolidada 1×día (opcional) — mismo scope + canales
    "enabled": true,
    "hora": "08:00", "zona": "CO · Bogotá (GMT-5)",
    "tn": 4                              // período: cierra a t-n (1..5). Corte SIEMPRE día anterior; hora ≠ período
  },
  "channels": {                    // aplican a ambas entregas
    "emails":   ["ana.torres@simetrik.com"],          // SES
    "slack":    ["#incidentes-finops"],               // Slack webhook (canales)
    "mentions": ["U01ABC23DEF"]                        // Slack user IDs (no @nombre)
  },
  "active": true
}
```
- **Validación FE:** `realtime.enabled || digest.enabled`; si `realtime.enabled` → `created || watching || confirmed || resolved`; `channels.emails.length || channels.slack.length`.
- **`Entidad`** = tablero **o** recurso. El backend resuelve un tablero a sus resources; todos los `Entidad` del scope se combinan con **OR** entre sí (no jerárquico, no AND tablero∧recurso).
- **Filtro "Tipo" → `incident.problem_category`** (catálogo cerrado de Ingesta): Archivo faltante `MISSING_FILE` · Archivo fallido `FAILED_FILE` · Archivo vacío `UNEXPECTED_EMPTY_FILE` · Archivo duplicado `DUPLICATED_FILE` · Variación de volumen `VOLUME_VARIATION`. Confirmar string exacto de `MISSING_FILE`/`FAILED_FILE`/`VOLUME_VARIATION` con backend BADS.
- **Severidad** (`URGENT` / `REQUIRES_ATTENTION`) la asigna el workflow runner de BADS, no es configurable → por eso el filtro Severidad y la condición "severidad alta" se quitaron.

### 6.3 · Mapeo a componentes desyk (§E) — filas de notificaciones

Refs: `fe-solutions-mf/.../skills/desyk/references/`.
| Patrón del proto | Componente desyk | Nota |
|---|---|---|
| Toggle on/off (activo, canal, updates, pausar) | **`Switch`** | reemplaza `.tm-notif-row-toggle`; `checked`/`onCheckedChange` + `role=switch` nativo |
| Tarjeta (paquete, config, canal) | **`Card`** (+ `CardHeader/Title/Content/Footer`) | |
| Dropdown (filtro guardado, incluir, zona horaria) | **`Select`** | |
| Chips de correos / canales / menciones | **`Combobox`** + render de chips | desyk no tiene token-input dedicado; Combobox con búsqueda + chips custom |
| Tabs de modo (Gestión/Alertas/Config) | **`Tabs`** o **`UnderlineTabs`** | |
| Checkbox (momento) | **`Checkbox`** | `checked: boolean \| "indeterminate"` |
| Botones (Crear, Guardar, Usar, Editar) | **`Button`** | variantes default/secondary/ghost/destructive; iconos con `size=icon-*` |
| Empty state / first-run | **`EmptyState`** (`EmptyStateTitle/Description/Content`) | reemplaza `.an-onb-*`; el diagrama va como contenido ilustrativo |
| Nota de ID de Slack | **`Alert` variant `info`** | reemplaza `.tm-notif-hint` |
| Aviso "regla no notifica nada" | **`Alert` variant `warning`** | reemplaza `.an-pkg-warn` |
| Estado/severidad como chip | **`Badge`** (variants success/warning/info/destructive) | |
| Menús de Filtrar/Ordenar/Guardados | **`Popover`** | |
| Tooltip de íconos | **`Tooltip`** | |

### 6.4 · Máquinas de estado (§F)

**Notificaciones de incidentes:** `lista` ⇄ `editor`. Entradas al editor: Crear (vacío), Usar plantilla (pre-llenado), Editar (carga el paquete), Duplicar (clona "… (copia)" → editor). Guardar válido → vuelve a `lista`. Lista vacía → **empty state** (no "Sin resultados").

**Resumen consolidado (entrega del paquete, 30-jun pm):** ya no es una máquina de 3 estados aparte. Es un **toggle** dentro del editor (`digest.enabled`) que despliega su sub-form (hora · zona · t-n). Se guarda con el paquete; el card de la lista muestra su tag.

### 6.5 · Validaciones / edge cases (§G)

- **Reglas de validación** (bloquear Guardar + `Alert warning`): **Nombre obligatorio**; **≥1 entrega activa** (aviso por evento o resumen); si aviso por evento, **≥1 momento** (created/watching/confirmed/resolved); **≥1 canal activo**; **cada canal activo con destinatarios** (Email→≥1 correo, Slack→≥1 canal). Una mención sin canal de Slack no entrega.
- **Scope vacío** = "Todos mis incidentes" (válido, no es error).
- Canal con toggle **apagado** → no se leen sus destinatarios al guardar.
- Severidad: no exponer como filtro ni condición (system-assigned).

### 6.6 · Motion y a11y (§H)

- Durations canónicas **120 / 200 / 320 ms**, **ease-out exponential** `cubic-bezier(0.22,1,0.36,1)`. Solo `transform`/`opacity`/`stroke-dashoffset`.
- Empty states: **pulso de flujo** (dashes recorriendo los wires, enseña dirección incidente→canales) + entrada escalonada. Diagrama `pointer-events:none` (ilustración, no UI) dentro de frame "Vista previa".
- **`@media (prefers-reduced-motion: reduce)`** desactiva las animaciones.
- **Skeleton** con forma sobre spinner en loading. **Light mode.**
- a11y: `Switch`/`Checkbox`/`Button` de desyk traen roles/aria; chips con `aria-label="Quitar"`; labels asociados (`for`/`id`) — obligatorio en la implementación.

---

## 7. Nota de deprecación — Épica 3 (resumen consolidado como sección propia) → ANULADA

> **Superseded el 30-jun pm.** En el design review con ingeniería (Sergio) se decidió mover el resumen **dentro del paquete de notificación**, porque como sección aparte obligaba a **repetir el filtro** y permitía resumir algo distinto a lo que se notifica en tiempo real. Ya **no** hay ítem de nav "Resumen consolidado" ni página independiente.
>
> El resumen vive como **segunda entrega** del editor de paquete (§2.3, Bloque 3): mismo **alcance** y mismos **canales** heredados del grupo, + hora + zona + **t-n** (1…5). Ver changelog #2 y #3. Esta épica se elimina del plan de ingeniería; su funcionalidad se absorbe en la Épica de Paquetes.

### Fuera de scope (documentado)

- Notificaciones de **flujo de la app** (asignación/etiquetado) — otro template, otro feature.
- **Severidad** como filtro o condición (hasta que sea configurable).
- Preview "con esta config tendrías X notificaciones" (deprioritizado).
- Del handoff de plantillas: **Email con gráfica** (depende de render PNG server-side, pendiente), **Slack `default`/`compact`**, la **vista modal** ("ver todos"), y el chrome de Santiago (`X-Slack-Template`, acciones a nivel mensaje, `mark_as_seen`, `x-slack-responsible`).

### Pendiente / a validar

- Visto bueno de **Cami** antes de entregar a **Edith**.
- Lógica de evaluación **tiempo real vs lote** — eng.
- Confirmación "al cierre de ventana" vs **workflow runner** (Iván).
- ID de usuario de Slack como **parámetro del template** (Iván) antes de comprometer el etiquetado; **2 templates** (creación vs updates); desacoplar en el listener la lógica compartida señales/incidentes.
- **Unificar construcción de títulos** de notificaciones/templates → se resuelve en la respuesta del API (cómo se arma el título del incidente), no es UI.

---

## 8. Checklist pre-implementación

**Paquetes de notificación (lista + editor)**
- [ ] Vista de lista plana con tarjeta (nombre, resumen del alcance, toggle activo, tags de entrega, Duplicar/Editar/Eliminar) + botón "Crear notificación".
- [ ] Empty state / first-run con mini-diagrama en frame "Vista previa" (`pointer-events:none`), plantillas pre-llenadas y CTA fuera del frame.
- [ ] Motion pedagógico del empty state (pulso de flujo + entrada escalonada) con `prefers-reduced-motion`.
- [ ] Editor con Bloque 1 (entidades, OR + filtro guardado que colapsa a Entidad), Bloque 2 (tipos, chips OR), Bloque 3 (dos entregas: aviso por evento + resumen), Canales.
- [ ] Elementos QUITADOS no reaparecen (severidad alta, sin responsable, "cuando me etiqueten", "qué incluir").
- [ ] Validación completa al Guardar (nombre, ≥1 entrega, ≥1 momento si por evento, ≥1 canal, canal con destinatarios) con `Alert warning`.
- [ ] Duplicar clona config → "… (copia)" → editor.

**Fixes de UI de Anomalías**
- [ ] Renombres: "Historial"→"Alertas levantadas" (+ columna "¿Notificada?"), "Notificaciones"→"Alertas" en el KPI.
- [ ] Segmented Gestión · Alertas levantadas · Configuración (activo icono+texto, inactivo solo icono).
- [ ] Botón de configuración dentro de Anomalías; botón "Resumen de incidentes" fuera de la tab del tablero.
- [ ] Revisar tarjeta de incidente (Gestión) vs producción.

**Plantillas del resumen**
- [ ] Contenido **1:1 del `bads_payload`** (title/summary/labels verbatim); única transformación: idioma + resolver `[n]`.
- [ ] Sin chrome de Santiago.
- [ ] Glosario aplicado en chrome (`tablero`, `Fuente`, `Incidente`, `Espacio de trabajo`); sin em-dashes en copy propio. Fix `templates.html`: "afecta 1 dashboard" → "tablero".
- [ ] `resource_id` no visible (solo en URL/target).
- [ ] Botones solo desde `recommended_actions` con `label`; orden por `priority`.
- [ ] ultra-compact: sin summary, sin botones, sin imagen; severidad como tag de color.
- [ ] Email sin gráfica: sin SVG/JS; legible en texto plano; light only.
- [ ] Estados: 0 incidentes (no enviar), 1, muchos (top-N). Conteos del header = count real.

**Datos y backend**
- [ ] Momento(s) ↔ eventos BADS del ciclo de vida; updates ↔ `status_changed`.
- [ ] Shape del paquete (scope/realtime/digest/channels/active) calza con `notifications-service`.
- [ ] Idempotencia/retry manejados por backend; FE solo produce el paquete válido.
- [ ] Componentes desyk canónicos (Switch, Card, Select, Combobox, Tabs, Checkbox, Button, EmptyState, Alert, Badge, Popover, Tooltip).
- [ ] a11y: roles/estado en toggles y checkboxes, labels asociados, `aria-label` en chips.
