---
epic: MONITOR_INGESTA
issue_type: Feature
priority: P0
estimate: M
labels: [ux, frontend, monitoring, cards]
depends_on: [02-vista-monitoreo]
blocks: [05-modal-configuracion, 06-activacion-masiva]
component_areas: [monitoring-view, cards-grid]
---

# 04 · Cards de monitores de ingesta

> Grid de cards que representa cada fuente del tablero en el tab Ingesta. Es la entrada principal al modal de configuración (doc 05) y refleja el estado de monitoreo de la fuente en un golpe de vista.

## Resumen

- **Quién lo ve**: usuario en `tmTab === 'ingesta'`, debajo de la barra de tabs (el buscador y la acción bulk viven a la derecha de los tabs, en `.tm-tabs-actions`; ver `03`).
- **Cuándo**: durante el monitoreo del tablero, tanto cuando todavía hay pendientes como cuando ya está todo configurado.
- **Qué decisión habilita**: entrar al detalle de una fuente para configurarla, revisarla o editarla.
- **Por qué existe**: la lista de fuentes es la unidad operativa del monitoreo de ingesta. Las cards comprimen identificación (nombre, tipo, workspace), estado (badge de monitoreo) y enriquecimiento (grupos detectados) en un objeto clickable. **Todas las fuentes se muestran en un grid único** (sin agrupar por estado); el estado lo comunica el badge de cada card.

## Anatomía

| Componente | Clase / selector | Función |
|---|---|---|
| Grid | `.tm-cards-grid` | Layout responsive de cards |
| Card | `.tm-chart-card` con `role="button" tabindex="0"` | Card de fuente clickable y teclable |
| Card activa | `.tm-chart-card.is-active` | Border violeta cuando la fuente está seleccionada en el detalle |
| Card monitoreada | `.tm-chart-card.is-monitored` | Border verde tenue cuando el estado es "monitored" |
| Head | `.tm-chart-card-head` | Contiene title + badge |
| Title | `.tm-chart-card-title` (x-text=name) | Nombre de la fuente |
| Subtype | `.tm-chart-card-subtype` | `ingestionTypeFor(r)` + workspace (`workspaceFor(r)`) separados por punto |
| Badge | `.tm-card-badge` con `.tm-card-badge-dot` + label | Estado del monitoreo |
| Footer | `.tm-chart-card-foot` con `.tm-chart-card-deps` | Conteo de grupos detectados + chips (`tm-dep-badge`) |

> ⚠️ **Cambio vs versión anterior**: las cards van en un **grid único** (`.tm-cards-grid`), sin secciones "Monitoreado / Sin monitoreo". El estado se lee en el badge de cada card.
>
> **Problema que resuelve el grid único:** las secciones por estado fragmentaban la lista y obligaban a saltar entre bloques (y a recolocar cards cuando cambiaban de estado). Un grid único mantiene las fuentes en un solo lugar estable; el badge de cada card comunica el estado sin partir la vista.

## Estados

| Estado UI | Condición (cliente) | Origen BADS | Badge visual |
|---|---|---|---|
| **Sin configurar** | `r.status === 'empty'` y `monitoringStateFor(r) === 'unconfigured'` | No hay KPIs registrados (`resources[i].status === 'empty'`) | Badge gris, dot color border |
| **Aprendiendo** | KPIs en `COLLECTING` | `monitoringStateFor(r) === 'learning'` | Badge info azul, dot `hsl(var(--info))` |
| **Monitoreado** | Todos los KPIs en `READY` | `monitoringStateFor(r) === 'monitored'` | Badge success verde, dot `hsl(var(--success))` |

Visual extra:

- Hover: border violeta, sombra suave (`box-shadow: 0 4px 12px rgba(110, 86, 207, 0.1)`).
- Activa: ring violeta `box-shadow: 0 0 0 1px hsl(var(--primary))`.
- Monitoreada: border `hsl(var(--success) / 0.4)`.

Máquina de estados:

```
SIN_CONFIGURAR ──► (click + bulk o daysetup save) ──► APRENDIENDO ──► (KPIs READY) ──► MONITOREADO
SIN_CONFIGURAR ──► (eliminar monitoreo) ──► sigue SIN_CONFIGURAR
MONITOREADO ────► (eliminar monitoreo) ──► SIN_CONFIGURAR
```

## Flujos de usuario (Experience-Driven User Story)

**Flujo A · Configurar una fuente pendiente**
- **Como** usuario con fuentes sin configurar
- **Quiero** entrar al detalle de una fuente
- **Para** activar su monitoreo y definir su comportamiento esperado
- **Camino**:
  1. Veo el grid de fuentes; las pendientes muestran badge gris "Sin configurar".
  2. Hago click en una card. Como `r.status === 'empty'`, `selectConfigSource(r)` dispara el activation loader (ver doc 06) y luego abre el modal daysetup en modo edición.

**Flujo B · Revisar una fuente ya monitoreada**
- **Como** usuario con fuentes monitoreadas
- **Quiero** ver y eventualmente editar su configuración
- **Para** ajustar valores si el comportamiento de la fuente cambió
- **Camino**:
  1. Veo el grid de fuentes; las monitoreadas muestran badge azul ("Aprendiendo") o verde ("Monitoreado").
  2. La card muestra el nombre, tipo de ingesta, workspace, badge "Monitoreado" o "Aprendiendo" y un footer con "N grupos detectados" cuando aplica.
  3. Hago click. Como ya tiene `dayConfig`, `selectConfigSource(r)` abre el modal daysetup en modo solo-lectura (`daySetupReadonly = true`).
  4. Puedo pulsar "Editar" para entrar a modo edición o "Eliminar monitoreo" para limpiar.

**Flujo C · Acceso por teclado**
- **Como** usuario que navega con teclado
- **Quiero** abrir cualquier card sin mouse
- **Para** mantener accesibilidad
- **Camino**:
  1. Tabulo hasta llegar a una card (`tabindex="0"`).
  2. Pulso Enter o Space. Se dispara `selectConfigSource(r)` (handler `@keydown.enter` y `@keydown.space.prevent`).

## Interacciones

| Trigger | Resultado | Side effects |
|---|---|---|
| Click en card sin configurar (`status === 'empty'`) | `selectConfigSource(r)` → `openActivationLoader(r)` → tras 2.9s `_enterConfigSource(r)` → `enterDaySetup()` | Modal loader 2.9s, luego daysetup en edición |
| Click en card con `dayConfig` | `selectConfigSource(r)` → `_enterConfigSource(r)` → `enterDayView()` | Daysetup directo en solo-lectura |
| Enter o Space sobre card | Igual que click | Mismo flujo |
| Hover | `border-color: hsl(var(--primary))` + sombra | Solo visual |

## Data contracts

Por cada fuente:

```
{
  id: string,
  name: string,
  workspace: string,           // se renderiza por workspaceFor(r)
  status: 'empty' | 'impacto-positivo' | ...,
  dayConfig?: DayConfig[],     // si existe, la fuente ya está monitoreada
  dayConfigShared?: object,    // config "shared" para perfil Low
  dayConfigWindow?: object,    // ventana de tiempo
  dayConfigMonitorMode?: 'igual' | 'por-dia',
  dayConfigUseGroupsAll?: boolean,
  readiness?: object           // ver doc 05
}
```

Helpers:

- `monitoringStateFor(r)` devuelve `'unconfigured' \| 'learning' \| 'monitored'`.
- `monitoringStateLabel(state)` devuelve el label localizado.
- `ingestionTypeFor(r)` devuelve uno de los 8 tipos (Manual, Simetrik, SFTP Push, SFTP Pull, S3 Pull, Distribución, Parseo, JAAS).
- `workspaceFor(r)` quita sufijos de país.

Endpoint sugerido: `GET /dashboards/{id}/sources` y `GET /sources/{id}/monitoring` para el detalle.

## Edge cases

- **Sin grupos detectados**: el footer `tm-chart-card-foot` se oculta (`x-show` condicional sobre `r.dayConfig.some(d => d.groups.length > 0)`).
- **Más de 3 grupos**: solo se muestran los primeros 3 `tm-dep-badge`; el conteo total queda en `<strong>` previo.
- **Workspace ausente**: se oculta el separador y el span de workspace.
- **Búsqueda activa**: solo se renderizan las cards cuyo `name.toLowerCase().includes(query)`.
- **Estado "Aprendiendo" sin grupos**: badge azul, sin footer. No genera ruido visual.
- **Cargando**: las cards deben mostrar skeleton (no resuelto en el prototipo).

## Empty states (importante)

| Escenario | Condición | Copy propuesto | CTA | Implementado en HTML? |
|---|---|---|---|---|
| Tablero sin fuentes | `resources.length === 0` | "Este tablero todavía no tiene fuentes asociadas." con ilustración | Link "Agregar fuente" | ❌ pendiente |
| Todas las fuentes en el mismo grid | siempre | No hay agrupación por estado: grid único, el badge de cada card comunica su estado | (ninguno) | ✅ implementado |
| Búsqueda sin resultados | `resources.filter(...).length === 0` | "Sin resultados para [query]" en `.bulk-search-empty` | "Limpiar búsqueda" | ✅ implementado parcial (revisar CTA) |
| Loading | Fetch `dashboards/{id}/sources` en curso | Skeleton grid de 6 cards con shimmer (rect 80px + 24px badge) | (ninguno) | ❌ pendiente |
| Error al cargar | Fetch falló | "No pudimos cargar las fuentes." card con icono `alert-triangle` | Botón "Reintentar" | ❌ pendiente |
| Fuente con error BADS | `monitoringStateFor(r) === 'error'` (no expuesto hoy) | Badge destructive "Error" + dot rojo. Card sigue clickable para diagnosticar | Click abre modal de detalle del error | ❌ pendiente |
| Fuente desactivada por op-center | `deactivation_reason !== null` | Badge ámbar "Desactivada: [razón]" | Click abre modal con opción de reactivar | ❌ pendiente |
| Workspace sin nombre | `workspaceFor(r) === ''` | Omitir separador y span de workspace en el subtype | (ninguno) | ✅ implementado |
| Más de 3 grupos detectados | `r.dayConfig.flatMap(d => d.groups).length > 3` | Mostrar primeros 3 chips + contador "+N más" | Click expande tooltip | ✅ parcial (limita a 3) |
| Nombre de fuente muy largo | `r.name.length > 40` | Truncar con ellipsis + tooltip nativo con nombre completo | (ninguno) | ❌ pendiente |

## Edge cases (validación)

- Búsqueda activa: solo se renderizan las cards cuyo `name.toLowerCase().includes(resourceSearch)`.
- Estado "Aprendiendo" sin grupos: badge azul, sin footer. No generar ruido visual.
- Card en hover y activa simultáneamente: prevalece el ring activo (no se duplican shadows).
- Click rápido doble: `selectConfigSource` debe ser idempotente (no abrir dos veces el loader).
- Workspace con sufijo de país (`· BO`): debe quitarse por `workspaceFor(r)`.

## Componentes desyk a usar

> Mapeo del prototipo HTML a los componentes oficiales del design system desyk
> (basado en shadcn/ui). El implementador debe reusar estos componentes en lugar
> de replicar las clases CSS custom del prototipo.

| Elemento del prototipo | Componente desyk | Variants / props | Notas de uso |
|---|---|---|---|
| `.tm-cards-grid` (grid de cards) | Layout custom con `grid grid-cols-*` | — | No es componente desyk; es layout Tailwind |
| `.tm-chart-card` (card de fuente clickable) | `Card` + `CardHeader` + `CardContent` + `CardFooter` | con `role="button" tabindex="0"` y handlers de teclado | Card de fuente, accesible por teclado |
| `.tm-chart-card.is-active` (ring violeta) | `Card` con className condicional `ring-1 ring-primary` | — | Estado seleccionado |
| `.tm-chart-card.is-monitored` (border verde) | `Card` con className condicional `border-success/40` | — | Estado monitoreado |
| `.tm-chart-card-title` (nombre de la fuente) | Tipografía heading (no componente desyk) | — | Texto plano |
| `.tm-chart-card-subtype` (tipo de ingesta + workspace) | Tipografía muted-foreground | — | Subtype con separador punto |
| `.tm-card-badge` (estado de monitoreo) | `Badge` | `variant="secondary"` (gris) / `variant="default"` con override (azul info) / `variant="default"` con override (verde success) | Tres variantes según estado: Sin configurar, Aprendiendo, Monitoreado |
| `.tm-card-badge-dot` (dot de color en el badge) | `<span>` decorativo con `bg-*` | — | Dot interno del badge, no es componente desyk |
| `.tm-chart-card-foot` con `.tm-chart-card-deps` (footer con grupos) | `CardFooter` + tipografía | — | Footer visible solo si hay grupos detectados |
| `.tm-dep-badge` (chip de grupo) | `Badge` | `variant="outline"` | Chips de grupos detectados, máximo 3 visibles |

**Componentes compuestos (no existen en desyk, hay que componerlos):**
- `SourceMonitorCard` — card de fuente clickable con estado de monitoreo. Wrapper sobre `Card` + `Badge` + handlers de teclado (Enter / Space). Incluye lógica de estados `is-active` / `is-monitored`.
- `MonitoringStateBadge` — `Badge` con variant dinámica según `monitoringStateFor(r)` (`'unconfigured' | 'learning' | 'monitored'`) y dot de color interno.
- `GroupsCountFooter` — footer con conteo de grupos detectados + chips truncados a 3. Wrapper sobre `CardFooter` + `Badge`.

**Referencias:**
- Repo desyk: `~/Simetrik/desyk-components` (read-only).
- Lista oficial de componentes shadcn/ui que desyk extiende.

## Implementation notes

- **Helpers Alpine ya existentes** a reusar: `monitoringStateFor(r)`, `monitoringStateLabel(state)`, `ingestionTypeFor(r)`, `workspaceFor(r)`, `selectConfigSource(r)`, `openActivationLoader(r)`.
- **CSS/clases**: `.tm-cards-grid`, `.tm-chart-card`, `.tm-card-badge`, `.tm-chart-card-foot`, `.tm-dep-badge`.
- **Endpoints BE**: `GET /dashboards/{id}/sources` y `GET /sources/{id}/monitoring` para precargar el detalle.
- **Tokens desyk**: `hsl(var(--primary))` para hover/active, `hsl(var(--success) / 0.4)` para border monitoreado, `hsl(var(--info))` para dot aprendiendo.
- **Animation / motion**: hover transform `translateY(-1px)` con shadow, 200ms ease-out.

## Out of scope

- Drag & drop reordenamiento de cards.
- Filtros avanzados (por tipo de ingesta, workspace, estado).
- Bulk-select desde las cards (lo hace el modal bulk).
- Indicador de salud en tiempo real (dot pulsante para anomalías activas).

## Criterios de aceptación

1. **Given** una fuente con `status === 'empty'`, **Then** la card muestra badge gris con label "Sin configurar".
2. **Given** una fuente con `monitoringStateFor(r) === 'learning'`, **Then** la card muestra badge azul (`is-learning`).
3. **Given** una fuente con todos los KPIs en `READY`, **Then** la card muestra badge verde (`is-monitored`) y border `hsl(var(--success) / 0.4)`.
4. **When** el usuario hace click en una card `empty`, **Then** se abre primero el activation loader y luego el daysetup en edición.
5. **When** el usuario hace click en una card con `dayConfig`, **Then** se abre el daysetup en solo-lectura.
6. La card es accesible por teclado: Enter y Space deben disparar la misma acción que click.
7. El footer con grupos solo aparece si existen grupos detectados.
8. El subtype combina tipo de ingesta y workspace separados por punto, con omitir workspace si no existe.
9. La lista se filtra correctamente con `resourceSearch` por nombre (case-insensitive).
10. Las fuentes se muestran en un grid único (sin agrupación "Monitoreado / Sin monitoreo"); el estado lo comunica el badge de cada card.

## Dependencies

- **Depende de**: `02-vista-monitoreo` (tab Ingesta).
- **Bloquea a**: `05-modal-configuracion` (entrada principal), `06-activacion-masiva` (activation loader desde card).
- **Relacionado con**: `03-banner-monitorear-tablero`, `00-CONTEXT.md`.

## Verification (cómo probarlo)

1. Abrir `index.html`, ir a tablero-monitoreo / tab Ingesta.
2. Validar que las cards se rendericen en grid.
3. Verificar las 3 variantes de badge (gris/azul/verde) según el estado de cada fuente mock.
4. Click en una card `status === 'empty'`: validar activation loader 2.9s y luego daysetup en edición.
5. Click en una card monitoreada: validar daysetup en solo-lectura.
6. Tabular y validar acceso por Enter y Space.
7. Filtrar con `resourceSearch` y validar case-insensitive.
8. Validar footer de grupos solo cuando existen.

## References

- **HTML** (ubicar por selector): grid `<div class="tm-cards-grid" ...>` dentro del tab Ingesta (comentario "Sin agrupación: todos los recursos en un solo grid"); card `<div class="tm-chart-card" role="button" tabindex="0" ...>`.
- **CSS** (por selector): `.tm-cards-grid`, `.tm-chart-card`, `.tm-card-badge`, `.tm-chart-card-foot`, `.tm-dep-badge`.
- **JS** (helpers en `appData()`): `selectConfigSource`, `openActivationLoader`, `monitoringStateFor`, `ingestionTypeFor`, `workspaceFor`.
- **Figma**: (pendiente de link)
- **Docs hermanos**: `[03-banner-monitorear-tablero.md](./03-banner-monitorear-tablero.md)`, `[05-modal-configuracion.md](./05-modal-configuracion.md)`, `[06-activacion-masiva.md](./06-activacion-masiva.md)`.
- **Backend**:
  - BADS: `~/Simetrik/bads/src/bads/models/kpi.py` (lifecycle KPI).
  - Op-center: `~/Simetrik/op-center-backend/apps/anomaly_configs/`.
