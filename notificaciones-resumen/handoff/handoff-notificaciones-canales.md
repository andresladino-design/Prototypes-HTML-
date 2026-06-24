# Handoff — Notificaciones por canal + Ventana de monitoreo

Fecha: 2026-06-24
Origen: `notificaciones-resumen/index.html` → sección `#dsec-notif` del diálogo de monitoreo (prototipo validado)
Registro: **Interno (Operation Center)** — operador Simetrik configurando el monitoreo inteligente de un gráfico (K Cast)
Patrón de presentación: **Cards apiladas con configuración progresiva** + **resumen visual (timeline)** — no formulario plano

---

## 1. Contexto y objetivo

Dentro del diálogo de "Monitoreo inteligente" de un gráfico, la pestaña **Notificaciones** define **por dónde** avisa el Agente IA cuando detecta un **incidente** y **cuándo** lo hace durante la ventana de monitoreo.

Objetivo de la interfaz: que el operador active uno o más canales (Email, Slack), indique destinatarios, decida el idioma y entienda de un vistazo **en qué franja horaria** se va a notificar — sin tener que reconstruir mentalmente lo que configuró en la pestaña Programación.

Decisión de patrón: **configuración progresiva**. El detalle de cada canal (correos, canales, menciones) aparece solo cuando el canal se enciende. La ventana de monitoreo se muestra como **recap visual de solo lectura**, deshabilitado hasta que exista al menos un canal activo.

## 2. Usuario y registro

- **Registro:** Interno / Op Center. Operador Simetrik que monitorea múltiples clientes.
- **Perfil:** power user, uso recurrente, alta tolerancia a densidad.
- **Modo de uso:** configura una vez por gráfico, edita ocasionalmente. Estado emocional: rutina concentrada, quiere confirmar que "a quién y cuándo" quedó bien sin error.
- **Dato clave al primer vistazo:** ¿qué canales están activos y en qué franja horaria notifican?

## 3. Historias de usuario

**HU-1 — Activar un canal de notificación**
> Como operador de Op Center, quiero encender Email o Slack para recibir el aviso del Agente IA cuando detecte un incidente en este gráfico, para enterarme por el medio donde ya trabajo.
- Al encender el toggle, se revela inline (misma card) el panel de configuración del canal.
- Al apagarlo, el panel se colapsa pero conserva lo escrito.

**HU-2 — Definir destinatarios como chips**
> Como operador, quiero agregar varios correos / canales / menciones y quitarlos fácil, para dirigir el aviso a las personas correctas.
- Escribir + Enter crea un chip removible. La "x" lo elimina.
- Slack normaliza a `# canal` y `@persona`.

**HU-3 — Entender cuándo se notifica (recap visual)**
> Como operador, quiero ver en una línea de tiempo en qué parte de la ventana voy a recibir avisos, para confiar en que no me perderé el incidente ni me llegará ruido fuera de horario.
- Recap deshabilitado mientras no haya canal activo (no hay a quién notificar).
- Toggle binario "Todo el tiempo" / "Solo al cierre" que reconfigura la barra del timeline y el copy.

**HU-4 — Elegir idioma de las notificaciones**
> Como operador, quiero fijar el idioma de correos y mensajes de Slack, para que el destinatario lo reciba en su idioma.

## 4. Arquitectura de componentes desyk

> Reemplazar el HTML mock por componentes reales de `@simetrikinc/desyk-components` + Tailwind. Mapeo:

| Mock (prototipo) | Componente desyk | Notas |
|---|---|---|
| `.tm-notif-card` | `Card` (composición) | contenedor por canal; estado `is-open` → render condicional del panel |
| `.tm-notif-row-toggle` | `Switch` | `checked`, `onCheckedChange`; color on = `--primary` |
| `.tm-notif-row-icon` | `Icon` (Lucide) | `mail`, ícono Slack, `globe` · 18px · `text-tertiary` |
| `.tm-chip-input` + `.tm-chip` | `TagInput` / `ChipInput` | entrada con chips removibles; `radius 999px` |
| `.tm-notif-row-lang` | `Select` / `DropdownMenu` (trigger botón) | valor por defecto "Español" |
| `.winrec` (recap) | `Card` solo-lectura + componente timeline custom | estado `disabled` controlado por canales activos |
| `.bgroup` (Todo el tiempo / Solo al cierre) | `SegmentedControl` | 2 opciones, valor controlado |
| `.winrec-badge` | `Badge` (variante outline) | recurrencia / horario / timezone (solo lectura) |

**Estructura sugerida (React):**

```
<NotificationsSection>
  <ChannelCard channel="email"  enabled={...} onToggle={...}>
    <TagInput label="¿A qué correos enviar la notificación?" type="email" values={emails} />
  </ChannelCard>
  <ChannelCard channel="slack" enabled={...} onToggle={...} aux="Slack · Simetrik">
    <TagInput label="¿A qué canales enviar?" type="channel" values={channels} />
    <TagInput label="¿Etiquetar a alguien en el canal?" optional type="mention" values={mentions} />
  </ChannelCard>
  <LanguageRow value={lang} onChange={...} />
  <MonitoringWindowRecap disabled={!anyChannelActive} mode={whenMode} schedule={...} />
</NotificationsSection>
```

Regla de habilitación (del prototipo, `syncWinrec()`):
`anyChannelActive = email.enabled || slack.enabled` → si es `false`, el recap va `disabled` (`opacity .45`, `pointer-events:none`).

## 5. Estados

- **Loading:** skeleton de las 3 cards (no spinner). El recap muestra placeholder de timeline.
- **Empty / inicial:** ambos canales apagados → recap deshabilitado con copy "Activa un canal para configurar cuándo notificar". Idioma por defecto Español.
- **Un canal activo:** panel del canal desplegado; recap habilitado.
- **Error de validación de chip:** correo inválido → borde `destructive`, no crea el chip, microcopy bajo el campo.
- **Partial:** canal encendido sin destinatarios → advertencia inline "Agrega al menos un destinatario" (bloquea guardar).
- **Success:** guardado confirma con toast efímero; no banner persistente.

## 6. Copy completo (glosario aplicado)

> Glosario Op Center respetado: **Incidente** (no "alerta"), **Agente IA** (no "bot"), **gráfico/KPI**.

**Card Email**
- Título: `Email`
- Sub: `Recibe un correo cuando el Agente IA detecte un incidente en este gráfico.`
  *(Cambio vs prototipo: "el agente" → "el Agente IA" para respetar glosario.)*
- Label campo: `¿A qué correos enviar la notificación?`
- Placeholder: `Agregar correo y Enter`

**Card Slack**
- Título: `Slack` · aux: `Slack · Simetrik`
- Label campo 1: `¿A qué canales enviar?` · placeholder: `Agregar canal y Enter`
- Label campo 2: `¿Etiquetar a alguien en el canal?` (Opcional) · placeholder: `@persona o @equipo y Enter`

**Card Idioma**
- Título: `Idioma de notificaciones`
- Sub: `Idioma en que recibirás los correos y mensajes de Slack.`
- Valor: `Español`

**Recap ventana de monitoreo — ¿cuándo notificar?**
- Modo `during` → Título: `Notificación · todo el tiempo` · Sub: `Avisa apenas se detecta y te manda las actualizaciones (reconfirmar, resolver) mientras dura la ventana.`
- Modo `close` → Título: `Notificación · solo al cierre` · Sub: `Avisa solo al cerrar la ventana, con el estado final. Si el incidente ya se resolvió, no te llega nada.`
- Segmented: `Todo el tiempo` / `Solo al cierre`
- Label badges: `Programación` · badges ejemplo: `Diario`, `08:00 a.m. – 08:00 p.m.`, `America/Bogota`

## 7. Microinteracciones

| Interacción | Detalle |
|---|---|
| Toggle canal | `background 150ms` + desplazamiento del knob `left 150ms`; revelar panel con altura/opacity `200ms ease-out` |
| Chip nuevo | aparece sin animación pesada; foco vuelve al input |
| Recap habilitar/deshabilitar | `opacity .2s ease-out` (canon: 200ms) |
| Barra del timeline (`winrec-fill`) | transición de `left`/`width` `320ms ease-out` al cambiar modo; en modo `close` pulso sutil `winrecPulse 1.8s` infinito |
| Focus en `TagInput` | ring `0 0 0 3px primary/12%`, borde `primary` |

Durations canónicas: 120 / 200 / 320 ms ease-out. No usar spinners; preferir skeleton.

## 8. AI integration

- El disparador del aviso es el **Agente IA / BADS** que detecta el **incidente** sobre el gráfico. El copy debe atribuir la detección al Agente IA (core del producto), sin badges "Powered by AI" ni sparkles.
- No hay AiChat embebido en esta sección. Si se ofrece asistencia conversacional, sigue el patrón Simetrik: botón en chrome → `Sheet` lateral. **Nunca** burbuja flotante ni auto-abrir.

## 9. Endpoints esperados

> Mockable si aún no existen. Forma sugerida:

`GET /monitoring/{chartId}/notifications` →
```json
{
  "channels": {
    "email": { "enabled": true, "recipients": ["ana.torres@simetrik.com"] },
    "slack": { "enabled": false, "channels": ["# incidentes-finops"], "mentions": [] }
  },
  "language": "es",
  "when": "during",
  "schedule": { "recurrence": "daily", "from": "08:00", "to": "20:00", "timezone": "America/Bogota" }
}
```
`PUT /monitoring/{chartId}/notifications` con el mismo shape.

> `schedule` es **read-only** aquí (se configura en la pestaña Programación). El recap solo lo refleja.

## 10. Edge cases y validaciones

- Correo con formato inválido → no crear chip, mostrar microcopy.
- Canal de Slack duplicado → ignorar o normalizar; no duplicar chip.
- Canal encendido sin destinatarios → bloquear guardado, advertencia inline.
- Workspace de Slack no conectado → estado del card Slack con CTA "Conectar Slack" en vez del toggle.
- Programación vacía (sin ventana definida) → recap muestra estado neutro "Configura la ventana en Programación".
- Lista larga de destinatarios → chips hacen wrap, el input mantiene `min-width`.
- i18n: el valor de idioma afecta el **contenido enviado**, no la UI de configuración.

## 11. Test cases sugeridos

1. Encender Email revela su panel; apagar lo colapsa conservando correos.
2. Agregar correo con Enter crea chip; la "x" lo elimina.
3. Slack normaliza `incidentes` → `# incidentes` y `juan` → `@juan`.
4. Con ambos canales apagados, el recap está deshabilitado e inerte.
5. Encender un canal habilita el recap.
6. Cambiar a "Solo al cierre" actualiza barra del timeline + título + subtítulo.
7. Guardar con canal activo sin destinatarios muestra advertencia y no persiste.

## 12. Tokens utilizados

`--primary #3D3BF5` (toggle on, foco, chips) · `--primary-soft` (fondo chip / ring) · `--border` / `border-default` (bordes cards/inputs) · `muted-foreground` (subtítulos, placeholders) · `text-primary #1F1B2E` · `text-tertiary` (íconos) · `--ai-purple` (acento monitoreo inteligente, si aplica al header). Radius: `12px` cards, `10px` inputs, `999px` chips/toggles.

## 13. Checklist pre-PR

- [ ] Cards y switch resueltos con componentes desyk (no toggles custom)
- [ ] Glosario aplicado: "Agente IA", "incidente" (corregir "el agente" del mock)
- [ ] Configuración progresiva: panel solo visible con canal activo
- [ ] Recap deshabilitado sin canal activo; habilitado al encender uno
- [ ] Estados completos: loading (skeleton), empty, partial, error de chip, success (toast)
- [ ] Microinteracciones 120/200/320 ms ease-out; sin spinner
- [ ] Light mode consistente
- [ ] A11y: `aria-label` en toggles y "x" de chips, foco visible, contraste AA
- [ ] Schedule tratado como read-only (fuente: Programación)
- [ ] Tests: happy path + canal sin destinatarios + recap deshabilitado
