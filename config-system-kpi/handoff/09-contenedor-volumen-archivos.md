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

# 09 · Contenedor Volumen de archivos

> Card indicador que define el rango esperado de archivos por ejecución (mínimo y máximo). Vive dentro del card de comportamiento, en el slot Low/Family (HTML ~21350) y replicado dentro de cada grupo en High (HTML ~21661).

## Propósito
- Acota cuántos archivos espera Simetrik en una ejecución del día. Si la cuenta queda fuera del rango, se dispara una anomalía.
- Es el primer indicador que el usuario ve después del toggle del día. Es la entrada más simple al modelo de KPIs.
- Aparece en Low (`shared`), Family (`day.simple`) y High (por cada `group`).

## Anatomía
| Subcomponente | Clase | Función |
|---|---|---|
| Header | `ds-indicator-head` | Title "Volumen de archivos" + icono `?` + subtítulo + switch on/off a la derecha. |
| Switch | `ds-switch` | Encendido/apagado del indicador. |
| Grid | `config-grid cols-2 ds-indicator-grid` | Dos columnas con los inputs `min` y `max`. |
| Input min | `config-input` + `ds-input-with-suffix` | Label "Como mínimo", input numérico, badge sufijo "Archivos". |
| Input max | `config-input` + `ds-input-with-suffix` | Label "Como máximo", input numérico, badge sufijo "Archivos". |
| Chip agente | `ds-ai-chip` | "Autocompletado por el agente" o "Sugerencia: N" si difiere. |
| Hint OFF | `ds-indicator-off-hint` | Copy "No te avisaremos por el volumen de archivos de este [día/grupo]". |

## Estados
| Estado | Trigger | Visual |
|---|---|---|
| ON con sugerencia | `active === true && min/max === seed` | Inputs editables, chips violetas "Autocompletado por el agente". |
| ON editado | `active === true && min !== _sMin` | Chips cambian a `Sugerencia: N` clickeables. |
| OFF | `active === false` | Card `is-off` (opacidad 0.55), grid oculto, hint visible debajo del header. |
| Readonly | `daySetupReadonly === true` | Switch e inputs deshabilitados, chips ocultos. |

## Comportamiento
| Condición | Visible? | Editable? | Datos que muestra |
|---|---|---|---|
| Low (`monitorMode === 'igual'`) | Sí | Sí | `dsActiveSimple().fileCount` = `daySetup.shared.fileCount`. Editar dispara `dsPromoteToFamily('edit')`. |
| Family (`por-dia`, `!useGroupsAll`) | Sí | Sí | `dsActiveSimple()` = `day.simple.fileCount` del día activo. |
| High (`useGroupsAll === true`) | Sí (dentro de cada grupo) | Sí | `g.fileCount` por grupo. No promueve nada al editar (ya es modo High). |
| `dsActiveDay().monitorEnabled === false` | No | N/A | Toggle del día apagado oculta este indicador. |

## Data binding
- Low/Family: `dsActiveSimple().fileCount.{active, min, max, _sMin, _sMax}`.
- High: `g.fileCount.{active, min, max, _sMin, _sMax}` para cada grupo iterado.
- Valores sugeridos `_sMin` y `_sMax` son la propuesta del agente; no se editan.
- Helper `dsChipText(current, suggested)` devuelve el texto del chip.

## Interacciones
| Trigger | Side effects | Próximo estado |
|---|---|---|
| Click switch en Low | `dsPromoteToFamily('edit')` + flip `active`. | Family con indicador en su nuevo estado. |
| Click switch en Family/High | Flip `active` directo. | Indicador ON u OFF. |
| `@change` en input min/max en Low | `dsPromoteToFamily('edit')`. | Family con banner de feedback. |
| `@change` en input min/max en Family/High | Actualiza el valor. | Chip cambia a `Sugerencia: N` si difiere. |
| Click chip `Sugerencia: N` | Restaura el valor seed en el input. | Chip vuelve a "Autocompletado por el agente". |

## Empty states (importante)

El prototipo HTML actual solo tiene algunos empty states (loaders, casos puntuales). Aunque no estén pintados, esta historia debe enumerarlos para que el implementador los considere.

| Escenario | Condición | Copy propuesto | CTA | Implementado en HTML? |
|---|---|---|---|---|
| Indicador apagado | `fileCount.active === false` | Hint "No te avisaremos por el volumen de archivos de este [día/grupo]." | Switch toggle ON. | ✅ (`ds-indicator-off-hint`) |
| Sugerencia no disponible | `_sMin === null && _sMax === null` | Chip "Sin sugerencia disponible" en gris muted, no clickeable. | (ninguno, el usuario tipea) | ❌ |
| Loading de sugerencias | Fetch del agente en curso | Skeleton 32px en cada input + chip con shimmer. | (ninguno) | ❌ |
| Error de red al cargar seed | Fetch falló | Chip "No pudimos cargar la sugerencia" con icono `alert-triangle` ámbar. | Botón "Reintentar" inline en el chip. | ❌ |
| Valor cero como mínimo | `min === 0 && max > 0` | Helper text bajo el input "0 archivos significa que aceptamos no recibir nada este día." | (ninguno, es válido) | ❌ |
| Rango inválido | `min > max` | Borde destructive en ambos inputs + helper "El mínimo debe ser menor o igual al máximo." | (ninguno, bloquea Guardar) | ❌ |
| Valores negativos | `min < 0` (browser permite con teclado en algunos casos) | Borde destructive + helper "Los valores deben ser positivos." | (ninguno, bloquea Guardar) | ❌ |
| Indicador sin histórico (High) | `g.filesFound === 0` y no hay seed | Card con badge "Sin histórico" ámbar y chip "Configura manualmente". | (manual) | ❌ |

## Edge cases
- Si `min > max`, el UI no bloquea. Validación queda en BE.
- Inputs con `min="0"`. Negativos quedan fuera del rango aceptado por el browser.
- En High, el indicador hereda el background `hsl(var(--muted) / 0.3)` para diferenciarse del contenedor de grupo.

## Componentes desyk a usar

> Mapeo del prototipo HTML a los componentes oficiales del design system desyk
> (basado en shadcn/ui). El implementador debe reusar estos componentes en lugar
> de replicar las clases CSS custom del prototipo.

| Elemento del prototipo | Componente desyk | Variants / props | Notas de uso |
|---|---|---|---|
| `.ds-indicator` (card del indicador) | `Card` + `CardHeader` + `CardContent` | con className condicional `is-off` para opacity 0.55 | Card del indicador Volumen |
| `.ds-indicator-head` (header con title + ? + subtítulo + switch) | `CardHeader` con layout custom | — | Header del indicador |
| `.ds-help` (ícono ? con tooltip) | `Tooltip` + `TooltipTrigger` + `TooltipContent` | con ícono `HelpCircle` de Lucide | Explica qué dispara una anomalía |
| `.ds-switch` (switch on/off del indicador) | `Switch` | `checked` + `onCheckedChange` | Activa o desactiva el indicador completo |
| `.config-grid.cols-2.ds-indicator-grid` (grid min/max) | Layout Tailwind (`grid grid-cols-2 gap-*`) | — | No es componente desyk |
| `.config-input` (input numérico min/max) | `Input` | `type="number"` con `min="0"` | Inputs de mínimo y máximo |
| `.ds-input-with-suffix` (wrapper con badge sufijo "Archivos") | Componente custom (compuesto) | — | Wrapper que combina `Input` + `Badge` sufijo |
| Badge sufijo "Archivos" | `Badge` | `variant="secondary"` | Píldora con el sufijo de unidad |
| Label por encima del input | `Label` | — | "Como mínimo" / "Como máximo" |
| `.ds-ai-chip` (chip violeta de sugerencia AI) | `Badge` | `variant="secondary"` con override violeta AI; clickable cuando `is-suggestion` | "Autocompletado por el agente" o "Sugerencia: N" |
| `.ds-indicator-off-hint` (hint cuando indicador OFF) | Tipografía muted-foreground | — | Copy contextual "No te avisaremos por el volumen..." |

**Componentes compuestos (no existen en desyk, hay que componerlos):**
- `IndicatorCard` — card del indicador con switch on/off + grid min/max + chips AI + hint OFF. Reusable para Volumen y Cantidad de registros. Compuesto sobre `Card` + `Switch` + `Input`.
- `NumberInputWithSuffix` — wrapper que combina `Input type="number"` + `Badge` sufijo a la derecha ("Archivos", "Registros"). Compuesto.
- `AiSuggestionChip` — chip violeta clickable (ver doc 07).

**Referencias:**
- Repo desyk: `~/Simetrik/desyk-components` (read-only).
- Lista oficial de componentes shadcn/ui que desyk extiende.

## Implementation notes

- **Helpers Alpine ya existentes** a reusar: `dsActiveSimple()`, `dsActiveDay()`, `dsPromoteToFamily('edit')`, `dsChipText(current, suggested)`, `daySetupHasConfig`, `daySetupReadonly`.
- **CSS/clases**: `.ds-indicator` (con `is-off`), `.ds-indicator-head`, `.ds-switch`, `.config-grid.cols-2.ds-indicator-grid`, `.config-input`, `.ds-input-with-suffix`, `.ds-ai-chip` (con `is-suggestion`), `.ds-indicator-off-hint`.
- **Endpoints BE**: `GET /sources/{id}/analysis` devuelve `_sMin` y `_sMax` por día/grupo.
- **Tokens desyk**: `hsl(var(--ai-purple))` para chip violeta, `hsl(var(--destructive))` para validación de rango, `hsl(var(--muted) / 0.3)` para fondo en High.
- **Animation / motion**: 200ms ease-out para transición ON/OFF del switch.

## Out of scope

- Validación cliente de `min > max` (delegada a BE).
- Soporte de unidades distintas a "Archivos" (siempre se usa este sufijo).
- Promedio o moving window (solo min/max estático).
- Histograma visual del rango (futura iteración).

## Criterios de aceptación
1. Title "Volumen de archivos" + tooltip explicando que define rango esperado y dispara anomalía.
2. Labels exactos "Como mínimo" y "Como máximo" con badge sufijo "Archivos".
3. Switch on/off opera sobre `fileCount.active`. En Low, promueve a Family antes de aplicar el cambio.
4. Chip violeta visible solo cuando `!daySetupHasConfig`. Texto dinámico según diferencia con seed.
5. Click en chip `Sugerencia: N` restaura el input al valor sugerido.
6. Cuando `active === false`, ocultar el grid y mostrar el hint OFF con copy contextual por día o por grupo.

## Dependencies

- **Depende de**: `08-contenedor-comportamiento-dia` (chasis padre).
- **Bloquea a**: ninguna.
- **Relacionado con**: `10-contenedor-cantidad-registros` (gemelo), `12-contenedor-grupos-high` (replicación en High).

## Verification (cómo probarlo)

1. Abrir daysetup de fuente nueva en Low. Validar Volumen con chips violetas en min/max.
2. Editar `min`: validar promoción a Family con banner feedback.
3. Click chip `Sugerencia: N`: validar restauración del valor.
4. Toggle switch OFF: validar hint visible y grid oculto.
5. En High (activar grupos), validar Volumen dentro de cada `ds-group` con fondo `muted/0.3`.
6. Modo readonly: inputs disabled, switch opacity 0.6, chips ocultos.

## References

- **HTML Low/Family**: `../index.html` líneas 21349-21399.
- **HTML High (por grupo)**: líneas 21661-21711.
- **Figma**: (pendiente de link)
- **Docs hermanos**: `[08-contenedor-comportamiento-dia.md](./08-contenedor-comportamiento-dia.md)` (padre), `[10-contenedor-cantidad-registros.md](./10-contenedor-cantidad-registros.md)` (hermano), `[12-contenedor-grupos-high.md](./12-contenedor-grupos-high.md)` (modo High).
