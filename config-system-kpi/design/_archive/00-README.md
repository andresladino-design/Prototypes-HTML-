# Config monitoreo "tablero-first" — Design package

Reframe del prototipo `index 2.html` desde "recursos monitoreados" hacia un punto de partida tablero-first con cadena de proceso visible.

## Entregables (lo que pidió el brief)

| # | Archivo | Contenido |
|---|---|---|
| 01 | [Arquitectura de información](01-arquitectura-informacion.md) | Jerarquía Tablero → Estado → KPIs/Dependencias/Notificaciones/Overrides · 7 decisiones IA |
| 02 | [User flow de configuración](02-user-flow.md) | Flujo principal 5 pasos · flujos secundarios (override, ver incidentes) · estados especiales |
| 03 | [Wireframes low-fi](03-wireframes-lowfi.md) | 4 vistas: banner del tablero · landing de monitoreo · config de tipo de alerta · incidentes filtrados |
| 04 | [Copy y glosario](04-copy-recomendaciones.md) | Glosario aplicado · banner · pipeline · wizard · incidentes · overrides · toasts · voz del agente |
| 05 | [Implementation summary](05-implementation-summary.md) | Cirugía aplicada al HTML, líneas tocadas, próximos pasos |

## Patrón visual elegido

**Patrón B — Pipeline-first**: la cadena de proceso (Ingesta → Calidad → Conciliación → KPIs) es el protagonista visual. Cliente entiende **arquitectura del sistema** en un vistazo.

## Decisiones constantes

| Constante | Valor |
|---|---|
| Scope | Refactor in-place sobre `index 2.html` |
| Usuario primario | Cliente final (analista/contador) — registro Producto |
| Rol del agente IA | Recomendador embebido (no asistente conversacional separado) |
| Estado del tablero | Landing dedicada como entry point a la configuración |
| Glosario | Fuente, Conciliación, KPI · NO "recurso", NO "dataset" en este flow |

## Bans aplicados

- Sin "Powered by AI", sin sparkle ✨, sin "Try with AI"
- Sin em-dashes (—) en copy
- Sin terminología técnica visible por defecto ("lineage", "threshold", "pipeline" → "cadena", "margen", "cómo se construye")
- Sin colores fuera de tokens desyk
- Sin glassmorphism, sin gradient text
