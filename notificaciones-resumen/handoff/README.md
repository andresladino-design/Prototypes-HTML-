# Handoff — Diálogo de monitoreo inteligente (notificaciones-resumen)

Specs autocontenidas para implementar las secciones del diálogo de monitoreo de un gráfico (KPI "Conteo De Registros") en Operation Center. Origen: prototipo validado `index.html`.

## Archivos

| Archivo | Cubre | Componentes mock |
|---|---|---|
| [`handoff-notificaciones-canales.md`](./handoff-notificaciones-canales.md) | Notificaciones en 3 cards: **¿Cuándo?** (eje de timing Nunca/Solo al final/En tiempo real + **barra-explicador con marcadores** + empty-state de primer ingreso) → **¿Dónde?** (canales Email/Slack) → **Idioma** | `#dsec-notif`, `tm-prog-card`, `.when-select`, `.winrec-timeline`+`.winrec-mk`, `.tm-notif-card`, `.tm-chip-input` |
| [`handoff-limites-sensibilidad.md`](./handoff-limites-sensibilidad.md) | **Detección de anomalías por serie** (reescrito 1-jul). Modelo **general + override**: **Límites generales de {métrica}** ("Todas las categorías") + **Límites por serie** en **colapsables inline**. Cada serie: **Límites fijos** vs **Sistema adaptativo** (Alta/Media/Baja + límites de seguridad), gráfica completa (sin AHORA), **aviso+simulación unificados**, estado **"Sin configurar"**, agregar/quitar serie. Deprecado el slider/bandas/grilla anterior. | `#nsWrap`, `.ns-acc*`, `.ns-radio`, `.ns-seg`, `.ns-lim`, `.ns-alert`, `svg.ns-chart` |
| [`handoff-notif-email-sinGrafica-slack-ultracompact.md`](./handoff-notif-email-sinGrafica-slack-ultracompact.md) | **Plantillas del Resumen de incidentes**: Email **sin gráfica** (MJML) + Slack Block Kit **ultra-compact**, ambas armadas 1:1 desde el JSON de incidentes (BADS), texto verbatim. Origen: `templates.html` | MJML (email) · Slack Block Kit `section`/`context`/`divider` (no desyk) |
| [`handoff-anomalias-historias-ux.md`](./handoff-anomalias-historias-ux.md) | **Historias de UX** (5 HU) que complementan el handoff de Anomalías: filtrar+guardar, crear notificación (first-run/plantilla), definir alcance/momento/canales, mantener notificaciones (editar/duplicar/pausar), resumen consolidado. Con estados de interfaz, criterios funcionales/experiencia, a11y. | persona: operador de Op Center |
| [`handoff-anomalias-filtros-notificaciones.md`](./handoff-anomalias-filtros-notificaciones.md) | **Vista de Anomalías** (cada cambio de UI enumerado). **Actualizado 1-jul:** **Filtros de Gestión** = Recurso, Tablero, Estado, Tipo, Fecha estática (multiselect O/Y, sin Severidad, botón Guardados icon-only) · **Notificaciones = paquetes de reglas**: alcance en dos bloques (**Entidades afectadas** con OR + conector "o" · **Tipo** en chips) + **dos entregas: aviso por evento (momentos por estado) + resumen consolidado (t-n)** · validaciones (nombre obligatorio, entrega, canal con destinatarios) · empty states/diagramas/motion. La unificación "Entidades afectadas" es **solo del editor**, no de Gestión. **Incluye Guía de implementación** (modelo BADS; mapeo desyk de `fe-solutions-mf`; shapes, máquinas de estado, validaciones). Origen: Granola 30-jun (am+pm) + Ohana | `#viewAnomalias`, `#anFMenu`, `#anCfgNotif` (`.an-pkg*`, `.an-deliv*`, `.an-scope-join`), `.an-onb-*` |

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
- En Notificaciones (rediseño 26-jun pm), **"¿Cuándo?" es un eje de timing**: **Nunca / Solo al final / En tiempo real** (señales e incidentes van juntos). Default real **`unset`** (primer ingreso) → empty-state con CTA "Configurar notificaciones". La **barra de la ventana es el explicador** (notificaciones como marcadores a su hora). Gating de canales **reactivo al Siguiente** (modo ≠ Nunca/unset y sin canal → alerta, no avanza). ⚠️ Validar con Iván el estado que reporta BADS al cierre.
- **Severidad = sensibilidad** (2 bandas: rojo = fuera de límites/urgente, amarillo = zona de atención/medio). Slider continuo 0–100% + **mini-dashboard de impacto** (3 tiles). Todo **por categoría** (el selector manda límites + slider + grilla), con herencia del global. Gráfica + impacto + límites + sensibilidad en **una sola card**. **Actualizado 30-jun pm:** extremos reencuadrados — izq **"Solo mi umbral"** (alerta de umbral fija) ↔ der **"Detección adaptativa"** (el sistema decide qué es anómalo); se quita "nula". La banda **nunca llega al centro** (núcleo normal `CORE=0.30`): aun al 100% no se cubre toda la gráfica.
- **Resumen de incidentes** (botón en la vista de monitoreo): label corto "Resumen de incidentes"; el popover aclara alcance ("de este tablero") y hora configurable ("a la hora que elijas", sin "cada mañana"). Plantillas en `handoff-notif-email-sinGrafica-slack-ultracompact.md`.
- Copy: **no se usa el concepto de "agente"/"Agente IA"** de cara al usuario — usar **"monitoreo"** (o voz pasiva). La sección Programación no tiene doc de handoff propio (su copy vive en `index.html`).
