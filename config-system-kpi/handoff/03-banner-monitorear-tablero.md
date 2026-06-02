---
epic: MONITOR_INGESTA
issue_type: Feature
priority: P1
estimate: S
labels: [ux, frontend, monitoring, bulk]
depends_on: [02-vista-monitoreo, 04-cards-monitores-ingesta]
blocks: [06-activacion-masiva]
component_areas: [monitoring-view, bulk-modal]
---

# 03 · Activación masiva de fuentes (acción del tab Ingesta)

> Acción bulk de la etapa Ingesta. Vive junto al buscador en el **extremo derecho de la barra de tabs** (`.tm-tabs-actions`), no dentro del contenido del tab. Aparece cuando todavía hay fuentes sin configurar. Permite activar el monitoreo de todas las fuentes pendientes en una sola operación.

## Resumen

- **Quién lo ve**: usuario en la vista `tmTab === 'ingesta'` mientras haya fuentes con `status === 'empty'`.
- **Cuándo**: durante la configuración del monitoreo del tablero, antes de tenerlo todo cubierto.
- **Qué decisión habilita**: abrir el modal bulk (`openBulkActivate()`) para activar varias fuentes con un solo flujo.
- **Por qué existe**: configurar el monitoreo de una fuente puede ser demorado. La promesa del producto es "tu tablero está monitoreado de extremo a extremo" y eso requiere reducir la fricción de N configuraciones a 1 acción. El botón vive en `.tm-tabs-actions` (junto al buscador "Buscar fuente", al extremo derecho de la barra de tabs) para estar siempre visible cuando hay pendientes en la etapa Ingesta.

## Anatomía

| Componente | Clase / selector | Función |
|---|---|---|
| Grupo de acciones | `.tm-tabs-actions` (extremo derecho de `.tm-tabs-bar`), `x-show="tmTab === 'ingesta'"` para este caso | Contiene el buscador + el botón bulk de la etapa Ingesta |
| Buscador | `.tm-search.tm-tab-header-search` con `input.tm-search-input` x-model="resourceSearch" | Filtro por nombre de fuente |
| Botón bulk | `.bulk-list-section-action` con `x-show="tmTab === 'ingesta' && resources.filter(r => r.status === 'empty').length > 0"` | Acción primaria para activar en bloque |
| Icono | SVG inline (apilado de tres capas) | Visual del botón |
| Label dinámico | Dos `span` con `x-show` por cantidad | "Activar 1 a la vez" o "Activar las N a la vez" |

> ⚠️ **Cambio vs versión anterior**: ya NO hay agrupación "Monitoreado / Sin monitoreo" (`.bulk-list-section-header`) en la lista. Las fuentes se muestran en un **grid único** y el estado lo refleja el badge de cada card (ver `04`). El CSS de sección existe pero no se usa.

**Problema que resuelve mover la acción a `.tm-tabs-actions`:** tener el buscador y el botón "Activar las N" dentro del contenido del tab empujaba la lista hacia abajo y restaba jerarquía a la acción. Anclados al extremo derecho de la barra de tabs quedan siempre visibles y a la mano, sin robar alto a la lista de fuentes.

## Estados

| Estado | Condición | Visual |
|---|---|---|
| Oculto | `resources.filter(r => r.status === 'empty').length === 0` | Botón no se renderiza |
| Singular | exactamente 1 fuente sin configurar | Label "Activar 1 a la vez" |
| Plural | 2 o más fuentes sin configurar | Label "Activar las N a la vez" (con `<span x-text>` para el número) |
| Hover | mouse encima | Estilo `:hover` de `.bulk-list-section-action` |
| Focus visible | foco por teclado | Outline de `.bulk-list-section-action:focus-visible` |

Máquina de estados del botón bulk:

```
N > 0 ──► (click Activar N) ──► abre bulk-modal stage 1
N == 0 ─► oculta el botón bulk (la lista sigue siendo un grid único)
```

## Flujos de usuario (Experience-Driven User Story)

**Flujo A · Activar todas las fuentes pendientes**
- **Como** usuario que entra al tab Ingesta
- **Quiero** activar el monitoreo de todas las fuentes pendientes sin configurar una por una
- **Para** garantizar que mi tablero esté completamente monitoreado en un solo flujo
- **Camino**:
  1. En la barra de tabs, a la derecha (`.tm-tabs-actions`), veo el buscador "Buscar fuente" y el botón "Activar las N a la vez". El contenido del tab abajo muestra el título "Ingesta de datos" + subtítulo y el grid de fuentes.
  2. Hago click en el botón. Se abre el modal bulk (`bulkActivateOpen = true`) con stage 1 (selección).
  3. Continúo el flujo en el doc 06 (Activación masiva).

**Flujo B · Filtrar antes de actuar**
- **Como** usuario con muchas fuentes
- **Quiero** filtrar el listado para enfocarme en un subset
- **Para** revisar pendientes sin abrumarme
- **Camino**:
  1. Escribo en el `tm-search-input`. El listado se filtra por `name.toLowerCase().includes(query)`.
  2. El contador del botón bulk no se ve afectado: sigue mostrando el total global de pendientes.

## Interacciones

| Trigger | Resultado | Side effects |
|---|---|---|
| Click en `.bulk-list-section-action` | Llama `openBulkActivate()` | Abre el modal bulk, preselecciona todas las fuentes `status === 'empty'`, set `bulkActivateStage = 1` |
| Input en `.tm-search-input` | Actualiza `resourceSearch` | Filtra el grid de fuentes por nombre |
| Cambio en `resources[i].status` | Re-renderiza el botón bulk si la cantidad llega a 0 | Botón se oculta |

## Data contracts

- `resources: Resource[]` cada uno con `{ id, name, workspace, status: 'empty' \| 'impacto-positivo' \| ... , dayConfig?, readiness? }`.
- El conteo se calcula en cliente con `resources.filter(r => r.status === 'empty').length`.

Endpoint sugerido: `GET /dashboards/{id}/sources` que devuelva la lista completa con sus estados de monitoreo derivados de BADS + op-center wrapper.

## Edge cases

- **Cero pendientes**: el botón bulk no se muestra (la lista sigue siendo un grid único de fuentes).
- **Una sola pendiente**: el copy cambia a singular ("Activar 1 a la vez").
- **Cargando**: si `resources` viene undefined o vacío durante el fetch, el botón no debe parpadear (verificar con `x-cloak`).
- **Búsqueda sin resultados**: se muestra el bloque `.bulk-search-empty` con mensaje "Sin resultados".
- **Permisos**: si el usuario no puede activar monitoreo, el botón debería deshabilitarse o esconderse (no resuelto en el prototipo).

## Empty states (importante)

| Escenario | Condición | Copy propuesto | CTA | Implementado en HTML? |
|---|---|---|---|---|
| Cero fuentes pendientes | `resources.filter(r => r.status === 'empty').length === 0` | Botón oculto. Sección "Sin monitoreo" oculta | (ninguno) | ✅ implementado |
| Una sola fuente pendiente | Exactamente 1 | "Activar 1 a la vez" | abre modal bulk con 1 fuente preseleccionada | ✅ implementado |
| Búsqueda sin resultados | `resources.filter(...).length === 0` por search | "Sin resultados para [query]" en `.bulk-search-empty` | Botón "Limpiar búsqueda" (clear `resourceSearch`) | ✅ implementado parcial (falta CTA) |
| Loading inicial | `resources === undefined` | Skeleton de 6 cards con shimmer + botón oculto hasta resolver | (ninguno) | ❌ pendiente |
| Error al cargar fuentes | Fetch `dashboards/{id}/sources` falló | "No pudimos cargar las fuentes." | Botón "Reintentar" | ❌ pendiente |
| Sin permisos para activar bulk | `user.canBulkActivate === false` | Botón oculto, mostrar tooltip "No tienes permisos" en hover | (ninguno) | ❌ pendiente |
| BE devuelve set parcial (paginación) | `resources.length < totalCount` | Banner info "Mostrando primeras N fuentes." | Link "Ver todas" | ❌ pendiente |

## Edge cases (validación)

- Cargando: usar `x-cloak` para evitar que el botón parpadee.
- Búsqueda activa: el contador del botón sigue siendo el total global, no el filtrado.
- Cambio en runtime de `resources[i].status` (otro usuario activa): el botón debe actualizarse reactivamente.
- Hover y focus por teclado con outline visible (accesibilidad).
- Cantidad muy alta (>99): el copy "Activar las 100 a la vez" no debe romper el ancho del botón.

## Componentes desyk a usar

> Mapeo del prototipo HTML a los componentes oficiales del design system desyk
> (basado en shadcn/ui). El implementador debe reusar estos componentes en lugar
> de replicar las clases CSS custom del prototipo.

| Elemento del prototipo | Componente desyk | Variants / props | Notas de uso |
|---|---|---|---|
| `.tm-tabs-actions` (acciones a la derecha de la barra de tabs) | Layout custom con `flex` (no es componente desyk) | — | Contenedor del buscador + botón bulk de la etapa activa |
| `.tm-search` + `input.tm-search-input` (buscador de fuentes) | `Input` | `type="search"` con ícono `Search` de Lucide como prefix | Filtro por nombre de fuente |
| `.bulk-list-section-action` (botón "Activar N a la vez") | `Button` | `variant="default" size="default"` con ícono leading | Acción primaria de activación bulk |
| Icono del botón bulk (apilado de tres capas) | SVG inline o ícono custom de Lucide | — | Visual decorativo del botón |
| `.bulk-search-empty` (mensaje "Sin resultados") | Componente custom (compuesto) | — | Empty state simple para búsqueda |

**Componentes compuestos (no existen en desyk, hay que componerlos):**
- `BulkActivateButton` — botón primario con label dinámico (singular vs plural) y ícono apilado custom. Wrapper sobre `Button`.
- `SearchEmptyState` — mensaje "Sin resultados para [query]" con CTA "Limpiar búsqueda". Compuesto sobre tipografía + `Button variant="link"`.

**Referencias:**
- Repo desyk: `~/Simetrik/desyk-components` (read-only).
- Lista oficial de componentes shadcn/ui que desyk extiende.

## Implementation notes

- **Helpers Alpine ya existentes**: `resources`, `resourceSearch`, `openBulkActivate()`.
- **CSS/clases**: `.tm-tabs-actions` (contenedor a la derecha de la barra de tabs), `.tm-search`, `.bulk-list-section-action`.
- **Endpoints BE**: `GET /dashboards/{id}/sources` que devuelva lista completa con `status` derivado de BADS + op-center.
- **Tokens desyk**: `hsl(var(--primary))` para fondo del botón bulk, `hsl(var(--primary-foreground))` para el texto.
- **Animation / motion**: hover `transform: translateY(-1px)` + sombra, 120ms ease-out.

## Out of scope

- Bulk activation de fuentes ya monitoreadas (edición masiva) — explícitamente NO se cubre en este flujo.
- Selección granular antes de abrir el modal (el modal hace eso en stage 1).
- Persistencia de filtros entre sesiones.

## Criterios de aceptación

1. **Given** un tablero con `resources.filter(r => r.status === 'empty').length === 0`, **Then** el botón `.bulk-list-section-action` no se renderiza.
2. **Given** una sola fuente sin configurar, **Then** el botón muestra "Activar 1 a la vez".
3. **Given** dos o más fuentes sin configurar, **Then** el botón muestra "Activar las N a la vez" con N actualizado dinámicamente.
4. **When** el usuario hace click en el botón, **Then** se ejecuta `openBulkActivate()` y se abre el modal bulk en stage 1.
5. **Given** el botón visible, **When** ocurre hover o focus por teclado, **Then** se aplica el estilo definido en CSS sin saltos visuales.
6. La búsqueda no debe afectar el conteo del botón bulk: este siempre refleja el total global.
7. El botón vive junto al buscador en `.tm-tabs-actions` (extremo derecho de la barra de tabs), no en el header del contenido del tab ni dentro de la lista. Solo se muestra en la etapa Ingesta (`tmTab === 'ingesta'`).
8. El copy no debe usar em-dashes ni "monitorear" como verbo en contextos donde debería ser sustantivo (verificar contra glosario `00-CONTEXT.md`).

## Dependencies

- **Depende de**: `02-vista-monitoreo` (tabs), `04-cards-monitores-ingesta` (visual de las cards).
- **Bloquea a**: `06-activacion-masiva` (el botón abre ese flujo).
- **Relacionado con**: `00-CONTEXT.md`.

## Verification (cómo probarlo)

1. Abrir `index.html`, ir a tablero-monitoreo en tab Ingesta.
2. Forzar mock con varias fuentes con `status === 'empty'`. Validar botón "Activar las N a la vez" visible.
3. Cambiar a una sola pendiente y validar copy singular.
4. Activar todas y validar que el botón desaparece.
5. Escribir en el buscador y validar que las cards filtran pero el contador del botón sigue siendo total global.
6. Click en el botón. Validar `bulkActivateOpen = true`, `bulkActivateStage = 1` y preselección completa.
7. Tabular hasta el botón y validar outline focus visible.

## References

- **HTML** (ubicar por selector): grupo de acciones `<div class="tm-tabs-actions" ...>` dentro de `<div class="tm-tabs-bar">`; botón `<button class="bulk-list-section-action" ... @click="openBulkActivate()">`; buscador `input.tm-search-input` con `x-model="resourceSearch"`. La lista es un grid único (comentario "Sin agrupación: todos los recursos en un solo grid").
- **CSS** (por selector): `.bulk-list-section-action`, `.tm-tabs-actions`, `.tm-search-input`. `.bulk-list-section-header` existe pero ya no se usa.
- **JS**: helper `openBulkActivate` (buscar por nombre en el `appData()`).
- **Figma**: (pendiente de link)
- **Docs hermanos**: `[02-vista-monitoreo.md](./02-vista-monitoreo.md)`, `[04-cards-monitores-ingesta.md](./04-cards-monitores-ingesta.md)`, `[06-activacion-masiva.md](./06-activacion-masiva.md)`.
