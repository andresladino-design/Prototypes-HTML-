# Plan 3 — Auditar el Operation Center actual

## Objetivo
Inventariar cómo está compuesto hoy el Operation Center para decidir qué patrones existentes reutiliza el centro de disputas y qué necesita ser nuevo — evitando inventar UI que ya existe.

## Contexto clave (Granola 7-jul)
- La idea inicial es que los gráficos de disputas vivan **dentro del Operation Center como un tab más**, con dataset preseleccionado al añadir gráfico.
- Pero la **tabla de control de reclamos tiene un esquema distinto** al del OC → hipótesis: sacarla del tablero estándar y dejarla como **vista propia** del módulo de disputas. Esta auditoría debe dar el veredicto.

## Fuentes a revisar (solo lectura)
- Prototipos previos en `ops-roadmap/` del repo Prototypes-HTML (convención del repo)
- `fe-solutions-mf` (estado real de prod, como se hizo en notif-resumen)
- `_refs/desyk-components` — componentes disponibles (tabla, tabs, badges, progress, charts) — **solo lectura**
- `_refs/ProductEngineeringBrain` — épicas/PRDs relacionadas con Operation Center y anomalías — **solo lectura**
- Trabajo previo de anomalías/notif-resumen (payload BADS: narrativa IA, severidad, recommended_actions→botones, agrupado por recurso — patrón directamente reutilizable para el agente de disputas)

## Actividades
1. **Inventario de patrones del OC:** navegación (tabs), tableros y widgets/gráficos, tablas con sort/filtros, sistema de severidades y badges, empty states, configuración de notificaciones.
2. **Mapear cada elemento del centro de disputas contra el inventario:**
   - KPIs (activas, por vencer <3d, win rate, VAMP) → ¿widgets de tablero existentes?
   - Gráficos (CBK por franquicia/moneda/semana, picos, anomalías por reason code) → ¿charts del OC con dataset preseleccionado?
   - Tabla de reclamos (reclamo, franquicia, país, adquirente, merchant, valor, moneda, SLA, win probability, estado) → ¿la tabla estándar soporta este esquema o exige vista propia?
   - Narrativa/acciones del agente → ¿reutilizar el patrón BADS de anomalías?
3. **Veredicto de arquitectura de información:** tab del OC vs. vista propia, con argumentos.
4. Registrar en `design.md` (via `ohana_init_design`/`ohana_update_design`) los tokens y componentes desyk que usará el prototipo.

## Entregables
- `handoff/auditoria-oc.md` — inventario, mapeo reutilizar/nuevo, veredicto de ubicación
- `design.md` inicializado con tokens y patrones elegidos

## Done cuando
Cada pieza del centro de disputas está clasificada como «reutiliza patrón X del OC» o «nuevo, porque…», y hay recomendación de ubicación para discutir con Andrea.
