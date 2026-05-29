---
epic: MONITOR_INGESTA
issue_type: Feature
priority: P0
estimate: XL
labels: [ux, frontend, monitoring, modal, bulk, ai, activation]
depends_on: [03-banner-monitorear-tablero, 04-cards-monitores-ingesta]
blocks: [05-modal-configuracion]
component_areas: [bulk-modal, activation-loader, ai-analysis]
---

# 06 · Activación masiva (bulk + activation loader)

> Flujo para activar el monitoreo de varias fuentes en un solo paso. Combina dos modales: el **bulk modal** de 3 stages (Selecciona · Revisa · Activa) y el **activation loader** que precede al daysetup cuando se entra a configurar una fuente individual sin configurar.

## Resumen

- **Quién lo ve**: usuario que pulsa el botón "Activar las N a la vez" en el header del tab Ingesta (ver doc 03), o usuario que entra a una card sin configurar (ver doc 04).
- **Cuándo**: durante la configuración del monitoreo del tablero, antes de que todas las fuentes estén cubiertas.
- **Qué decisión habilita**: confirmar el conjunto de fuentes a activar, revisar la línea base propuesta por el análisis inteligente y disparar la activación en lote.
- **Por qué existe**: configurar fuentes una por una es costoso. La promesa es: el agente analiza cada fuente, propone una baseline plausible y el usuario solo confirma. El activation loader cumple la misma promesa para flujos individuales.

## Anatomía

### Bulk modal

| Componente | Clase / selector | Función |
|---|---|---|
| Backdrop | `.dialog-backdrop.bulk-modal-backdrop` con `x-show="bulkActivateOpen"` | Cierra al click fuera |
| Panel | `.bulk-modal-panel` | Contenedor 768 x 740 |
| Header | `.bulk-modal-header` con `.bulk-modal-title`, `.bulk-modal-sub`, `.bulk-modal-title-help`, `.bulk-modal-close` | Título y subtitle pedagógico |
| Stepper | `.bulk-modal-stepper` con 3 `.bulk-modal-step` | Indicador visual de la etapa actual |
| Body | `.bulk-modal-body` | Scrolleable, contenido stage-aware |
| Footer | `.bulk-modal-footer` con `.secondary-btn` + `.primary-btn` | Acciones stage-aware |

**Stage 1 · Selecciona**:

- `.bulk-modal-list-wrap`
- `.bulk-modal-toolbar` con `.bulk-modal-selectall` (checkbox + label) y `.bulk-modal-counter` ("X de Y seleccionados")
- `.bulk-modal-row` por fuente: checkbox + nombre + badges (tipo de ingesta + workspace)

**Stage 2 · Revisa**:

- `.bulk-ai-banner` con icono violeta, "Análisis inteligente" y disclaimer sobre edición posterior
- `.bulk-preview-card` por fuente, con `.bulk-preview-header` colapsable
- Body expandida: `.bulk-preview-window-row` (ventana de tiempo con `bulk-preview-time-pill`)
- Modo grupos: `.bulk-preview-subgroup` con `.bulk-preview-indicator` (Volumen y Cantidad de registros) y `.bulk-preview-num-pill`
- Modo single: indicador unico de "Cantidad de registros"

**Stage 3 · Activa**:

- `.bulk-activation-list` con `.bulk-activation-row` por fuente
- Estados visuales: `.bulk-activation-status.is-pending` (spinner), `.is-calculating` (spinner), `.is-success` (check), `.is-partial` (warning ámbar)

### Activation loader

| Componente | Clase / selector | Función |
|---|---|---|
| Backdrop | `.dialog-backdrop.activation-loader-backdrop` con `x-show="activationLoaderOpen"` | Bloquea interacción |
| Panel | `.activation-loader-panel` | Contenedor 768 x 740 |
| Ilustración | `.activation-loader-illu` con `.activation-loader-glyph` (database), 3 `.activation-loader-ring` (pulse rings) y 3 `.activation-loader-float` (mini-archivos) | Visual decorativo pedagógico |
| Contenido | `.activation-loader-content` con `.activation-loader-eyebrow`, `.activation-loader-title` (nombre fuente) y `.activation-loader-sub` | Texto principal |
| Steps | `.activation-loader-steps` con 3 `.activation-loader-step` (Detectando archivos · Identificando patrones · Calculando monitoreo inicial) | Progreso visual |

## Estados

**Bulk modal**:

| Estado | Condición | Footer |
|---|---|---|
| Cerrado | `!bulkActivateOpen` | n/a |
| Stage 1 | `bulkActivateStage === 1` | "Salir" + "Revisar análisis" (deshabilitado si `bulkActivateSelected.length === 0`) |
| Stage 2 | `bulkActivateStage === 2` | "Salir" + "Activar monitores" |
| Stage 3 procesando | `bulkActivateStage === 3 && !bulkActivationComplete` | "Salir" + "Activando" con spinner |
| Stage 3 completo | `bulkActivateStage === 3 && bulkActivationComplete` | "Salir" + "Cerrar" |

Por fuente en stage 3: `status: 'pending' \| 'calculating' \| 'success' \| 'partial'`.

Stepper visual: cada step muestra el número, o un check cuando `bulkActivateStage > N` (o `bulkActivationComplete` para el step 3).

**Activation loader**:

| Estado | `activationLoaderStep` | Visual |
|---|---|---|
| Detectando | 0 | Step 0 con spinner |
| Identificando | 1 | Step 0 done, step 1 con spinner |
| Calculando | 2 | Steps 0 y 1 done, step 2 con spinner |
| Listo | 3 | Los 3 done. Cierra y abre `_enterConfigSource(r)` |

Timing canónico (líneas 15161-15171):

```
0ms     openActivationLoader(r)
800ms   step = 1
1600ms  step = 2
2400ms  step = 3
2900ms  loader cierra, abre daysetup
```

Máquina de estados completa:

```
INGESTA TAB
    │
    │ (click "Activar las N a la vez")
    ▼
BULK STAGE 1 (selecciona) ──► STAGE 2 (revisa) ──► STAGE 3 (activa) ──► (cierre)
    │ (click Salir o X)
    ▼
INGESTA TAB

INGESTA TAB
    │ (click card status === 'empty')
    ▼
ACTIVATION LOADER (2.9s) ──► DAYSETUP MODAL (edit)
```

## Flujos de usuario (Experience-Driven User Story)

**Flujo A · Activar en bloque todas las fuentes pendientes**
- **Como** usuario con varias fuentes sin configurar
- **Quiero** activar todo en una sola pasada
- **Para** salir de la pantalla con el tablero completamente cubierto
- **Camino**:
  1. Pulso "Activar las N a la vez". Se abre el bulk modal stage 1 con todas las fuentes preseleccionadas (`bulkActivateSelected = empty.map(r => r.id)`).
  2. Deselecciono las que no quiero o uso "Seleccionar todos".
  3. Pulso "Revisar análisis". Se construye `bulkPreview[]` y se va a stage 2.
  4. Expando una o varias cards para ver la baseline: ventana de tiempo, grupos detectados (o modo single) y los indicadores con sus rangos.
  5. Leo el banner "Análisis inteligente" que me confirma que puedo editar después.
  6. Pulso "Activar monitores". Se va a stage 3.
  7. Veo cada fuente con spinner, luego check verde (success) o warning ámbar (partial).
  8. Cuando todas terminan, el botón "Activando" cambia a "Cerrar". Cierro y veo las cards moverse a la sección "Monitoreado".

**Flujo B · Activar una sola fuente (con activation loader)**
- **Como** usuario que quiere configurar una fuente puntual
- **Quiero** ver que Simetrik está analizando antes de pedirme decisiones
- **Para** confiar en que la sugerencia viene de un análisis real
- **Camino**:
  1. Hago click en una card `status === 'empty'`. Se ejecuta `selectConfigSource(r)` que primero llama `openActivationLoader(r)`.
  2. Veo el panel con el nombre de la fuente, el subtitle "Simetrik está analizando tu fuente...", la ilustración con database + pulse rings + mini-archivos, y los 3 steps progresando.
  3. Tras 2.9s, el loader cierra y se abre el daysetup en edición (`_enterConfigSource(r) → enterDaySetup()`).

**Flujo C · Salir del bulk a mitad de camino**
- **Como** usuario que cambia de opinión
- **Quiero** abandonar el flujo bulk
- **Para** volver al tab Ingesta sin afectar nada
- **Camino**:
  1. En cualquier stage pulso "Salir" o la X. Se llama `closeBulkActivate()`.
  2. Tras 200ms el estado interno se resetea (`bulkActivateStage = 1`, listas vacías).

## Interacciones

| Trigger | Resultado | Side effects |
|---|---|---|
| Click "Activar las N a la vez" | `openBulkActivate()` | Si hay 0 pendientes, toast info; si hay, abre stage 1 con todo preseleccionado |
| Toggle `.bulk-modal-selectall` | `toggleBulkSelectAll()` | Marca o desmarca todos los IDs |
| Toggle `.bulk-modal-checkbox` por fila | `toggleBulkSelect(r.id)` | Agrega/quita el ID del array |
| Click "Revisar análisis" | `bulkProceedToReview()` | Llama `bulkBuildPreview()` y avanza a stage 2 |
| Click header de `.bulk-preview-card` | `bulkTogglePreviewExpand(pi)` | Toggle `preview.expanded` |
| Click "Activar monitores" | `bulkRunActivation()` | Avanza a stage 3 y simula activación con 700ms por fuente |
| Click "Cerrar" en stage 3 | `closeBulkActivate()` | Cierra el modal, fuentes con status actualizado |
| Click card empty fuera del bulk | `selectConfigSource(r)` → `openActivationLoader(r)` | Loader 2.9s + 3 timers + apertura daysetup |
| Cierre del loader (no expuesto) | n/a | Solo se cierra al completar los 2.9s |

## Data contracts

`bulkPreview` por fuente:

```
{
  id, name, workspace,
  expanded: boolean,
  mode: 'groups' | 'single',
  hasHistory: boolean,
  groups: Group[],          // si mode === 'groups'
  singleBaseline: object,   // si mode === 'single'
  indicators: { upload, fileCount, rowCount },
  status: 'pending' | 'calculating' | 'success' | 'partial'
}

Group {
  name, count, cadence, window,
  baseRowsMin, baseRowsMax,
  expRowsMin, expRowsMax
}
```

`bulkProgress: { current, total }` y getter `bulkActivationComplete` (`current >= total`).

`activationLoaderResource: Resource | null` y `activationLoaderStep: 0|1|2|3`.

Endpoints sugeridos:

- `POST /dashboards/{id}/monitoring/bulk-preview` con `source_ids[]` devuelve previews con baselines del análisis.
- `POST /dashboards/{id}/monitoring/bulk-activate` con `source_ids[]` devuelve stream de progreso o array de resultados.
- `GET /sources/{id}/analysis-preview` para el activation loader individual.

## Edge cases

- **Cero pendientes al abrir bulk**: `openBulkActivate()` muestra toast "No hay fuentes sin monitoreo en este tablero" y no abre el modal.
- **Sin selección en stage 1**: el botón "Revisar análisis" queda `:disabled` con `.is-disabled` (CSS dim).
- **Fuente sin historia en preview (último elemento)**: en la simulación queda con `status === 'partial'` (warning ámbar) tras la activación.
- **Click fuera del modal durante stage 3**: cerrar resetea timers pero no detiene activaciones ya disparadas (`setTimeout` programados antes del cierre seguirán mutando los items que ya no se muestran). En producción debería cancelarse.
- **Activation loader interrumpido**: si el usuario cierra el navegador, los timers se pierden y la fuente queda en `status === 'empty'`.
- **Stream de progreso interrumpido (real)**: definir retry/fallback en BE.
- **Workspace vacío**: la badge muestra placeholder `{workspace}` (verificar copy).

## Empty states (importante)

| Escenario | Condición | Copy propuesto | CTA | Implementado en HTML? |
|---|---|---|---|---|
| Bulk sin fuentes pendientes | `resources.filter(r => r.status === 'empty').length === 0` al abrir | Toast info "No hay fuentes sin monitoreo en este tablero." y modal NO abre | (ninguno) | ✅ implementado (toast) |
| Stage 1 sin selección | `bulkActivateSelected.length === 0` | Botón "Revisar análisis" deshabilitado con `.is-disabled` | (ninguno) | ✅ implementado |
| Stage 2 todas las cards colapsadas | Default tras `bulkProceedToReview()` | Cards inician con `expanded: false`. Banner AI educativo arriba | Expandir card individual | ✅ implementado |
| Stage 3 procesando | `bulkActivateStage === 3 && !bulkActivationComplete` | Botón "Activando..." con spinner. Per-fuente: spinner → check / warning | (ninguno) | ✅ implementado |
| Stage 3 con fallback parcial | `status === 'partial'` en alguna fuente | Badge ámbar + helper "Configura manualmente para mejorar precisión." | Click abre daysetup individual de esa fuente | ❌ pendiente (visual ya existe, falta CTA) |
| Activation loader en curso | `activationLoaderOpen === true` | Panel modal con database glyph, pulse rings, mini-archivos flotantes, 3 steps | (ninguno, auto-progresa) | ✅ implementado |
| Loading sugerencias bulk-preview | Fetch `POST /monitoring/bulk-preview` en curso | Skeleton de N cards en stage 2 con shimmer en `bulk-preview-num-pill` | (ninguno) | ❌ pendiente |
| Error al cargar bulk-preview | Fetch falló al avanzar de stage 1 a 2 | Card destructive "No pudimos calcular el análisis para algunas fuentes." con lista | Botón "Reintentar" + opción "Continuar sin esas fuentes" | ❌ pendiente |
| Error parcial al activar (real) | Algunas fuentes responden 5xx en `bulk-activate` | Per-fuente `status === 'partial'` + banner global "N de M activadas con éxito." | Botón "Reintentar las pendientes" | ❌ pendiente |
| Activation loader interrumpido (cierre browser) | Page unload durante 2.9s | Timers se pierden, fuente queda en `empty` | (ninguno, requiere retry manual) | ❌ pendiente |
| Cero fuentes seleccionables (todas con permisos negados) | `user.canBulkActivate === false` | Botón bulk oculto desde el header (ver doc 03) | (ninguno) | ❌ pendiente |
| Activación de 0 fuentes (edge) | `bulkActivateSelected.length === 0` en stage 1 | Botón "Revisar análisis" `.is-disabled` | (ninguno) | ✅ implementado |
| Stage 2 todas con `hasHistory: false` | Todas las fuentes son nuevas | Banner warning global "Algunas fuentes no tienen historial. El monitoreo empezará en modo aprendizaje." | (ninguno, informativo) | ❌ pendiente |
| Workspace vacío en preview row | `workspace === ''` | Omitir badge de workspace en la card de preview | (ninguno) | ❌ pendiente |

## Edge cases (validación)

- Cero pendientes al abrir bulk: toast + modal NO abre.
- Click fuera del modal durante stage 3: cerrar resetea timers pero no detiene activaciones en curso (en producción debe cancelarse).
- Activation loader interrumpido por close de browser: timers se pierden, requiere retry.
- Cantidad muy alta (>50): scroll virtualizado en stage 1 y 3 (no resuelto en prototipo, asumir scroll nativo).
- Última fuente del demo (`hasHistory === false`): queda en `partial` para representar el edge case (intencional).
- Botón "Salir" en stage 3 mientras activa: debe permitir cerrar pero advertir que las activaciones siguen.

## Componentes desyk a usar

> Mapeo del prototipo HTML a los componentes oficiales del design system desyk
> (basado en shadcn/ui). El implementador debe reusar estos componentes en lugar
> de replicar las clases CSS custom del prototipo. Este doc cubre dos modales
> independientes: el bulk modal (3 stages) y el activation loader.

### Bulk modal

| Elemento del prototipo | Componente desyk | Variants / props | Notas de uso |
|---|---|---|---|
| `.dialog-backdrop.bulk-modal-backdrop` + `.bulk-modal-panel` | `Dialog` + `DialogContent` | Modal centrado 768x740 | Contenedor del bulk |
| `.bulk-modal-header` + `.bulk-modal-title` + `.bulk-modal-sub` | `DialogHeader` + `DialogTitle` + `DialogDescription` | — | Header con título y subtítulo pedagógico |
| `.bulk-modal-title-help` (ícono ?) | `Tooltip` + `TooltipTrigger` + `TooltipContent` | con ícono `HelpCircle` de Lucide | Ayuda contextual |
| `.bulk-modal-close` (X) | `Button` | `variant="ghost" size="icon"` con ícono `X` de Lucide | Cierra el modal |
| `.bulk-modal-stepper` (3 steps) | Componente custom (compuesto) | — | Stepper visual de 3 etapas (no existe en desyk) |
| `.bulk-modal-footer` con `.secondary-btn` + `.primary-btn` | `DialogFooter` + `Button` (`variant="outline"`) + `Button` (`variant="default"`) | — | Footer stage-aware |
| Botón "Activando..." con spinner | `Button` con ícono `Loader2` de Lucide en animación spin | `disabled` durante la activación | Estado de loading del botón |
| **Stage 1 · Selecciona** | | | |
| `.bulk-modal-toolbar` | Layout custom (`flex`) | — | Toolbar con select-all + counter |
| `.bulk-modal-selectall` (checkbox + label) | `Checkbox` + `Label` | — | Selecciona todas las fuentes |
| `.bulk-modal-counter` ("X de Y seleccionados") | `Badge` | `variant="secondary"` | Contador de selección en tiempo real |
| `.bulk-modal-list-wrap` | Layout custom con scroll | — | Lista scrolleable de fuentes |
| `.bulk-modal-row` (fila de fuente) | Layout custom con `Checkbox` + tipografía + `Badge` | — | Fila con checkbox + nombre + tipo + workspace |
| `.bulk-modal-checkbox` | `Checkbox` | controlado | Toggle por fuente |
| Badges de tipo de ingesta y workspace | `Badge` | `variant="outline"` | Identificación de la fuente |
| **Stage 2 · Revisa** | | | |
| `.bulk-ai-banner` (banner "Análisis inteligente") | `Alert` + `AlertTitle` + `AlertDescription` | `variant="default"` con override violeta AI | Banner pedagógico arriba del listado |
| `.bulk-preview-card` (card de preview por fuente) | `Card` + `Collapsible` + `CollapsibleTrigger` + `CollapsibleContent` | — | Card colapsable que muestra la baseline |
| `.bulk-preview-header` (header colapsable con chevron) | `CollapsibleTrigger` + `Button variant="ghost"` con ícono `ChevronDown` rotable | — | Toggle del expand |
| `.bulk-preview-window-row` (ventana de tiempo) | Layout custom dentro de `CollapsibleContent` | — | Renderiza dos `bulk-preview-time-pill` |
| `.bulk-preview-time-pill` | `Badge` | `variant="outline"` | Píldora con hora propuesta |
| `.bulk-preview-subgroup` (subgrupo en modo grupos) | `Card` con fondo `muted/0.3` | — | Card anidada por grupo |
| `.bulk-preview-indicator` (Volumen / Cantidad de registros) | Layout custom con tipografía + `Badge` | — | Indicador dentro del subgrupo |
| `.bulk-preview-num-pill` (pill con rango min-max) | `Badge` | `variant="outline"` | Píldora numérica del rango |
| **Stage 3 · Activa** | | | |
| `.bulk-activation-list` | Layout custom con scroll | — | Lista de fuentes con su status |
| `.bulk-activation-row` (fila con status) | Layout custom (`flex`) | — | Fila por fuente con ícono de estado |
| `.bulk-activation-status.is-pending` | Ícono `Circle` de Lucide en gris | — | Estado esperando |
| `.bulk-activation-status.is-calculating` | Ícono `Loader2` de Lucide en spin violeta | — | Estado procesando |
| `.bulk-activation-status.is-success` | Ícono `CheckCircle2` de Lucide en verde | — | Estado activada |
| `.bulk-activation-status.is-partial` | Ícono `AlertTriangle` de Lucide en ámbar | — | Estado parcial (caveat) |

### Activation loader (individual)

| Elemento del prototipo | Componente desyk | Variants / props | Notas de uso |
|---|---|---|---|
| `.dialog-backdrop.activation-loader-backdrop` + `.activation-loader-panel` | `Dialog` + `DialogContent` | Modal centrado 768x740 sin botón close | Loader bloqueante 2.9s |
| `.activation-loader-illu` (ilustración decorativa) | Componente custom (compuesto) | — | Database glyph + pulse rings + mini-archivos flotantes |
| `.activation-loader-content` con eyebrow + title + sub | Tipografía custom (no es componente desyk) | — | Contenido textual del loader |
| `.activation-loader-steps` (3 steps con progreso) | Componente custom (compuesto) | — | Stepper vertical con spinner por step |

### Toast de feedback

| Elemento del prototipo | Componente desyk | Variants / props | Notas de uso |
|---|---|---|---|
| Toast "No hay fuentes sin monitoreo" | `Toast` + `useToast` | `variant="default"` (info) | Aparece cuando se intenta abrir bulk sin pendientes |

**Componentes compuestos (no existen en desyk, hay que componerlos):**
- `BulkStepper` — stepper de 3 etapas (Selecciona / Revisa / Activa) con números y checks. No existe en desyk; construir custom.
- `BulkPreviewCard` — card colapsable con header + body que muestra ventana, grupos (o single) y rangos. Compuesto sobre `Card` + `Collapsible`.
- `ActivationStatusIcon` — ícono dinámico según status (`pending` / `calculating` / `success` / `partial`). Compuesto sobre íconos de Lucide.
- `ActivationLoader` — modal con database glyph animado, pulse rings (delays 0/0.6s/1.2s), mini-archivos flotantes (`activationFloat` keyframe) y stepper de 3 pasos. Compuesto custom; reusa `Dialog` como contenedor.
- `ActivationStepper` — stepper vertical de 3 pasos (Detectando / Identificando / Calculando) con spinner activo por paso. Construir custom.
- `BulkAiBanner` — banner con ícono violeta + eyebrow "Análisis inteligente" + disclaimer. Wrapper sobre `Alert`.

**Referencias:**
- Repo desyk: `~/Simetrik/desyk-components` (read-only).
- Lista oficial de componentes shadcn/ui que desyk extiende.

## Implementation notes

- **Helpers Alpine ya existentes** a reusar: `openBulkActivate()`, `closeBulkActivate()`, `toggleBulkSelectAll()`, `toggleBulkSelect(id)`, `bulkProceedToReview()`, `bulkBuildPreview()`, `bulkTogglePreviewExpand(pi)`, `bulkRunActivation()`, `bulkActivationComplete` (getter), `openActivationLoader(r)`.
- **CSS/clases** ya existentes: `.bulk-modal-panel`, `.bulk-modal-header`, `.bulk-modal-stepper`, `.bulk-modal-body`, `.bulk-modal-list-wrap`, `.bulk-modal-toolbar`, `.bulk-modal-row`, `.bulk-ai-banner`, `.bulk-preview-card`, `.bulk-preview-window-row`, `.bulk-preview-subgroup`, `.bulk-preview-indicator`, `.bulk-preview-num-pill`, `.bulk-activation-list`, `.bulk-activation-row`, `.bulk-activation-status` (con `is-pending`, `is-calculating`, `is-success`, `is-partial`), `.activation-loader-panel`, `.activation-loader-illu`, `.activation-loader-glyph`, `.activation-loader-ring`, `.activation-loader-float`, `.activation-loader-steps`, `.activation-loader-step`.
- **Endpoints BE**:
  - `POST /dashboards/{id}/monitoring/bulk-preview` con `source_ids[]` (devuelve previews con baselines).
  - `POST /dashboards/{id}/monitoring/bulk-activate` con `source_ids[]` (devuelve stream o array).
  - `GET /sources/{id}/analysis-preview` para activation loader individual.
- **Tokens desyk**: `hsl(var(--ai-purple))` para banner AI y el botón "Activar monitores", `hsl(var(--success))` para check de stage 3, `hsl(var(--warning))` para `is-partial`, `hsl(var(--primary))` para stepper activo.
- **Animation / motion**: `activationFloat` keyframe para mini-archivos, pulse rings con delays 0/0.6s/1.2s, 700ms entre transiciones de estado por fuente en stage 3, 2.9s total del activation loader (800/1600/2400ms por step).

## Out of scope

- Edición masiva (bulk edit) de configuraciones existentes — explícitamente NO se cubre. La edición sigue siendo uno-a-uno desde la lista (ver doc 05).
- Bulk delete de monitores ya configurados.
- Stream de progreso real (WebSocket / SSE) en stage 3 — la simulación usa `setTimeout` por ahora.
- Configuración personalizada por fuente dentro del bulk (todas usan baseline AI).
- Retry automático de las fuentes `partial`.
- Persistencia del estado bulk si el usuario cierra el browser a mitad.

## Criterios de aceptación

1. **Given** 0 fuentes con `status === 'empty'`, **When** se llama `openBulkActivate()`, **Then** se muestra un toast y el modal no se abre.
2. **Given** N fuentes pendientes, **When** se abre el modal, **Then** todas quedan preseleccionadas en stage 1.
3. **When** el usuario marca/desmarca filas, **Then** el contador "X de Y seleccionados" se actualiza en tiempo real.
4. **Given** `bulkActivateSelected.length === 0`, **Then** "Revisar análisis" está deshabilitado con `.is-disabled`.
5. **When** se avanza a stage 2, **Then** `bulkPreview` se construye y cada card empieza colapsada (`expanded: false`).
6. El stepper muestra un check en el step 1 cuando el usuario llega a stage 2 (`bulkActivateStage > 1`).
7. **When** se pulsa "Activar monitores", **Then** se va a stage 3 y cada fuente progresa de `pending` a `calculating` a `success` o `partial` con 700ms entre transiciones.
8. La última fuente del demo (`hasHistory === false`) debe quedar en `partial` para representar el edge case.
9. **Given** `bulkActivationComplete`, **Then** el botón cambia de "Activando" (con spinner) a "Cerrar".
10. **Given** una card con `r.status === 'empty'`, **When** el usuario hace click, **Then** se abre el activation loader por exactamente 2.9s y luego el daysetup en edición.
11. El activation loader muestra el nombre de la fuente en el title y progresa por los 3 steps en 800/1600/2400ms.
12. La ilustración del loader debe mantener las animaciones (`activationFloat`, pulse rings con delays 0/0.6s/1.2s) sin saltos.
13. Los textos del modal no deben usar em-dashes ni slang regional (verificar contra `00-CONTEXT.md`).

## Dependencies

- **Depende de**: `03-banner-monitorear-tablero` (entrada principal), `04-cards-monitores-ingesta` (entrada para activation loader individual).
- **Bloquea a**: `05-modal-configuracion` (el activation loader desemboca en el daysetup).
- **Relacionado con**: `00-CONTEXT.md`.

## Verification (cómo probarlo)

1. Abrir `index.html`. Ir a tab Ingesta con varias fuentes `status === 'empty'`.
2. Click "Activar las N a la vez". Validar stage 1 con todas preseleccionadas.
3. Desmarcar algunas, validar contador y botón habilitado/deshabilitado.
4. Click "Revisar análisis". Validar stage 2 con cards colapsadas y banner AI.
5. Expandir una card y validar ventana de tiempo, grupos (o single) y baseline.
6. Click "Activar monitores". Validar stage 3 con progresión 700ms por fuente.
7. Validar que la última fuente queda en `partial` (ámbar).
8. Click "Cerrar" cuando termine. Validar cierre y cards movidas a sección "Monitoreado".
9. Probar el activation loader individual: click en una card `empty` y validar 2.9s de loader → daysetup en edición.

## References

- **HTML**: `../index.html` líneas 20520-20607 (activation loader), 20613-20922 (bulk modal: header 20617-20641, stepper 20644-20677, stage 1 20683-20709, stage 2 20712-20839, stage 3 20842-20880, footer 20885-20919).
- **CSS**: líneas 9122-9525 (bulk modal styles), 14913-15047 (activation loader styles).
- **JS**: líneas 15151-15172 (`openActivationLoader`), 15191-15198 (`selectConfigSource`), 16109-16234 (`openBulkActivate`, `bulkBuildPreview`, `bulkProceedToReview`, `bulkRunActivation`, `bulkActivationComplete` getter).
- **Figma**: (pendiente de link)
- **Docs hermanos**: `[03-banner-monitorear-tablero.md](./03-banner-monitorear-tablero.md)`, `[04-cards-monitores-ingesta.md](./04-cards-monitores-ingesta.md)`, `[05-modal-configuracion.md](./05-modal-configuracion.md)`.

---

## Flujos específicos

### Activación masiva (bulk creación)

- **Como** usuario con N fuentes sin configurar
- **Quiero** activar todas las que me interesen en un solo paso, confiando en las baselines del agente
- **Para** dejar el tablero monitoreado de extremo a extremo sin pasar por N modales individuales

**Camino**:

1. **Estado inicial**: en tab Ingesta, sección "Sin monitoreo" con N >= 1 cards `status === 'empty'`. Botón visible en el header del tab con copy "Activar las N a la vez".
   - *Visual*: `.bulk-list-section-action` activo con icono apilado de tres capas y label dinámico.

2. **Click "Activar las N a la vez"**: `openBulkActivate()`.
   - *Side effect*: `bulkActivateOpen = true`, `bulkActivateStage = 1`, `bulkActivateSelected` se rellena con todos los IDs de fuentes `empty`.
   - *Visual*: backdrop `.dialog-backdrop.bulk-modal-backdrop` + panel `.bulk-modal-panel` (768×740) abre.

3. **Stage 1 · Selecciona**: el modal muestra el listado de fuentes pendientes con checkboxes y un toolbar superior.
   - *Componentes visibles*: `.bulk-modal-stepper` (3 steps con el 1 activo), `.bulk-modal-toolbar` (`Seleccionar todos` + contador "X de Y seleccionados"), `.bulk-modal-list-wrap` con N `.bulk-modal-row` (checkbox + nombre + tipo de ingesta + workspace).
   - *Interacciones*:
     - Toggle `Seleccionar todos` (`toggleBulkSelectAll()`).
     - Toggle fila individual (`toggleBulkSelect(id)`).
     - Contador actualiza en tiempo real.
   - *Footer*: "Salir" + "Revisar análisis" (deshabilitado si `bulkActivateSelected.length === 0`).

4. **Click "Revisar análisis"**: `bulkProceedToReview()` invoca `bulkBuildPreview()` y avanza a stage 2.
   - *Side effect*: para cada fuente seleccionada construye `bulkPreview[i]` con baseline AI (ventana, grupos o single, indicadores).
   - *Visual*: stepper muestra check en step 1, step 2 activo.

5. **Stage 2 · Revisa con análisis inteligente**: cards de preview con análisis AI.
   - *Banner top*: `.bulk-ai-banner` con icono violeta, eyebrow "Análisis inteligente" y disclaimer "Puedes editar cada configuración después de activar."
   - *Cards*: `.bulk-preview-card` por fuente, colapsadas por default. Header con nombre + chevron.
   - *Expansión*: click en header expande el body.
     - *Ventana de tiempo*: `.bulk-preview-window-row` con dos `.bulk-preview-time-pill` (llega a las / avisar si pasa).
     - *Modo grupos* (`mode === 'groups'`): `.bulk-preview-subgroup` por grupo con `.bulk-preview-indicator` (Volumen y Cantidad de registros) y `.bulk-preview-num-pill` con rangos.
     - *Modo single* (`mode === 'single'`): indicador único de "Cantidad de registros".
   - *Footer*: "Salir" + "Activar monitores".

6. **Click "Activar monitores"**: `bulkRunActivation()` avanza a stage 3.
   - *Side effect*: cada fuente progresa de `pending` → `calculating` → `success` o `partial` con 700ms entre transiciones (simulado con `setTimeout`).
   - *Visual*: stepper muestra checks en steps 1 y 2, step 3 activo.

7. **Stage 3 · Activa**: lista de fuentes con su status visual.
   - *Componentes*: `.bulk-activation-list` con `.bulk-activation-row` por fuente.
   - *Estados visuales*:
     - `is-pending`: dot gris (esperando).
     - `is-calculating`: spinner violeta (procesando).
     - `is-success`: check verde (activada).
     - `is-partial`: warning ámbar (activada con caveats, ej. sin historia).
   - *Footer*: "Salir" + "Activando..." (con spinner) → cambia a "Cerrar" cuando `bulkActivationComplete === true`.

8. **Click "Cerrar"**: `closeBulkActivate()` cierra el modal.
   - *Side effect*: tras 200ms el estado interno se resetea (`bulkActivateStage = 1`, listas vacías).
   - *Visual*: las cards activadas aparecen en la sección "Monitoreado" del tab Ingesta.

**Copy esperado clave**:
- Header: "Activar monitores en bloque" / subtitle "Selecciona las fuentes, revisa el análisis y actívalas todas a la vez."
- Banner AI stage 2: "Análisis inteligente · Estas baselines vienen del histórico de cada fuente. Puedes editar cada configuración después de activar."
- Footer stage 1: "Revisar análisis"
- Footer stage 2: "Activar monitores"
- Footer stage 3 procesando: "Activando..." con spinner
- Footer stage 3 listo: "Cerrar"

---

### Edición masiva (NO cubierta)

**Decisión de producto explícita**: la edición masiva de configuraciones existentes **NO** está cubierta en este flujo.

- **Por qué**: el bulk modal está diseñado para **activación** (de `empty` a monitoreado con baseline AI), no para edición. Editar config existente requiere ver y modificar valores ya guardados, lo cual no es bien soportado por el formato de preview cards colapsables.
- **Workaround actual**: la edición sigue siendo **uno-a-uno** desde la lista. El usuario debe:
  1. Identificar la card monitoreada en la sección "Monitoreado".
  2. Click → abre daysetup en `daySetupReadonly === true`.
  3. Click "Editar" en el footer → habilita edición.
  4. Modificar valores → click "Guardar".
- **Out of scope futuros**:
  - Selección multi-card en la lista con toolbar contextual ("Editar N seleccionados").
  - Bulk update de un campo específico (ej. cambiar ventana de tiempo de 5 fuentes a la vez).
  - Plantillas reutilizables ("Aplicar configuración de fuente A a fuentes B y C").

**Si en el futuro se necesita edición masiva**, considerar:
- Un modo distinto del bulk modal con stages "Selecciona" + "Edita campo" + "Aplica".
- Restricciones por tipo de fuente (no todas comparten esquema de KPIs).
- Confirmación destructiva (sobrescribir config existente requiere doble check).
- Audit log de cambios masivos para rollback.

---

### Activation loader individual

Cubierto en el cuerpo principal (Flujo B). Resumen: cuando el usuario hace click en una card `empty` desde la lista (no desde bulk), `selectConfigSource(r)` detecta el estado y dispara `openActivationLoader(r)` antes del daysetup. El loader es **idéntico visualmente** al stage de "preparación" del bulk, pero es para una sola fuente y precede a la apertura del modal de configuración en modo edición (`daySetupReadonly === false`, `daySetupHasConfig === false`).
