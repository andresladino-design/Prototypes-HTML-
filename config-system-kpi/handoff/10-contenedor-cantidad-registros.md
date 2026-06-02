---
epic: MONITOR_INGESTA
issue_type: Feature
priority: P0
estimate: M
labels: [ux, frontend, monitoring, modal-config, daysetup, indicator, ai]
depends_on: [08-contenedor-comportamiento-dia]
blocks: []
component_areas: [modal-config, daysetup, indicator]
---

# 10 · Contenedor Cantidad de registros

> Card indicador hermana de "Volumen de archivos". Define el rango esperado de filas (registros) por ejecución. Vive debajo del indicador de volumen en el slot Low/Family (HTML ~21402) y replicado en cada grupo en High (HTML ~21713).

## Propósito
- Permite distinguir un archivo que llega vacío o saturado de uno con volumen normal. Una vez fuera del rango (mínimo/máximo), se dispara una anomalía.
- Aparece junto al indicador de volumen porque, juntos, dan la lectura más útil del estado de la carga.
- Tiene exactamente la misma mecánica que `09-contenedor-volumen-archivos.md`: cambia el binding y el copy.

## Anatomía
| Subcomponente | Clase | Función |
|---|---|---|
| Header | `ds-indicator-head` | Title "Cantidad de registros" + icono `?` + subtítulo + switch on/off. |
| Switch | `ds-switch` | Encendido/apagado del indicador. |
| Grid | `config-grid cols-2 ds-indicator-grid` | Dos columnas con `min` y `max`. |
| Input min | `config-input` + `ds-input-with-suffix` | Label "Al menos", input numérico, badge sufijo "Registros". |
| Input max | `config-input` + `ds-input-with-suffix` | Label "No más de", input numérico, badge sufijo "Registros". |
| Chip agente | `ds-ai-chip` | "Autocompletado por el agente" o "Sugerencia: N". |
| Hint OFF | `ds-indicator-off-hint` | Copy "No te avisaremos por la cantidad de registros de este [día/grupo]". |

## Estados
| Estado | Trigger | Visual |
|---|---|---|
| ON con sugerencia | `active === true && min/max === seed` | Inputs editables con chips "Autocompletado por el agente". |
| ON editado | `active === true && min !== _sMin` | Chips `Sugerencia: N` clickeables. |
| OFF | `active === false` | Card `is-off`, grid oculto, hint visible. |
| Readonly | `daySetupReadonly === true` | Inputs y switch deshabilitados, chips ocultos. |

## Comportamiento
| Condición | Visible? | Editable? | Datos que muestra |
|---|---|---|---|
| Low | Sí | Sí | `dsActiveSimple().rowCount` = `daySetup.shared.rowCount`. Editar dispara `dsPromoteToFamily('edit')`. |
| Family | Sí | Sí | `dsActiveSimple()` = `day.simple.rowCount` del día activo. |
| High | Sí (dentro de cada grupo) | Sí | `g.rowCount` por grupo. No promueve. |
| Día con `monitorEnabled === false` | No | N/A | Indicador oculto cuando el día está apagado. |

## Data binding
- Low/Family: `dsActiveSimple().rowCount.{active, min, max, _sMin, _sMax}`.
- High: `g.rowCount.{active, min, max, _sMin, _sMax}` por grupo.
- Helper `dsChipText(current, suggested)` produce el texto.

## Interacciones
| Trigger | Side effects | Próximo estado |
|---|---|---|
| Click switch en Low | `dsPromoteToFamily('edit')` + flip `active`. | Family con indicador on/off. |
| Click switch en Family/High | Flip `active` directo. | Indicador on/off. |
| `@change` en input min/max en Low | `dsPromoteToFamily('edit')`. | Family. |
| `@change` en input en Family/High | Actualiza valor. | Chip cambia a `Sugerencia: N` si difiere del seed. |
| Click chip `Sugerencia: N` | Restaura el valor seed. | Chip vuelve a "Autocompletado por el agente". |

## Empty states (importante)

El prototipo HTML actual solo tiene algunos empty states (loaders, casos puntuales). Aunque no estén pintados, esta historia debe enumerarlos para que el implementador los considere.

| Escenario | Condición | Copy propuesto | CTA | Implementado en HTML? |
|---|---|---|---|---|
| Indicador apagado | `rowCount.active === false` | Hint "No te avisaremos por la cantidad de registros de este [día/grupo]." | Switch toggle ON. | ✅ (`ds-indicator-off-hint`) |
| Sugerencia no disponible | `_sMin === null && _sMax === null` | Chip "Sin sugerencia disponible" en gris muted, no clickeable. | (ninguno) | ❌ |
| Loading de sugerencias | Fetch del agente en curso | Skeleton 32px en cada input + chip con shimmer. | (ninguno) | ❌ |
| Error de red al cargar seed | Fetch falló | Chip "No pudimos cargar la sugerencia" con icono `alert-triangle` ámbar. | Botón "Reintentar" inline. | ❌ |
| Valor cero | `min === 0` | Helper text "0 registros significa que aceptamos archivos vacíos este día." | (ninguno, es válido pero raro) | ❌ |
| Rango inválido | `min > max` | Borde destructive en ambos inputs + helper "El mínimo debe ser menor o igual al máximo." | (ninguno, bloquea Guardar) | ❌ |
| Sin histórico de registros (High) | El grupo no tiene baseline de `rowCount` | Chip "Sin histórico para este grupo" + botón "Configura manualmente". | (manual) | ❌ |
| Fuente no entrega registros (archivos binarios) | El BE indica `supportsRowCount: false` | Indicador deshabilitado completo con leyenda "Esta fuente no expone conteo de registros." | (ninguno, indicador oculto) | ❌ |

## Edge cases
- Mismo comportamiento que volumen frente a `min > max`: el UI no bloquea, BE valida.
- Cuando el indicador está OFF, el hint usa "este día" en Low/Family y "este grupo" en High (mismo patrón que volumen).
- Inputs admiten enteros grandes (no hay límite UI). Spinner del navegador disponible.

## Componentes desyk a usar

> Mapeo del prototipo HTML a los componentes oficiales del design system desyk
> (basado en shadcn/ui). Este indicador es gemelo del doc 09: usa los mismos
> componentes con bindings y copy distintos.

| Elemento del prototipo | Componente desyk | Variants / props | Notas de uso |
|---|---|---|---|
| `.ds-indicator` (card del indicador) | `Card` + `CardHeader` + `CardContent` | con className condicional `is-off` | Card del indicador Cantidad de registros |
| `.ds-indicator-head` (header con title + ? + subtítulo + switch) | `CardHeader` con layout custom | — | Header del indicador |
| `.ds-help` (ícono ? con tooltip) | `Tooltip` + `TooltipTrigger` + `TooltipContent` | con ícono `HelpCircle` de Lucide | Explica qué dispara una anomalía |
| `.ds-switch` (switch on/off del indicador) | `Switch` | `checked` + `onCheckedChange` | Activa o desactiva el indicador |
| `.config-grid.cols-2.ds-indicator-grid` (grid min/max) | Layout Tailwind (`grid grid-cols-2 gap-*`) | — | No es componente desyk |
| `.config-input` (input numérico min/max) | `Input` | `type="number"` con `min="0"` | Inputs de mínimo y máximo |
| `.ds-input-with-suffix` (wrapper con badge sufijo "Registros") | Componente custom (compuesto, ver doc 09) | — | Wrapper que combina `Input` + `Badge` sufijo |
| Badge sufijo "Registros" | `Badge` | `variant="secondary"` | Píldora con sufijo de unidad |
| Label por encima del input | `Label` | — | "Al menos" / "No más de" |
| `.ds-ai-chip` (chip violeta de sugerencia AI) | `Badge` | `variant="secondary"` con override violeta AI; clickable cuando `is-suggestion` | "Autocompletado por el agente" o "Sugerencia: N" |
| `.ds-indicator-off-hint` (hint cuando indicador OFF) | Tipografía muted-foreground | — | Copy contextual "No te avisaremos por la cantidad de registros..." |

**Componentes compuestos (no existen en desyk, hay que componerlos):**
- `IndicatorCard` — mismo componente reusado del doc 09 (genérico para Volumen y Cantidad de registros).
- `NumberInputWithSuffix` — mismo componente reusado del doc 09 (sufijo "Registros" en este caso).
- `AiSuggestionChip` — chip violeta clickable (ver doc 07).

**Referencias:**
- Repo desyk: `~/Simetrik/desyk-components` (read-only).
- Lista oficial de componentes shadcn/ui que desyk extiende.

## Implementation notes

- **Helpers Alpine ya existentes** a reusar: `dsActiveSimple()`, `dsActiveDay()`, `dsPromoteToFamily('edit')`, `dsChipText(current, suggested)`, `daySetupHasConfig`, `daySetupReadonly`.
- **CSS/clases**: idénticas a `09-contenedor-volumen-archivos.md` (`.ds-indicator`, `.ds-indicator-head`, `.ds-switch`, `.config-grid.cols-2.ds-indicator-grid`, `.config-input`, `.ds-input-with-suffix`, `.ds-ai-chip`, `.ds-indicator-off-hint`).
- **Endpoints BE**: `GET /sources/{id}/analysis` devuelve `_sMin` y `_sMax` de `rowCount` por día/grupo.
- **Tokens desyk**: idénticos a Volumen (`hsl(var(--ai-purple))`, `hsl(var(--destructive))`, `hsl(var(--muted) / 0.3)`).
- **Animation / motion**: idénticas a Volumen.

## Out of scope

- Validación cliente de `min > max` (delegada a BE).
- Indicador adicional de tamaño en bytes (futura iteración).
- Comparación contra histórico in-line (sería una variante del modal de análisis).
- Soporte de fuentes binarias sin row count (caso edge en empty states).

## Criterios de aceptación
1. Title "Cantidad de registros" + tooltip describiendo rango y anomalía.
2. Labels "Al menos" y "No más de" con badge sufijo "Registros".
3. Switch on/off opera sobre `rowCount.active`. En Low, dispara `dsPromoteToFamily('edit')` antes del flip.
4. Chip violeta visible solo cuando `!daySetupHasConfig`. Texto dinámico según seed.
5. Click en chip `Sugerencia: N` restaura el input al valor sugerido.
6. Hint OFF cambia el copy según contexto (día vs grupo).

## Dependencies

- **Depende de**: `08-contenedor-comportamiento-dia` (chasis padre).
- **Bloquea a**: ninguna.
- **Relacionado con**: `09-contenedor-volumen-archivos` (gemelo), `12-contenedor-grupos-high` (replicación en High).

## Verification (cómo probarlo)

1. Abrir daysetup nuevo en Low. Validar card "Cantidad de registros" debajo de "Volumen de archivos".
2. Editar `min`: validar promoción a Family.
3. Click chip `Sugerencia: N`: validar restauración.
4. Toggle OFF: validar hint contextual ("este día" vs "este grupo").
5. En High, validar replicación por grupo con fondo `muted/0.3`.
6. Modo readonly: inputs disabled, switch opacity 0.6.

## References

- **HTML** (por selector, los números de línea cambian): indicador de cantidad de registros (`.ds-indicator`, hermano del de volumen) dentro del modal `.resource-config-panel`. En Low/Family vive en el slot compartido; en High se repite por cada `.ds-group`.
- **Figma**: (pendiente de link)
- **Docs hermanos**: `[09-contenedor-volumen-archivos.md](./09-contenedor-volumen-archivos.md)` (gemelo), `[08-contenedor-comportamiento-dia.md](./08-contenedor-comportamiento-dia.md)` (padre), `[12-contenedor-grupos-high.md](./12-contenedor-grupos-high.md)` (modo High).
