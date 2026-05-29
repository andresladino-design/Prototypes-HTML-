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

> Pantalla principal del monitoreo de un tablero. Organiza el proceso en 4 tabs (Ingesta · Calidad · Conciliación · Métricas) y muestra un onboarding educativo arriba con los conceptos clave del monitoreo.

## Resumen

- **Quién lo ve**: usuario que entra a `currentView === 'tablero-monitoreo'`.
- **Cuándo**: después de pulsar el CTA del banner del tablero, o entrando directo desde el sidebar.
- **Qué decisión habilita**: cambiar de etapa del monitoreo y entender qué se monitorea en cada una.
- **Por qué existe**: el monitoreo es un proceso de cuatro etapas y el usuario necesita un mapa mental para saber dónde está parado. La barra de tabs lo orienta y el banner "Conceptos clave" funciona como onboarding plegable estilo Datadog adaptado a violeta Simetrik.

## Anatomía

| Componente | Clase / selector | Función |
|---|---|---|
| Barra de tabs | `.tm-tabs-bar` con `.tm-tabs[role=tablist]` | Contenedor de los 4 tabs |
| Tab individual | `.tm-tab` con `:class="tmTab === '<nombre>' && 'is-active'"` | Cambia el valor de `tmTab` |
| Badge "Pronto" | `.tm-tab-soon` | Marca tabs deshabilitados (Calidad y Conciliación) |
| Banner conceptos | `.tm-concepts` con `x-show="!tmConceptsDismissed && (tmTab === 'ingesta' \|\| tmTab === 'metricas')"` | Onboarding cerrable |
| Intro | `.tm-concepts-intro` con `.tm-concepts-eyebrow`, `.tm-concepts-title`, `.tm-concepts-text` | Encabezado del banner |
| Card de concepto | `.tm-concept-card` con `.tm-concept-card-head`, `.tm-concept-card-desc`, `.tm-concept-preview` | Preview por concepto |
| Showcase anomalía | `.tm-concept-card.is-anomaly-showcase` con `.tm-anomaly-shot` y `.tm-anomaly-flag` | Card especial con captura peeking |
| Cerrar | `.tm-concepts-close` | Descarta el banner |

Tabs disponibles:

1. **Ingesta de datos** (`tmTab === 'ingesta'`) — activo.
2. **Calidad de datos** (`tmTab === 'calidad'`) — placeholder "Pronto".
3. **Salud de conciliaciones** (`tmTab === 'conciliacion'`) — placeholder "Pronto".
4. **Métricas de gráficos** (`tmTab === 'metricas'`) — activo.

## Estados

| Estado | Condición | Visual |
|---|---|---|
| Tab activo | `tmTab === '<id>'` | Border-bottom violeta, texto foreground |
| Tab inactivo | otro tab activo | Texto muted-foreground |
| Tab "Pronto" | Calidad o Conciliación | Badge gris `.tm-tab-soon` al lado del label |
| Conceptos visibles | `!tmConceptsDismissed && (tmTab === 'ingesta' \|\| tmTab === 'metricas')` | Cuatro cards en grid |
| Conceptos cerrados | `tmConceptsDismissed === true` | Banner oculto. No vuelve a aparecer en la sesión. |

## Flujos de usuario (Experience-Driven User Story)

**Flujo A · Recorrer las etapas del monitoreo**
- **Como** usuario que llega a la vista de monitoreo
- **Quiero** entender qué se monitorea en cada etapa
- **Para** decidir por dónde empezar
- **Camino**:
  1. Entro a la vista. Veo la barra de tabs con Ingesta activo por default y dos tabs marcados como "Pronto".
  2. Leo el banner "Conceptos clave" que explica las tres conceptos: ingesta, métricas y gestión de anomalías.
  3. Cierro el banner con la X cuando ya lo entendí.

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
| Click en cualquier `.tm-tab` | Set `tmTab` al id correspondiente | Re-render del body, oculta banner conceptos si el tab no es ingesta ni metricas |
| Click en `.tm-concepts-close` | Set `tmConceptsDismissed = true` | Banner cierra con transición ease-in 200ms |
| Cambio de `tmTab` a 'calidad' o 'conciliacion' | Banner conceptos se oculta automáticamente | El banner solo aplica a tabs implementados |

## Data contracts

- `tmTab: 'ingesta' \| 'calidad' \| 'conciliacion' \| 'metricas'` (state cliente).
- `tmConceptsDismissed: boolean` (cliente, idealmente persistido por usuario para no mostrar en futuras visitas).
- Lista de tabs disponibles (`available_tabs`) que podría venir del BE para feature-flag los placeholders.

Endpoint sugerido: `GET /dashboards/{id}/monitoring-tabs` con el set de tabs habilitados.

## Edge cases

- **Default**: cuando se entra a la vista de monitoreo, `tmTab` debe partir en `'ingesta'`. Desde el banner del tablero llega como `'metricas'`.
- **Tab "Pronto" sin contenido**: la plantilla muestra un soon-card. No debe romper el layout.
- **Banner conceptos en tab no soportado**: oculto automáticamente.
- **Pantalla angosta**: el banner conceptos debe colapsar a una columna (verificar animation-delay y media queries entre líneas 14559-14577).

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

- Default `tmTab === 'ingesta'` al entrar directo; `tmTab === 'metricas'` cuando llega desde banner del tablero.
- Cambio rápido entre tabs no debe causar parpadeo (verificar `x-cloak`).
- `tmConceptsDismissed` debe persistir en sesión (al menos en cliente).
- Animation-delay escalonado de las concept cards (40/120/200/280ms) no debe ejecutarse de nuevo al cambiar de tab si el banner ya estaba visible.

## Componentes desyk a usar

> Mapeo del prototipo HTML a los componentes oficiales del design system desyk
> (basado en shadcn/ui). El implementador debe reusar estos componentes en lugar
> de replicar las clases CSS custom del prototipo.

| Elemento del prototipo | Componente desyk | Variants / props | Notas de uso |
|---|---|---|---|
| `.tm-tabs-bar` + `.tm-tabs` (barra de 4 tabs) | `Tabs` + `TabsList` + `TabsTrigger` + `TabsContent` | controlado con `value={tmTab}` y `onValueChange` | Border-bottom violeta en tab activo |
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

- **Helpers Alpine ya existentes**: `tmTab`, `tmConceptsDismissed`.
- **CSS/clases**: `.tm-tabs-bar`, `.tm-tab`, `.tm-tab-soon`, `.tm-concepts`, `.tm-concept-card`.
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

## Dependencies

- **Depende de**: ninguna (estructura base de la vista).
- **Bloquea a**: `03-banner-monitorear-tablero`, `04-cards-monitores-ingesta`.
- **Relacionado con**: `01-banner-tablero` (origen del CTA), `00-CONTEXT.md`.

## Verification (cómo probarlo)

1. Abrir `index.html` y navegar a `currentView = 'tablero-monitoreo'`.
2. Verificar los 4 tabs en orden: Ingesta · Calidad · Conciliación · Métricas.
3. Verificar que Calidad y Conciliación muestren badge "Pronto" gris.
4. Hacer click en cada tab y validar que `tmTab` cambia y el body se re-renderiza.
5. Verificar el banner conceptos visible en Ingesta y Métricas, oculto en Calidad y Conciliación.
6. Cerrar el banner conceptos con la X y validar que no vuelva a aparecer al cambiar de tab.
7. Validar el animation-delay escalonado al abrir el banner conceptos por primera vez.

## References

- **HTML**: `../index.html` líneas 18894-18917 (tabs bar), 18922-19023 (banner conceptos).
- **CSS**: líneas 13830-13871 (`.tm-tabs-bar`), 14422-14577 (`.tm-concepts`).
- **Figma**: (pendiente de link)
- **Docs hermanos**: `[00-CONTEXT.md](./00-CONTEXT.md)`, `[01-banner-tablero.md](./01-banner-tablero.md)`, `[03-banner-monitorear-tablero.md](./03-banner-monitorear-tablero.md)`.
