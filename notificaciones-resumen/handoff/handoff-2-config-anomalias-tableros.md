# Handoff 2 — Configuración de detección de anomalías (vista de tableros / monitoreo)

Fecha: 2026-07-01 (consolidado)
Prototipo: `notificaciones-resumen/index.html`
Registro: Interno / Operation Center — operador Simetrik configurando cómo el monitoreo detecta anomalías de un gráfico/KPI y de una fuente.

**Alcance de este handoff:** toda la configuración de "cómo se detecta una anomalía" que vive DENTRO del diálogo de monitoreo de un gráfico/KPI (wizard Programación → Alertas → Series y valores) y en la configuración por fuente (Ingesta de datos) del detalle del tablero.

**Qué NO cubre:** las **notificaciones de incidentes** (lista de paquetes/reglas en Anomalías → Configuración) son **Handoff 3**. Los **filtros de la vista de Gestión** son **Handoff 1**. Aquí solo tratamos la detección y las alertas/señales que originan los incidentes, más las alertas del propio KPI.

> **Glosario (obligatorio en los tres handoffs):** **monitoreo** (nunca "agente" / "Agente IA" / "IA" de cara al usuario), **incidente**, **señal / alerta**, **KPI**, **Tablero**, **serie / categoría**. Sin em-dashes. Sin mayúsculas sostenidas en títulos. Motion canónico 120 / 200 / 320 ms, ease-out `cubic-bezier(0.22,1,0.36,1)`; skeleton sobre spinner; light mode.

---

## 0. Mapa de la vista

La detección de anomalías se configura desde dos lugares del producto:

**A. El diálogo de monitoreo del KPI — wizard de 3 pasos:**

```
Programación  →  Alertas  →  Series y valores
   (paso 1)      (paso 2)       (paso 3)
```

- **Programación** (paso 1): recurrencia, horario y zona horaria de la ventana de monitoreo. **No tiene doc propio**: su copy vive directamente en `index.html`. Sus valores son la fuente de la ventana que las Alertas leen como read-only (recurrencia / horario / timezone).
- **Alertas** (paso 2): ¿Cuándo notificar? / ¿Dónde notificar? / Idioma. Ver **Sección A**.
- **Series y valores** (paso 3): detección de anomalías por serie (Análisis inteligente + Límites fijos vs Sistema adaptativo). Ver **Sección B**. Es la parte más pesada de este handoff.

Footer del wizard: **Atrás / Cancelar** (izquierda) y **Siguiente / Guardar** (derecha). En el primer paso la izquierda dice "Cancelar"; en el último la derecha dice "Guardar".

**B. La configuración por fuente (Ingesta de datos):** desde el detalle del tablero (tab "Ingesta de datos") o desde Anomalías → Configuración → Ingesta. Grid de fuentes → modal de detalle con sidebar Configuración / Alertas. Ver **Sección C**.

---

# Sección A · Alertas del KPI (¿Cuándo? → ¿Dónde? → Idioma)

> Origen: `notificaciones-resumen/index.html` → sección `#dsec-notif` del diálogo de monitoreo (prototipo validado). Rediseño 26-jun pm.
>
> ⚠️ **Reencuadre:** esta sección del diálogo del KPI se llama **"Alertas"** (señales del KPI), no "Notificaciones de incidentes". Donde el texto original decía "incidente", **léase alerta / señal del KPI**. Las notificaciones de incidentes NO se configuran aquí (son Handoff 3).

## A.1 Contexto y objetivo

Dentro del diálogo de monitoreo de un gráfico, la sección **Alertas** define **cuándo** avisa el monitoreo al detectar una alerta/señal del KPI, **por dónde** lo hace y en qué **idioma**. Se ordenó como un arco narrativo en **tres tarjetas**, todas abiertas (sin colapsar), con el mismo patrón visual que la pestaña Programación (`tm-prog-card`):

1. **¿Cuándo notificar?** — eje de **timing** de 3 estados: **Nunca** / **Solo al final** / **En tiempo real**.
2. **¿Dónde notificar?** — canales (Email, Slack) y sus destinatarios.
3. **Idioma** — idioma de correos y mensajes.

El selector solo gobierna el *cuándo*, no el *qué*: señales e alertas van juntas (se descartó separarlas en dos bloques).

## A.2 Usuario y registro

- Interno / Op Center. Power user, uso recurrente, alta tolerancia a densidad.
- Configura una vez por gráfico, edita ocasionalmente. Quiere confirmar "cuándo, a quién y en qué idioma" sin error.
- Dato clave al primer vistazo: en qué franja se notifica y qué canales están activos.

## A.3 Historias de usuario

**HU-1 — Decidir cuándo recibir el aviso (y ver, en la barra, qué recibiría)**
> Como operador, quiero elegir si no me avisan (Nunca), me avisan solo con el estado final al cierre, o en tiempo real durante el horario, viendo sobre la barra de la ventana qué notificaciones llegarían y cuándo, para calibrar ruido vs. cobertura.
- Selector (dropdown) con **tres** opciones, con ícono c/u; cada una describe su comportamiento. Orden: **Nunca / Solo al final / En tiempo real**. **Default real: `unset`** (sin configurar) → empty-state con CTA "Configurar notificaciones" (aplica "Solo al final").
- **La barra de la ventana es el explicador:** las notificaciones aparecen como **marcadores** ubicados a su hora, con tooltip. **Solo al final** → 1 marcador al cierre ("Estado final del incidente"). **En tiempo real** → varios (señal · abierto · reconfirmado · resuelto).
- Con **Nunca**: se ocultan barra y Programación (solo queda la línea explicativa); ¿Dónde?/Idioma quedan atenuados; el operador puede continuar sin canales.
- Con **Solo al final / En tiempo real**: se exige al menos un canal (ver HU-2 y A.9).
- Los badges de Programación (recurrencia / horario / timezone) son **solo lectura**; junto a ellos, un icon-button "Editar en programación" lleva a ese paso.

**HU-2 — Activar un canal de notificación**
> Como operador, quiero encender Email o Slack para recibir el aviso por el medio donde ya trabajo.
- Al encender el toggle se revela inline (misma tarjeta del canal) su configuración. Al apagarlo, el panel se colapsa pero conserva lo escrito.

**HU-3 — Definir destinatarios como chips**
> Como operador, quiero agregar varios correos / canales / menciones y quitarlos fácil.
- Escribir + Enter crea un chip removible; la "x" lo elimina. Slack normaliza a `# canal` y `@persona`.

**HU-4 — Elegir idioma de las notificaciones**
> Como operador, quiero fijar el idioma de correos y mensajes de Slack, para que el destinatario lo reciba en su idioma.

## A.4 Estructura y arquitectura de componentes desyk

> Las tres tarjetas usan el **mismo patrón visual** (header con ícono + título + aux / control a la derecha, y un body), consistente con Programación (`tm-prog-card`).

| Mock (prototipo) | Componente desyk | Notas |
|---|---|---|
| `tm-prog-card` (×3) | `Card` (composición) | una por bloque: ¿Cuándo? / ¿Dónde? / Idioma |
| `tm-prog-card-header` + título + ícono | header de `Card` | ícono Lucide 16px + título 14px/600; control a la derecha, subtítulo debajo del título |
| `.when-select` (¿Cuándo?) | `Select` / `DropdownMenu` | opciones "Nunca" / "Solo al final" / "En tiempo real", cada una con ícono (`bell-off`/`bell`/`bell-ring`) + descripción; ícono activo en el botón; controla los marcadores |
| `.when-empty` (primer ingreso, `unset`) | empty-state + CTA dentro de la card | `bell-plus` + "Aún no configuras las notificaciones" + botón **"Configurar notificaciones"** (`whenConfigure` → modo `final`) |
| `.winrec-edit` (editar programación) | `IconButton` ghost | lápiz en la fila de badges; navega al paso Programación |
| `.winrec-timeline` + `.winrec-mk` | componente timeline custom | barra 12–12; banda = ventana monitoreada (08–20). Cada marcador = una notificación a su hora, coloreada por tipo con tooltip. En `final` = 1 al cierre; en `live` = stream; en `never` la barra se oculta |
| `.winrec-badge` | `Badge` (outline) | recurrencia / horario / timezone — solo lectura |
| `.tm-notif-card` (canal) | `Card` ligera / row | contenedor por canal; fondo gris muy claro **sin borde**; `is-open` → render del panel |
| `.tm-notif-row-toggle` | `Switch` | `checked`, `onCheckedChange`; on = `--primary` |
| `.tm-chip-input` + `.tm-chip` | `TagInput` / `ChipInput` (desyk: `Combobox` + chips) | chips removibles, radius 999px |
| `.tm-notif-row-lang` (Idioma) | `Select` | valor por defecto "Español"; en el header de la card Idioma |

**Estructura sugerida (React):**

```
<NotificationsSection>            // 3 cards, orden fijo

  <WhenCard
    mode={whenMode}              // 'unset' | 'never' | 'final' | 'live'  (default 'unset')
    onChange={setWhenMode}
    schedule={schedule}>          // read-only, viene de Programación
    {whenMode === 'unset'
      ? <WhenEmptyState onConfigure={() => setWhenMode('final')} />  // CTA "Configurar notificaciones"
      : whenMode === 'never'
        ? <WhenNeverNote />        // solo la línea explicativa; barra + Programación ocultas
        : <>
            <WindowBar mode={whenMode}        // marcadores = notificaciones a su hora
                       window={schedule.from..schedule.to} />
            <ScheduleBadges schedule={schedule} onEdit={goToSchedule} />  // "Editar en programación"
          </>}
  </WhenCard>
  // whenMode 'unset' | 'never' → <WhereCard> y <LanguageCard> atenuados e inertes (aria-disabled)

  <WhereCard>
    <ChannelCard channel="email" enabled onToggle>
      <TagInput label="Correos" type="email" values={emails} />
    </ChannelCard>
    <ChannelCard channel="slack" enabled onToggle aux="Slack · Simetrik">
      <TagInput label="Canales" type="channel" values={channels} />
      <TagInput label="Etiquetar" optional type="mention" values={mentions} />
    </ChannelCard>
  </WhereCard>

  <LanguageCard value={lang} onChange={setLang} />

</NotificationsSection>
```

> Ya **no** existe la regla `anyChannelActive → recap disabled`. "¿Cuándo?" es independiente y siempre editable. El gating es reactivo: `whenMode !== 'never' && sinCanales` bloquea **Siguiente** (muestra alerta), no deshabilita "¿Cuándo?".

## A.5 Estados

- **Loading:** skeleton de las 3 cards (no spinner).
- **Inicial (primer ingreso):** "¿Cuándo?" en **`unset`** → body empty-state con CTA "Configurar notificaciones"; ¿Dónde?/Idioma atenuados, canales apagados; Idioma "Español".
- **Modo Nunca:** se **ocultan barra y Programación**, queda solo la línea "No enviaremos notificaciones…"; ¿Dónde? e Idioma `opacity .45` + `pointer-events:none`; **Siguiente habilitado** (no exige canal).
- **Modo Solo al final / En tiempo real:** la barra muestra los marcadores (1 al cierre vs. stream). Sin canal activo: al pulsar **Siguiente**, alerta inline ámbar en ¿Dónde? y no avanza; se oculta al activar un canal o volver a Nunca.
- **Canal apagado:** solo su fila (gris) sin config.
- **Canal activo sin destinatarios:** advertencia inline "Agrega al menos un destinatario" (bloquea guardar).
- **Error de chip:** correo inválido → borde `destructive`, no crea el chip, microcopy bajo el campo.
- **Success:** guardado confirma con toast efímero.

## A.6 Copy completo (glosario aplicado)

**Card ¿Cuándo notificar?**
- Título: `¿Cuándo notificar?` (ícono reloj)
- Opciones del selector, c/u con ícono:
  - `Nunca` (`bell-off`) → `No recibirás avisos. El monitoreo igual registra todo in-app.`
  - `Solo al final` (`bell`, etiqueta `recomendado`) → `Al cerrar la ventana, el estado final del incidente.`
  - `En tiempo real` (`bell-ring`) → `Cada cambio de estado, a medida que ocurre.`
- Valor del selector: default **`Sin configurar`** (`unset`); tras configurar, label + ícono del modo elegido.
- **Empty-state (`unset`):** título `Aún no configuras las notificaciones` · sub `Define cuándo quieres recibir avisos de los incidentes de este monitoreo.` · botón `Configurar notificaciones` (ícono `settings-2` → aplica "Solo al final"). Ícono del estado: `bell-plus`.
- **Línea explicativa por modo** (debajo de la barra): `final` → `Al cerrar la ventana te comunico el estado final del incidente. Si se resolvió antes del cierre, no recibes nada.` · `live` → `Te aviso de cada cambio de estado (señales e incidente) a medida que ocurre durante la ventana.` · `never` → `No enviaremos notificaciones de este monitoreo. El monitoreo seguirá analizando y registrando incidentes in-app.`
- Tooltips de los marcadores: `Estado final del incidente` (final) · `Señal: conteo por debajo` / `Incidente abierto · faltan archivos` / `Reconfirmado · severidad sube` / `Resuelto` (live).
- Label badges: `Programación` · ejemplo: `Diario`, `08:00 a.m. – 08:00 p.m.`, `America/Bogota` · icon-button (lápiz) `Editar en programación`.

**Alerta de canales (en ¿Dónde?, reactiva al Siguiente)**
- `Te hace falta configurar al menos un canal para recibir las notificaciones. Activa Email o Slack, o cambia ¿Cuándo notificar? a Nunca.` (ícono `alert-triangle`, ámbar)

**Card ¿Dónde notificar?**
- Título: `¿Dónde notificar?` (ícono campana) · Subtítulo: `Activa uno o varios canales y configura sus destinatarios`
- Canal Email: título `Email` · label `Correos` · placeholder `Agregar correo y Enter`
- Canal Slack: título `Slack` · aux `Slack · Simetrik` · label `Canales` (placeholder `Agregar canal y Enter`) · label `Etiquetar` (Opcional, placeholder `@persona o @equipo y Enter`)

**Card Idioma**
- Título: `Idioma` (ícono globo) · Selector: `Español`

## A.7 Microinteracciones

| Interacción | Detalle |
|---|---|
| Selector "¿Cuándo?" | abre menú con descripciones+íconos; al elegir, actualiza valor+ícono del botón, re-renderiza los marcadores y cierra; cierra al clic fuera |
| Empty-state → configurar | CTA (o elegir en el dropdown) sale de `unset` y aplica el modo; reactiva ¿Dónde?/Idioma |
| Modo "Nunca" | oculta barra + Programación (deja la línea explicativa); ¿Dónde?/Idioma atenúan/reactivan con `opacity .15s` |
| Marcadores de la barra | tooltip al hover (qué + cuándo); la posición sobre la línea ya comunica la hora |
| Alerta de canales | aparece solo al pulsar Siguiente (modo ≠ Nunca/unset y sin canal); se oculta al activar un canal o volver a Nunca |
| "Editar en programación" | icon-button hover sutil; al click navega al paso Programación |
| Toggle canal | `background 150ms` + knob `left 150ms`; revelar panel con altura/opacity `200ms ease-out` |
| Chip nuevo | aparece sin animación pesada; foco vuelve al input |
| Focus en `TagInput` | ring `0 0 0 3px primary/12%`, borde `primary` |

Durations canónicas: 120 / 200 / 320 ms ease-out. Sin spinners; preferir skeleton.

## A.8 Endpoints esperados (Alertas del KPI)

> Mockable si aún no existen. Forma sugerida:

`GET /monitoring/{chartId}/notifications` →
```json
{
  "when": "unset",            // "unset" | "never" | "final" | "live"  (default "unset" = primer ingreso)
  "channels": {
    "email": { "enabled": true, "recipients": ["ana.torres@simetrik.com"] },
    "slack": { "enabled": false, "channels": ["# incidentes-finops"], "mentions": [] }
  },
  "language": "es",
  "schedule": { "recurrence": "daily", "from": "08:00", "to": "20:00", "timezone": "America/Bogota" }
}
```
`PUT /monitoring/{chartId}/notifications` con el mismo shape. `schedule` es **read-only** aquí (se configura en Programación); el timeline y los badges solo lo reflejan.

## A.9 Edge cases y validaciones (Alertas del KPI)

- Correo inválido → no crear chip, microcopy.
- Canal de Slack duplicado → normalizar; no duplicar chip.
- Canal encendido sin destinatarios → bloquear guardado, advertencia inline.
- Workspace de Slack no conectado → estado del card Slack con CTA "Conectar Slack" en vez del toggle.
- Programación vacía (sin ventana) → timeline/badges en estado neutro "Configura la ventana en Programación".
- Lista larga de destinatarios → chips hacen wrap, input con `min-width`.
- i18n: el idioma afecta el **contenido enviado**, no la UI de configuración.
- `when === 'never' | 'unset'`: no se exige canal; al guardar/avanzar no bloquea por canales.
- `when === 'final' | 'live'` y sin canal activo: bloquear avance del wizard (alerta en ¿Dónde?), no el guardado silencioso.
- `when === 'final'`: si el incidente se resolvió **dentro** de la ventana, no se envía nada. ⚠️ **A validar con Iván/BADS:** el copy dice "estado final al cierre", pero el backend confirma cuando responde el workflow runner (`OPEN`), no estrictamente al cerrar la ventana. Si no calza, ajustar wording.
- **Mención en Slack**: se etiqueta con **ID de usuario** (no `@handle` escrito a mano, que llega como texto y no notifica). El hint explica cómo copiarlo desde el perfil de Slack.

## A.10 Tokens (Alertas del KPI)

`--primary #3D3BF5` (toggle on, foco, chips) · `--primary-soft` (fondo chip / ring) · `--border` / `border-default` · `muted/0.5` (fondo de canales) · `muted-foreground` (subtítulos, placeholders, label badges) · `text-primary #1F1B2E` · `text-tertiary` (íconos). Radius: `12px` cards, `10–11px` canales, `8px` inputs, `999px` chips/toggles.

---

# Sección B · Series y valores: detección por serie

> Origen: `notificaciones-resumen/index.html` → paso **Series y valores** del diálogo de monitoreo (KPI "Conteo De Registros", COUNT_DISTINCT). Bloques `.ns-ai*` (Análisis inteligente) + `#nsWrap` (`ns-*`), estado `NS_*` en JS.
> Patrón: **narrativa previa (Análisis inteligente) → colapsables inline** con modelo **configuración general + override por serie**.
>
> **Modelo VIGENTE (1-jul-2026).** Reemplaza el modelo anterior (slider 0–100 + severidad por dos bandas + grilla "POR SERIE" + selector de categoría). El viejo (`.sens-*`, `.cat-*`, `.tm-series-*`, `.tm-dialog-preview-card`) quedó **deprecado y eliminado** (ver Sección D). **Ajustes 1-jul pm:** (a) narrativa "Análisis inteligente" arriba + carga "Pensando…"/skeleton; (b) se quitó agregar/quitar serie (siempre las 6); (c) default = Límites fijos; (d) la simulación muestra un solo total.

## B.1 Contexto y objetivo

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

## B.2 Usuario y registro

- Interno / Op Center. Power user, alta tolerancia a densidad, uso recurrente.
- Modo de uso: revisar la narrativa, configurar el KPI (general) y personalizar solo las series que lo ameriten.
- Dato clave al primer vistazo: de cada serie, **cómo está detectando** (badge de modo) y **cuántas alertas** daría.
- **Primera versión = evangelizar:** enseñar el modelo mental (fijo vs adaptativo). La config es explicativa, no una tabla densa. La vista súper-colapsada a tabla queda para una iteración futura.

## B.3 Estructura de la vista

```
[✦] Análisis inteligente                         ← narrativa, ver B.4
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
- Al abrir una fila, se despliega **la card de configuración** (B.5) inline.
- El **badge de cada fila** refleja el modo efectivo: `Límites fijos` (ámbar) o `Sistema adaptativo` (azul). Al lado, un resumen: rango mín/máx (fijo) o sensibilidad (adaptativo).
- **Las series son fijas** (catálogo del KPI): no hay agregar ni quitar; siempre se muestran todas. El contador es un **badge outline** (`{N} series`).

## B.4 Análisis inteligente (narrativa) + carga

Antes de los colapsables, Simetrik muestra su lectura del histórico (portado de `config-system-kpi`, adaptado a vanilla, **sin gráfica** — la gráfica vive en cada colapsable).

- **Header** "Análisis inteligente" (indigo + ícono sparkle gradiente), fuera de la card.
- **Card tintada** con: **stats** (Media · Límite inferior sugerido · Límite superior sugerido) → **descripción** ("Línea base estable y limpia - 30 días…") → toggle **"Ver análisis detallado"** (colapsable) que despliega **Tendencia · Estacionalidad · Valores atípicos · Brechas de datos** → divisor → **footer** "ⓘ Este análisis refleja el agregado de todas las categorías".

**Estado de carga (al entrar a Series y valores):**
- El análisis entra en **"Pensando…"**: spinner + pasos que aparecen uno a uno (*Consultando datos históricos · Calculando línea base · Detectando patrones · Identificando atípicos · Generando narrativa*), el último con ícono gradiente, los previos con dot. El botón "Pensando…" colapsa/expande los pasos.
- Mientras "Pensando…", **los colapsables (`#nsWrap`) muestran un skeleton** (filas con shimmer) en vez del contenido real.
- Al terminar (~4–5 s en el prototipo), se **revela la narrativa** y se **renderizan los colapsables reales** (mismo instante).
- En prod: la narrativa, los sugeridos y el conteo los provee el BE; el "Pensando…" refleja la latencia real del análisis.

## B.5 La card de configuración (global y por serie, mismo template)

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

## B.6 Arquitectura de componentes / clases

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

## B.7 Estados

- **Carga:** narrativa en "Pensando…" (pasos) + `#nsWrap` en **skeleton**. Al terminar → narrativa + colapsables reales.
- **Inicial (post-carga):** "Todas las categorías" y las 6 series en **Límites fijos** (mín 10 · máx 24), todas heredando el global; contador `6 series`.
- **Serie heredando:** badge del modo del global; al editar pasa a personalizada (sin badge extra; el override se refleja en su resumen/gráfica).
- **Global expandido:** todas las series superpuestas + simulación agregada.
- **Bound apagado:** input atenuado e inerte (conserva valor); ese límite no marca ni se dibuja.
- **Validación:** valor no numérico / `lower ≥ upper` con ambos activos → error + microcopy (pendiente de cablear).

## B.8 Copy (glosario aplicado)

- Narrativa: título `Análisis inteligente`; desc `Línea base estable y limpia - 30 días de observaciones de baja dispersión, sin brechas ni valores atípicos. Una línea base simple para anclar el monitoreo.`; toggle `Ver análisis detallado`; footer `Este análisis refleja el agregado de todas las categorías.`; pasos de carga (ver B.4).
- Encabezados: `Límites generales de {métrica}` · `Límites por serie` + badge `{N} series`.
- Pregunta: `¿Cómo quieres detectar las anomalías (por defecto)?` (global) / `…de esta serie?` (serie).
- Radios: **Límites fijos** — `Tú defines el mínimo y el máximo válidos.` · **Sistema adaptativo** — `Simetrik aprende lo normal y avisa de lo inusual.`
- Sensibilidad: `Alta` (`Detecta hasta cambios chicos`) · `Media` (`Recomendada`) · `Baja` (`Solo lo muy fuera de lo normal`).
- Seguridad: `Agregar límites de seguridad` — `Un mínimo/máximo que avisa sí o sí, aunque el sistema lo vea normal. Para valores que jamás deberían pasar.`
- Límites: `Límite inferior` / `Límite superior` · chip `Valor sugerido: N`.
- Aviso (por modo): fijo → `Te avisamos solo cuando la serie se salga del rango que definiste. Predecible y bajo tu control.` · adaptativo → `Te avisamos cuando la serie se comporte distinto a lo habitual (sensibilidad {nivel}). Se ajusta solo.` · adaptativo+seguridad → `…y siempre que cruce tus límites de seguridad.` (global: "cada serie").
- **Simulación (número único):** `{N} avisos en los últimos 30 días`.

## B.9 Microinteracciones

| Interacción | Detalle |
|---|---|
| Entrar a "Series y valores" | narrativa en "Pensando…" (pasos animados) + skeleton en colapsables; al terminar, reveal + render real |
| Ver análisis detallado | despliega/colapsa las secciones (chevron rota) |
| Abrir colapsable | cierra los demás; despliega la card; render de gráfica + simulación |
| Elegir modo / nivel / seguridad | re-render de panel, gráfica, aviso y total en vivo |
| Editar límite / toggle bound | redibuja banda/línea y recalcula el total; chip sugerido se muestra/oculta |

Durations canónicas: 120 / 200 / 320 ms ease-out. Skeleton para carga; spinner solo en el loader "Pensando…". Light mode.

## B.10 Investigación que respalda el diseño (1-jul)

- **Patrón dominante en monitoreo** (Datadog, New Relic, Dynatrace): una config declarativa + el motor la instancia por serie; override por excepción. La lista de series es de **inspección**.
- **Adaptativo + límite duro coexisten** (Anodot) → "sistema adaptativo + límites de seguridad".
- **UX (NN/g):** para editar config compleja de varios ítems, se eligió **colapsables inline (una abierta)** + **default global** (el default enseña el modelo mental) para una v1 que debe evangelizar.
- **Diferenciador de mercado:** análisis narrativo previo + simulación de impacto en vivo. Se mantienen.

---

# Sección C · Alertas por fuente (Ingesta de datos)

> Origen: Épica 4 del handoff de anomalías (sesiones Granola 30-jun). Prototipo `notificaciones-resumen/index.html`.
> **Dónde:** en el **detalle del tablero** (Tableros → abrir tablero) → tab **"Ingesta de datos"** (junto a Calidad / Salud / Métricas). También accesible desde Anomalías → Configuración → Ingesta. Clic en una fuente → **modal** "Monitorear <fuente>" (`#sourceDialog`, overlay).

> Aquí se definen las **señales / alertas a nivel de fuente** (los thresholds que generan los `AnomalySignal` / problem categories que BADS luego agrupa en incidentes). Es el origen de los incidentes que el Handoff 1 (filtros) y el Handoff 3 (notificaciones) consumen.

## C.1 Cambios de UI (enumerados)

1. **Grid de fuentes** (ya existía): cada fuente con "Activar monitoreo AI" / "Monitoreo activo". Ahora la tarjeta es **clickeable** → abre el detalle (reemplaza la grid; "Volver" regresa).
2. **Modal de detalle de fuente** (`#sourceDialog`, overlay) con **sidebar izquierdo de 2 ítems**: **Configuración** y **Alertas** (mismo patrón visual que el sidebar del diálogo del KPI, pero solo esos dos). Adaptado a vanilla desde `config-system-kpi/index.html` → `inline-source-detail`:
   - **Configuración** (1er ítem del sidebar) contiene:
     - **Análisis inteligente** (colapsable): resumen + límites sugeridos (Media / inferior / superior). Estático.
     - **Ventana de tiempo**: llega a las · avisar si pasa de las · zona horaria → señal de **archivo faltante/tarde**.
     - **Cómo se monitorea**: radio *Igual todos los días* / *Por día de la semana* (este último marcado **Próx.**).
     - **Comportamiento de la fuente**: Cantidad de archivos (mín/máx + sugerencia) · Cantidad de registros (mín/máx) · **Otros comportamientos**: Archivos vacíos / duplicados / fallidos (switch + umbral %).
   - **Alertas** (2do ítem del sidebar) = **mismo patrón de 3 tarjetas que las Alertas del KPI** (Sección A): ¿Cuándo notificar? (Nunca / Solo al final / En tiempo real + empty state + ventana de monitoreo, editar→Configuración) · ¿Dónde notificar? (Email/Slack + ID de Slack) · Idioma. Las funciones del patrón (`whenPick`, `renderWhen`, `toggleChannel`, `isChannelInvalid`/`showChannelWarning`) son **scope-aware** vía `data-notif-section` (un warning por sección, no chocan KPI vs fuente).
   - Footer: Salir / Guardar.

## C.2 Mapeo a BADS `problem_category`

| Sección del panel | señal / `problem_category` |
|---|---|
| Ventana de tiempo (llega/avisar) | `MISSING_FILE` |
| Cantidad de archivos / registros (mín/máx) | `VOLUME_VARIATION` |
| Otros comportamientos → Archivos vacíos | `UNEXPECTED_EMPTY_FILE` |
| Otros comportamientos → Archivos duplicados | `DUPLICATED_FILE` |
| Otros comportamientos → Archivos fallidos | `FAILED_FILE` |

## C.3 Fuera de este prototipo (vive completo en `config-system-kpi`)

Lo más pesado del original (Alpine) se marcó **Próx.** o se omitió: **config por día (tabs Lu→Do), grupos de archivos, y el "análisis inteligente" completo por métrica/día**. La versión fiel y completa está en `config-system-kpi/index.html`; acá quedó una adaptación vanilla con lo esencial.

---

# Guía de implementación consolidada (BADS + fe-solutions-mf)

> **La feature YA existe** en el repo `fe-solutions-mf`. Este prototipo **rediseña** los pasos de detección/alertas del diálogo actual, **no es greenfield**. Stack: React + TS, `@simetrikinc/desyk-components`, **zustand** (solo modales/estado local), **@tanstack/react-query** (server state), sin react-hook-form. Microfrontend (Module Federation, rsbuild). CSS scoped a `#solutions-app`. i18n por namespace (es/en/pt).

## I.1 Contra qué datos se implementa (BADS)

Fuente: `ProductEngineeringBrain/versions/v2.8/operation-center/funcionalidades/anomalias/`.

**Dos entidades (no mezclar):**
- **AnomalySignal** (`anomaly_signal`) — señal atómica. Estados `ACTIVE`/`RESOLVED`; categorías `TRIGGER` / `TRAJECTORY` / `NEW_SERIES`. Es la "alerta/señal" del KPI y de la fuente. **La detección de la Sección B/C produce estos.**
- **Incident** (`incident`) — agrupa señales con causa raíz. Es lo que filtran/notifican los Handoffs 1 y 3.

**Detección → categorías de AnomalySignal:**
- **Sistema adaptativo** (Sección B) → detección de patrón de BADS (`TRIGGER` / `TRAJECTORY` / `NEW_SERIES`); el **nivel** (Alta/Media/Baja) mapea a un parámetro real del detector → **confirmar valores con BE**.
- **Límites fijos / de seguridad** (Sección B) → umbral duro del usuario (condición adicional OR sobre el adaptativo; modelo Anodot).

**`problem_category` (catálogo cerrado de Ingesta)** — usado por la config por fuente (Sección C) y por el filtro "Tipo" de Handoff 1:
| Label UI | enum BADS |
|---|---|
| Archivo faltante | `MISSING_FILE` |
| Archivo fallido | `FAILED_FILE` |
| Archivo vacío | `UNEXPECTED_EMPTY_FILE` |
| Archivo duplicado | `DUPLICATED_FILE` |
| Variación de volumen | `VOLUME_VARIATION` |
- Nombres del catálogo exactos (Brain); `UNEXPECTED_EMPTY_FILE`/`DUPLICATED_FILE` verbatim, el resto inferido del patrón → **confirmar string exacto con BE**. `ALL_OK` es interno (auto-cierra), no se muestra.

**Severidad:** enum `URGENT` / `REQUIRES_ATTENTION`, **asignada por el workflow runner de BADS (system-assigned), NO configurable por el usuario**. La UI de detección **no la discrimina** en la simulación (solo total). Vuelve cuando exista severidad configurable.

## I.2 Componentes desyk (tablas unificadas)

> Verificado contra el paquete instalado en `fe-solutions-mf/node_modules/@simetrikinc/desyk-components/dist`. **No existen** en desyk: `RadioCard`, `SegmentedControl` (usar RadioGroup+wrapper y Tabs/ToggleGroup); tampoco token-input dedicado (usar `Combobox` + chips custom).

| Patrón del proto | Componente desyk real | Nota |
|---|---|---|
| Wizard del diálogo | `DialogNavigation` vía `SolutionsDialogNavigation` | ya en `AnomalyMonitoringConfig`; usar wrappers `Solutions*` por el Shadow DOM del OC Box |
| Colapsables (`.ns-acc`, `.ds-analysis`, sidebar fuente) | `Accordion` (`type="single"`, `collapsible`; `AccordionItem variant="rounded"|"simple"`) / `Collapsible` | patrón `AiSection` en `SystemKpiDetailView` |
| Radios fijo/adaptativo (`.ns-radio`) | `RadioGroup` + `RadioGroupItem` (patrón `MonitoringOptionCard`) | no hay `RadioCard` |
| Segmented sensibilidad (`.ns-seg`) | `Tabs` o `ToggleGroup` (`variant "default"|"outline"`, `joined`) | no hay `SegmentedControl` |
| Inputs de límite (`.ns-lim`) | `Input` (`variant "default"|"error"`) + wrapper `ThresholdInput` (formateo `Intl`) | reusar el existente |
| Chip valor sugerido (`.ns-limsug`) | `Badge`/`Button` chip | valor de baseline (p5/p95/mean) |
| Badges de modo (`.ns-badge`) | `Badge` (`variant`: fijo → `warning`, adaptativo → `info`/`ai`, contador → `outline`) | |
| Skeleton (`.ns-skel`) | `Skeleton` (`className`) | placeholder de los colapsables |
| Aviso / simulación (`.ns-alert`) | `Alert` (`variant "default"|"info"|"warning"|…`) / `Card` | |
| Gráfica (`svg.ns-chart`) | **recharts** (`ReferenceLine`=límite fijo, `ReferenceArea`=banda) | **no** SVG a mano; existe wrapper `@simetrikinc/desyk-components/chart` (confirmar con FE si migrar) |
| Toggle canal (`.tm-notif-row-toggle`) | `Switch` (`checked`/`onCheckedChange`) | Secciones A y C |
| Checkbox (bound on/off, seguridad, momento) | `Checkbox` (Radix; `checked`/`onCheckedChange`) | |
| Select (idioma, ¿Cuándo?, zona) | `Select` / `DropdownMenu` | |
| Chips de correos / canales / menciones | `Combobox` + chips custom | |
| Empty-state (¿Cuándo? unset) | `EmptyState` (`EmptyStateTitle/Description/Content`) | |
| Nota de ID de Slack | `Alert variant="info"` | |
| Tooltip de íconos | `Tooltip` | |

## I.3 Archivos clave del repo (`fe-solutions-mf`)

Ubicación: `src/oc/features/anomalies/` (Operation Center). El diálogo vive en `components/AnomalyMonitoringConfig/`.

| Qué | Ruta |
|---|---|
| Diálogo de config (wizard: Programación → Alertas → Series y valores) | `components/AnomalyMonitoringConfig/AnomalyMonitoringConfig.tsx` |
| Detalle por KPI (baseline + narrativa + secciones colapsables) | `components/AnomalyMonitoringConfig/SystemKpiDetailView.tsx` |
| Narrativa IA + "Pensando…" | `components/AnomalyMonitoringConfig/AiReasoningSteps.tsx`, `AiCollectingLoader.tsx` |
| Input de límite (formateo `Intl`) | `components/AnomalyMonitoringConfig/components/ThresholdInput/ThresholdInput.tsx` |
| Radio de modo (patrón card) | `components/MonitoringConfigForm/components/MonitoringOptionCard/MonitoringOptionCard.tsx` |
| Alertas del KPI (email/slack) | `components/AnomalyMonitoringConfig/NotificationsSection`, `SlackChannelCard.tsx` |
| Form de monitoreo de ingesta (config-system-kpi) | `components/MonitoringConfigForm/` (`sections/*`) |
| Servicios | `services/anomalies/monitoringConfig` (config KPI), `services/anomalies/badsProxy` (baseline/preview + narrativa), `services/dashboards/notificationConfig` |
| Store | `features/anomalies/store/index.ts` (zustand: modales + analyzing) |
| Wrappers de portal (Shadow DOM en OC Box) | `shared/components/desyk-components-with-portals` (`Solutions*`) |

**Qué YA existe vs. qué cambia:**
- **Narrativa "Análisis inteligente" + "Pensando…" → YA EXISTE** (`AiReasoningSteps` + `AiCollectingLoader`; baseline `KpiNarrative` con `seasonality/trend/data_gaps/outliers/overall_assessment` multilingüe, y `baseline.{mean,stddev,p5,p95,ci_*}`). El prototipo **alinea copy/layout**: header, "Ver análisis detallado", footer "agregado de todas las categorías", y los **límites sugeridos** salen de `p5`/`p95`/`mean`.
- **Skeleton de carga en los colapsables → NUEVO/menor** (usar `Skeleton`).
- **"Límites fijos vs Sistema adaptativo"** → mapea al **tri-estado de límite** que ya maneja el repo: `number` (fijo) · `null` (adaptativo) · `{mode:"off"}` (apagado). El prototipo lo vuelve una **pregunta explícita con 2 radios**. Default = fijo.
- **Colapsables por serie (general + override)** → hoy es `MetricPanelSection` + filas de threshold (`kpi_configs[].thresholds[]` con `series_value`). El prototipo propone **Collapsible por serie** con "Todas las categorías" como base heredable.
- **Simulación = total único → NUEVO**: requiere que BADS devuelva el **conteo de disparos por config** sobre la ventana (hoy no existe explícito). Sin discriminar tipo.
- **Series fijas (sin agregar/quitar)** → coherente con `series_column_ids` del KPI.

**Tipos reales a tocar:**
- `services/anomalies/monitoringConfig/types.ts` → `AnomalyMonitoringConfig` (`kpi_configs[].thresholds[] {operator, value, series_value}`, `days_of_week`, `granularity`, `series_column_ids`).
- `services/anomalies/badsProxy/types.ts` → `BaselinePreviewResult` / `KpiBaselineResponse` (`baseline` + `KpiNarrative`).
- `services/dashboards/notificationConfig/types.ts` → `NotificationConfig` (email/slack/in-app + locale).

**Notas de implementación:**
- Sin react-hook-form: estado con `useState` + hooks (`useScheduleForm`, `useThresholdRules`, `useNotificationsForm`) o el patrón section-descriptor (`useMonitoringConfigForm`); validación manual + Zod en el payload al guardar.
- Usar los wrappers `Solutions*` (portal) por el Shadow DOM del OC Box.
- i18n: crear namespace + `handle.i18nNs` + `locales/{es,en,pt}`.

## I.4 Endpoints esperados (detección)

- **Alertas del KPI:** `GET/PUT /monitoring/{chartId}/notifications` (ver A.8).
- **Detección por serie (borrador):** `GET/PUT /monitoring/{chartId}/detection` con `analysis` (narrativa + sugeridos), `general` (config base) + `series[]` (`{id, override?}`); `data`, `band`, `suggested`, `signals` read-only del BE.

## I.5 Preguntas abiertas para BE / producto

1. **Conteo de simulación** (total de disparos por config sobre la ventana) — ¿lo expone BADS? Misma ventana (30 días) para serie, banda y conteo.
2. Mapeo de **nivel adaptativo** (Alta/Media/Baja) → parámetro real del detector.
3. **Sugeridos por serie** desde baseline (`p5`/`p95`/`mean`) — ¿por serie o solo agregado?
4. ¿El override adaptativo **por serie** se permite, o se restringe a límites duros? (Splunk lo prohíbe; decisión de producto pendiente.)
5. String exacto de los enum `problem_category` (`MISSING_FILE`/`FAILED_FILE`/`VOLUME_VARIATION`).
6. ⚠️ Heredado (Iván/BADS): confirmación "al cierre de ventana" vs **workflow runner** (`OPEN`). Si no calza, ajustar el wording de "estado final al cierre".

---

# Nota de deprecación y fuera de scope

## Deprecado / superseded

- **Slider de sensibilidad 0–100 + severidad por dos bandas (changelog #6 del handoff de anomalías).** En su momento se reencuadró el slider quitando "nula" (extremos "Solo mi umbral" ↔ "Detección adaptativa", con `CORE=0.30` para que la banda de atención nunca llegara al centro). **Ese slider ya NO existe:** fue reemplazado (1-jul) por el rediseño de detección **por serie** (Sección B): dos radios explícitos (Límites fijos / Sistema adaptativo) + segmented Alta/Media/Baja. Las clases viejas `.sens-*`, `.cat-*`, `.tm-series-*`, `.tm-dialog-preview-card` quedaron eliminadas del prototipo.

## Fuera de scope (documentado)

- **Notificaciones de incidentes** (lista de paquetes/reglas, editor, resumen consolidado, empty-state con diagrama) → **Handoff 3**.
- **Filtros de la vista de Gestión** (multiselect, filtros guardados, chips OR/AND) → **Handoff 1**.
- **Config por fuente completa** (config por día Lu→Do, grupos de archivos, análisis inteligente por métrica/día) → vive completa en `config-system-kpi/index.html`; aquí solo la adaptación vanilla esencial.
- **Severidad** como control del usuario (system-assigned hasta que sea configurable).
- Notificaciones de **flujo de la app** (asignación/etiquetado) — otro feature/template.

---

# Checklist pre-implementación (unificado)

**Sección A · Alertas del KPI**
- [ ] Las 3 cards con el mismo patrón de `Card` que Programación (header ícono+título+control/aux, body).
- [ ] "¿Cuándo?" arranca en **`unset`** (primer ingreso) con empty-state + CTA "Configurar notificaciones"; canales apagados; ¿Dónde?/Idioma atenuados.
- [ ] Selector con 3 opciones **Nunca / Solo al final / En tiempo real**, íconos (`bell-off`/`bell`/`bell-ring`), ícono activo en el botón; badges de Programación read-only.
- [ ] **La barra es el explicador:** marcadores a su hora con tooltip (final = 1 al cierre · live = stream); en **Nunca** se ocultan barra + Programación.
- [ ] **Solo al final**: si se resolvió durante la ventana, no llega nada.
- [ ] Gating **reactivo al Siguiente**: modo ≠ Nunca/unset + sin canales → alerta inline en ¿Dónde? y no avanza (sin `disabled` preventivo).
- [ ] "Editar en programación" (icon-button) navega al paso Programación.
- [ ] Wizard prog→alertas→series con footer Atrás/Cancelar + Siguiente/Guardar.
- [ ] ¿Dónde?: canales con fondo gris sin borde; toggle revela config inline; labels cortos (Correos/Canales/Etiquetar).
- [ ] Idioma como card propia con selector en el header.
- [ ] Mención de Slack por **ID de usuario** (no `@nombre`).
- [ ] `schedule` tratado como read-only (fuente: Programación).

**Sección B · Series y valores (detección por serie)**
- [ ] **Narrativa "Análisis inteligente"** arriba: header + card (stats sugeridos + descripción + "Ver análisis detallado" + footer). Sin gráfica propia.
- [ ] **Carga:** estado "Pensando…" (pasos) + **skeleton** en los colapsables; al terminar, reveal narrativa + render real.
- [ ] Dos secciones tituladas (sin uppercase): **Límites generales de {métrica}** + **Límites por serie** (badge outline `{N} series`).
- [ ] Colapsables inline, una abierta a la vez (global + series). **Series fijas** (sin agregar/quitar).
- [ ] Card de config compartida: gráfica completa (sin AHORA) → pregunta modo → panel (fijo/adaptativo) → caja blanca aviso + **total único**.
- [ ] **Default = Límites fijos** (global y todas las series).
- [ ] Modo **Límites fijos** (mín/máx con on/off por bound + valor sugerido) y **Sistema adaptativo** (Alta/Media/Baja + límites de seguridad).
- [ ] Card "Todas las categorías" = base heredable; gráfica con series superpuestas + simulación agregada.
- [ ] Simulación = **un solo número** ("avisos en los últimos 30 días"), sin discriminar tipo.

**Sección C · Alertas por fuente (Ingesta)**
- [ ] Grid de fuentes clickeable → modal `#sourceDialog` con sidebar Configuración / Alertas.
- [ ] Configuración: Análisis inteligente (colapsable estático) · Ventana de tiempo · Cómo se monitorea (Por día = Próx.) · Comportamiento (archivos/registros/otros).
- [ ] Alertas de la fuente = mismo patrón de 3 tarjetas que las Alertas del KPI, scope-aware (`data-notif-section`, un warning por sección).
- [ ] Mapeo correcto a `problem_category` (MISSING_FILE / VOLUME_VARIATION / UNEXPECTED_EMPTY_FILE / DUPLICATED_FILE / FAILED_FILE).

**Transversal**
- [ ] Glosario ("monitoreo", no "agente"; "incidente"; "señal/alerta"), sin em-dashes, sin mayúsculas sostenidas.
- [ ] Tokens desyk; 120/200/320 ms ease-out `cubic-bezier(0.22,1,0.36,1)`; skeleton sobre spinner; light mode.
- [ ] A11y AA: `aria-label` en toggles y "x" de chips, foco visible, contraste; `prefers-reduced-motion`.
- [ ] Componentes desyk (no custom): `Switch`, `Checkbox`, `RadioGroup`, `Tabs`/`ToggleGroup`, `Accordion`/`Collapsible`, `Badge`, `Alert`, `Skeleton`, recharts para gráficas.
- [ ] BE: narrativa + banda + simulación + sugeridos reales (hoy mockeados); mapeo de nivel → parámetro del detector; conteo de disparos por config.
