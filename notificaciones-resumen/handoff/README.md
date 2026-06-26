# Handoff — Diálogo de monitoreo inteligente (notificaciones-resumen)

Specs autocontenidas para implementar las secciones del diálogo de monitoreo de un gráfico (KPI "Conteo De Registros") en Operation Center. Origen: prototipo validado `index.html`.

## Archivos

| Archivo | Cubre | Componentes mock |
|---|---|---|
| [`handoff-notificaciones-canales.md`](./handoff-notificaciones-canales.md) | Notificaciones en 3 cards (mismo patrón que Programación): **¿Cuándo?** (selector + timeline 12–12 + recap) → **¿Dónde?** (canales Email/Slack) → **Idioma** | `#dsec-notif`, `tm-prog-card`, `.when-select`, `.winrec-timeline`, `.tm-notif-card`, `.tm-chip-input` |
| [`handoff-limites-sensibilidad.md`](./handoff-limites-sensibilidad.md) | **Sensibilidad = severidad por 2 bandas** (slider continuo + coloreado invertido) + límites por bound, **por categoría** (selector manda) + pill por serie + foco | `#sens-chart`, `.sens-slider`, `.cat-select`, `#cat-limits`, `#series-block`, `.tm-series-sens` |
| [`handoff-notif-email-sinGrafica-slack-ultracompact.md`](./handoff-notif-email-sinGrafica-slack-ultracompact.md) | **Plantillas de notificación del Resumen diario**: Email **sin gráfica** (MJML) + Slack Block Kit **ultra-compact**, ambas armadas 1:1 desde el JSON de incidentes (BADS), texto verbatim. Origen: `templates.html` | MJML (email) · Slack Block Kit `section`/`context`/`divider` (no desyk) |

## Cómo consumir

1. Cada `.md` es autocontenido (contexto, HU, mapeo desyk, estados, copy, endpoints, edge cases, tests, checklist).
2. Para implementar: abrí rama nueva y usá `/simetrik-ui craft <handoff>.md` como input, o pasáselo al dev.
3. Para revisar el copy: `/simetrik-ui clarify <handoff>.md`.
4. Cuando esté en código: `/simetrik-ui audit <implementación>`.

## Notas transversales

- Registro: **Interno / Op Center**. Glosario: **monitoreo**, **incidente**, **gráfico/KPI**, **valor sugerido**.
- Light mode consistente. Microinteracciones canon 120/200/320 ms ease-out. Skeleton sobre spinner.
- `schedule` (recurrencia/horario/timezone), `series`, `suggested` y `signals` son read-only en estas secciones (provienen de Programación y del monitoreo / BE respectivamente).
- **El diálogo es un wizard de 3 pasos:** Programación → Notificaciones → Series y valores (footer Atrás/Cancelar + Siguiente/Guardar).
- En Notificaciones, **"¿Cuándo?" arranca en "Nunca"** (default, empty-state) y siempre es editable. El gating es **reactivo al Siguiente**: si el modo ≠ Nunca y no hay canal, al avanzar aparece una alerta y se bloquea (no hay `disabled` preventivo).
- **Severidad = sensibilidad** (2 bandas: rojo = fuera de límites/urgente, amarillo = zona de atención/medio). Slider continuo 0–100%. Todo **por categoría** (el selector de la gráfica manda límites + slider + visibilidad de la grilla), con herencia del global.
- Copy: **no se usa el concepto de "agente"/"Agente IA"** de cara al usuario — usar **"monitoreo"** (o voz pasiva). La sección Programación no tiene doc de handoff propio (su copy vive en `index.html`).
