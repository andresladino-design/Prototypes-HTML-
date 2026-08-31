# Memoria del proyecto — Contracargos

**Volcado:** 26-ago-2026 · **Origen:** `~/.claude/projects/-Users-andres94ladino-Simetrik-UxTeam-Prototypes-HTML/memory/`

## Qué es este archivo

Claude mantiene una memoria persistente de este workspace: un archivo por hecho, con su índice en `MEMORY.md`. Esa memoria vive fuera del repo y solo la ve Claude al arrancar una sesión. Este documento la vuelca completa y legible, filtrada por lo que aplica a contracargos, para que el equipo la pueda leer, corregir y discutir.

**Es un espejo, no la fuente.** La fuente sigue siendo la carpeta de memoria. Si acá hay algo mal, hay que arreglarlo en los dos lados.

---

## 1 · Memoria núcleo del proyecto

> `disputas-contexto.md` · tipo: `project`

Proyecto con **Andrea Giraldo** (Product Engineering Manager) + **Santi** (backend del skill) + **Vicky** (decide producto). Estructura Ohana.

✅ **Consolidado el 26-ago-2026 en `Prototypes_HTML/contracargos/`.** Los 7 planes de julio, su `design.md` y el board de Moka se migraron desde `Disputas/`, que ya no existe. Los planes históricos viven en `plans/archivo-julio-2026/`.

**Problema:** los ~11 marketplaces de Simetrik (Rappi, PedidosYa, iFood, Falabella) reciben contracargos por SFTP, en archivos `notificados` y `debitados`, o como una columna de estado en una sola base. No tienen dónde verlos: el control se entrega como export que el cliente baja y mole en otra herramienta.

**Reacote del 26-ago-2026** (sesión Wispr "Ladi - Andre chargebacks"), que **supera** lo acordado en julio: el rol primario pasa de PSP adquirente a **merchant / marketplace**. Sigue vigente lo demás: emisor fuera, sin win rate ni "$ recuperado" agregados, monitoreo vía el modelo de paquetes. Se suma: la vista gerencial de pérdidas queda fuera del alcance inicial.

**La pregunta que Andrea pidió resolver:** no rediseñar el centro de disputas, sino **cómo se llega al tablero**. Cuatro rutas: CLI, Simetrik Agent, sugerencia en el Operation Center, template en Marketplace.

**Dato técnico clave** (aporte de Ladi en esa sesión): el monitoreo necesita el dato de negocio en una **columna normalizada del dataset**, y se activan **dos** monitoreos, sobre esa columna y sobre **la fuente**, porque sin la fuente no se puede distinguir una anomalía real de un archivo que no llegó.

**Insumos de Andrea:** el prototipo `Simetrik · Centro de Disputas — Operations Center.html` (2.011 líneas, vanilla JS, se conserva como spec de contenido y se rehace sobre desyk), el Figma "Ideación 2.9 — DO", y el competidor de referencia `app.chargeflow.io/prevent` (de donde sale el ChargeScore).

**Por qué está en memoria:** es contexto de negocio no derivable del repo, y el cambio de rol primario contradice los planes de julio que siguen escritos en disco.

---

## 2 · Memorias heredadas que aplican acá

Ninguna de estas nació en contracargos. Vienen del trabajo de notificaciones y del Operation Center, y aplican por reutilización.

### 2.1 · Modelo de paquetes para notificaciones
> `notif-resumen-modelo-paquetes.md` · tipo: `project` · origen: Granola 30-jun-2026

Las notificaciones de incidentes **no son una configuración global**, son un **modelo de paquetes (reglas) por usuario**. Se crean varias notificaciones; un incidente se evalúa contra todas las activas, con lógica tipo filtro de Gmail; si machea varias, notifica por todas esas vías.

Correcciones de Andres sobre ese modelo:
- La lista es **plana**. No hay dueño ni equipo, no va "Mías / Del equipo" ni avatar de dueño ni "Agregarme". Se muestran todas y ya.
- **Duplicar / clonar sí va** ("me gusta esta config, me la copio").
- **Tablero y Recurso se fusionan en un solo bloque "Entidades afectadas"** con lógica OR, porque tratarlos como filtros planos jerárquicos dejaba armar condiciones imposibles. Esto es **solo del editor de notificación**, no de los filtros de la vista de Gestión, que quedaron como estaban.
- El **resumen consolidado es una propiedad del paquete**, no una sección propia: dentro de "¿Cuándo te avisamos?" hay dos entregas sobre el mismo alcance, en tiempo real y resumen consolidado 1×día.
- El **estado sale del alcance** del paquete. Alcance = entidades + tipo; el momento va aparte.
- Se **quita Severidad** de los filtros hasta que sea configurable.
- Slider de sensibilidad: se quita "nula", los extremos son "Solo mi umbral" y "Detección adaptativa".

Modelo implementado: `{name, scope:[entidad|tipo], realtime:{enabled,created,confirmed,updates}, digest:{enabled,hora,zona,tn}, channels, active}`. Validación: al menos una entrega, y si es realtime al menos un momento y un canal.

**Cómo aplica acá:** el monitoreo de contracargos **no diseña un sistema paralelo**. Las reglas de este dominio (distancia al umbral de red, débito diario sobre lo aprendido, reason code disparado, fuente sin llegar) son tipos de regla dentro de este modelo. Es la decisión 5 de julio, que sigue vigente.

### 2.2 · El copy no dice "agente"
> `notif-resumen-no-agente.md` · tipo: `feedback`

En el prototipo de notificaciones, el copy de cara al usuario **no usa "agente" ni "Agente IA"**. En vez de "el agente detecta / analiza", se dice **"el monitoreo"**, o voz pasiva. Andres corrigió un empty state que decía "El agente seguirá analizando…" → "El monitoreo seguirá analizando…", y fue explícito: *"no usamos el concepto de agentes aquí"*.

Nota de la propia memoria: los handoffs de notificaciones **todavía dicen "Agente IA"** en el glosario, así que quedó inconsistente y hay que confirmar si se barren también.

**Cómo aplica acá:** el `design.md` de contracargos ya adopta "monitoreo" por defecto y lo marca como pendiente de confirmar con Andrea. Ojo con la tensión: el glosario oficial de `simetrik-ui` **sí** lista "Agente IA" como término correcto para Op Center. Gana la corrección de Andres hasta que él diga lo contrario.

### 2.3 · Payload real del detector (BADS)
> `notif-resumen-payload-real.md` · tipo: `project`

Shape real del incidente que produce el detector de anomalías, alineado el 25-jun-2026 con los Block Kit que mandó Santiago Quintero:

- Agrupado por `scope.resource_refs[]` → `resource_name`, `resource_id`, `resource_type`.
- `findings[]` con `title` y `summary` **generados por IA** (con `ai_provenance` → claude-sonnet en Bedrock), en es / en / pt. La narrativa **sí** es IA; lo auditable son las métricas dentro del texto.
- `severity`: `URGENT` (rojo) / `REQUIRES_ATTENTION` (ámbar). `status`: `OPEN`.
- Confianza doble: `finding.confidence` numérica 0–1, y `hypothesis.confidence` como enum `INDICATIVE` / `PROBABLE` / `CONFIRMED`.
- `problem_category`: `MISSING_FILE`, `VOLUME_VARIATION`, `UNEXPECTED_NULL_COLUMN`.
- `recommended_actions[]` → **botones**: `go_to` (Abrir), `create_support_ticket` (Crear ticket, con `body` pre-llenado), `send_message` (Enviar mensaje). Ordenados por `priority`.
- Marcadores `[1][2][4]` en el texto se resuelven contra `references[]` por `ref_id`.
- `blast_radius` / `affected_dashboards_count` → "Afecta N dashboards".

**Regla dura:** en las plantillas **no se genera texto nuevo**. Todo se muestra verbatim del JSON; la única transformación permitida es resolver los marcadores a `resource_name`. No fabricar chips de métricas, IDs ni líneas de "Resumen / Acción recomendada" que no estén en el payload.

**Cómo aplica acá:** es el patrón de los bloques AI del tablero de contracargos. La narrativa, la confianza y los botones de acción recomendada salen de esta misma forma. Además explica por qué en el `design.md` el gradiente AI marca **solo lo inferido**: hay que poder distinguir el texto generado del dato auditable.

### 2.4 · Los handoffs van antes → después
> `notif-resumen-handoff-antes-despues.md` · tipo: `feedback`

Un cambio del prototipo vale como tal **solo si se enumera contra el estado actual de producción**. Describir la propuesta no basta: hay que dejar el **antes → después** explícito, o el dev no lo construye. Prod vive en `/Users/andres94ladino/Simetrik/fe-solutions-mf`.

Surgió porque Andres señaló que el nav de Configuración del prototipo "es diferente vs el repo" y el handoff describía el estado propuesto sin marcar que reemplazaba lo actual.

**Cómo aplica acá:** cuando llegue el momento de `handoff/`, cada cambio se escribe contra lo que hoy existe en el Operation Center y en el Marketplace, no en abstracto. Aplica en particular a la ruta 4 de acceso, que toca el flujo de instalación de templates que ya está en producción.

### 2.5 · Épicas por sistema en Linear
> `linear-epicas-por-sistema.md` · tipo: `feedback` · decisión de reunión 2-jul-2026

En Linear la documentación va **ligera**: en vez de pegar el spec, se vincula el repo y los links al handoff. El detalle vive versionado en el handoff, no en Linear.

En el issue épico se **documentan los sistemas que intervienen** y se **listan los sub-issues por sistema**: OC backend (`op-center-backend`), Frontend Solutions (`fe-solutions-mf`), BATs / BADS (el detector), Graph Service (catálogo de recursos y tableros, `/graph/resources`).

**Formato obligatorio en cada issue**, épica y sub-issue: cuatro secciones cortas de 1–2 líneas — **Contexto**, **Objetivo**, **Alcance** (qué incluye y qué sistema), **Resultado esperado** — más una línea `Ref:` al handoff.

**Cómo aplica acá:** contracargos suma un sistema nuevo a esa lista, el **skill del Simetrik Agent** que está armando Santi. Cuando esto se cargue a Linear, ese es un sub-issue propio.

### 2.6 · Workflow de Ohana / Moka
> `ohana-moka-workflow.md` · tipo: `reference` · jul-2026

Ohana (MCP `ohana-comments`) ya no es solo comentarios: gestiona proyectos de diseño con boards tipo Moka.

**Estructura de proyecto:** `prototipos/` (HTML autocontenidos, uno por flujo), `planes/` (planes .md antes de ejecutar), `handoff/` (docs exportables), `design/` más `design.md` en la raíz, y `.ohana/flow.json` (los boards, **nunca editar a mano**).

**Flujos y sitemaps:** layout automático, **nunca poner coordenadas x/y**. Arrancar la sesión con `ohana_status` y leer `ohana_flow_guide` antes de construir. Un user flow es una secuencia horizontal que empieza con `kind:"start"` y termina cada camino con `kind:"end"`; las bifurcaciones son un paso `kind:"decision"` más un `ohana_flow_add_branch` por salida. Colores de edge: verde para sí / éxito, rojo para no / error, azul para normal. Regla de oro: usar las tools de intención (`add_step` / `add_branch` / `add_page`), que conectan solas; si se usa `add_screen` o `connect` directo, llamar `ohana_flow_layout` al final. El prototipo se enlaza al board con `ohana_flow_set_proto`.

**Gotcha:** con el previewer abierto, el flow activo vuelve solo al que el usuario tiene en pantalla, así que el `active` que devuelve `ohana_flow_new` no es confiable. Verificar con `ohana_flow_list` **antes** de construir. No hay tools para renombrar ni borrar flows, eso se hace desde la UI.

**⚠️ Corrección a esta memoria (26-ago):** la convención registrada dice `prototipos/` y `planes/` en español. Pero Ohana scaffoldeó `contracargos/` con **`prototypes/` y `plans/` en inglés**, con el mismo timestamp que `.ohana/`. O sea que la convención cambió y la memoria quedó desactualizada. Se adopta el inglés, que es lo que genera la herramienta hoy.

### 2.7 · Forma de trabajo de Andres
> `forma-de-trabajo-andres.md` · tipo: `feedback`

Ante un problema de diseño no trivial: **investigar el estándar y los patrones primero**, **presentar varias alternativas con pros, contras y una recomendación**, y **que decida Andres**. No saltar directo a una solución. La memoria registra que rechazó dos soluciones propuestas al vuelo antes de pedir que se investigaran patrones.

Para recoger feedback de terceros antes del handoff le gustan las **demos A/B**: dos alternativas vivas con un switch para alternar, más una nota visible aclarando que es demostrativo y que en el handoff queda una sola.

**Por qué:** valora la velocidad, pero no a costa de saltarse la exploración; las soluciones improvisadas no le aterrizan.

**Cómo aplica acá:** es la razón de que `01-spec-acceso-al-tablero.md` compare cuatro rutas contra criterios en vez de proponer una, y de que el prototipo del viernes sea un A/B/C con switch. Coincide además con la Ley 0 del skill `simetrik-ui`, que exige discovery socrático y 2–3 patrones con trade-offs antes de generar diseño.

### 2.8 · Convención y publicación del repo
> `prototypes-html-repo-convention.md` + `prototypes-html-git-publish.md`

Repo `andresladino-design/Prototypes-HTML-`, en `Simetrik/UxTeam/Prototypes_HTML`.

- El trabajo del Operation Center / Anomaly Management **no va como prototipo suelto en la raíz**: va en `ops-roadmap/<##-nombre>/` con un `README.md` estructurado (Qué se necesita · Estado en Linear · Contexto Brain · Gap UX) y un `mock.html`. Andres corrigió esto una vez y hubo que reubicar carpetas en un PR.
- Los prototipos top-level son solo los grandes: `monitor-anomaly-recon/`, `config-system-kpi/`.
- GitHub Pages sirve desde **`main` / raíz** → `https://andresladino-design.github.io/Prototypes-HTML-/`. El deploy tarda ~1 min tras el merge.
- **Cuentas git:** hay dos en `gh`. Solo **`andresladino-design`** tiene push. Si da 403: `gh auth switch --user andresladino-design && gh auth setup-git`.
- `.gitignore` excluye `.claude/` y `.ohana/`. Nunca subirlos.
- Andres prefiere **flujo por Pull Request**, no commits directos a main.

**⚠️ Tensión sin resolver:** la convención dice que el trabajo de Operation Center va en `ops-roadmap/<##-nombre>/`. Contracargos es Operation Center y **no** está ahí, está como carpeta suelta. Puede ser correcto (es un proyecto Ohana propio, no un item del roadmap de anomalías), pero conviene confirmarlo antes de publicar.

---

## 3 · Memorias del workspace que no aplican a contracargos

Se listan para que el volcado esté completo.

| Memoria | Por qué no aplica |
|---|---|
| `notif-resumen-alcance` | Alcance del diálogo de monitoreo de notificaciones, otro prototipo |
| `startup-exp-team-repo` | Repo git independiente anidado en Prototypes_HTML, sin relación |
| `investigacion-usuarios-simetrik` | Investigación de perfiles de usuario en Startup-exp-team |

---

## 4 · Lo que NO está en memoria y sí en este repo

La memoria guarda lo que no es derivable del código ni del historial. Todo esto vive en disco y es la fuente de verdad:

| Dónde | Qué |
|---|---|
| `plans/00-plan-de-trabajo.md` | Alcance, cronograma, riesgos, y la tabla de qué decisión de julio quedó superada |
| `plans/04-respuestas-preguntas-abiertas.md` | Las 5 preguntas resueltas con evidencia del Brain y del código |
| `plans/archivo-julio-2026/` | Los 7 planes de julio y su `design.md`, migrados desde `Disputas/` |
| `.ohana/flow.json` | Board de Moka: 4 flujos, 34 pantallas. Migrado desde `Disputas/` |
| `plans/01-spec-acceso-al-tablero.md` | Las cuatro rutas evaluadas y la recomendación para Vicky |
| `plans/02-spec-tablero-merchant.md` | KPIs, gráficos, controles, monitoreo, y qué se conserva del proto de Andrea |
| `design.md` | Tokens desyk 1.30.0-0 reales, principios, glosario, bans, bitácora |
| `plans/archivo-julio-2026/00..07` | Los 7 planes de julio, incluido el inventario del prototipo de Andrea |
| Sesión Wispr 26-ago | La fuente de todo el reacote. Transcripción completa en Wispr Flow |

---

## 5 · Cómo mantener esto

Cuando cambie algo de fondo del proyecto, actualizar **los dos**: el archivo de memoria en `~/.claude/projects/.../memory/` y esta sección. Si divergen, gana el archivo de memoria, porque es el que Claude lee al arrancar.

Lo que **sí** va a memoria: decisiones de negocio, correcciones de Andres sobre cómo trabajar, acuerdos de reunión que no quedan en ningún ticket.
Lo que **no** va: estructura del código, historial de git, cualquier cosa que ya esté escrita en un `.md` del repo.
