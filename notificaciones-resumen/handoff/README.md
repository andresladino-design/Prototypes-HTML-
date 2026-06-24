# Handoff — Diálogo de monitoreo inteligente (notificaciones-resumen)

Specs autocontenidas para implementar las secciones del diálogo de monitoreo de un gráfico (K Cast) en Operation Center. Origen: prototipo validado `index.html`.

## Archivos

| Archivo | Cubre | Componentes mock |
|---|---|---|
| [`handoff-notificaciones-canales.md`](./handoff-notificaciones-canales.md) | Canales de notificación (Email, Slack, Idioma) + recap de la ventana de monitoreo ("¿cuándo notificar?") | `#dsec-notif`, `.tm-notif-card`, `.tm-chip-input`, `.winrec`, `.bgroup` |
| [`handoff-limites-sensibilidad.md`](./handoff-limites-sensibilidad.md) | Sensibilidad del KPI + límites duros por bound con valor sugerido por el Agente IA | `.sens-row`, `.tm-limits-block`, `.tm-limit-field` |

## Cómo consumir

1. Cada `.md` es autocontenido (contexto, HU, mapeo desyk, estados, copy, endpoints, edge cases, tests, checklist).
2. Para implementar: abrí rama nueva y usá `/simetrik-ui craft <handoff>.md` como input, o pasáselo al dev.
3. Para revisar el copy: `/simetrik-ui clarify <handoff>.md`.
4. Cuando esté en código: `/simetrik-ui audit <implementación>`.

## Notas transversales

- Registro: **Interno / Op Center**. Glosario: **Agente IA**, **incidente**, **gráfico/KPI**, **valor sugerido**.
- Light mode consistente. Microinteracciones canon 120/200/320 ms ease-out. Skeleton sobre spinner.
- `schedule` (recurrencia/horario/timezone) y `suggested` son read-only en estas secciones (provienen de Programación y del Agente IA respectivamente).
