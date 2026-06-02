---
epic: MONITOR_INGESTA
issue_type: Feature
priority: P1
estimate: M
labels: [ux, frontend, monitoring, navigation, onboarding]
depends_on: []
blocks: [03-banner-monitorear-tablero, 04-cards-monitores-ingesta]
component_areas: [shell, monitoring-view]
---

# 02 · Vista de monitoreo del tablero

> Pantalla principal del monitoreo de un tablero. **No es una página aparte: es un MODO del mismo tablero** (una lente sobre la misma entidad). Se entra y se sale con un botón en el header ("Monitoreo" ↔ "Volver al tablero"), sin breadcrumb intermedio. Organiza el proceso en 4 tabs (Ingesta · Calidad · Conciliación · Métricas) y muestra un onboarding educativo arriba con los conceptos clave del monitoreo.

## Resumen

- **Quién lo ve**: usuario que entra a `currentView === 'tablero-monitoreo'`.
- **Cuándo**: al activar una de las 3 entradas al monitoreo (ver `01-banner-tablero`): botón "Monitoreo" del header, CTA del banner zero-state, o item "Monitoreo" del menú contextual (⋮) del tablero.
- **Qué decisión habilita**: cambiar de etapa del monitoreo y entender qué se monitorea en cada una.
- **Por qué existe**: el monitoreo es un proceso de cuatro etapas y el usuario necesita un mapa mental para saber dónde está parado. La barra de tabs lo orienta y el banner "Conceptos clave" funciona como onboarding plegable estilo Datadog adaptado a violeta Simetrik.
- **Modelo de navegación (clave)**: el monitoreo es un modo, no una navegación con stack. El tab global "Tableros" del header superior **se mantiene activo** en ambos modos. El header de la entidad (nombre del tablero) es estable y de **altura igualada** entre Tablero y Monitoreo (`.entity-header`, evita saltos). En modo monitoreo se **ocultan** las acciones de tablero (Editar / Descargar / Compartir) y aparece una **señal de chrome**: un glow azul (`.tm-mode-glow`) bajo el header. Ver `01-banner-tablero` para las entradas y el botón de modo.

## Anatomía

Orden vertical de la vista: **header de entidad → banner conceptos → barra de tabs (con acciones a la derecha) → contenido del tab activo**.

| Componente | Clase / selector | Función |
|---|---|---|
| Header de entidad | `.entity-header.is-monitor` (mismo patrón que el header del dashboard) | Nombre del tablero a la izquierda; estable y de altura igualada entre modos |
| Botón de modo (salida) | `.secondary-btn` con `@click="currentView = 'dashboard'"` (chevron-left + "Volver al tablero") | Anclado al borde derecho del header. Es el mismo botón que en el dashboard dice "Monitoreo"; acá se transforma en la salida. NO hay breadcrumb |
| Glow de modo | `.tm-mode-glow` con `x-show="currentView === 'tablero-monitoreo'"` | Sombra interna azul (`--info`) solo en el borde superior del contenido, bajo el header (overlay fijo, `pointer-events:none`, fade 500ms). Señal de "estás en modo monitoreo" |
| Barra de tabs | `.tm-tabs-bar` (flex `space-between`) con `.tm-tabs[role=tablist]` | Contenedor de los 4 tabs (izquierda) |
| Acciones de etapa | `.tm-tabs-actions` (extremo derecho de `.tm-tabs-bar`) | Buscador + acción contextual de la etapa activa (ver detalle abajo y `03`/`04`) |
| Tab individual | `.tm-tab` con `:class="tmTab === '<nombre>' && 'is-active'"` | Cambia el valor de `tmTab` |
| Badge "Pronto" | `.tm-tab-soon` | Marca tabs deshabilitados (Calidad y Conciliación) |
| Banner conceptos | `.tm-concepts` con `x-show="!tmConceptsDismissed && (tmTab === 'ingesta' \|\| tmTab === 'metricas')"` | Onboarding cerrable, **arriba de la barra de tabs** |
| Intro | `.tm-concepts-intro` con `.tm-concepts-eyebrow`, `.tm-concepts-title`, `.tm-concepts-text` | Encabezado del banner |
| Card de concepto | `.tm-concept-card` con `.tm-concept-card-head`, `.tm-concept-card-desc`, `.tm-concept-preview` | Preview por concepto |
| Showcase anomalía | `.tm-concept-card.is-anomaly-showcase` con `.tm-anomaly-shot` y `.tm-anomaly-flag` | Card especial con captura peeking |
| Cerrar | `.tm-concepts-close` | Descarta el banner |

**Acciones por etapa (`.tm-tabs-actions`, contextual por `tmTab`):**

| Etapa | Acciones a la derecha de los tabs |
|---|---|
| Ingesta (`tmTab === 'ingesta'`) | Buscador "Buscar fuente" (`x-model="resourceSearch"`) + botón "Activar las N a la vez" (`@click="openBulkActivate()"`, ver `03`) |
| Métricas (`tmTab === 'metricas'`) | Buscador "Buscar gráfico" (`x-model="tmSearch"`) |
| Calidad / Conciliación | Sin acciones (Pronto) |

> Nota: el buscador y el botón de activación masiva **vivían antes dentro del header de cada tab** (`.tm-tab-header-actions`). Se movieron al extremo derecho de la barra de tabs (`.tm-tabs-actions`). El `.tm-tab-header` del contenido conserva solo título + subtítulo.

Tabs disponibles:

1. **Ingesta de datos** (`tmTab === 'ingesta'`) — activo.
2. **Calidad de datos** (`tmTab === 'calidad'`) — placeholder "Pronto".
3. **Salud de conciliaciones** (`tmTab === 'conciliacion'`) — placeholder "Pronto".
4. **Métricas de gráficos** (`tmTab === 'metricas'`) — activo.

## Estados

| Estado | Condición | Visual |
|---|---|---|
| Modo monitoreo activo | `currentView === 'tablero-monitoreo'` | Glow azul superior (`.tm-mode-glow`) visible; acciones de tablero ocultas; botón header = "Volver al tablero"; tab global "Tableros" sigue activo |
| Tab activo | `tmTab === '<id>'` | Tab marcado activo (segmented `.tm-tabs`) |
| Tab inactivo | otro tab activo | Texto muted-foreground |
| Tab "Pronto" | Calidad o Conciliación | Badge gris `.tm-tab-soon` al lado del label |
| Acciones de etapa | `tmTab === 'ingesta'` o `'metricas'` | `.tm-tabs-actions` con buscador (+ bulk en Ingesta) a la derecha de los tabs |
| Conceptos visibles | `!tmConceptsDismissed && (tmTab === 'ingesta' \|\| tmTab === 'metricas')` | Cuatro cards en grid, arriba de los tabs |
| Conceptos cerrados | `tmConceptsDismissed === true` | Banner oculto. No vuelve a aparecer en la sesión. |

## Flujos de usuario (Experience-Driven User Story)

**Flujo A · Recorrer las etapas del monitoreo**
- **Como** usuario que llega a la vista de monitoreo
- **Quiero** entender qué se monitorea en cada etapa
- **Para** decidir por dónde empezar
- **Camino**:
  1. Entro a la vista (desde cualquiera de las 3 entradas). Por default aterrizo en **Métricas de gráficos** (`tmTab = 'metricas'`); veo la barra de tabs con dos tabs marcados como "Pronto" y el glow azul superior que confirma que estoy en modo monitoreo.
  2. Leo el banner "Conceptos clave" que explica los tres conceptos: ingesta, métricas y gestión de anomalías.
  3. Cierro el banner con la X cuando ya lo entendí.

**Flujo D · Volver al tablero**
- **Como** usuario que terminó de revisar el monitoreo
- **Quiero** volver a la vista normal del tablero
- **Para** seguir trabajando con mis gráficos
- **Camino**:
  1. Hago click en "Volver al tablero" (borde derecho del header). `currentView = 'dashboard'`.
  2. Reaparecen las acciones del tablero (Editar / Descargar) y el glow azul desaparece. El botón vuelve a decir "Monitoreo".

**Flujo B · Cambiar de tab**
- **Como** usuario familiarizado con el monitoreo
- **Quiero** moverme entre Ingesta y Métricas
- **Para** configurar y revisar cada etapa
- **Camino**:
  1. Hago click en "Métricas de gráficos". El tab activo cambia, el body muestra el grid de gráficos.
  2. Vuelvo a click en "Ingesta de datos". El body muestra la lista de fuentes.

**Flujo C · Tab no disponible**
- **Como** usuario curioso
- **Quiero** ver qué hay en Calidad o Conciliación
- **Para** entender qué viene
- **Camino**:
  1. Hago click en "Calidad de datos". El tab cambia pero el body muestra un placeholder "Pronto" (definido en otra plantilla `x-if="tmTab === 'calidad'"`).

## Interacciones

| Trigger | Resultado | Side effects |
|---|---|---|
| Entrar al modo (botón "Monitoreo" / banner / menú ⋮) | `currentView = 'tablero-monitoreo'`, `tmTab = 'metricas'` | Aparece glow azul (fade 500ms), se ocultan acciones de tablero, el botón pasa a "Volver al tablero" |
| Click en "Volver al tablero" (`.secondary-btn`) | `currentView = 'dashboard'` | Desaparece el glow, reaparecen acciones de tablero, el botón vuelve a "Monitoreo" |
| Click en cualquier `.tm-tab` | Set `tmTab` al id correspondiente | Re-render del body, oculta banner conceptos si el tab no es ingesta ni metricas, cambia las acciones de `.tm-tabs-actions` |
| Click en `.tm-concepts-close` | Set `tmConceptsDismissed = true` | Banner cierra con transición ease-in 200ms |
| Cambio de `tmTab` a 'calidad' o 'conciliacion' | Banner conceptos y `.tm-tabs-actions` se ocultan automáticamente | El banner y las acciones solo aplican a tabs implementados |

## Data contracts

- `tmTab: 'ingesta' \| 'calidad' \| 'conciliacion' \| 'metricas'` (state cliente).
- `tmConceptsDismissed: boolean` (cliente, idealmente persistido por usuario para no mostrar en futuras visitas).
- Lista de tabs disponibles (`available_tabs`) que podría venir del BE para feature-flag los placeholders.

Endpoint sugerido: `GET /dashboards/{id}/monitoring-tabs` con el set de tabs habilitados.

## Edge cases

- **Default**: las 3 entradas al monitoreo setean `tmTab = 'metricas'` (y el init de Alpine es `tmTab: 'metricas'`). No se entra en Ingesta por default. Solo algunos resets internos (cambio de tablero, deep-link a una fuente) fuerzan `tmTab = 'ingesta'`.
- **Tab "Pronto" sin contenido**: la plantilla muestra un soon-card. No debe romper el layout.
- **Banner conceptos en tab no soportado**: oculto automáticamente.
- **Pantalla angosta**: el banner conceptos debe colapsar a una columna (verificar animation-delay y las media queries de `.tm-concepts`).

## Empty states (importante)

| Escenario | Condición | Copy propuesto | CTA | Implementado en HTML? |
|---|---|---|---|---|
| Tablero sin fuentes | `resources.length === 0` en tab Ingesta | "Este tablero todavía no tiene fuentes asociadas." | Link "Agregar fuente" o ayuda contextual | ❌ pendiente |
| Tab Calidad seleccionado | `tmTab === 'calidad'` | "Calidad de datos llega pronto." + ilustración placeholder | (ninguno) | ✅ implementado (`tm-tab-soon-card`) |
| Tab Conciliación seleccionado | `tmTab === 'conciliacion'` | "Salud de conciliaciones llega pronto." + ilustración | (ninguno) | ✅ implementado |
| Loading inicial de tabs | Fetch `monitoring-tabs` en curso | Skeleton de 4 tabs con shimmer | (ninguno) | ❌ pendiente |
| Error al cargar tabs disponibles | Fetch falló | Toast destructive "No pudimos cargar el monitoreo. Reintenta." | Botón "Reintentar" | ❌ pendiente |
| Sin permisos para ver monitoreo | `user.canViewMonitoring === false` | "No tienes permiso para ver el monitoreo de este tablero." | Link "Solicitar acceso" | ❌ pendiente |
| Banner conceptos descartado | `tmConceptsDismissed === true` | Banner oculto. No restaurar automáticamente | (ninguno) | ✅ implementado |
| Viewport angosto | < 768px | Banner conceptos colapsa a una columna | (ninguno) | ✅ parcial (verificar media queries) |

## Edge cases (validación)

- Default `tmTab === 'metricas'` desde todas las entradas (botón header, banner, menú ⋮) y desde el init de Alpine.
- Cambio rápido entre tabs no debe causar parpadeo (verificar `x-cloak`).
- `tmConceptsDismissed` debe persistir en sesión (al menos en cliente).
- Animation-delay escalonado de las concept cards (40/120/200/280ms) no debe ejecutarse de nuevo al cambiar de tab si el banner ya estaba visible.

## Componentes desyk a usar

> Mapeo del prototipo HTML a los componentes oficiales del design system desyk
> (basado en shadcn/ui). El implementador debe reusar estos componentes en lugar
> de replicar las clases CSS custom del prototipo.

| Elemento del prototipo | Componente desyk | Variants / props | Notas de uso |
|---|---|---|---|
| `.entity-header` + botón "Volver al tablero" | layout custom + `Button` | `Button variant="outline"` con ícono `ChevronLeft` | Header estable; el botón cambia de "Monitoreo" (dashboard) a "Volver al tablero" (monitoreo) según `currentView` |
| `.tm-mode-glow` (señal de modo) | overlay custom (no desyk) | inset box-shadow azul `--info`, `pointer-events:none`, fade 500ms | Sombra interna superior bajo el header. Réplica top-only del `dashboard-edit-mode-glow` del producto |
| `.tm-tabs-actions` (buscador + acción a la derecha de los tabs) | `Input` (con ícono search) + `Button` | `Button variant="outline"` para "Activar las N" | Contextual por `tmTab` (ver `03`/`04`) |
| `.tm-tabs-bar` + `.tm-tabs` (barra de 4 tabs) | `Tabs` + `TabsList` + `TabsTrigger` + `TabsContent` | controlado con `value={tmTab}` y `onValueChange` | Tab activo marcado (segmented) |
| `.tm-tab-soon` (badge "Pronto" para tabs deshabilitados) | `Badge` | `variant="secondary"` (gris) | Marca Calidad y Conciliación como no disponibles aún |
| `.tm-concepts` (banner onboarding plegable) | `Card` + `CardHeader` + `CardContent` | con prop o estilo override para acento violeta | Banner pedagógico de Conceptos clave |
| `.tm-concepts-close` (X del banner) | `Button` | `variant="ghost" size="icon"` con ícono `X` de Lucide | Descarta el banner para la sesión |
| `.tm-concepts-eyebrow` (eyebrow "Conceptos clave") | `Badge` o texto con estilo eyebrow | `variant="outline"` | Tipografía pequeña en mayúscula |
| `.tm-concept-card` (card por concepto) | `Card` + `CardHeader` + `CardContent` | — | Preview por concepto, 4 cards en grid |
| `.tm-concept-card.is-anomaly-showcase` (showcase de anomalía con captura) | `Card` + ilustración SVG custom + `Badge` flotante | `Badge` con `variant="destructive"` para el pill "Anomalía detectada" | Card especial con captura peeking |
| Soon-card (placeholder para tabs Calidad / Conciliación) | Componente custom (compuesto) | — | Empty state con ilustración + copy "Llega pronto" |

**Componentes compuestos (no existen en desyk, hay que componerlos):**
- `TabSoonCard` — empty state visual con ilustración placeholder + copy "Llega pronto" para tabs no implementados (Calidad y Conciliación). Compuesto sobre `Card`.
- `ConceptsBanner` — banner de onboarding con grid de 4 `Card` y animation-delay escalonado (40/120/200/280ms). Wrapper alrededor de `Card` con lógica de stagger.
- `AnomalyShowcaseCard` — card con captura SVG peeking y pill flotante. Compuesto sobre `Card` + `Badge` + ilustración custom.

**Referencias:**
- Repo desyk: `~/Simetrik/desyk-components` (read-only).
- Lista oficial de componentes shadcn/ui que desyk extiende.

## Implementation notes

- **Helpers Alpine ya existentes**: `currentView` ('dashboard' | 'tablero-monitoreo'), `tmTab` (default 'metricas'), `tmConceptsDismissed`, `resourceSearch`, `tmSearch`, `openBulkActivate()`.
- **CSS/clases**: `.entity-header`, `.tm-mode-glow`, `.tm-tabs-bar`, `.tm-tabs-actions`, `.tm-tab`, `.tm-tab-soon`, `.tm-concepts`, `.tm-concept-card`.
- **Modo (chrome)**: al entrar/salir solo cambia `currentView`; no hay navegación con stack ni breadcrumb. El header (`.entity-header`) tiene `min-height` igualado para evitar saltos entre Tablero y Monitoreo.
- **Endpoints BE** sugeridos: `GET /dashboards/{id}/monitoring-tabs` con set de tabs habilitados (feature-flag los placeholders).
- **Tokens desyk**: `hsl(var(--primary))` para border-bottom del tab activo, `hsl(var(--muted-foreground))` para tabs inactivos, `hsl(var(--ai-purple))` para acentos del banner conceptos.
- **Animation / motion**: 200ms ease-in para cierre del banner conceptos, 40ms stagger entre concept cards al abrir.

## Out of scope

- Implementación real de Calidad y Conciliación (esta historia solo cubre el placeholder "Pronto").
- Persistencia server-side de `tmConceptsDismissed`.
- Onboarding tour interactivo (queda como follow-up).

## Criterios de aceptación

1. **Given** el usuario en `currentView === 'tablero-monitoreo'`, **Then** se muestran 4 tabs en este orden: Ingesta · Calidad · Conciliación · Métricas.
2. **Given** los tabs Calidad y Conciliación, **Then** muestran un badge "Pronto" a la derecha del label.
3. **When** el usuario hace click en un tab, **Then** `tmTab` se actualiza y el body cambia sin recargar la página.
4. **Given** el banner conceptos visible, **When** se hace click en la X, **Then** el banner se oculta con la transición leave (200ms).
5. **Given** `tmConceptsDismissed === true`, **Then** el banner conceptos no debe renderizar en ningún tab.
6. **Given** `tmTab === 'calidad'` o `'conciliacion'`, **Then** el banner conceptos está oculto incluso si `tmConceptsDismissed === false`.
7. Las cards del banner aparecen con animation-delay escalonado (40ms, 120ms, 200ms, 280ms) cuando se muestra el banner.
8. La card "Gestión de anomalías" muestra un showcase estático con la captura peeking y un pill flotante "Anomalía detectada".
9. **Given** `currentView === 'tablero-monitoreo'`, **Then** el tab global "Tableros" del header superior sigue marcado activo, y las acciones de tablero (Editar / Descargar / Compartir) no se muestran.
10. **Given** que entro al modo monitoreo, **Then** aparece el glow azul superior (`.tm-mode-glow`) con fade de 500ms, y el botón del header dice "Volver al tablero".
11. **When** hago click en "Volver al tablero", **Then** `currentView = 'dashboard'`, el glow desaparece y reaparecen las acciones de tablero (sin breadcrumb intermedio).
12. **Given** la barra de tabs, **Then** el buscador y la acción de la etapa activa viven en `.tm-tabs-actions` (extremo derecho), no dentro del header de cada tab.

## Dependencies

- **Depende de**: ninguna (estructura base de la vista).
- **Bloquea a**: `03-banner-monitorear-tablero`, `04-cards-monitores-ingesta`.
- **Relacionado con**: `01-banner-tablero` (origen del CTA), `00-CONTEXT.md`.

## Verification (cómo probarlo)

1. Abrir `index.html`, entrar a un tablero y pulsar "Monitoreo" (o el CTA del banner / menú ⋮). Verificar que `currentView = 'tablero-monitoreo'`, aparece el glow azul superior, el tab global "Tableros" sigue activo y el botón dice "Volver al tablero".
2. Verificar los 4 tabs en orden: Ingesta · Calidad · Conciliación · Métricas, y que el buscador (+ "Activar las N" en Ingesta) está al extremo derecho de la barra de tabs. "Volver al tablero" regresa al dashboard sin breadcrumb.
3. Verificar que Calidad y Conciliación muestren badge "Pronto" gris.
4. Hacer click en cada tab y validar que `tmTab` cambia y el body se re-renderiza.
5. Verificar el banner conceptos visible en Ingesta y Métricas, oculto en Calidad y Conciliación.
6. Cerrar el banner conceptos con la X y validar que no vuelva a aparecer al cambiar de tab.
7. Validar el animation-delay escalonado al abrir el banner conceptos por primera vez.

## References

- **HTML** (ubicar por selector, no por línea — el archivo se reordena): header de entidad `<div class="entity-header is-monitor ...">`, salida `<button class="secondary-btn" @click="currentView = 'dashboard'">` ("Volver al tablero"), glow `<div ... class="tm-mode-glow">`, barra `<div class="tm-tabs-bar">`, acciones `<div class="tm-tabs-actions">`, banner `<div class="tm-concepts" ...>`.
- **CSS** (por selector): `.entity-header`, `.tm-mode-glow`, `.tm-tabs-bar`, `.tm-tabs-actions`, `.tm-tab`, `.tm-tab-soon`, `.tm-concepts`.
- **Figma**: (pendiente de link)
- **Docs hermanos**: `[00-CONTEXT.md](./00-CONTEXT.md)`, `[01-banner-tablero.md](./01-banner-tablero.md)`, `[03-banner-monitorear-tablero.md](./03-banner-monitorear-tablero.md)`.
