---
epic: MONITOR_INGESTA
issue_type: Feature
priority: P0
estimate: L
labels: [ux, frontend, monitoring, modal-config, daysetup, day-behavior]
depends_on: [05-modal-configuracion]
blocks: [09-contenedor-volumen-archivos, 10-contenedor-cantidad-registros, 11-contenedor-notas-adicionales, 12-contenedor-grupos-high]
component_areas: [modal-config, daysetup, day-behavior, tab-switcher]
---

# 08 · Contenedor Comportamiento de la fuente

> Card que aloja el tab switcher Lu-Do, el subtítulo del día activo y el toggle de monitoreo del día. Es el chasis sobre el que se montan los indicadores y, en High, las cards de grupo. Vive en `<section class="ds-card">` dentro del modal `.resource-config-panel`.

## Propósito
- Concentra todo lo que cambia día por día: qué día estoy viendo, si lo monitoreo o no, y cómo. Es el contenedor donde se materializa el modelo Low / Family / High.
- En el journey, es el segundo card que ve el usuario al abrir el modal. Su comportamiento muta según `monitorMode` y `useGroupsAll`.

## Anatomía
| Subcomponente | Clase | Función |
|---|---|---|
| Tabs row | `ds-tabs-row` | Contenedor del tab switcher + badge warning. |
| Candado | `ds-lock` (con `is-closed` cuando Low) | Icono `lock` cerrado en Low y `lock-open` en Family/High. |
| Tab switcher | `tm-tabs` con `tm-tab` por día | Botones `Lu Ma Mi Ju Vi Sa Do` (label corto). Dot `ds-tab-dot` cuando el día está en `por-dia` y `monitorEnabled`. |
| Badge warning Low | `ds-low-chip` | Pill con icono candado + texto "Igual todos los días". Solo en Low. |
| Subtítulo | `ds-day-head` | Texto "Comportamiento de la fuente" + chip `ds-day-chip` con el nombre del día activo. |
| Toggle día | `ds-day-toggle` | Switch full-width con título dinámico, subtítulo y icono `?`. |
| Loader pedagógico | `calc-loader` | Spinner + "Detectando los grupos de archivos" durante la transición a High. |
| Slot Low/Family | `template x-if` con `monitorEnabled && !useGroupsAll` | Renderiza indicadores `dsActiveSimple()`. |
| Slot High | `template x-if` con `monitorEnabled && useGroupsAll` | Renderiza cards `ds-group` por grupo. |

## Estados
| Estado | monitorMode | useGroupsAll | Visual |
|---|---|---|---|
| Low | `igual` | `false` | Candado cerrado. Badge `Igual todos los días` visible. Tabs sin dot. |
| Family | `por-dia` | `false` | Candado abierto. Sin badge. Dot azul en días con `monitorEnabled`. |
| High | `por-dia` | `true` | Candado abierto. Sin badge. Slot renderiza cards `ds-group` en vez de indicadores simples. |
| Día apagado | cualquiera, `d.monitorEnabled === false` | cualquiera | Toggle OFF. Indicadores y banner ocultos. Subtítulo del toggle invita a activar. |

## Comportamiento
| Condición | Visible? | Editable? | Datos que muestra |
|---|---|---|---|
| `daySetupReadonly` | Sí | No | Toggle oculto. Solo se ven los indicadores (lectura). |
| `daySetup.loading` | Sí | No | Loader pedagógico ~1.4s. Reemplaza el contenido. |
| `dsActiveDay().monitorEnabled === false` | Sí | Sí (toggle) | Solo se ve el toggle OFF y el hint. Sin banner, sin indicadores. |
| `monitorMode === 'igual'` | Sí | Sí | El cambio de día no varía la config (toda viene de `daySetup.shared`). |
| `monitorMode === 'por-dia' && !useGroupsAll` | Sí | Sí | Cada día tiene su `simple` propio. |
| `useGroupsAll === true` | Sí | Sí | Cada día tiene sus `groups` con configuración individual. |

## Data binding
- `daySetup.activeDay` (string `lun` | `mar` | ... | `dom`): día seleccionado en el switcher.
- `daySetup.days[]`: cada item tiene `{ key, label, monitorEnabled, simple, groups }`.
- `daySetup.monitorMode`, `daySetup.useGroupsAll`, `daySetup.loading`.
- Helper `dsActiveDay()` resuelve el día actual del switcher.

## Interacciones
| Trigger | Side effects | Próximo estado |
|---|---|---|
| Click en tab Lu-Do | Setea `daySetup.activeDay`. | Render del día seleccionado. |
| Click en toggle del día | Llama `dsToggleDayMonitor()`. Si Low, fuerza promoción a Family (`dsPromoteToFamily('toggle')`). Apaga/prende `d.monitorEnabled`. | Family o cambio de estado on/off del día. |
| Editar input de indicador en Low | `dsPromoteToFamily('edit')`. | Family con banner de feedback 6s. |
| Click `Monitorear grupos` (en banner del día) | `dsActivateGroups()` + loader 1.4s + siembra de grupos en todos los días. | High. |
| Hover sobre candado | Tooltip nativo via `:title`. | Sin cambio. |

## Empty states (importante)

El prototipo HTML actual solo tiene algunos empty states (loaders, casos puntuales). Aunque no estén pintados, esta historia debe enumerarlos para que el implementador los considere.

| Escenario | Condición | Copy propuesto | CTA | Implementado en HTML? |
|---|---|---|---|---|
| Día sin patrones detectados (High) | `useGroupsAll === true && dsActiveDay().groups.length === 0` | "No detectamos grupos los [día]. Esta fuente no recibe archivos este día, o todavía no hay histórico para detectar sus patrones." | (ninguno) | ✅ (`ds-day-off`) |
| Día con monitor apagado | `dsActiveDay().monitorEnabled === false` | Toggle OFF. Subtítulo "Activa el monitoreo cuando quieras recibir alertas para este dia." | Switch toggle ON. | ✅ |
| Loading de grupos (transición a High) | `daySetup.loading === true` | "Detectando los grupos de archivos. Simetrik está identificando los archivos que comparten patrón..." con spinner. | (ninguno) | ✅ (`calc-loader`) |
| Error al cargar configuración del día | Fetch del `dayConfig` falló | Card destructive con "No pudimos cargar la configuración de este día." | Botón "Reintentar". | ❌ |
| Fuente sin histórico (todos los días sin patrones) | `daySetup.days.every(d => d.groups.length === 0)` en High | Banner global "Sin histórico suficiente para detectar patrones. Vuelve cuando tengamos al menos 2 semanas de datos." | Botón "Volver a Family". | ❌ |
| Todos los días apagados | `daySetup.days.every(d => !d.monitorEnabled)` | Banner warning sobre el card "Esta fuente quedará sin monitoreo. Activa al menos un día para guardar." | (ninguno, bloquea Guardar) | ❌ |
| Promoción fallida (Low → Family) | `dsPromoteToFamily()` lanzó excepción | Toast destructive "No pudimos cambiar a configuración por día. Intenta de nuevo." | Botón "Reintentar" en el toast. | ❌ |

## Edge cases
- En Family, si un día queda con `monitorEnabled === false`, el dot azul desaparece (solo se pinta cuando el día está activo).
- En High, si el día no tiene patrones detectados (`groups.length === 0`), se muestra `ds-day-off` con copy "No detectamos grupos los [día]".
- En readonly, el toggle se oculta completo (`x-show="!daySetupReadonly"`), no se muestra deshabilitado.

## Componentes desyk a usar

> Mapeo del prototipo HTML a los componentes oficiales del design system desyk
> (basado en shadcn/ui). El implementador debe reusar estos componentes en lugar
> de replicar las clases CSS custom del prototipo.

| Elemento del prototipo | Componente desyk | Variants / props | Notas de uso |
|---|---|---|---|
| `.ds-card` (contenedor del chasis) | `Card` + `CardHeader` + `CardContent` | — | Card del comportamiento de la fuente |
| `.ds-tabs-row` (fila con candado + tabs + badge) | Layout custom (`flex`) | — | Contenedor del switcher de día |
| `.ds-lock` (candado Lu-Do) | Ícono `Lock` o `LockOpen` de Lucide | — | Toggle visual entre Low (cerrado) y Family/High (abierto) |
| `.tm-tabs` con `.tm-tab` (tabs Lu Ma Mi Ju Vi Sa Do) | `Tabs` + `TabsList` + `TabsTrigger` | controlado con `value={activeDay}` | Tab switcher de 7 días |
| `.ds-tab-dot` (dot primary en días con monitoreo activo) | `<span>` decorativo con `bg-primary` | — | Indicador visual dentro del `TabsTrigger`, no es componente desyk |
| `.ds-low-chip` (badge warning "Igual todos los días") | `Badge` | `variant="default"` con override warning + ícono `Lock` | Visible solo en Low |
| `.ds-day-head` (subtítulo + chip del día activo) | Tipografía + `Badge` | `Badge variant="secondary"` para el día | Encabezado del día actual |
| `.ds-day-chip` (chip con el nombre del día activo) | `Badge` | `variant="secondary"` | "Lunes", "Martes", etc. |
| `.ds-day-toggle` (switch full-width Monitorear día) | `Switch` + `Label` (layout custom como tarjeta) | `checked` + `onCheckedChange` | Switch grande con title + subtítulo |
| `.ds-switch` (switch del toggle) | `Switch` | — | Componente shadcn standard |
| `.calc-loader` (loader pedagógico de transición a High) | Componente custom (compuesto) | — | Spinner 1.4s con copy "Detectando los grupos de archivos" |
| `.ds-day-off` (estado vacío "No detectamos grupos los [día]") | Componente custom (compuesto) | — | Empty state cuando High y `groups.length === 0` |
| Slot Low/Family (indicadores planos) | Ver docs 09, 10, 11 | — | Renderizado condicional |
| Slot High (cards de grupo) | Ver doc 12 | — | Renderizado condicional |

**Componentes compuestos (no existen en desyk, hay que componerlos):**
- `DayBehaviorCard` — chasis del card de comportamiento. Orquesta el tab switcher + toggle + loader + slot según `monitorMode` y `useGroupsAll`.
- `DaysTabSwitcher` — tab switcher con candado + 7 días + dots por día con monitoreo activo. Compuesto sobre `Tabs` + ícono `Lock`/`LockOpen` de Lucide + dots decorativos.
- `MonitorModeChip` — badge warning "Igual todos los días" con ícono `Lock`. Wrapper sobre `Badge`.
- `DayMonitorToggle` — toggle full-width tipo tarjeta con title + subtítulo + ícono ? + `Switch`. Compuesto sobre `Switch` + `Tooltip` + layout custom.
- `PedagogicalLoader` — ver doc 05 (mismo componente reusado).
- `DayOffEmptyState` — empty state vertical con copy "No detectamos grupos los [día]". Compuesto con tipografía + ilustración placeholder.

**Referencias:**
- Repo desyk: `~/Simetrik/desyk-components` (read-only).
- Lista oficial de componentes shadcn/ui que desyk extiende.

## Implementation notes

- **Helpers Alpine ya existentes** a reusar: `daySetup.activeDay`, `daySetup.days[]`, `daySetup.monitorMode`, `daySetup.useGroupsAll`, `daySetup.loading`, `dsActiveDay()`, `dsActiveSimple()`, `dsToggleDayMonitor()`, `dsPromoteToFamily()`, `dsActivateGroups()`.
- **CSS/clases**: `.ds-card`, `.ds-tabs-row`, `.ds-lock` (con `is-closed`), `.tm-tabs`, `.tm-tab` (con `ds-tab-dot`), `.ds-low-chip`, `.ds-day-head`, `.ds-day-chip`, `.ds-day-toggle`, `.ds-switch`, `.calc-loader`, `.ds-day-off`.
- **Endpoints BE**: `GET /sources/{id}/monitoring` debe devolver `days[]` con `monitorEnabled` y la lógica de modo (`monitorMode`, `useGroupsAll`).
- **Tokens desyk**: `hsl(var(--primary))` para dots de día activo, `hsl(var(--warning))` para badge Low chip, `hsl(var(--muted))` para candado cerrado.
- **Animation / motion**: 200ms ease-out al cambiar de día, 1.4s loader pedagógico al activar grupos, transición de candado lock → lock-open suave.

## Out of scope

- Configuración multi-día simultánea (ej. "configurar Lu y Ma con los mismos valores").
- Reordenamiento de días o vista no lineal.
- Modo "downgrade" Family → Low o High → Family.
- Vista por horario dentro del día.

## Criterios de aceptación
1. El candado muestra `lock` cerrado solo cuando `monitorMode === 'igual'`, y `lock-open` en los otros dos modos.
2. El badge "Igual todos los días" aparece exclusivamente en Low.
3. Los dots azules en los tabs solo se renderizan cuando `monitorMode === 'por-dia'` y ese día tiene `monitorEnabled`.
4. El título del toggle cambia entre "Monitorear fuente los [día]" (ON) y "No monitoreamos esta fuente los [día]" (OFF).
5. Al apagar el toggle en Low, se dispara `dsPromoteToFamily('toggle')` antes de cambiar el flag.
6. Durante `daySetup.loading`, el loader reemplaza todo el contenido por debajo del subtítulo del día.

## Dependencies

- **Depende de**: `05-modal-configuracion` (modal padre).
- **Bloquea a**: `09`, `10`, `11`, `12` (slots dentro del card).
- **Relacionado con**: `13-journey-low-family-high` (síntesis del modelo).

## Verification (cómo probarlo)

1. Abrir daysetup de fuente nueva: validar candado cerrado y badge Low chip.
2. Cambiar dropdown a "Por día": validar candado abierto y badge oculto.
3. Click en tab "Mar": validar `activeDay === 'mar'` y subtítulo actualizado.
4. Apagar toggle día: en Low debe promover a Family con banner; en Family debe simplemente apagar.
5. Click "Monitorear grupos": validar loader 1.4s y siembra de grupos en los 7 días.
6. En High con `groups.length === 0` para el día activo: validar render del `ds-day-off`.
7. Modo readonly: validar toggle oculto, switches con opacity 0.6.

## References

- **HTML** (por selector): `<section class="ds-card">` con el tab switcher Lu-Do (`.ds-day-tabs`) y el toggle de día, dentro de `.resource-config-panel`.
- **JS** (helpers en `appData()`): `dsToggleDayMonitor()`, `dsPromoteToFamily()`, `dsActivateGroups()`.
- **Figma**: (pendiente de link)
- **Docs hermanos**: `[09-contenedor-volumen-archivos.md](./09-contenedor-volumen-archivos.md)`, `[10-contenedor-cantidad-registros.md](./10-contenedor-cantidad-registros.md)`, `[11-contenedor-notas-adicionales.md](./11-contenedor-notas-adicionales.md)`, `[12-contenedor-grupos-high.md](./12-contenedor-grupos-high.md)`, `[13-journey-low-family-high.md](./13-journey-low-family-high.md)`.
