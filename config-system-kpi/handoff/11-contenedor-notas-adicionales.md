---
epic: MONITOR_INGESTA
issue_type: Feature
priority: P2
estimate: S
labels: [ux, frontend, monitoring, modal-config, daysetup, notes]
depends_on: [08-contenedor-comportamiento-dia]
blocks: []
component_areas: [modal-config, daysetup, notes]
---

# 11 · Contenedor Notas adicionales

> Card colapsable opcional que captura comportamientos esperados de la fuente (en lenguaje humano) para que el agente los considere al evaluar anomalías. Vive al final del slot Low/Family (HTML ~21455) y replicado por grupo en High (HTML ~21765).

## Propósito
- Permite al usuario documentar particularidades que no se modelan con KPIs numéricos: "llega con retraso", "volumen variable", "archivo dividido", etc.
- Es opcional. Por eso vive colapsado por default y solo expone su contenido al pedirlo explícitamente con el botón `+`.
- En el journey aparece después de los indicadores. En modo detalle (config existente) solo se muestra si el usuario realmente cargó tags o detalle.

## Anatomía
| Subcomponente | Clase | Función |
|---|---|---|
| Header | `ds-notes-head` | Title "Notas adicionales" + icono `?` + subtítulo descriptivo + botón `+` a la derecha. |
| Botón add | `ds-notes-add` (con `is-open` cuando abierto) | Caja 40×40. Icono `plus` cerrado, icono `minus` abierto. |
| Tags grid | `ds-notes-tags` | Chips de comportamientos predefinidos. Multi-select. |
| Tag | `ds-notes-tag` (con `is-selected`) | Pill con icono `circle-plus` (deselect) o `circle-minus` (selected) + label. |
| Textarea group | `ds-notes-textarea-group` | Label "Detalle *" + textarea + counter `N/250`. |
| Textarea | `ds-notes-textarea` | `maxlength="250"`, placeholder "Describe qué comportamiento quieres que Simetrik tenga en cuenta". |

**Tags predefinidos** (mismo array Low/Family/High): `'Llega con retraso', 'Volumen variable', 'Archivo dividido', 'Sin datos los festivos', 'Carga manual'`.

## Estados
| Estado | Trigger | Visual |
|---|---|---|
| Colapsado | `notes.open === false` | Solo header con botón `+`. Sin tags ni textarea. |
| Expandido | `notes.open === true` | Header con botón `−` + grid de tags + textarea con counter. |
| Tag seleccionado | `notes.tags.includes(tag)` | Pill con `is-selected`, icono cambia a `minus`. |
| Counter | `notes.detail.length` | `N/250`, alineado a la derecha bajo el textarea. |
| Oculto en detalle | `daySetupHasConfig && !dsSimpleHasNotes()` (o `!dsGroupHasNotes(g)`) | Card no se renderiza. |
| Readonly | `daySetupReadonly === true` | Botón `+` deshabilitado (opacity 0.6), textarea y tags `:disabled`. |

## Comportamiento
| Condición | Visible? | Editable? | Datos que muestra |
|---|---|---|---|
| Low (sin config) | Sí, colapsado | Sí (abrir promueve a Family) | `dsActiveSimple().notes` = `daySetup.shared.notes`. |
| Family (sin config) | Sí, colapsado | Sí | `day.simple.notes`. |
| High (sin config) | Sí, colapsado por grupo | Sí | `g.notes` por grupo. No promueve. |
| Detalle con notas | Sí, contenido visible | No (readonly) | Solo lectura. |
| Detalle sin notas | No (card oculta) | N/A | El card no se renderiza. |

## Data binding
- Low/Family: `dsActiveSimple().notes.{open, tags:[], detail}`.
- High: `g.notes.{open, tags:[], detail}` por grupo.
- Helpers: `dsSimpleHasNotes()` y `dsGroupHasNotes(g)` evalúan si hay contenido y deciden si el card se muestra en modo detalle.
- Condición de render: `x-show="!daySetupHasConfig || dsSimpleHasNotes()"` (Low/Family) o `dsGroupHasNotes(g)` (High).

## Interacciones
| Trigger | Side effects | Próximo estado |
|---|---|---|
| Click botón `+` (cerrado) en Low | `dsPromoteToFamily('edit')` + flip `notes.open = true`. | Family expandido. |
| Click botón `+` (cerrado) en Family/High | Flip `notes.open = true`. | Expandido. |
| Click botón `−` (abierto) | Flip `notes.open = false`. | Colapsado. Los tags y el detalle persisten. |
| Click sobre un tag | Toggle en `notes.tags` (push o splice). | Tag selected o deselected. |
| Escribir en textarea | Actualiza `notes.detail`. Counter se incrementa. | `N/250` visible. |

## Empty states (importante)

El prototipo HTML actual solo tiene algunos empty states (loaders, casos puntuales). Aunque no estén pintados, esta historia debe enumerarlos para que el implementador los considere.

| Escenario | Condición | Copy propuesto | CTA | Implementado en HTML? |
|---|---|---|---|---|
| Sin notas (default) | `notes.open === false && notes.tags.length === 0 && notes.detail === ''` | Header con subtítulo "Selecciona los comportamientos adicionales que son normales en esta fuente." | Botón `+` abre el panel. | ✅ (estado colapsado) |
| Detalle sin notas (readonly) | `daySetupHasConfig && !dsSimpleHasNotes()` | Card oculto completo. | (ninguno) | ✅ (`x-show`) |
| Sin tags predefinidos del catálogo | El array de tags llega vacío del BE | Mensaje "No hay etiquetas disponibles. Describe el comportamiento en el detalle." sustituye al grid de tags. | (ninguno, solo textarea) | ❌ |
| Loading de catálogo de tags | Fetch del catálogo en curso | Skeleton de 5 pills (rect 24×80) en el grid. | (ninguno) | ❌ |
| Error al cargar catálogo | Fetch falló | Mensaje "No pudimos cargar las etiquetas." con icono `alert-triangle`. | Botón "Reintentar" inline. | ❌ |
| Detalle vacío con tags seleccionados | `notes.tags.length > 0 && notes.detail === ''` al guardar | Borde destructive en textarea + helper "Cuéntanos en qué consiste el comportamiento que marcaste." | (ninguno, bloquea Guardar) | ❌ |
| Counter al máximo | `notes.detail.length === 250` | Counter `250/250` en color destructive. | (ninguno, el browser corta) | ❌ |
| Tag obsoleto en config existente | Tag guardado que ya no está en el catálogo actual | Pill con icono `alert-triangle` ámbar + label "Etiqueta no disponible". | Click la quita de `notes.tags`. | ❌ |

## Edge cases
- En High, el card de notas usa fondo `hsl(var(--muted) / 0.3)` para diferenciarse del contenedor del grupo (mismo patrón que los indicadores en High).
- El subtítulo del card en High dice "esta fuente" pero el helper apunta a "este grupo" (`dsGroupHasNotes`). Es intencional: el copy general es de fuente, los datos son por grupo.
- El textarea aplica `maxlength="250"` a nivel HTML: el navegador corta input. El counter es solo informativo.
- Tags y detalle persisten al colapsar (no se reinician); el botón `−` solo oculta el contenido.

## Componentes desyk a usar

> Mapeo del prototipo HTML a los componentes oficiales del design system desyk
> (basado en shadcn/ui). El implementador debe reusar estos componentes en lugar
> de replicar las clases CSS custom del prototipo.

| Elemento del prototipo | Componente desyk | Variants / props | Notas de uso |
|---|---|---|---|
| `.ds-notes` (card colapsable) | `Card` + `Collapsible` + `CollapsibleTrigger` + `CollapsibleContent` | con className condicional `is-open` | Card colapsable opcional |
| `.ds-notes-head` (header con title + ? + subtítulo + botón +) | `CardHeader` con layout custom | — | Header de la card |
| `.ds-help` (ícono ? con tooltip) | `Tooltip` + `TooltipTrigger` + `TooltipContent` | con ícono `HelpCircle` de Lucide | Ayuda contextual |
| `.ds-notes-add` (botón 40x40 con + o −) | `Button` | `variant="ghost" size="icon"` con ícono `Plus` o `Minus` de Lucide | Expand/collapse del card |
| `.ds-notes-tags` (grid de chips) | Layout Tailwind (`flex flex-wrap gap-*`) | — | Grid de tags predefinidos |
| `.ds-notes-tag` (chip de comportamiento) | `ToggleGroupItem` dentro de `ToggleGroup` | `ToggleGroup type="multiple"` con `Badge` interno | Multi-select de tags |
| Ícono dentro del tag (`circle-plus` / `circle-minus`) | Ícono `CirclePlus` / `CircleMinus` de Lucide | — | Indica selección visual del tag |
| `.ds-notes-textarea-group` (label + textarea + counter) | Layout custom (`Label` + `Textarea` + counter) | — | Grupo del textarea con su contador |
| Label "Detalle *" | `Label` | con asterisco indicador required | Label del textarea |
| `.ds-notes-textarea` | `Textarea` | `maxLength={250}` | Textarea para describir el comportamiento |
| `.ds-notes-counter` (counter `N/250`) | Tipografía muted-foreground | — | Contador de caracteres |

**Componentes compuestos (no existen en desyk, hay que componerlos):**
- `AdditionalNotesCard` — card colapsable con header + grid de tags + textarea + counter. Compuesto sobre `Card` + `Collapsible` + `ToggleGroup` + `Textarea`.
- `NotesTagToggleGroup` — multi-select de los 5 tags predefinidos con íconos `CirclePlus`/`CircleMinus`. Compuesto sobre `ToggleGroup` + `Badge` interno por item.
- `CharCounter` — contador `N/250` con estilo destructive cuando llega al máximo. Compuesto sobre tipografía.

**Referencias:**
- Repo desyk: `~/Simetrik/desyk-components` (read-only).
- Lista oficial de componentes shadcn/ui que desyk extiende.

## Implementation notes

- **Helpers Alpine ya existentes** a reusar: `dsActiveSimple()`, `dsSimpleHasNotes()`, `dsGroupHasNotes(g)`, `dsPromoteToFamily('edit')`, `daySetupHasConfig`, `daySetupReadonly`.
- **CSS/clases**: `.ds-notes` (con `is-open`), `.ds-notes-head`, `.ds-notes-add` (con `is-open`), `.ds-notes-tags`, `.ds-notes-tag` (con `is-selected`), `.ds-notes-textarea-group`, `.ds-notes-textarea`, `.ds-notes-counter`.
- **Endpoints BE**: el catálogo de tags predefinidos podría venir de `GET /monitoring/notes-tags` (hoy hardcoded en el HTML).
- **Tokens desyk**: `hsl(var(--primary))` para el botón `+`, `hsl(var(--muted))` para tags no seleccionados, `hsl(var(--primary) / 0.1)` para tags seleccionados, `hsl(var(--destructive))` para counter al máximo.
- **Animation / motion**: 200ms ease-out para expand/collapse del card, transición de icono `+` a `−` con rotación.

## Out of scope

- Edición rich-text en el textarea (solo texto plano).
- Tags personalizados (solo los 5 predefinidos).
- Markdown rendering en lectura.
- Adjuntos o links externos en las notas.
- Sincronización con un sistema de tickets externo (Jira, Linear).

## Criterios de aceptación
1. Card colapsado por default. Botón `+` (40×40) abre el contenido.
2. En Low, abrir el card dispara `dsPromoteToFamily('edit')` antes del flip de `open`.
3. Renderizar exactamente los 5 tags predefinidos en el orden dado.
4. Tag actúa como multi-select. Click toggle en `notes.tags`.
5. Textarea limitado a 250 caracteres con counter `N/250` visible y label "Detalle *".
6. En modo detalle, ocultar el card si `dsSimpleHasNotes()` (o `dsGroupHasNotes(g)` en High) devuelve `false`.

## Dependencies

- **Depende de**: `08-contenedor-comportamiento-dia` (chasis padre).
- **Bloquea a**: ninguna.
- **Relacionado con**: `12-contenedor-grupos-high` (replicación por grupo en High).

## Verification (cómo probarlo)

1. Abrir daysetup nuevo en Low. Validar card "Notas adicionales" colapsado por default.
2. Click botón `+`: en Low debe promover a Family y abrir el card.
3. Validar los 5 tags predefinidos en orden.
4. Click en tags: validar multi-select con toggle.
5. Escribir en textarea: validar counter `N/250` actualiza.
6. Click `−`: validar collapse manteniendo valores.
7. Modo detalle sin notas (`dsSimpleHasNotes() === false`): validar card oculto.
8. Modo detalle con notas: validar visible y readonly.

## References

- **HTML Low/Family**: `../index.html` líneas 21455-21529.
- **HTML High (por grupo)**: líneas 21765-21826.
- **JS**: `dsSimpleHasNotes()` (línea 17408), `dsGroupHasNotes()` (línea 17413).
- **Figma**: (pendiente de link)
- **Docs hermanos**: `[08-contenedor-comportamiento-dia.md](./08-contenedor-comportamiento-dia.md)` (padre), `[12-contenedor-grupos-high.md](./12-contenedor-grupos-high.md)` (replicación High).
