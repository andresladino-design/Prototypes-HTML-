# Handoff — Notificaciones (¿Cuándo? → ¿Dónde? → Idioma)

Fecha: 2026-06-25
Origen: `notificaciones-resumen/index.html` → sección `#dsec-notif` del diálogo de monitoreo (prototipo validado)
Registro: **Interno (Operation Center)** — operador Simetrik configurando el monitoreo inteligente de un gráfico (K Cast)
Patrón de presentación: **3 cards en orden narrativo** (`tm-prog-card`, mismo patrón visual que Programación) — primero **cuándo**, luego **dónde**, luego **idioma**

---

## 1. Contexto y objetivo

Dentro del diálogo de "Monitoreo inteligente" de un gráfico, la sección **Notificaciones** define **cuándo** avisa el Agente IA al detectar un **incidente**, **por dónde** lo hace y en qué **idioma**.

La sección se ordenó como un **arco narrativo de configuración** en tres tarjetas, todas abiertas (sin colapsar) y con el mismo patrón visual que la pestaña Programación:

1. **¿Cuándo notificar?** — durante todo el horario monitoreado o solo con el resultado al cierre.
2. **¿Dónde notificar?** — canales (Email, Slack) y sus destinatarios.
3. **Idioma** — idioma de los correos y mensajes.

> **Cambio clave vs. versión anterior del handoff:** "¿Cuándo notificar?" pasó a ser el **primer paso y de primera clase** (ya no es un recap deshabilitado al final que se habilitaba solo al activar un canal). Esto resuelve el problema de descubribilidad: el operador decide el "cuándo" primero y siempre lo ve, y los canales se expanden debajo sin enterrarlo. **Se eliminó el gating** (`syncWinrec` / estado `disabled`).

## 2. Usuario y registro

- **Registro:** Interno / Op Center. Operador Simetrik que monitorea múltiples clientes.
- **Perfil:** power user, uso recurrente, alta tolerancia a densidad.
- **Modo de uso:** configura una vez por gráfico, edita ocasionalmente. Quiere confirmar "cuándo, a quién y en qué idioma" sin error.
- **Dato clave al primer vistazo:** ¿en qué franja se notifica y qué canales están activos?

## 3. Historias de usuario

**HU-1 — Decidir cuándo recibir el aviso**
> Como operador, quiero elegir si me avisan durante todo el horario monitoreado o solo con el resultado al cierre, viendo en una línea de tiempo en qué parte de la franja ocurre, para confiar en que no me perderé el incidente ni recibiré ruido fuera de horario.
- Selector (dropdown) con dos opciones; cada una describe su comportamiento.
- La barra 12–12 refleja la elección (cobertura completa de la ventana vs. punto al cierre).
- Los badges de Programación (recurrencia / horario / timezone) son **solo lectura** (vienen de la pestaña Programación).

**HU-2 — Activar un canal de notificación**
> Como operador, quiero encender Email o Slack para recibir el aviso por el medio donde ya trabajo.
- Al encender el toggle se revela inline (misma tarjeta del canal) su configuración.
- Al apagarlo, el panel se colapsa pero conserva lo escrito.

**HU-3 — Definir destinatarios como chips**
> Como operador, quiero agregar varios correos / canales / menciones y quitarlos fácil.
- Escribir + Enter crea un chip removible; la "x" lo elimina.
- Slack normaliza a `# canal` y `@persona`.

**HU-4 — Elegir idioma de las notificaciones**
> Como operador, quiero fijar el idioma de correos y mensajes de Slack, para que el destinatario lo reciba en su idioma.

## 4. Estructura y arquitectura de componentes desyk

> Las tres tarjetas usan el **mismo patrón visual** (header con ícono + título + aux / control a la derecha, y un body), consistente con la pestaña Programación (`tm-prog-card`).

| Mock (prototipo) | Componente desyk | Notas |
|---|---|---|
| `tm-prog-card` (×3) | `Card` (composición) | una por bloque: ¿Cuándo? / ¿Dónde? / Idioma |
| `tm-prog-card-header` + título + ícono | header de `Card` | ícono Lucide 16px + título 14px/600. El control (dropdown/selector) va a la **derecha** del header; el subtítulo, **debajo** del título cuando aplica |
| `.when-select` (¿Cuándo?) | `Select` / `DropdownMenu` | opciones "Todo el tiempo" / "Solo al cierre", cada una con descripción; controla el modo del timeline |
| `.winrec-timeline` | componente timeline custom | barra 12–12; banda = ventana monitoreada (08–20), `fill` = cobertura del aviso (toda la banda en `during`, punto al cierre en `close`) |
| `.winrec-badge` | `Badge` (outline) | recurrencia / horario / timezone — **solo lectura** |
| `.tm-notif-card` (canal) | `Card` ligera / row | contenedor por canal; fondo gris muy claro **sin borde**; estado `is-open` → render del panel de config |
| `.tm-notif-row-toggle` | `Switch` | `checked`, `onCheckedChange`; on = `--primary` |
| `.tm-chip-input` + `.tm-chip` | `TagInput` / `ChipInput` | chips removibles, radius 999px |
| `.tm-notif-row-lang` (Idioma) | `Select` | valor por defecto "Español"; va en el header de la card Idioma |

**Estructura sugerida (React):**

```
<NotificationsSection>            // 3 cards, orden fijo

  <WhenCard
    mode={whenMode}              // 'during' | 'close'  (default 'during')
    onChange={setWhenMode}
    schedule={schedule}>          // read-only, viene de Programación
    <Timeline mode={whenMode} window={schedule.from..schedule.to} />
    <ScheduleBadges schedule={schedule} />
  </WhenCard>

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

> Ya **no** existe la regla `anyChannelActive → recap disabled`. "¿Cuándo?" es independiente y siempre editable.

## 5. Estados

- **Loading:** skeleton de las 3 cards (no spinner).
- **Inicial:** "¿Cuándo?" en `during` (Todo el tiempo); Email activo con un destinatario de ejemplo; Slack apagado; Idioma "Español". (En producción, estado real del backend.)
- **Canal apagado:** la tarjeta del canal muestra solo su fila (gris) sin config.
- **Canal activo sin destinatarios:** advertencia inline "Agrega al menos un destinatario" (bloquea guardar).
- **Error de validación de chip:** correo inválido → borde `destructive`, no crea el chip, microcopy bajo el campo.
- **Success:** guardado confirma con toast efímero.

## 6. Copy completo (glosario aplicado)

> Glosario Op Center: **Incidente** (no "alerta"), **Agente IA** (no "bot"), **gráfico/KPI**. Registro algo más formal que el mock original (se subió el tono y se quitó "el agente" donde no aportaba).

**Card ¿Cuándo notificar?**
- Título: `¿Cuándo notificar?` (ícono reloj)
- Opciones del selector:
  - `Todo el tiempo` → `Avisa al detectar el incidente y durante el horario programado.`
  - `Solo al cierre` → `Avisa solo al terminar, con el estado final.`
- Texto del selector (valor actual): `Todo el tiempo` / `Solo al cierre`
- Label badges: `Programación` · ejemplo: `Diario`, `08:00 a.m. – 08:00 p.m.`, `America/Bogota`

**Card ¿Dónde notificar?**
- Título: `¿Dónde notificar?` (ícono campana) · Subtítulo (debajo): `Activa uno o varios canales y configura sus destinatarios`
- Canal Email: título `Email` · label config `Correos` · placeholder `Agregar correo y Enter`
- Canal Slack: título `Slack` · aux `Slack · Simetrik` · label `Canales` (placeholder `Agregar canal y Enter`) · label `Etiquetar` (Opcional, placeholder `@persona o @equipo y Enter`)
  - *(Se quitaron los subtítulos redundantes por canal — "Recibe un correo/mensaje cuando…" — porque repetían lo mismo y ya lo enmarca el header.)*

**Card Idioma**
- Título: `Idioma` (ícono globo) · Selector: `Español`

## 7. Microinteracciones

| Interacción | Detalle |
|---|---|
| Selector "¿Cuándo?" | abre menú con descripciones; al elegir, actualiza el valor visible, el modo del timeline y cierra; cierra al clic fuera |
| Barra del timeline (`winrec-fill`) | transición de `left`/`width` `320ms ease-out` al cambiar modo; en modo `close`, pulso sutil `winrecPulse 1.8s` infinito |
| Toggle canal | `background 150ms` + knob `left 150ms`; revelar panel con altura/opacity `200ms ease-out` |
| Chip nuevo | aparece sin animación pesada; foco vuelve al input |
| Focus en `TagInput` | ring `0 0 0 3px primary/12%`, borde `primary` |

Durations canónicas: 120 / 200 / 320 ms ease-out. Sin spinners; preferir skeleton.

## 8. AI integration

- El disparador del aviso es el **Agente IA / BADS** que detecta el **incidente** sobre el gráfico. El copy atribuye la detección al Agente IA, sin badges "Powered by AI" ni sparkles.
- No hay AiChat embebido. Si se ofrece asistencia conversacional, patrón Simetrik: botón en chrome → `Sheet` lateral. Nunca burbuja flotante ni auto-abrir.

## 9. Endpoints esperados

> Mockable si aún no existen. Forma sugerida:

`GET /monitoring/{chartId}/notifications` →
```json
{
  "when": "during",
  "channels": {
    "email": { "enabled": true, "recipients": ["ana.torres@simetrik.com"] },
    "slack": { "enabled": false, "channels": ["# incidentes-finops"], "mentions": [] }
  },
  "language": "es",
  "schedule": { "recurrence": "daily", "from": "08:00", "to": "20:00", "timezone": "America/Bogota" }
}
```
`PUT /monitoring/{chartId}/notifications` con el mismo shape.

> `schedule` es **read-only** aquí (se configura en la pestaña Programación). El timeline y los badges solo lo reflejan.

## 10. Edge cases y validaciones

- Correo con formato inválido → no crear chip, mostrar microcopy.
- Canal de Slack duplicado → normalizar; no duplicar chip.
- Canal encendido sin destinatarios → bloquear guardado, advertencia inline.
- Workspace de Slack no conectado → estado del card Slack con CTA "Conectar Slack" en vez del toggle.
- Programación vacía (sin ventana definida) → el timeline/badges muestran estado neutro "Configura la ventana en Programación".
- Lista larga de destinatarios → chips hacen wrap, el input mantiene `min-width`.
- i18n: el valor de idioma afecta el **contenido enviado**, no la UI de configuración.

## 11. Test cases sugeridos

1. Cambiar a "Solo al cierre" actualiza el valor del selector, la barra del timeline y su descripción.
2. "¿Cuándo?" es editable de entrada (no depende de canales activos).
3. Encender Email revela su panel; apagar lo colapsa conservando correos.
4. Agregar correo con Enter crea chip; la "x" lo elimina.
5. Slack normaliza `incidentes` → `# incidentes` y `juan` → `@juan`.
6. Guardar con canal activo sin destinatarios muestra advertencia y no persiste.
7. Las tres cards comparten el patrón visual de Programación (header ícono+título, body).

## 12. Tokens utilizados

`--primary #3D3BF5` (toggle on, foco, chips) · `--primary-soft` (fondo chip / ring) · `--border` / `border-default` (bordes cards/inputs) · `muted /0.5` (fondo de las tarjetas de canal en ¿Dónde?) · `muted-foreground` (subtítulos, placeholders, label badges) · `text-primary #1F1B2E` · `text-tertiary` (íconos). Radius: `12px` cards, `10–11px` tarjetas de canal, `8px` inputs, `999px` chips/toggles.

## 13. Checklist pre-PR

- [ ] Las 3 cards resueltas con el mismo patrón de `Card` que Programación (header ícono+título+control/aux, body)
- [ ] "¿Cuándo?" es primer paso y **siempre editable** (sin gating por canales)
- [ ] Selector "¿Cuándo?" controla timeline (`during`/`close`); badges de Programación read-only
- [ ] ¿Dónde?: canales con fondo gris sin borde; toggle revela config inline; labels cortos (Correos/Canales/Etiquetar)
- [ ] Idioma como card propia con selector en el header
- [ ] Switch y chips con componentes desyk (no custom)
- [ ] Glosario aplicado: "Agente IA", "incidente"
- [ ] Estados completos: loading (skeleton), canal apagado/activo, partial (sin destinatarios), error de chip, success (toast)
- [ ] Microinteracciones 120/200/320 ms ease-out; sin spinner
- [ ] Light mode consistente · A11y: `aria-label` en toggles y "x" de chips, foco visible, contraste AA
- [ ] `schedule` tratado como read-only (fuente: Programación)
