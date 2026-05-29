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

# 03 · Banner para monitorear todo el tablero

> Acción bulk dentro del tab Ingesta. Aparece junto al buscador cuando todavía hay fuentes sin configurar. Permite activar el monitoreo de todas las fuentes pendientes en una sola operación.

## Resumen

- **Quién lo ve**: usuario en la vista `tmTab === 'ingesta'` mientras haya fuentes con `status === 'empty'`.
- **Cuándo**: durante la configuración del monitoreo del tablero, antes de tenerlo todo cubierto.
- **Qué decisión habilita**: abrir el modal bulk (`openBulkActivate()`) para activar varias fuentes con un solo flujo.
- **Por qué existe**: configurar el monitoreo de una fuente puede ser demorado. La promesa del producto es "tu tablero está monitoreado de extremo a extremo" y eso requiere reducir la fricción de N configuraciones a 1 acción. El botón vive al lado del buscador para estar siempre visible cuando hay pendientes.

## Anatomía

| Componente | Clase / selector | Función |
|---|---|---|
| Header del tab | `.tm-tab-header` con `.tm-tab-header-text` y `.tm-tab-header-actions` | Título "Ingesta de datos" + subtitle + acciones |
| Buscador | `.tm-search.tm-tab-header-search` con `input.tm-search-input` x-model="resourceSearch" | Filtro por nombre de fuente |
| Botón bulk | `.bulk-list-section-action` con `x-show="resources.filter(r => r.status === 'empty').length > 0"` | Acción primaria para activar en bloque |
| Icono | SVG inline (apilado de tres capas) | Visual del botón |
| Label dinámico | Dos `span` con `x-show` por cantidad | "Activar 1 a la vez" o "Activar las N a la vez" |
| Encabezados de sección | `.bulk-list-section-header` con `.bulk-list-section-label` y `.bulk-list-section-counter` | Agrupa cards por estado: Monitoreado / Sin monitoreo |

## Estados

| Estado | Condición | Visual |
|---|---|---|
| Oculto | `resources.filter(r => r.status === 'empty').length === 0` | Botón no se renderiza |
| Singular | exactamente 1 fuente sin configurar | Label "Activar 1 a la vez" |
| Plural | 2 o más fuentes sin configurar | Label "Activar las N a la vez" (con `<span x-text>` para el número) |
| Hover | mouse encima | Estilo `:hover` definido en línea 7682 |
| Focus visible | foco por teclado | Outline definido en línea 7689 |

Máquina de estados de la sección Sin monitoreo:

```
N > 0 ──► (click Activar N) ──► abre bulk-modal stage 1
N == 0 ─► oculta sección "Sin monitoreo" y botón bulk
```

## Flujos de usuario (Experience-Driven User Story)

**Flujo A · Activar todas las fuentes pendientes**
- **Como** usuario que entra al tab Ingesta
- **Quiero** activar el monitoreo de todas las fuentes pendientes sin configurar una por una
- **Para** garantizar que mi tablero esté completamente monitoreado en un solo flujo
- **Camino**:
  1. Veo el header del tab con título "Ingesta de datos", subtitle pedagógico y a la derecha el buscador con el botón "Activar las N a la vez".
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
| Input en `.tm-search-input` | Actualiza `resourceSearch` | Filtra ambas secciones (Monitoreado y Sin monitoreo) |
| Cambio en `resources[i].status` | Re-renderiza el botón bulk si la cantidad llega a 0 | Botón se oculta |

## Data contracts

- `resources: Resource[]` cada uno con `{ id, name, workspace, status: 'empty' \| 'impacto-positivo' \| ... , dayConfig?, readiness? }`.
- El conteo se calcula en cliente con `resources.filter(r => r.status === 'empty').length`.

Endpoint sugerido: `GET /dashboards/{id}/sources` que devuelva la lista completa con sus estados de monitoreo derivados de BADS + op-center wrapper.

## Edge cases

- **Cero pendientes**: el botón y la sección "Sin monitoreo" no se muestran.
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
| `.tm-tab-header` (header del tab Ingesta) | Layout custom con `flex` (no es componente desyk) | — | Contenedor del título + acciones del tab |
| Título del tab + subtítulo pedagógico | Tipografía custom (heading + muted-foreground) | — | Texto plano, sin componente desyk especifico |
| `.tm-search` + `input.tm-search-input` (buscador de fuentes) | `Input` | `type="search"` con ícono `Search` de Lucide como prefix | Filtro por nombre de fuente |
| `.bulk-list-section-action` (botón "Activar N a la vez") | `Button` | `variant="default" size="default"` con ícono leading | Acción primaria de activación bulk |
| Icono del botón bulk (apilado de tres capas) | SVG inline o ícono custom de Lucide | — | Visual decorativo del botón |
| `.bulk-list-section-header` (encabezado de sección Monitoreado / Sin monitoreo) | Layout custom con tipografía + `Badge` | `Badge variant="secondary"` para el counter | Agrupa cards por estado |
| `.bulk-list-section-counter` (contador "N fuentes") | `Badge` | `variant="secondary"` | Contador junto al label |
| `.bulk-search-empty` (mensaje "Sin resultados") | Componente custom (compuesto) | — | Empty state simple para búsqueda |

**Componentes compuestos (no existen en desyk, hay que componerlos):**
- `BulkActivateButton` — botón primario con label dinámico (singular vs plural) y ícono apilado custom. Wrapper sobre `Button`.
- `SearchEmptyState` — mensaje "Sin resultados para [query]" con CTA "Limpiar búsqueda". Compuesto sobre tipografía + `Button variant="link"`.

**Referencias:**
- Repo desyk: `~/Simetrik/desyk-components` (read-only).
- Lista oficial de componentes shadcn/ui que desyk extiende.

## Implementation notes

- **Helpers Alpine ya existentes**: `resources`, `resourceSearch`, `openBulkActivate()`.
- **CSS/clases**: `.tm-tab-header`, `.tm-tab-header-actions`, `.tm-search`, `.bulk-list-section-action`.
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
7. El botón vive al lado del buscador en `.tm-tab-header-actions`, no dentro de las secciones de la lista.
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

- **HTML**: `../index.html` líneas 19398-19432 (header + acción bulk), 19438-19500 (sección Monitoreado), 19502-19540 (sección Sin monitoreo), 19541-19553 (búsqueda vacía).
- **CSS**: líneas 7666-7694 (`.bulk-list-section-action`), 7700+ (contadores y headers).
- **JS**: línea 16116 (`openBulkActivate`).
- **Figma**: (pendiente de link)
- **Docs hermanos**: `[02-vista-monitoreo.md](./02-vista-monitoreo.md)`, `[04-cards-monitores-ingesta.md](./04-cards-monitores-ingesta.md)`, `[06-activacion-masiva.md](./06-activacion-masiva.md)`.
