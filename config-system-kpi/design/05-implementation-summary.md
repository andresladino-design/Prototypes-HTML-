# Implementation summary — Cirugía sobre `index 2.html`

Cambios aplicados al prototipo en este pase de `craft`. Todos son **in-place y reversibles** (el código viejo del popover se conserva con `display:none`).

## Cambios visibles

### 1 · Health Banner del tablero (NUEVO)

**Qué**: Banner persistente entre el header del tablero y los sub-tabs, con 3 bloques:
- Estado verbal narrativo ("2 KPIs podrían retrasarse hoy")
- Pipeline horizontal Ingesta → Calidad → Conciliación → KPIs
- CTAs "Ver incidentes (1)" + "Configurar monitoreo"

**Estados** soportados vía clase: `is-warn`, `is-critical`, `is-ok` (default), `is-idle` (sin monitoreo).

**Reemplaza a**: el popover "Recursos monitoreados" del header (queda oculto, no eliminado).

### 2 · Reorganización del sidebar de monitoreo

Antes (Salud de los datos colapsable):
```
Incidencias
Historial
Configuración ▾
  Salud de los datos
    · Ingesta
    · Calidad (próx.)
    · Conciliación (próx.)
  Monitoreo en gráficos
```

Después (IA tablero-first):
```
Estado del monitoreo  ← NUEVO landing
Incidentes (1)        ← renombrado, ahora con counter
Historial
Configuración ▾
  KPIs monitoreados   ← subido al top (era "Monitoreo en gráficos")
  Dependencias        ← renombrado de "Salud de los datos"
    · Fuentes         ← renombrado de "Ingesta"
    · Calidad (próx.)
    · Conciliación (próx.)
  Notificaciones (próx.)  ← NUEVO
  Overrides (próx.)       ← NUEVO
```

### 3 · Landing "Estado del monitoreo" (NUEVA vista)

**Qué**: Template Alpine que aparece cuando `anomaliesNav === 'monitoring.landing'` (default al entrar a la sección).

Contenido:
- Resumen actionable (callout) con CTA directo al incidente activo.
- Pipeline visual full (4 stages) con click en cada una para ir a su sub-sección.
- Lista de 5 KPIs monitoreados con estado individual + chip de override / aprendizaje.

### 4 · Copy actualizado en vistas bulk existentes

- **"Monitoreo de ingesta"** → **"Fuentes que alimentan tu tablero"** (header + sub-copy reescritos).
- **"Monitoreo en gráficos"** → **"KPIs monitoreados"** (header + sub-copy reescritos).
- **Wizard paso 1** → "¿Cómo querés monitorear esta Fuente?" (era "recurso").
- **`currentSectionTitle`** ahora soporta los 7 estados nuevos.

### 5 · Default state del prototipo

`anomaliesNav` inicial = `'monitoring.landing'` (era `'incidents'`). Al hacer clic en el tab "Incidentes" del header global o el CTA "Configurar monitoreo" del banner, el usuario aterriza en la nueva landing.

## Líneas tocadas (aprox)

| Bloque | Líneas (aprox) | Tipo |
|---|---|---|
| CSS `.tb-health-*` + `.tm-*` | añadidas antes de `</style>` | nuevo |
| Botón group "Recursos monitoreados" | header del tablero | oculto (`display:none`) |
| Health Banner del tablero | inserción entre header y sub-tabs | nuevo |
| Sidebar de monitoreo (anomalies-nav-panel) | bloque navegación lateral | rewrite |
| Default `anomaliesNav` | inicialización JS de Alpine | cambio de valor |
| `currentSectionTitle` switch | helper JS | expandido |
| Wizard paso 1 título/subtítulo | dentro del setup wizard | copy update |
| Vista bulk Ingesta | header del bulk | copy update |
| Vista bulk Charts | header del bulk | copy update |
| Landing template (monitoring.landing) | inicio del `.anomaly-detail-area` | nuevo |

## Lo que se mantuvo (compatibilidad)

- Shell Op Center (sidebar dark 48px + header tabs principales).
- Lista de tableros del panel izquierdo (`width:268px`).
- Wizard de setup completo (solo cambió copy del paso 1).
- Componentes desyk usados (botones, popovers, sheets — todos legacy).
- Tokens HSL del prototipo.
- AI gradient (--ai-purple → --ai-blue) — preservado, podrá usarse cuando aparezca el agente recomendador en pasos siguientes.

## Lo que NO se implementó en este pase

Diferido por ser estructural (requiere más sesiones de design + dev):

- **Diagrama de lineage del Paso 2** del wizard (Fuentes → KPIs). Hoy aparece como texto. Necesita componente custom (candidato para `extract` después).
- **Modal de override** del flujo secundario. Diseñado en `02-user-flow.md` pero no implementado.
- **Modo prudente** con countdown. Diseñado en copy, no en lógica de estado.
- **Reescritura del wizard de 5 pasos** del brief. Hoy el wizard tiene su propia secuencia legacy (treatment → groups → cadencia → indicadores). Hay overlap parcial con los 5 pasos del brief pero requiere mapeo más fino.
- **Vista "Notificaciones"** y **"Overrides"** — están en el nav como `próx.`, sin templates de contenido.

## Próximos pasos sugeridos

1. **Validar en browser** abriendo `index 2.html` y navegando: dashboard view → click "Configurar monitoreo" del banner → debería caer en "Estado del monitoreo" landing.
2. **`/simetrik-ui critique`** sobre el banner para review heurístico independiente.
3. **`/simetrik-ui polish`** del banner si la jerarquía visual necesita ajustes finos.
4. **Diseñar el wizard de 5 pasos** como sesión separada (puede ser `shape` + `craft` enfocado solo en el wizard).
5. **`/simetrik-ui extract`** del pipeline component (`.tb-health-pipeline` + `.tm-pipeline-full`) como candidato a desyk-components nuevo (`<DataPipeline />`).

## Componentes custom introducidos (candidatos a extract)

| Componente | Selector | Reutilización potencial |
|---|---|---|
| Tablero Health Banner | `.tb-health` + `.tb-stage` + `.tb-health-actions` | Cualquier vista que necesite estado de un proceso multi-stage |
| Data Pipeline visualization | `.tm-pipeline-full` + `.tm-pipeline-stage` + `.tm-pipeline-arrow` | Vistas de lineage, ETL status, flujos de conciliación |
| KPI Row con estado + chip | `.tm-kpi-row` + `.tm-kpi-state` + `.tm-kpi-chip` | Listas de KPIs en cualquier dashboard |
| Summary callout actionable | `.tm-summary` con `tm-summary-link` | Banners de alertas en otras secciones |
