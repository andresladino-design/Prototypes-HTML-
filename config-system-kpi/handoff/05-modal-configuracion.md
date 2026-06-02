---
epic: MONITOR_INGESTA
issue_type: Feature
priority: P0
estimate: XL
labels: [ux, frontend, monitoring, modal, ai, daysetup]
depends_on: [04-cards-monitores-ingesta]
blocks: [07-contenedor-ventana-de-tiempo, 08-contenedor-comportamiento-dia, 09-contenedor-volumen-archivos, 10-contenedor-cantidad-registros, 11-contenedor-notas-adicionales, 12-contenedor-grupos-high]
component_areas: [modal-config, daysetup, ai-analysis]
---

# 05 · Modal de configuración del monitor (daysetup)

> Modal principal donde se define cómo monitorear una fuente. Soporta tres perfiles (Low / Family / High), ventana de tiempo, configuración por día y agrupación por patrones detectados. Es el corazón del flujo de monitoreo de ingesta.

## Resumen

- **Quién lo ve**: usuario que entró por una card de fuente (`selectedConfigSource !== null`).
- **Cuándo**: configurando una fuente nueva (después del activation loader) o revisando/editando una fuente ya monitoreada.
- **Qué decisión habilita**: definir el comportamiento esperado de una fuente (ventana de tiempo, volumen, cantidad de registros, notas) y elegir el nivel de granularidad (uniforme, por día o por grupos de archivos).
- **Por qué existe**: el monitoreo no es one-size-fits-all. Una fuente puede tener un comportamiento estable (Low), variar por día (Family) o tener patrones internos por tipo de archivo (High). El modal escala progresivamente: empieza fácil (Low) y se promueve solo cuando el usuario lo necesita.

## Anatomía

| Componente | Clase / selector | Función |
|---|---|---|
| Backdrop | `.dialog-backdrop` con `x-show="selectedConfigSource"` | Cierra el modal al click en el fondo |
| Panel | `.resource-config-panel` con `:class="inlineActiveMode === 'daysetup' && 'is-fixed-h'"` | Contenedor del modal (768 x 740) |
| Cerrar | `.resource-config-close` | Limpia `selectedConfigSource`, `inlineActiveMode`, `editMode`, `setupMode` |
| Header fuente | `.src-header` con `.src-thumb`, `.src-name`, `.src-meta` | Identificación de la fuente |
| Shell daysetup | `.ds-mode > .ds-shell > .ds-scroll` | Cuerpo scrolleable + footer fijo |
| Feedback Low→Family | `.ds-feedback` con `x-show="daySetup.changeFeedback"` | Banner informativo cuando se promueve a Family |
| Topbar | `.ds-topbar` con `.ds-monitor` (dropdown) y `.ds-ai-btn` | Dropdown "Monitorear" + botón "Resultados de análisis" |
| Card ventana | `.ds-card.has-hanging-footer` con `.ds-card-head`, `config-grid.cols-2` | Ventana de tiempo (transversal a los 3 perfiles) |
| Card comportamiento | `.ds-card` con `.ds-tabs-row` y `.ds-day-head` | Tab switcher + contenido del día activo |
| Tab switcher | `.ds-tabs-wrap` con `.ds-lock` (candado) + `.tm-tabs` (7 días) | Switch de días con dot primary cuando hay monitoreo |
| Badge Low | `.ds-low-chip` con `x-show="daySetup.monitorMode === 'igual'"` | Warning "Igual todos los días" |
| Toggle día | `.ds-day-toggle` con `.ds-switch` | Monitorear o no monitorear el día activo |
| Banner grupos | `.ds-groups-banner` con `.ds-groups-banner-illu`, `.ds-groups-banner-pill`, `.ds-groups-cta` | Promoción a High (botón "Monitorear grupos") |
| Loader pedagógico | `.calc-loader` con `x-show="daySetup.loading"` | Spinner 1.4s al activar grupos |
| Indicadores | `.ds-indicator` (Volumen, Cantidad de registros) con `.ds-indicator-head`, `.ds-input-with-suffix`, `.ds-ai-chip` | Configuración numérica con sugerencias AI |
| Notas | `.ds-notes` con `.ds-notes-tags`, `.ds-notes-textarea` | Comportamientos adicionales (colapsado por default) |
| Grupos High | `.ds-group` con `.ds-group-head`, `.ds-group-body`, `.ds-peek-card` | Cards colapsables por grupo de archivos |
| Peek | `.ds-peek-card` con `.ds-peek-section` (patrón + archivos + revisión) | Inspector estilo "go-to-definition" |
| Footer wizard | `.wizard-actions` con `.wizard-btn-secondary` y `.wizard-btn-primary` | Salir / Guardar (edición) o Eliminar / Editar (read-only) |
| Modal Análisis | Doc separado `aiAnalysisOpen` + `.ai-analysis-panel` | "Resultados de análisis" con 5 cards colapsables |

## Estados

| Estado | Origen | Visual |
|---|---|---|
| **Cerrado** | `selectedConfigSource === null` | Modal no renderiza |
| **Daysetup edición (fuente nueva)** | `inlineActiveMode === 'daysetup'`, `daySetupReadonly === false`, `daySetupHasConfig === false` | Inputs editables, chips AI visibles, banner grupos visible si no se activaron, footer "Salir / Guardar" |
| **Daysetup edición (fuente existente)** | `inlineActiveMode === 'daysetup'`, `daySetupReadonly === false`, `daySetupHasConfig === true` | Inputs editables, chips AI ocultos, footer "Salir / Guardar" |
| **Daysetup solo-lectura** | `daySetupReadonly === true` | Inputs disabled, switches con opacity 0.6, footer "Eliminar monitoreo / Editar" |
| **Low** | `monitorMode === 'igual'`, `useGroupsAll === false` | Candado cerrado, badge `.ds-low-chip` visible, sin dots en tabs, una sola config compartida (`daySetup.shared`) |
| **Family** | `monitorMode === 'por-dia'`, `useGroupsAll === false` | Candado abierto, dots primary en días con monitoreo prendido, una config por día (`daySetup.days[i].simple`) |
| **High** | `useGroupsAll === true` | Banner grupos oculto, contenido por grupo (cards `.ds-group`), una config por grupo por día |
| **Loading grupos** | `daySetup.loading === true` | Loader pedagógico visible 1.4s, grupos se siembran en background |
| **Day off** | `dsActiveDay().monitorEnabled === false` | Solo se muestra el toggle, sin indicadores ni notas |
| **Day off High sin grupos** | `useGroupsAll && dsActiveDay().groups.length === 0` | Estado vacío "No detectamos grupos los \<día\>" |
| **Feedback transitorio** | `daySetup.changeFeedback !== null` | Banner azul auto-dismissed por timer |

Transiciones (`monitorMode` y `useGroupsAll`):

```
LOW ──(dropdown→por-dia | edit input | toggle día off)──► FAMILY  [dispara dsPromoteToFamily(reason)]
FAMILY ──(click Monitorear grupos)──► HIGH               [dispara dsActivateGroups(), loader 1.4s]
LOW ──(click Monitorear grupos)─────► HIGH               [promueve a Family + activa grupos]
HIGH ──(no hay downgrade en el prototipo)
```

## Flujos de usuario (Experience-Driven User Story)

**Flujo A · Configurar Low desde cero**
- **Como** usuario que entra a configurar una fuente nueva
- **Quiero** aceptar las sugerencias del agente con mínima fricción
- **Para** activar el monitoreo sin pensar demasiado
- **Camino**:
  1. Llego desde el activation loader. El modal abre en `daysetup` edición, `monitorMode === 'igual'`.
  2. Veo el dropdown "Monitorear" en "Igual todos los días", el candado cerrado, badge `.ds-low-chip`, y la ventana de tiempo prellenada con sugerencias (08:00 / 09:00).
  3. Los chips `.ds-ai-chip` muestran "Sugerencia: X" si pisé un valor. Puedo clickearlos para revertir.
  4. Pulso "Guardar". Se persiste el monitoreo con `daySetup.shared` aplicado a todos los días.

**Flujo B · Promoción Low → Family**
- **Como** usuario que ve que un día tiene comportamiento distinto
- **Quiero** ajustar solo ese día
- **Para** que el monitoreo no genere falsos positivos
- **Camino**:
  1. En Low, edito un input del indicador "Volumen de archivos". Se dispara `dsPromoteToFamily('edit')`.
  2. El candado se abre, los dots primary aparecen en los días con monitoreo, y el banner `.ds-feedback` me dice "Cambiaste a configuración por día de la semana".
  3. Cada día queda con una copia del `shared` previo. Sigo editando solo el día que necesito.

**Flujo C · Promoción Family → High (grupos)**
- **Como** usuario con una fuente que tiene varios patrones de archivos
- **Quiero** monitorear por grupos detectados
- **Para** ganar precisión cuando un solo grupo falla
- **Camino**:
  1. Veo el banner `.ds-groups-banner` con la ilustración SVG y el texto "Esta fuente tiene 3 grupos de archivos con comportamientos diferentes".
  2. Pulso "Monitorear grupos". Se dispara `dsActivateGroups()`: spinner pedagógico por 1.4s con copy "Detectando los grupos de archivos".
  3. Tras el loader, cada día activo se siembra con grupos (cards `.ds-group` colapsables).
  4. Cada grupo tiene su propio Volumen y Cantidad de registros. Puedo expandir el ojo (peek) para ver el patrón de agrupación, los archivos del grupo y la fecha de revisión.

**Flujo D · Revisar y editar una fuente ya monitoreada**
- **Como** usuario con una fuente monitoreada
- **Quiero** revisar la configuración actual y editarla si hace falta
- **Para** mantener el monitoreo afinado
- **Camino**:
  1. Entro desde la card. Modal abre en `daysetup` con `daySetupReadonly === true`.
  2. Veo todos los valores actuales sin chips AI (ya no son sugerencias).
  3. Pulso "Editar". `daySetupReadonly = false` y el footer cambia a "Salir / Guardar".
  4. Edito y guardo, o pulso "Eliminar monitoreo" para limpiar la configuración (confirm dialog).

**Flujo E · Consultar Análisis inteligente**
- **Como** usuario que quiere entender por qué Simetrik propone esos valores
- **Quiero** ver el detalle del análisis
- **Para** confiar en la sugerencia
- **Camino**:
  1. Pulso el botón `.ds-ai-btn` "Resultados de análisis" en la topbar.
  2. Se abre `aiAnalysisOpen = true` con un modal independiente que muestra 5 cards colapsables (Resumen, etc.) con el periodo, muestras y métrica seleccionable (Ventana, Volumen, Registros).

## Interacciones

| Trigger | Resultado | Side effects |
|---|---|---|
| Click `.ds-monitor-trigger` | Toggle `daySetup.monitorMenuOpen` | Muestra menú con dos opciones |
| Click opción "Por día" | `daySetup.monitorMode = 'por-dia'`, `dsPromoteToFamily('dropdown')` | Cambio a Family sin banner (acción explícita) |
| Cambiar input numérico en Low | `daySetup.monitorMode = 'por-dia'`, `dsPromoteToFamily('edit')` | Banner `.ds-feedback` por 4s (timer) |
| Toggle día OFF en Low | `dsPromoteToFamily('toggle')` | Banner feedback + día desactivado |
| Click tab de día (`.ds-tabs > .tm-tab`) | `daySetup.activeDay = d.key` | Re-render del contenido del día |
| Click `.ds-groups-cta` "Monitorear grupos" | `dsActivateGroups()` | Loader 1.4s, luego `useGroupsAll = true` y `days[i].groups` poblado |
| Click `.ds-day-toggle .ds-switch` | `dsToggleDayMonitor()` | Si en Low, primero promueve a Family |
| Toggle switch indicador (`.ds-indicator-head .ds-switch`) | Activa/desactiva el indicador | Si en Low y se apaga, no promueve; si se edita un input, sí |
| Click chip `.ds-ai-chip.is-suggestion` | Revierte al valor sugerido (`_sMin`/`_sMax`) | Solo si `!daySetupReadonly` y el valor difiere |
| Click `.ds-notes-add` | Toggle `notes.open` | Si en Low y se abre, promueve a Family |
| Click tag `.ds-notes-tag` | Toggle en `notes.tags[]` | Modifica array reactivo |
| Click `.ds-ai-btn` | `openAiAnalysis()` | Abre modal `aiAnalysisOpen` |
| Click `.ds-group-head` | Toggle `g.expanded` | Expande/colapsa la card de grupo |
| Click `.ds-group-icon-btn` (ojo) | Toggle `peek` (local Alpine) | Muestra `.ds-peek-card` anclado al botón |
| Click outside peek | `peek = false` | Cierra el peek menos cuando se hace click en el trigger |
| Click `.wizard-btn-primary` "Guardar" | `daySetupSave()` | Persiste la config y cierra el modal |
| Click "Eliminar monitoreo" (read-only) | `confirmDeleteMonitoring(selectedConfigSource)` | `window.confirm` y reset a `status === 'empty'` |
| Hover sobre `.ds-help[data-tip]` | Tooltip CSS-only con el texto | Aparece debajo o al lado |

## Data contracts

Modelo `daySetup`:

```
daySetup: {
  monitorMode: 'igual' | 'por-dia',
  activeDay: 'lun' | 'mar' | 'mie' | 'jue' | 'vie' | 'sab' | 'dom',
  window: {
    arrivesAt: 'HH:MM',
    warnIfPast: 'HH:MM',
    _sArrivesAt: 'HH:MM',   // sugerencia AI
    _sWarnIfPast: 'HH:MM'
  },
  shared: SimpleConfig,      // usado cuando Low
  useGroupsAll: boolean,
  days: DayConfig[],         // 7 entries
  loading: boolean,
  loadStep: 0 | 1,
  changeFeedback: { reason, text } | null,
  monitorMenuOpen: boolean
}

SimpleConfig {
  fileCount: { active, min, max, _sMin, _sMax },
  rowCount:  { active, min, max, _sMin, _sMax },
  notes:     { open, tags: string[], detail: string (<=250) }
}

DayConfig {
  key: 'lun' | ...,
  label: 'Lunes' | ...,
  monitorEnabled: boolean,
  simple: SimpleConfig,
  groups: Group[]
}

Group {
  id, name, filesFound, samples: string[], expanded: boolean,
  fileCount, rowCount, notes (igual que SimpleConfig)
}
```

Persistencia en la fuente:

- `r.dayConfig`, `r.dayConfigShared`, `r.dayConfigWindow`, `r.dayConfigMonitorMode`, `r.dayConfigUseGroupsAll`.

Endpoints sugeridos:

- `GET /sources/{id}/monitoring` para precargar.
- `POST /sources/{id}/monitoring` para guardar.
- `DELETE /sources/{id}/monitoring` para eliminar.
- `GET /sources/{id}/analysis` para datos del modal Análisis inteligente.

## Edge cases

- **Fuente sin historia**: chips AI no se muestran (`daySetupHasConfig` true tras guardar) y los rangos pueden estar en 0.
- **Día sin archivos**: en High, se muestra el bloque `.ds-day-off` con copy "No detectamos grupos los \<día\>".
- **Notas en config existente**: solo aparece el bloque `.ds-notes` si `dsSimpleHasNotes()` o `dsGroupHasNotes(g)` es true.
- **Detalle de notas vacío con tags marcados**: el textarea es requerido (asterisco `req`) y debe validarse antes de guardar.
- **Loader con timers pendientes**: si el usuario cierra el modal durante el loader, los `setTimeout` se cancelan (`_daySetupTimers.forEach(clearTimeout)`).
- **`daySetupReadonly` con peek abierto**: el peek se permite igual (es solo inspección).
- **Cambio rápido de día activo durante carga**: no debe perder los valores; cada día tiene su propio sub-objeto.
- **Promoción Low→Family con shared en 0**: las copias quedan en 0; el usuario debe poder editar sin reset.

## Empty states (importante)

| Escenario | Condición | Copy propuesto | CTA | Implementado en HTML? |
|---|---|---|---|---|
| Modal cerrado | `selectedConfigSource === null` | Modal no renderiza | (ninguno) | ✅ implementado |
| Loader pedagógico (Family → High) | `daySetup.loading === true` | "Detectando los grupos de archivos. Simetrik está identificando..." con spinner | (ninguno) | ✅ implementado (`calc-loader`) |
| Día sin grupos detectados (High) | `useGroupsAll && dsActiveDay().groups.length === 0` | "No detectamos grupos los [día]. Esta fuente no recibe archivos este día, o todavía no hay histórico." | (ninguno) | ✅ implementado (`ds-day-off`) |
| Día apagado | `dsActiveDay().monitorEnabled === false` | Solo se muestra el toggle OFF con hint "Activa el monitoreo cuando quieras recibir alertas." | Switch toggle ON | ✅ implementado |
| Fuente sin historia BADS | API devuelve `analysis: null` para la fuente | Modal sigue funcionando pero chips AI ocultos. Rangos en 0. Banner info "Sin historial suficiente todavía." | (ninguno) | ❌ pendiente |
| Loading inicial del modal | Fetch `GET /sources/{id}/monitoring` en curso | Skeleton de los 3 cards principales con shimmer | (ninguno) | ❌ pendiente |
| Error al cargar configuración existente | Fetch falló | "No pudimos cargar la configuración." card destructive | Botón "Reintentar" | ❌ pendiente |
| Error al guardar | `daySetupSave()` falló | Toast destructive "No pudimos guardar la configuración." | Botón "Reintentar" + mantener modal abierto | ❌ pendiente |
| Sin sugerencias AI disponibles | `_sArrivesAt === null && _sMin === null` (etc.) | Chips muestran "Sin sugerencia disponible" en gris muted | (ninguno) | ❌ pendiente |
| Eliminación con confirm | `confirmDeleteMonitoring(r)` invocado | Confirm nativo "¿Estás seguro?" | "Cancelar" / "Eliminar" | ✅ implementado (window.confirm) |
| Todos los días apagados (Family/High) | `daySetup.days.every(d => !d.monitorEnabled)` | Banner warning "La fuente quedará sin monitoreo. Activa al menos un día." | (ninguno, bloquea Guardar) | ❌ pendiente |
| Feedback transitorio activo | `daySetup.changeFeedback !== null` | Banner azul `.ds-feedback` auto-dismissed por timer | (ninguno) | ✅ implementado |
| Notas obligatorias sin detalle | `notes.tags.length > 0 && notes.detail === ''` al guardar | Helper destructive bajo textarea "Cuéntanos en qué consiste el comportamiento marcado." | (ninguno, bloquea Guardar) | ❌ pendiente |

## Edge cases (validación)

- Cambio rápido de día durante carga: cada día tiene su propio sub-objeto, no debe perder valores.
- Promoción Low→Family con shared en 0: las copias quedan en 0; usuario debe poder editar sin reset.
- Cierre del modal durante loader pedagógico: timers se cancelan (`_daySetupTimers.forEach(clearTimeout)`).
- `daySetupReadonly` con peek abierto: peek se permite (es solo inspección).
- Click outside peek dentro del modal: cierra peek pero no el modal.
- Tooltip en `.ds-help[data-tip]` accesible por teclado (`tabindex="0"`).
- maxlength 250 en textarea de notas: browser corta input automáticamente.

## Componentes desyk a usar

> Mapeo del prototipo HTML a los componentes oficiales del design system desyk
> (basado en shadcn/ui). El implementador debe reusar estos componentes en lugar
> de replicar las clases CSS custom del prototipo. Este doc cubre el chasis del
> modal; el detalle por contenedor vive en los docs 07-12.

| Elemento del prototipo | Componente desyk | Variants / props | Notas de uso |
|---|---|---|---|
| `.dialog-backdrop` + `.resource-config-panel` (modal contenedor) | `Dialog` + `DialogContent` + `DialogHeader` + `DialogTitle` | Modal centrado, ancho 768px alto 740px | Contenedor principal del daysetup |
| `.resource-config-close` (X del header) | `Button` | `variant="ghost" size="icon"` con ícono `X` de Lucide | Cierra el modal |
| `.src-header` (header con thumb + nombre + meta) | Layout custom con `Avatar` + tipografía | `Avatar` con ícono o imagen del tipo de fuente | Identificación de la fuente en el header |
| `.src-thumb` (avatar de la fuente) | `Avatar` + `AvatarFallback` | — | Ícono según tipo de ingesta |
| `.ds-feedback` (banner azul transitorio Low→Family) | `Alert` | `variant="default"` con override azul info | Auto-dismissed por timer de 6s |
| `.ds-topbar` (topbar con dropdown + botón AI) | Layout custom (`flex`) | — | Contenedor del dropdown Monitorear + botón Análisis |
| `.ds-monitor` (dropdown "Monitorear" con label + sub por opción) | `DropdownMenu` + `DropdownMenuTrigger` + `DropdownMenuContent` + `DropdownMenuItem` | — | Cambia entre "Igual todos los días" y "Por día de la semana" |
| `.ds-ai-btn` (botón "Resultados de análisis") | `Button` | `variant="outline"` con ícono leading violeta | Abre el modal de análisis (`aiAnalysisOpen`) |
| `.ds-card` (cards de ventana, comportamiento, indicadores) | `Card` + `CardHeader` + `CardContent` + `CardFooter` | `CardFooter` con className para footer colgante | Cards internas del modal |
| `.ds-help[data-tip]` (íconos ? con tooltip) | `Tooltip` + `TooltipTrigger` + `TooltipContent` | con ícono `HelpCircle` de Lucide | Accesible por teclado (`tabindex="0"`) |
| `.wizard-actions` (footer del modal) | `DialogFooter` | — | Contenedor de las acciones del footer |
| `.wizard-btn-primary` (Guardar / Editar) | `Button` | `variant="default"` | Acción primaria del footer |
| `.wizard-btn-secondary` (Salir) | `Button` | `variant="outline"` | Acción secundaria |
| "Eliminar monitoreo" (en readonly) | `Button` | `variant="outline"` con className destructive | Botón destructivo de eliminación |
| `.calc-loader` (loader pedagógico 1.4s al activar grupos) | Componente custom (compuesto) | — | Spinner + copy "Detectando los grupos de archivos" |
| Confirm dialog ("¿Estás seguro de eliminar?") | `AlertDialog` + `AlertDialogContent` + `AlertDialogAction` + `AlertDialogCancel` | — | Reemplaza el `window.confirm` nativo del prototipo |
| Modal "Resultados de análisis" (`aiAnalysisOpen`) | `Dialog` + `DialogContent` + `Accordion` para las 5 cards colapsables | `Accordion` con `type="multiple"` | Modal independiente del daysetup |
| `.ai-analysis-panel` (selector de métrica Ventana/Volumen/Registros) | `ToggleGroup` + `ToggleGroupItem` | `type="single"` | Segmented control para elegir métrica |

**Componentes compuestos (no existen en desyk, hay que componerlos):**
- `DaysetupModal` — chasis completo del modal de configuración. Wrapper sobre `Dialog` que orquesta los cards internos según `monitorMode` y `useGroupsAll`. Maneja `ds-mode`, `ds-shell`, `ds-scroll`.
- `MonitorModeDropdown` — dropdown con dos opciones (label + subtítulo por opción). Compuesto sobre `DropdownMenu` con `DropdownMenuItem` enriquecido.
- `PedagogicalLoader` — loader visual de 1.4s con spinner + copy explicativo. Compuesto sobre `Loader2` de Lucide + tipografía.
- `AiAnalysisModal` — modal "Resultados de análisis" con 5 cards colapsables (Resumen, periodo, muestras, métricas). Compuesto sobre `Dialog` + `Accordion` + `ToggleGroup`.
- `SourceHeader` — header del modal con thumb + nombre + meta. Compuesto sobre `Avatar` + tipografía.

**Componentes referenciados de docs hermanos (ver docs 07-12 para detalle):**
- Card Ventana de tiempo (doc 07).
- Card Comportamiento + tabs Lu-Do + toggle día (doc 08).
- Indicadores Volumen / Cantidad (docs 09 y 10).
- Card Notas (doc 11).
- Cards de grupo High + peek (doc 12).

**Referencias:**
- Repo desyk: `~/Simetrik/desyk-components` (read-only).
- Lista oficial de componentes shadcn/ui que desyk extiende.

## Implementation notes

- **Helpers Alpine ya existentes** a reusar: `dsActiveSimple()`, `dsActiveDay()`, `dsPromoteToFamily(reason)`, `dsActivateGroups()`, `dsToggleDayMonitor()`, `dsSeedGroupsFor()`, `dsPatternTokens()`, `dsChipText()`, `dsSimpleHasNotes()`, `dsGroupHasNotes()`, `enterDaySetup()`, `enterDayView()`, `daySetupSave()`, `confirmDeleteMonitoring()`, `openAiAnalysis()`, `daySetupHasConfig` (getter).
- **CSS/clases** ya existentes: `.ds-mode`, `.ds-shell`, `.ds-scroll`, `.ds-feedback`, `.ds-topbar`, `.ds-monitor`, `.ds-ai-btn`, `.ds-card`, `.ds-card-head`, `.ds-tabs-row`, `.ds-lock`, `.ds-low-chip`, `.ds-day-head`, `.ds-day-toggle`, `.ds-switch`, `.ds-groups-banner`, `.ds-groups-cta`, `.ds-indicator`, `.ds-input-with-suffix`, `.ds-ai-chip`, `.ds-notes`, `.ds-group`, `.ds-peek-card`, `.calc-loader`, `.wizard-actions`, `.wizard-btn-primary`, `.wizard-btn-secondary`.
- **Endpoints BE**:
  - `GET /sources/{id}/monitoring` (precarga).
  - `POST /sources/{id}/monitoring` (guardar).
  - `DELETE /sources/{id}/monitoring` (eliminar).
  - `GET /sources/{id}/analysis` (modal "Resultados de análisis").
- **Tokens desyk**: `hsl(var(--primary))` para CTAs activos, `hsl(var(--ai-purple))` para chips de agente y banner grupos, `hsl(var(--info))` para banner feedback, `hsl(var(--warning))` para badge Low chip.
- **Animation / motion**: 200ms ease-out al expandir grupos, 1.4s loader pedagógico, 6s timer del banner `changeFeedback`, 2.9s activation loader, 320ms ease-out al abrir/cerrar modal.

## Out of scope

- Edición masiva (bulk edit) de configuraciones existentes — explícitamente NO se cubre; la edición es uno-a-uno desde la lista.
- Historial de versiones del monitor.
- Compartir configuración entre fuentes (template).
- Configuración de ventana de tiempo por día (`Configurar ventana por día · Próx.` es placeholder).
- Modo "downgrade" High → Family (no soportado en el modelo actual).
- Bulk delete de monitores configurados.

## Criterios de aceptación

1. **Given** una fuente nueva, **When** se abre el modal, **Then** parte en Low (`monitorMode === 'igual'`), candado cerrado, badge `.ds-low-chip` visible.
2. **When** el usuario cambia el dropdown a "Por día", **Then** `monitorMode` pasa a `'por-dia'` y el candado se abre, sin banner feedback (acción explícita).
3. **When** el usuario edita un input en Low, **Then** se dispara `dsPromoteToFamily('edit')` y aparece el banner `.ds-feedback` durante 4s.
4. **When** el usuario apaga el toggle del día en Low, **Then** se promueve a Family con feedback.
5. **Given** el banner `.ds-groups-banner` visible, **When** se pulsa "Monitorear grupos", **Then** se muestra el loader pedagógico por 1.4s y luego `useGroupsAll = true` con grupos sembrados por día.
6. En High, cada grupo es una card colapsable con su propio Volumen, Cantidad de registros y Notas.
7. El botón ojo del grupo abre el peek anclado al botón y se cierra al click fuera (excepto sobre el trigger).
8. **Given** `daySetupReadonly === true`, **Then** todos los inputs están disabled, los switches con opacity 0.6 y el footer muestra "Eliminar monitoreo / Editar".
9. El chip `.ds-ai-chip.is-suggestion` aparece solo cuando el valor actual difiere del `_sValue` y la fuente no tiene config previa (`!daySetupHasConfig`).
10. Hover en `.ds-help[data-tip]` muestra el tooltip con el copy exacto del atributo.
11. **When** se pulsa "Eliminar monitoreo", **Then** aparece confirm nativo y al confirmar se resetea `r.status = 'empty'` y se cierra el modal.
12. Los textos del modal no usan em-dashes ni slang regional (verificar contra `00-CONTEXT.md`).

## Dependencies

- **Depende de**: `04-cards-monitores-ingesta` (entrada al modal).
- **Bloquea a**: `07` a `12` (contenedores internos del modal), parcialmente `13-journey-low-family-high` (síntesis).
- **Relacionado con**: `06-activacion-masiva` (activation loader precede al modal en flujos individuales).

## Verification (cómo probarlo)

1. Abrir `index.html`. Click en una card `status === 'empty'`. Validar activation loader 2.9s → daysetup edición.
2. Validar default Low: candado cerrado, badge `.ds-low-chip`, dropdown "Igual todos los días".
3. Editar input de Volumen: validar promoción a Family y banner `.ds-feedback`.
4. Cambiar dropdown a "Por día": validar promoción sin banner.
5. Click "Monitorear grupos": validar loader 1.4s y cards `.ds-group` sembradas.
6. Click ojo en grupo: validar peek con patrón, archivos y footer.
7. Click outside del peek: validar cierre.
8. Click "Guardar": validar persistencia y cierre del modal.
9. Click en una card monitoreada: validar daysetup en solo-lectura (sin chips AI, footer "Eliminar / Editar").
10. Click "Eliminar monitoreo": validar confirm y reset a `status === 'empty'`.
11. Click "Resultados de análisis": validar apertura de `aiAnalysisOpen`.

## References

> ⚠️ Las referencias por número de línea no son confiables: el archivo se reordenó (el modal de configuración hoy vive **después** del bulk modal / activation loader, no antes). Ubicar por selector.
- **HTML** (por selector): modal `<div class="resource-config-panel" ...>` (buscar `selectedConfigSource`). Dentro: topbar del modal, `<section class="ds-card has-hanging-footer">` "Ventana de tiempo", tab switcher Lu-Do (`.ds-day-tabs`), toggle día (`.ds-day-toggle`), banner grupos (`.ds-groups-banner`), indicadores Low/Family (`.ds-indicator`), notas (`.ds-notes`), grupos High (`.ds-group`), footer del modal. Modal de análisis: `<div class="ai-analysis-panel" ...>` (buscar `aiAnalysisOpen`).
- **CSS** (por selector): `.ds-mode`, `.ds-card`, `.ds-indicator`, `.ds-notes`, `.ds-group`, `.ds-peek-card`, `.ds-ai-chip`, `.ds-feedback`, `.ds-low-chip`.
- **JS** (helpers en `appData()`): `dsPromoteToFamily`, `dsActivateGroups`, `daySetupSave`, `daySetupMakeSimple`, `daySetupMakeWindow`, `selectConfigSource`, `enterDaySetup`, `enterDayView`.
- **Figma**: (pendiente de link)
- **Docs hermanos**: `[06-activacion-masiva.md](./06-activacion-masiva.md)`, `[07-contenedor-ventana-de-tiempo.md](./07-contenedor-ventana-de-tiempo.md)`, `[08-contenedor-comportamiento-dia.md](./08-contenedor-comportamiento-dia.md)`, `[13-journey-low-family-high.md](./13-journey-low-family-high.md)`.
- **Backend**:
  - BADS: `~/Simetrik/bads/src/bads/models/kpi.py` (lifecycle).
  - Op-center: `~/Simetrik/op-center-backend/apps/anomaly_configs/` (config wrapper).

---

## Flujos específicos

### Creación de un monitor (uno-a-uno)

- **Como** usuario que entra a configurar una fuente nueva (`status === 'empty'`)
- **Quiero** ir desde la card hasta una configuración guardada con mínima fricción
- **Para** activar el monitoreo confiando en las sugerencias del agente

**Camino**:

1. **Estado inicial**: estoy en `tablero-monitoreo` / tab Ingesta. La card de la fuente está en el grid de fuentes con badge gris "Sin configurar".
   - *Visual*: `.tm-chart-card` sin clases `is-active` ni `is-monitored`.

2. **Click en la card**: se ejecuta `selectConfigSource(r)`.
   - *Side effect*: como `r.status === 'empty'`, dispara `openActivationLoader(r)` antes del modal.
   - *Visual*: el activation loader abre (`activationLoaderOpen = true`).

3. **Activation loader (2.9s)**: panel modal con database glyph, pulse rings, mini-archivos flotantes y 3 steps progresando (Detectando archivos · Identificando patrones · Calculando monitoreo inicial).
   - *Copy*: "Simetrik está analizando tu fuente..."
   - *Timing*: 0ms abre, 800ms step 1, 1600ms step 2, 2400ms step 3, 2900ms cierra.

4. **Apertura del daysetup en edición**: `_enterConfigSource(r)` → `enterDaySetup()`.
   - *Estado*: `inlineActiveMode === 'daysetup'`, `daySetupReadonly === false`, `daySetupHasConfig === false`.
   - *Defaults*: `monitorMode: 'igual'`, `useGroupsAll: false`, `activeDay: 'lun'`, `window` precargada con sugerencia del agente, `shared` con valores `_sMin/_sMax` aplicados.
   - *Visual*: candado cerrado, badge `.ds-low-chip` "Igual todos los días", chips violetas `.ds-ai-chip` en cada input ("Autocompletado por el agente"), banner `.ds-groups-banner` si la fuente tiene grupos detectables.

5. **Usuario configura**: tres caminos posibles según complejidad.
   - **5a. Acepta sugerencias Low**: ajusta uno o ningún input. Los chips siguen diciendo "Autocompletado por el agente" o cambian a "Sugerencia: N" cuando se aparta. Va al paso 7.
   - **5b. Promueve a Family**: edita un input (`dsPromoteToFamily('edit')`), o cambia dropdown a "Por día" (`dsPromoteToFamily('dropdown')`), o apaga toggle del día (`dsPromoteToFamily('toggle')`). Aparece banner `.ds-feedback` por 6s "Cambiaste a configuración por día de la semana".
     - *Side effect*: candado se abre, `shared` se clona a `days[i].simple`, dots primary aparecen en tabs.
   - **5c. Activa grupos (High)**: click "Monitorear grupos" en el banner → `dsActivateGroups()` → loader pedagógico 1.4s "Detectando los grupos de archivos" → grupos sembrados en los 7 días.
     - *Visual*: slot Low/Family se reemplaza por cards `.ds-group` (primer grupo expandido).

6. **Usuario revisa Análisis (opcional)**: click `.ds-ai-btn` "Resultados de análisis" → abre `aiAnalysisOpen = true` (modal independiente con 5 cards colapsables: Resumen, periodo, muestras, métricas).

7. **Click "Guardar"**: `daySetupSave()` persiste `r.dayConfig`, `r.dayConfigShared`, `r.dayConfigWindow`, `r.dayConfigMonitorMode`, `r.dayConfigUseGroupsAll`.
   - *Side effect*: cierra modal (`selectedConfigSource = null`), `r.status` pasa a `'monitored'` (o `'learning'` si BADS está en `COLLECTING`).
   - *Visual*: la card vuelve al grid de fuentes con su badge actualizado a verde ("Monitoreado") o azul ("Aprendiendo"). No hay secciones: es un grid único.

**Copy esperado clave**:
- Activation loader subtitle: "Simetrik está analizando tu fuente..."
- Banner feedback: "Cambiaste a configuración por día de la semana."
- Loader grupos: "Detectando los grupos de archivos."
- Chip AI default: "Autocompletado por el agente"
- Chip AI editado: "Sugerencia: HH:MM" o "Sugerencia: N"

---

### Edición de un monitor existente (uno-a-uno)

- **Como** usuario con una fuente monitoreada
- **Quiero** revisar la configuración actual y editarla
- **Para** mantener el monitoreo afinado cuando el comportamiento de la fuente cambia

**Camino**:

1. **Estado inicial**: la card está en el grid de fuentes con badge verde (o azul si aprendiendo). El footer muestra grupos detectados si aplica.

2. **Click en la card**: `selectConfigSource(r)` detecta `r.dayConfig` existente → NO dispara activation loader → llama directo `_enterConfigSource(r)` → `enterDayView()`.
   - *Estado*: `inlineActiveMode === 'daysetup'`, `daySetupReadonly === true`, `daySetupHasConfig === true`.

3. **Daysetup en solo-lectura**: el usuario ve la configuración actual.
   - *Visual*:
     - Inputs `:disabled` con `opacity` reducido y cursor `not-allowed`.
     - Switches con `opacity: 0.6` (no clickeables).
     - Chips `.ds-ai-chip` ocultos (ya no son sugerencias, son valores oficiales).
     - Banner `.ds-groups-banner` oculto (no aplica reactivación).
     - Toggle del día oculto (`x-show="!daySetupReadonly"`).
     - Notas: card visible solo si `dsSimpleHasNotes()` o `dsGroupHasNotes(g)` devuelve true.
   - *Footer*: muestra "Eliminar monitoreo" (secondary destructive) y "Editar" (primary).

4. **Click "Editar"**: `daySetupReadonly = false`. El footer cambia a "Salir / Guardar".
   - *Visual*: inputs se vuelven editables, switches activos, chips AI siguen ocultos (ya hay config), toggle del día vuelve a aparecer.

5. **Usuario edita**: cualquier cambio es igual al flujo de creación, excepto que las promociones Low→Family pueden no aplicar si la fuente ya estaba en Family/High.

6. **Click "Guardar"**: `daySetupSave()` persiste cambios.
   - *Side effect*: cierra modal y refresca la card en la lista.

7. **Camino alternativo · Eliminar**: click "Eliminar monitoreo" → `confirmDeleteMonitoring(selectedConfigSource)`.
   - *Visual*: confirm nativo del browser "¿Estás seguro de eliminar el monitoreo?"
   - *Si confirma*: `r.status = 'empty'`, limpia `dayConfig*`, cierra modal. La card vuelve a "Sin monitoreo".
   - *Si cancela*: nada cambia.

**Copy esperado clave**:
- Footer readonly secundario: "Eliminar monitoreo"
- Footer readonly primario: "Editar"
- Footer edit secundario: "Salir"
- Footer edit primario: "Guardar"
- Confirm: "¿Estás seguro de eliminar el monitoreo de esta fuente?"

---

### Vista de detalle (readonly) — qué se oculta vs setup nuevo

Diferencias visibles vs el flujo de creación:

| Elemento | Setup nuevo (`!daySetupHasConfig`) | Detalle (`daySetupReadonly && daySetupHasConfig`) |
|---|---|---|
| Chips AI `.ds-ai-chip` | Visibles (violetas, "Autocompletado por el agente" o "Sugerencia: N") | Ocultos |
| Banner `.ds-groups-banner` | Visible si hay grupos detectables (Family/Low sin grupos activos) | Oculto siempre |
| Toggle día `.ds-day-toggle` | Visible y clickable | Oculto (`x-show="!daySetupReadonly"`) |
| Switches indicador `.ds-indicator-head .ds-switch` | Activos | `opacity: 0.6`, no clickeables |
| Inputs `config-input` | Editables | `:disabled` con cursor `not-allowed` |
| Notas `.ds-notes` | Visible siempre (card colapsado por default) | Visible solo si tiene contenido (`dsSimpleHasNotes()` o `dsGroupHasNotes(g)`) |
| Badge `.ds-low-chip` | Visible en Low | Visible en Low (sigue siendo señal del modo) |
| Footer | "Salir / Guardar" | "Eliminar monitoreo / Editar" |
| Peek `.ds-peek-card` (High) | Funcional | Funcional (es solo inspección, no edición) |
| Banner `.ds-feedback` | Aparece tras promoción Low→Family | No aplica (no hay promociones en readonly) |
| Botón `.ds-ai-btn` "Resultados de análisis" | Visible y funcional | Visible y funcional (consulta histórica) |
