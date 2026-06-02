# 06 · Métricas de experiencia

> Cómo sabremos que el rediseño de navegación del monitoreo funcionó. Cierra el trío **problema → solución → métrica**: los problemas y soluciones están en [`05-implementation-summary.md`](./05-implementation-summary.md); acá definimos qué seguir, cómo instrumentarlo y cómo validarlo. Documento de trabajo: las baselines y targets se llenan a medida que medimos.

## North star del feature

**% de tableros con monitoreo configurado** (al menos una fuente o métrica monitoreada por tablero activo).

Todo lo demás son métricas que explican por qué ese número sube o no. Las dividimos en: comprensión del modo (¿el rediseño se entiende?), activación/eficiencia (¿mueve el north star?), confianza (¿se fían del resultado?) y guardrails (¿rompimos algo de al lado?).

## 1 · Métricas atadas a cada cambio

Cada fila conecta una decisión de diseño (ver `05`) con la métrica que la valida.

| Cambio | Problema que resolvía | Métrica | Cómo se mide | Señal de éxito |
|---|---|---|---|---|
| Botón "Volver al tablero" (sin breadcrumb) | "¿cómo me devuelvo, dónde estoy?" | % de salidas por el botón vs back del browser / clic al sidebar; tiempo hasta volver | evento `mode_exit` con `method`; replay | Mayoría sale por el botón; salir no requiere "buscar cómo" |
| Modo (no página) + tab "Tableros" activo + glow | sentía que se iba a otra página / no sabía en qué modo estaba | **lost-then-found**: entradas a monitoreo con salida <5s sin acción; mode-awareness en test ("¿estás en monitoreo o en el tablero?") | `mode_enter`→`mode_exit` sin eventos intermedios; test moderado | Baja la salida inmediata; alta mode-awareness |
| Acciones ocultas en monitoreo | ofrecían acciones inejecutables | intentos de Editar/Descargar desde monitoreo | (no debería existir el evento) | ~0 clicks frustrados |
| Acciones en la barra de tabs (buscar + Activar N) | dispersas, costaba encontrarlas | time-to-first-interaction con buscar/activar; uso de "Activar las N" vs config 1-a-1 | `tab_change`, `search_input`, `bulk_activate_open` | Encuentran rápido; mayor uso del bulk |
| Banner conceptos arriba + contexto persistente | al cerrar el banner se perdía contexto | dismiss-rate del banner **y** si tras cerrarlo igual completan una config | `banner_dismiss` + `source_config_save` en la misma sesión | Cierran el banner sin que caiga la activación |
| Reset de modo por entidad | abrir otro tablero directo en monitoreo (impredecible) | % de aperturas de tablero que arrancan en modo Tablero | `dashboard_open` con `mode` inicial | ~100% arrancan en Tablero |

## 2 · Activación y eficiencia (mueven el north star)

| Métrica | Definición | Baseline | Target |
|---|---|---|---|
| Tasa de activación | de los que entran a monitoreo, % que guarda ≥1 configuración | _por medir_ | _por definir_ |
| Time-to-first-monitor | desde abrir el tablero hasta la primera config guardada | _por medir_ | _por definir_ |
| Cobertura | fuentes monitoreadas / fuentes del tablero | _por medir_ | _por definir_ |
| Profundidad por etapa | distribución de tabs visitados (Ingesta / Métricas / …) | _por medir_ | _por definir_ |
| Uso de activación masiva | sesiones que usan "Activar las N" vs solo 1-a-1 | _por medir_ | _por definir_ |

## 3 · Confianza (lagging, cualitativo)

- **Reducción del monitoreo manual** (lo que salió en las reuniones de Granola: entrar al gestor de archivos / monitor de fuentes a mano). Medir vía encuesta o entrevista; idealmente proxy de uso si existe telemetría de esas vistas.
- **CSAT / SUS** post-tarea, con una pregunta puntual: *"¿qué tan claro fue entrar y salir del monitoreo?"* (escala 1-5).
- **% de anomalías accionadas** (¿confían en lo que detecta?).

## 4 · Guardrails (no romper lo de al lado)

- Uso normal del tablero y tiempo de tarea en el dashboard **no deben caer**.
- El glow de modo no debe generar quejas (se valida en el test, no por métrica).
- La frecuencia de "Volver al tablero" inmediato no debe dispararse (señal de entrada accidental al modo).

## 5 · Plan de instrumentación (eventos a loguear)

Eventos mínimos para construir los ratios de arriba (nombres sugeridos):

| Evento | Props |
|---|---|
| `dashboard_open` | `dashboard_id`, `initial_mode` |
| `mode_enter` | `dashboard_id`, `source` = `header_button` \| `banner` \| `context_menu` |
| `mode_exit` | `dashboard_id`, `method` = `back_button` \| `browser_back` \| `sidebar` |
| `tab_change` | `from`, `to` (ingesta/calidad/conciliacion/metricas) |
| `search_input` | `tab`, `has_query` |
| `bulk_activate_open` / `bulk_activate_complete` | `count`, `partial_count` |
| `source_config_open` / `source_config_save` | `source_id`, `profile` (low/family/high) |
| `banner_dismiss` | `banner` = `conceptos` \| `zero_state` |
| `monitoring_activated` | `dashboard_id` (primera vez que el tablero queda monitoreado) |

## 6 · Cómo medir según la etapa

- **Ahora (prototipo)** → **test de usabilidad moderado, ~5 usuarios**, sobre las 3 tareas clave:
  1. Entrar al monitoreo de un tablero.
  2. Configurar el monitoreo de una fuente.
  3. Volver al tablero.
  Capturar: mode-awareness, lost-then-found, dónde dudan, y SUS al cierre. Es lo más barato y lo que más aprende a este nivel; no requiere instrumentación.
- **Post-dev** → instrumentar los eventos de la sección 5 y armar los ratios. Revisar a las 2 y 6 semanas del release.

## 7 · Set priorizado para arrancar (5)

Si hay que empezar por pocas, estas cinco cubren comprensión + activación:

1. **Tasa de activación** (north star operativo).
2. **Lost-then-found** (¿el modelo de modo se entiende?).
3. **Método de salida** (¿usan "Volver al tablero"?).
4. **Time-to-first-monitor** (¿hay fricción para configurar?).
5. **SUS / pregunta de claridad** del test moderado (señal cualitativa temprana).

## Pendiente de este doc

- [ ] Correr el test moderado de 5 usuarios y llenar mode-awareness + SUS.
- [ ] Definir baselines y targets de las tablas (secciones 1 y 2).
- [ ] Confirmar con datos/eng si existe telemetría del "monitoreo manual" para el proxy de confianza.
