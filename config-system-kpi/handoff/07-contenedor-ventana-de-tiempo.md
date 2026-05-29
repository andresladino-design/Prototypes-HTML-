---
epic: MONITOR_INGESTA
issue_type: Feature
priority: P1
estimate: S
labels: [ux, frontend, monitoring, modal-config, daysetup, ai]
depends_on: [05-modal-configuracion]
blocks: []
component_areas: [modal-config, daysetup, time-window]
---

# 07 · Contenedor Ventana de tiempo

> Card transversal al modal de configuración del monitor. Define la franja horaria esperada para la llegada de la fuente. Vive arriba en el modal (línea HTML ~21097) y se mantiene igual en Low, Family y High.

## Propósito
- Permite acordar con la fuente dos horas: cuándo se espera que llegue y a partir de qué hora considerar que llegó tarde.
- Es lo primero que el usuario configura. Aparece antes del card de comportamiento porque la ventana es global a la fuente, no depende del día de la semana ni de los grupos.
- En el journey aparece siempre: al crear monitor (estado vacío con chips de agente) y al revisar uno existente (lectura, sin chips).

## Anatomía
| Subcomponente | Clase | Función |
|---|---|---|
| Header | `ds-card-head` | Título "Ventana de tiempo" + icono `?` con tooltip + subtítulo descriptivo. |
| Grid de inputs | `config-grid cols-2` | Dos columnas iguales con los dos `time` inputs. |
| Input 1 | `config-input` (`type="time"`) | Label "Llega a las". Bind a `daySetup.window.arrivesAt`. |
| Input 2 | `config-input` (`type="time"`) | Label "Avisar si pasa de las". Bind a `daySetup.window.warnIfPast`. |
| Chip agente | `ds-ai-chip` | Estado vacío: "Autocompletado por el agente". Editado: "Sugerencia: HH:MM" clickeable que restaura el valor sugerido. |
| Footer colgante | `ds-card-footer` | "Configurar ventana por día" + chip `Próx.`. Adelanto de feature, no es interactivo. |

## Estados
| Estado | Trigger | Visual |
|---|---|---|
| Default sin config | `!daySetupHasConfig` | Chips violetas visibles. Inputs editables con valores sugeridos por el agente. |
| Valor editado | `arrivesAt !== _sArrivesAt` | Chip cambia a `Sugerencia: HH:MM` y se vuelve clickeable (`is-suggestion`). |
| Detalle existente | `daySetupHasConfig === true` | Inputs visibles sin chips. Si además `daySetupReadonly`, inputs deshabilitados. |
| Tooltip activo | hover/focus en icono `?` | Tooltip explica el comportamiento de la ventana y qué dispara la anomalía. |

## Comportamiento
| Condición | Visible? | Editable? | Datos que muestra |
|---|---|---|---|
| `monitorMode === 'igual'` (Low) | Sí | Sí | Hora compartida por todos los días. |
| `monitorMode === 'por-dia'` (Family) | Sí | Sí | Sigue siendo global a la fuente. Aún no se configura por día (footer indica `Próx.`). |
| `useGroupsAll === true` (High) | Sí | Sí | Igual que Family, la ventana es de fuente. |
| `daySetupReadonly === true` | Sí | No | Inputs `:disabled`, chips ocultos. |

## Data binding
- `daySetup.window.arrivesAt` (string `HH:MM`) y `daySetup.window.warnIfPast`.
- Valores sugeridos read-only en `_sArrivesAt` y `_sWarnIfPast` (la sugerencia viene del agente al abrir el modal).
- El chip usa `dsChipText(current, suggested)` que devuelve `Autocompletado por el agente` cuando coinciden o `Sugerencia: HH:MM` cuando difieren.

## Interacciones
| Trigger | Side effects | Próximo estado |
|---|---|---|
| Cambiar hora en input | Actualiza `daySetup.window.*`. **No** promueve a Family (no es config por día). | Chip cambia a `Sugerencia: ...` si difiere del seed. |
| Click chip `Sugerencia: HH:MM` | Restaura el valor sugerido en el input. | Chip vuelve a `Autocompletado por el agente`. |
| Hover o focus en `?` | Muestra tooltip. | Sin cambio de estado. |
| Click en footer `Configurar ventana por día` | No-op (placeholder de roadmap). | Sin cambio. |

## Empty states (importante)

El prototipo HTML actual solo tiene algunos empty states (loaders, casos puntuales). Aunque no estén pintados, esta historia debe enumerarlos para que el implementador los considere.

| Escenario | Condición | Copy propuesto | CTA | Implementado en HTML? |
|---|---|---|---|---|
| Sin datos del BE | El endpoint no devuelve `_sArrivesAt` ni `_sWarnIfPast` | Inputs vacíos con placeholder `--:--`. Chip muestra "Sin sugerencia disponible" en gris muted. | (ninguno, el usuario tipea) | ❌ |
| Agente no autocompletó | `daySetup.window.arrivesAt === null` y existe `_sArrivesAt` | Chip "Pulsa para autocompletar" clickeable que llena el input. | Click llena el input. | ❌ |
| Loading de sugerencias | Fetch del agente en curso al abrir el modal | Skeleton 32px alto en cada input + chip con shimmer. | (ninguno) | ❌ |
| Error de red | Fetch de sugerencias falló | Chip "No pudimos cargar la sugerencia" con icono `alert-triangle` ámbar. | Botón "Reintentar" en el chip. | ❌ |
| Valor inválido | `warnIfPast <= arrivesAt` o formato malformado | Borde input destructive + helper text bajo el input "La hora límite debe ser posterior a la de llegada." | (ninguno, bloquea Guardar) | ❌ |
| Detalle sin ventana configurada (legacy) | Fuente migrada de BADS sin `window` | Mensaje "Sin ventana de tiempo configurada" en el card. | Botón "Configurar ahora" abre el card en edición. | ❌ |

## Edge cases
- Si `warnIfPast` queda antes que `arrivesAt`, el UI no bloquea; la validación queda en BE.
- En modo readonly, los chips no se renderizan aunque la fuente nunca haya sido configurada antes (la flag `daySetupReadonly` dominante).
- El footer "Próx." es solo informativo: no abre nada y no rompe la altura de la card (`has-hanging-footer`).

## Componentes desyk a usar

> Mapeo del prototipo HTML a los componentes oficiales del design system desyk
> (basado en shadcn/ui). El implementador debe reusar estos componentes en lugar
> de replicar las clases CSS custom del prototipo.

| Elemento del prototipo | Componente desyk | Variants / props | Notas de uso |
|---|---|---|---|
| `.ds-card.has-hanging-footer` (contenedor de la ventana) | `Card` + `CardHeader` + `CardContent` + `CardFooter` | `CardFooter` con className para footer colgante | Card transversal a los 3 perfiles |
| `.ds-card-head` (título + ícono ? + subtítulo) | `CardHeader` + `CardTitle` + `CardDescription` | — | Header de la card con tooltip integrado |
| `.ds-help` (ícono ? con tooltip) | `Tooltip` + `TooltipTrigger` + `TooltipContent` | con ícono `HelpCircle` de Lucide | Accesible por teclado (`tabindex="0"`) |
| `.config-grid.cols-2` (grid de dos columnas) | Layout Tailwind (`grid grid-cols-2 gap-*`) | — | No es componente desyk |
| `.config-input` (`type="time"`) (inputs de hora) | `Input` | `type="time"` | Dos inputs: "Llega a las" y "Avisar si pasa de las" |
| Label por encima del input | `Label` | — | Labels "Llega a las" / "Avisar si pasa de las" |
| `.ds-ai-chip` (chip violeta de sugerencia AI) | `Badge` | `variant="secondary"` con override violeta AI; clickable cuando `is-suggestion` | "Autocompletado por el agente" o "Sugerencia: HH:MM" |
| `.ds-card-footer` (footer "Configurar ventana por día · Próx.") | `CardFooter` + `Badge` | `Badge variant="outline"` con texto "Próx." | Footer colgante informativo (no interactivo) |

**Componentes compuestos (no existen en desyk, hay que componerlos):**
- `AiSuggestionChip` — chip violeta clickable que muestra "Autocompletado por el agente" o "Sugerencia: HH:MM" y restaura el valor sugerido al clickear. Wrapper sobre `Badge` con lógica de `dsChipText()`.
- `TimeWindowCard` — card de Ventana de tiempo con dos `Input type="time"` + chips AI + footer colgante. Compuesto sobre `Card`.

**Referencias:**
- Repo desyk: `~/Simetrik/desyk-components` (read-only).
- Lista oficial de componentes shadcn/ui que desyk extiende.

## Implementation notes

- **Helpers Alpine ya existentes** a reusar: `daySetup.window`, `dsChipText(current, suggested)`, `daySetupHasConfig`, `daySetupReadonly`.
- **CSS/clases**: `.ds-card.has-hanging-footer`, `.ds-card-head`, `.config-grid.cols-2`, `.config-input`, `.ds-ai-chip`, `.ds-card-footer`, `.ds-help`.
- **Endpoints BE**: `GET /sources/{id}/analysis` debe devolver `_sArrivesAt` y `_sWarnIfPast` derivados del histórico.
- **Tokens desyk**: `hsl(var(--ai-purple))` para el chip violeta, `hsl(var(--destructive))` para validación, `hsl(var(--muted))` para estado "Sin sugerencia".
- **Animation / motion**: 200ms ease-out al expandir tooltip del icono `?`.

## Out of scope

- Configuración de ventana por día (placeholder `Próx.` en el footer, no es funcional).
- Validación cliente-side de `warnIfPast > arrivesAt` (delegada a BE).
- Soporte de timezones (asumir hora local del usuario).
- Ventanas multi-tramo (ej. dos llegadas por día).

## Criterios de aceptación
1. Renderizar dos inputs `type="time"` en grid `cols-2` con labels exactos "Llega a las" y "Avisar si pasa de las".
2. Mostrar chip "Autocompletado por el agente" cuando el valor coincida con la sugerencia y "Sugerencia: HH:MM" cuando difiera.
3. Click en chip de sugerencia restaura el valor sugerido del input correspondiente.
4. Ocultar chips cuando `daySetupHasConfig` o cuando `daySetupReadonly`.
5. Mantener el footer colgante con copy "Configurar ventana por día · Próx." sin handler asociado.
6. Tooltip en icono `?` accesible vía teclado (`tabindex="0"`).

## Dependencies

- **Depende de**: `05-modal-configuracion` (modal padre).
- **Bloquea a**: ninguna.
- **Relacionado con**: `08-contenedor-comportamiento-dia`, `13-journey-low-family-high`.

## Verification (cómo probarlo)

1. Abrir `index.html`, abrir daysetup de una fuente nueva.
2. Validar dos inputs `time` en grid de dos columnas con labels exactos.
3. Validar chips violetas "Autocompletado por el agente" con valores precargados.
4. Editar `arrivesAt`: validar que el chip cambia a "Sugerencia: HH:MM".
5. Click en el chip: validar restauración del valor sugerido.
6. Abrir modal sobre fuente monitoreada (readonly): validar inputs disabled y chips ocultos.
7. Hover en icono `?`: validar tooltip con copy del `data-tip`.

## References

- **HTML**: `../index.html` líneas 21096-21135 (`<section class="ds-card has-hanging-footer">` con title "Ventana de tiempo").
- **Figma**: (pendiente de link)
- **Docs hermanos**: `[05-modal-configuracion.md](./05-modal-configuracion.md)` (shell del modal), `[13-journey-low-family-high.md](./13-journey-low-family-high.md)` (por qué es transversal).
