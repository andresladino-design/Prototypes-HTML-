---
epic: MONITOR_INGESTA
issue_type: Feature
priority: P0
estimate: L
labels: [ux, frontend, monitoring, modal-config, daysetup, groups, ai, high-mode]
depends_on: [08-contenedor-comportamiento-dia, 09-contenedor-volumen-archivos, 10-contenedor-cantidad-registros, 11-contenedor-notas-adicionales]
blocks: []
component_areas: [modal-config, daysetup, groups-high, peek]
---

# 12 · Contenedor Grupos (modo High)

> Card colapsable por cada grupo de archivos detectado por el agente. Aparece solo en modo High (`useGroupsAll === true`) y reemplaza los indicadores planos de Low/Family por una configuración por grupo. Vive dentro del slot High del card de comportamiento (HTML ~21545).

## Propósito
- Permite monitorear por separado cada subconjunto de archivos de una fuente que tiene patrones diferentes (ej: `Visa_TC05_*.csv`, `Mastercard_IPM_*.csv`, `Acquirer_*.csv`).
- Es la respuesta a "esta fuente trae archivos con comportamientos muy distintos, configurar un solo umbral pierde precisión". El agente detecta los grupos a partir del histórico y los siembra cuando el usuario hace click en `Monitorear grupos`.
- Cada grupo es un mini-contenedor con su propio Volumen, Cantidad y Notas. El primer grupo del día arranca expandido (Figma); los demás colapsados.

## Anatomía
| Subcomponente | Clase | Función |
|---|---|---|
| Card grupo | `ds-group` (con `is-expanded` cuando abierto) | Contenedor border + radius. |
| Header | `ds-group-head` | Clickeable. Toggle expand. |
| Header left | `ds-group-head-left` | Icono `scan` + nombre del grupo mono + meta. |
| Nombre | `ds-group-name` | Mono, ej: `Visa_TC05_Settlement`. |
| Badge archivos | `ds-group-badge` | `N archivos` (singular `archivo` si N === 1). |
| Badge estado | `ds-group-badge is-status` | "Configurado" verde. |
| Header right | `ds-group-head-right` | Botón inspeccionar (`ds-group-icon-btn`) + chevron + peek popover. |
| Botón inspeccionar | `ds-group-icon-btn` con `data-peek-trigger` | Icono ojo. Toggle del peek. |
| Chevron | `ds-group-chev` (con `is-up`) | Expand/collapse del body. |
| Peek popover | `ds-peek-card` | Card absoluto anclado al botón. Patrón + archivos + footer. |
| Sección patrón | `ds-peek-section` | Title "Patrón de agrupación" + chips de tokens. |
| Token chip | `ds-peek-pattern-chip` / `-sep` / `-ext` | Visualización del `chain` del grupo. |
| Sección archivos | `ds-peek-section` con counter | Lista scroll (`max-height:200px`) de samples. |
| Footer peek | `ds-peek-footer` | Icono clock + "Utiliza revisión: [fecha]". |
| Body | `ds-group-body` | Volumen + Cantidad + Notas (todos con fondo `muted/0.3`). |

## Estados
| Estado | Trigger | Visual |
|---|---|---|
| Colapsado | `g.expanded === false` | Solo header. Chevron apuntando abajo. |
| Expandido | `g.expanded === true` | Header con borde `primary/0.25` + body con indicadores. Chevron rotado 180. |
| Peek abierto | `peek === true` (estado Alpine local del grupo) | Popover absoluto debajo del header-right. |
| Inspector activo | `peek === true` | Botón `ds-group-icon-btn` con `is-active`. |
| Día sin patrones | `dsActiveDay().groups.length === 0` | Card `ds-day-off` reemplaza la lista con "No detectamos grupos los [día]". |

## Comportamiento
| Condición | Visible? | Editable? | Datos que muestra |
|---|---|---|---|
| `useGroupsAll === false` | No | N/A | Modo Low o Family: se renderiza el slot simple, no este. |
| `useGroupsAll === true && monitorEnabled === true` | Sí | Sí | Lista de `dsActiveDay().groups`. |
| `monitorEnabled === false` | No | N/A | Toggle del día apaga todo el slot. |
| `daySetupReadonly === true` | Sí | No | Switches e inputs deshabilitados, peek sigue funcionando. |
| `daySetup.loading === true` | No | N/A | Loader pedagógico reemplaza el slot. |

## Data binding
- `daySetup.useGroupsAll` (boolean global): habilita el slot.
- `dsActiveDay().groups[]`: array de grupos del día. Cada item: `{ id, name, pattern, chain, filesFound, samples, expanded, fileCount, rowCount, notes }`.
- `g.expanded`: local al grupo.
- `peek`: estado Alpine local (`x-data="{ peek: false }"`).
- Helper `dsPatternTokens(g)`: parte `g.chain` en chips/separadores/extension para el peek.

## Interacciones
| Trigger | Side effects | Próximo estado |
|---|---|---|
| Click en `ds-group-head` (no en botones) | Flip `g.expanded`. | Expand o collapse. |
| Click en chevron | `@click.stop` + flip `g.expanded`. | Igual que click en head. |
| Click en botón inspeccionar | `@click.stop` + flip `peek`. | Peek visible u oculto. |
| Click fuera del peek (no en trigger) | `@click.outside` cierra peek. | Peek oculto. |
| Click `Monitorear grupos` en banner (Family) | `dsActivateGroups()` siembra grupos en todos los días + loader 1.4s. | High activo. |

## Empty states (importante)

El prototipo HTML actual solo tiene algunos empty states (loaders, casos puntuales). Aunque no estén pintados, esta historia debe enumerarlos para que el implementador los considere.

| Escenario | Condición | Copy propuesto | CTA | Implementado en HTML? |
|---|---|---|---|---|
| Día sin grupos detectados | `dsActiveDay().groups.length === 0` | "No detectamos grupos los [día]. Esta fuente no recibe archivos este día, o todavía no hay histórico para detectar sus patrones." | (ninguno, informativo) | ✅ (`ds-day-off`) |
| Loading de detección de grupos | `daySetup.loading === true` | Spinner + "Detectando los grupos de archivos. Simetrik está identificando los archivos que comparten patrón..." | (ninguno) | ✅ (`calc-loader`) |
| Grupo sin archivos del último batch | `g.filesFound === 0` | Badge `0 archivos` en gris muted + chip warning "Sin archivos en la última ejecución". | Click expande el grupo para configurar. | ❌ |
| Grupo con un solo archivo | `g.filesFound === 1` | Badge `1 archivo` (singular). Resto igual. | (ninguno) | ✅ (singular hardcoded) |
| Peek con lista vacía de archivos | `g.samples.length === 0` | Sección "Archivos del grupo" con mensaje "Aún no hay archivos de muestra para este grupo." | (ninguno) | ❌ |
| Peek con patrón no parseable | `g.chain` vacío o malformado | Sección "Patrón de agrupación" con mensaje "Sin patrón detectado." | (ninguno) | ❌ |
| Error al cargar grupos | `dsActivateGroups()` falló | Banner destructive sobre el slot "No pudimos detectar los grupos. Intenta de nuevo." | Botón "Reintentar". | ❌ |
| Detección sin patrones en toda la fuente | Activar grupos resultó en 0 grupos en todos los días | Banner "No encontramos grupos diferenciados en esta fuente. Vuelve a Family." | Botón "Volver a Family" (`useGroupsAll = false`). | ❌ |
| Grupo con configuración fallida (parcial) | `g` sin `fileCount` o `rowCount` válidos | Badge `is-status` cambia a "Sin configurar" ámbar en lugar de "Configurado" verde. | (ninguno, expandir para configurar) | ❌ (siempre "Configurado") |

## Empty states (importante)

| Escenario | Condición | Copy propuesto | CTA | Implementado en HTML? |
|---|---|---|---|---|
| Día sin grupos sembrados | `useGroupsAll && dsActiveDay().groups.length === 0` | "No detectamos grupos los [día]. Esta fuente no recibe archivos este día, o todavía no hay histórico para detectar sus patrones." | (ninguno) | ✅ implementado (`ds-day-off`) |
| Loading de grupos (Family → High) | `daySetup.loading === true` | Loader pedagógico "Detectando los grupos de archivos." spinner 1.4s | (ninguno) | ✅ implementado (`calc-loader`) |
| Grupo sin samples para peek | `g.samples.length === 0` | En el peek: "No hay ejemplos de archivos disponibles para este grupo." | (ninguno) | ❌ pendiente |
| Patrón mal parseado | `dsPatternTokens(g)` devuelve vacío o malformado | En el peek: "No pudimos visualizar el patrón. Contacta a soporte." | Link a soporte | ❌ pendiente |
| Error al sembrar grupos | `dsActivateGroups()` falló (BE 5xx) | Toast destructive "No pudimos detectar los grupos. Sigue en Family." con botón "Reintentar" | (ninguno, vuelve a Family) | ❌ pendiente |
| Más de 10 grupos detectados | `dsActiveDay().groups.length > 10` | Banner info "Detectamos N grupos. Considera consolidar patrones si son demasiados." | Link "Aprender más" | ❌ pendiente |
| Sin sugerencia AI para indicador del grupo | `g.fileCount._sMin === null` | Chips muestran "Sin sugerencia disponible" | (ninguno) | ❌ pendiente |
| Grupo con `filesFound === 0` | Grupo registrado pero sin archivos en el último periodo | Badge "Sin archivos" ámbar reemplaza `N archivos`. Body con helper "Este grupo no recibió archivos en la última ventana." | (ninguno) | ❌ pendiente |
| Loading del catálogo de grupos (BE async) | Fetch específico para grupos en curso | Skeleton de 2-3 cards `ds-group` con shimmer | (ninguno) | ❌ pendiente |
| Readonly con peek | `daySetupReadonly && peek === true` | Peek funcional (es inspección, no edición) | (ninguno) | ✅ implementado |
| Nombre de grupo muy largo | `g.name.length > 32` | Truncar con ellipsis + tooltip nativo | (ninguno) | ❌ pendiente |

## Edge cases (validación)
- Si el día activo no tiene grupos sembrados (`groups.length === 0`), se muestra estado vacío `ds-day-off`.
- El peek se posiciona absoluto debajo del `head-right` del grupo, no se ancla al card completo: si el grupo está expandido y se abre el peek, se solapa con el header del body.
- Los indicadores y notas dentro del grupo usan fondo `hsl(var(--muted) / 0.3)` para diferenciarse del contenedor padre.
- El badge `Configurado` está hardcoded en verde: no representa estado real, es un placeholder para futura lógica (ej. partial vs full config).
- `useGroupsAll` es global a la fuente: o todos los días usan grupos o ninguno (no hay mezcla Family + High parcial).
- Primer grupo del día arranca con `expanded: true` (Figma); los demás colapsados.

## Componentes desyk a usar

> Mapeo del prototipo HTML a los componentes oficiales del design system desyk
> (basado en shadcn/ui). El implementador debe reusar estos componentes en lugar
> de replicar las clases CSS custom del prototipo.

| Elemento del prototipo | Componente desyk | Variants / props | Notas de uso |
|---|---|---|---|
| `.ds-group` (card colapsable de grupo) | `Card` + `Collapsible` + `CollapsibleTrigger` + `CollapsibleContent` | con className condicional `is-expanded` para border violeta | Card colapsable por grupo |
| `.ds-group-head` (header clickeable) | `CollapsibleTrigger` con layout custom | — | Toggle expand del grupo |
| Ícono `scan` del header | Ícono `Scan` o `ScanLine` de Lucide | — | Visual del header del grupo |
| `.ds-group-name` (nombre mono del grupo) | Tipografía mono (`font-mono`) | — | Ej: `Visa_TC05_Settlement` |
| `.ds-group-badge` (`N archivos`) | `Badge` | `variant="outline"` | Conteo de archivos con singular/plural |
| `.ds-group-badge.is-status` ("Configurado") | `Badge` | `variant="default"` con override success | Estado del grupo |
| `.ds-group-icon-btn` (botón ojo "inspeccionar") | `Button` | `variant="ghost" size="icon"` con ícono `Eye` de Lucide | Toggle del peek popover |
| `.ds-group-chev` (chevron expand/collapse) | Ícono `ChevronDown` de Lucide con rotación | — | Indicador visual del expand |
| `.ds-peek-card` (popover de inspección) | `Popover` + `PopoverTrigger` + `PopoverContent` | `align="end"` | Popover anclado al botón ojo |
| `.ds-peek-section` (secciones del peek) | Layout custom dentro de `PopoverContent` | — | Secciones Patrón + Archivos + Footer |
| Title de sección del peek ("Patrón de agrupación") | Tipografía heading | — | Encabezado de sección |
| `.ds-peek-pattern-chip` (chips de tokens del patrón) | `Badge` | `variant="outline"` | Visualización del `chain` parseado |
| `.ds-peek-pattern-sep` (separadores `_`, `-`) | Tipografía mono | — | Separadores entre chips |
| `.ds-peek-pattern-ext` (extensión `.csv`) | `Badge` | `variant="secondary"` | Token de extensión |
| Lista de samples (scroll vertical) | Layout custom con `max-h-[200px] overflow-y-auto` | — | Lista scrolleable de archivos de muestra |
| `.ds-peek-footer` (icon clock + "Utiliza revisión: [fecha]") | Tipografía muted-foreground + ícono `Clock` de Lucide | — | Footer del peek |
| `.ds-group-body` (body con Volumen + Cantidad + Notas) | `CollapsibleContent` con fondo `muted/0.3` | — | Body del grupo con indicadores replicados |
| `.ds-day-off` (estado vacío "No detectamos grupos los [día]") | Componente custom (compuesto, ver doc 08) | — | Empty state cuando `groups.length === 0` |
| Indicadores Volumen / Cantidad dentro del grupo | Ver docs 09 y 10 (`IndicatorCard`) | — | Componentes reusados |
| Notas dentro del grupo | Ver doc 11 (`AdditionalNotesCard`) | — | Componente reusado |

**Componentes compuestos (no existen en desyk, hay que componerlos):**
- `GroupCard` — card colapsable por grupo con header (nombre mono + badges + botón ojo + chevron) + body (indicadores + notas). Compuesto sobre `Card` + `Collapsible` + `Popover`.
- `GroupPeekPopover` — popover con tres secciones: Patrón (chips parseados de `dsPatternTokens`), Archivos (lista scroll), Footer (fecha de revisión). Compuesto sobre `Popover` + `Badge` + layout.
- `GroupPatternViz` — visualización del `chain` del grupo como secuencia de `Badge` chips + separadores + extension. Compuesto a partir de `dsPatternTokens(g)`.
- `GroupStatusBadge` — badge dinámico ("Configurado" verde / "Sin configurar" ámbar según futura lógica). Wrapper sobre `Badge`.
- `DayOffEmptyState` — ver doc 08 (mismo componente reusado).

**Referencias:**
- Repo desyk: `~/Simetrik/desyk-components` (read-only).
- Lista oficial de componentes shadcn/ui que desyk extiende.

## Implementation notes

- **Helpers Alpine ya existentes** a reusar: `daySetup.useGroupsAll`, `dsActiveDay()`, `dsActivateGroups()`, `dsSeedGroupsFor()`, `dsPatternTokens(g)`, `daySetupReadonly`.
- **CSS/clases**: `.ds-group` (con `is-expanded`), `.ds-group-head`, `.ds-group-head-left`, `.ds-group-head-right`, `.ds-group-name`, `.ds-group-badge` (con `is-status`), `.ds-group-icon-btn` (con `is-active`), `.ds-group-chev` (con `is-up`), `.ds-group-body`, `.ds-peek-card`, `.ds-peek-section`, `.ds-peek-pattern-chip`, `.ds-peek-pattern-sep`, `.ds-peek-pattern-ext`, `.ds-peek-footer`, `.ds-day-off`.
- **Endpoints BE**: `POST /sources/{id}/groups/detect` para sembrar grupos al activar; `GET /sources/{id}/groups/{group_id}` para detalle del peek.
- **Tokens desyk**: `hsl(var(--primary) / 0.25)` para border del grupo expandido, `hsl(var(--success))` para badge "Configurado", `hsl(var(--muted) / 0.3)` para fondo de indicadores dentro del grupo, `hsl(var(--ai-purple))` para acentos AI.
- **Animation / motion**: 200ms ease-out para expand/collapse del grupo, rotación del chevron, 1.4s loader pedagógico al sembrar grupos.

## Out of scope

- Edición del patrón de agrupación (`g.chain`) desde el UI. Es lectura, lo detecta el agente.
- Eliminación de un grupo específico desde el peek (el modelo es all-or-nothing en `useGroupsAll`).
- Renombrar grupos.
- Downgrade High → Family.
- Crear grupos manuales (todos los grupos vienen del análisis del agente).

## Criterios de aceptación
1. La lista de grupos solo se renderiza si `daySetup.useGroupsAll === true && dsActiveDay().monitorEnabled === true && !daySetup.loading`.
2. Cada grupo muestra: nombre mono, badge `N archivos` (singular `archivo` si N=1), badge `Configurado` verde, botón inspeccionar, chevron.
3. El primer grupo del día arranca con `expanded: true` (Figma).
4. El peek se abre y cierra con click en el botón inspeccionar. Click fuera (excepto en el trigger) lo cierra.
5. El body del grupo contiene Volumen + Cantidad + Notas con binding a `g.fileCount`, `g.rowCount`, `g.notes`.
6. Si `dsActiveDay().groups.length === 0`, se muestra el estado vacío `ds-day-off`.

## Dependencies

- **Depende de**: `08-contenedor-comportamiento-dia` (chasis), `09`, `10`, `11` (indicadores y notas que se replican por grupo).
- **Bloquea a**: ninguna.
- **Relacionado con**: `13-journey-low-family-high` (síntesis del modelo).

## Verification (cómo probarlo)

1. Abrir daysetup nuevo y promover a High (click "Monitorear grupos").
2. Validar loader pedagógico 1.4s y siembra de grupos.
3. Validar primer grupo expandido por default, los demás colapsados.
4. Click chevron: validar expand/collapse.
5. Click botón ojo: validar peek anclado al `head-right`.
6. Click fuera del peek (no en el trigger): validar cierre.
7. Cambiar día activo a uno sin grupos: validar `ds-day-off`.
8. Validar indicadores y notas dentro del grupo con fondo `muted/0.3`.
9. Modo readonly con peek: validar peek sigue funcional.

## References

- **HTML**: `../index.html` líneas 21534-21832 (slot High y cards `ds-group`).
- **JS**: `dsActivateGroups()` (línea 15280), `dsSeedGroupsFor()` (línea 15300), `dsPatternTokens()` (línea 15324).
- **Figma**: (pendiente de link)
- **Docs hermanos**: `[08-contenedor-comportamiento-dia.md](./08-contenedor-comportamiento-dia.md)` (padre), `[09-contenedor-volumen-archivos.md](./09-contenedor-volumen-archivos.md)`, `[10-contenedor-cantidad-registros.md](./10-contenedor-cantidad-registros.md)`, `[11-contenedor-notas-adicionales.md](./11-contenedor-notas-adicionales.md)`, `[13-journey-low-family-high.md](./13-journey-low-family-high.md)`.
