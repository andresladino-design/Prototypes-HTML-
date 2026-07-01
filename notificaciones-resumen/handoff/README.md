# Handoff — Monitoreo inteligente de anomalías (notificaciones-resumen)

Specs autocontenidas para implementar el rediseño del monitoreo de anomalías de Operation Center. Origen: prototipo validado `../index.html`.

El handoff está organizado en **3 estructuras de detalle**, una por épica de ingeniería. Cada una es un `.md` autocontenido (contexto, cambios de UI enumerados, historias de UX, copy, mapeo desyk/BADS, estados, edge cases y checklist).

## Las 3 estructuras

| # | Estructura | Archivo | Qué cubre |
|---|---|---|---|
| **1** | **Filtros en la vista de incidentes** | [`handoff-1-filtros-incidentes.md`](./handoff-1-filtros-incidentes.md) | Los filtros de la lista de incidentes en **Anomalías → Gestión**: multiselect por categoría (Recurso, Tablero, Estado, Tipo, Fecha estática), lógica de combinación **O/Y**, quitar Severidad, y **filtros guardados** reutilizables (icon-only). Incluye HU-1 y el mapeo BADS de Estado/Tipo. Recurso y Tablero van **separados** (no se unifican aquí). |
| **2** | **Configuración de detección de anomalías (vista de tableros / monitoreo)** | [`handoff-2-config-anomalias-tableros.md`](./handoff-2-config-anomalias-tableros.md) | Todo lo que define **cómo se detecta una anomalía**, dentro del diálogo de monitoreo del KPI (wizard **Programación → Alertas → Series y valores**) y en la config **por fuente** (Ingesta). Sección A: **Alertas del KPI** (¿Cuándo/¿Dónde/Idioma). Sección B: **detección por serie** (Análisis inteligente + carga, general + override, Límites fijos vs Sistema adaptativo, simulación). Sección C: **Alertas por fuente** (modal de fuente + mapeo `problem_category`). |
| **3** | **Notificaciones de incidentes + vista de Anomalías (config y gestión)** | [`handoff-3-notificaciones-y-vista-anomalias.md`](./handoff-3-notificaciones-y-vista-anomalias.md) | Los **paquetes de notificación** (lista + editor con alcance "Entidades afectadas" OR, momentos del ciclo de vida, **resumen consolidado t-n** como entrega), first-run con diagrama, HU-2 a HU-5, **plantillas Email (MJML) + Slack (Block Kit)** del resumen, y los **fixes de UI** de la vista de Anomalías (segmented Gestión · Alertas levantadas · Configuración). |

### Cómo se relacionan
- La **detección** (Handoff 2) origina las señales/alertas que BADS agrupa en **incidentes**.
- Los incidentes se **filtran** en la lista de Gestión (Handoff 1) y se **notifican** por reglas/paquetes (Handoff 3).
- Los **filtros guardados** se crean en Gestión (Handoff 1); el editor de notificación (Handoff 3) los reutiliza, colapsando Tablero/Recurso a "Entidad".

## Cómo consumir
1. Cada `.md` es autocontenido: se puede implementar como épica independiente.
2. Para implementar: abrí rama nueva y usá `/simetrik-ui craft <handoff>.md` como input, o pasáselo al dev.
3. Para revisar el copy: `/simetrik-ui clarify <handoff>.md`. Cuando esté en código: `/simetrik-ui audit <implementación>`.
4. Regla del equipo: **donde un cambio de UI no se enumere explícitamente, no se ejecuta en desarrollo.** Por eso cada handoff lista todos los cambios, incluso los chicos.

## Notas transversales
- **Registro:** Interno / Operation Center. Desktop (shell de OC). Power user, alta tolerancia a densidad.
- **Glosario:** **monitoreo** (nunca "agente"/"Agente IA"/"IA" de cara al usuario), **incidente**, **señal/alerta**, **KPI**, **Tablero**, **Recurso**, **serie/categoría**.
- **Severidad** (`URGENT` / `REQUIRES_ATTENTION`) es **system-assigned** por el workflow runner de BADS → no se expone como filtro ni condición hasta que sea configurable.
- Light mode consistente. Microinteracciones canónicas **120 / 200 / 320 ms**, ease-out `cubic-bezier(0.22,1,0.36,1)`. Skeleton sobre spinner. Sin em-dashes, sin mayúsculas sostenidas en títulos.
- Guía de implementación (BADS Brain v2.8 + componentes desyk de `fe-solutions-mf`) incluida en cada handoff, acotada a su alcance.

## Origen
Estas 3 estructuras consolidan 5 handoffs previos que estaban organizados por tema (filtros+notificaciones, historias UX, límites/sensibilidad, plantillas email/slack, canales). Su contenido se reorganizó por épica de ingeniería. Los originales se conservan en el **historial de git** (borrados de la carpeta; recuperables con `git log --diff-filter=D` + `git show`).
