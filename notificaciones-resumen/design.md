# Design — notificaciones-resumen

> Fuente de verdad del diseño de este prototipo. Ohana y Claude lo leen para
> mantener consistencia. Mantenlo corto y accionable.

## Principios
- **Fidelidad con Simetrik / desyk** — replica el shell del producto (sidebar, top tabs, paneles) usando los tokens de desyk; no inventar estilos nuevos.
- **Configuración progresiva** — los controles se habilitan al cumplir su precondición (ej: el timing de notificación solo se activa al encender un canal Email/Slack).
- **Resumen visual antes que formularios** — la ventana de monitoreo y los KPIs se muestran como referencia visual, no como campos sueltos.
- **Densidad de producto, no de landing** — tipografía 12–14px, spacing ajustado, jerarquía por peso y color antes que por tamaño.
- **Iconografía y tabs unificadas** — un solo set (Lucide), tabs segmentadas consistentes en toda la pantalla.
- **Velocidad sobre perfección** — es prototipo; Tailwind CDN + Alpine + vanilla donde haga falta.

## Tokens

### Color
| Token | Valor | Uso |
|-------|-------|-----|
| `--background` | `#FFFFFF` | Fondo de app y cards |
| `--foreground` / text-primary | `#18181B` (hsl 240 6% 10%) | Texto principal |
| sidebar-foreground / text-secondary | `#3C4452` | Texto secundario, sidebar |
| text-tertiary | `#71717E` (hsl 240 4% 46%) | Texto terciario, iconos |
| muted-foreground | `#8C8C8C` (hsl 0 0% 55%) | Texto deshabilitado/placeholder |
| `--primary` | `#3D3BF5` (hsl 240 94% 60%) | Acción primaria, foco, selección activa |
| primary-soft | `#ECECFE` (hsl 240 94% 96%) | Fondo suave de selección |
| `--ai-purple` | `#B638FF` (hsl 280 100% 61%) | Acento IA / monitoreo inteligente |
| `--ai-blue` | `#5490FE` (hsl 222 97% 66%) | Acento IA secundario |
| success | `#15A14A` (hsl 138 76% 36%) | Estado OK, dentro de rango |
| warning | `#C8920A` (hsl 41 96% 40%) | Advertencia, sensibilidad media |
| destructive | `#DC2626` (hsl 360 72% 51%) | Error, hard limit excedido |
| info | `#2563EB` (hsl 221 83% 53%) | Informativo |
| border-strong | `#D9D9D9` (hsl 0 0% 85%) | Bordes de inputs/cards |
| border-subtle | `#E4E4E9` (sidebar-border) | Separadores suaves |
| `--chart-bar` | `#3C4452` | Barras de gráficos (K Cast) |

> Convención: el color se define en HSL en `:root` y se consume con `hsl(var(--token))`. Mantener esa indirección al agregar tonos.

### Tipografía
- **Familia:** `Inter`, fallback `-apple-system, BlinkMacSystemFont, sans-serif`.
- **Body base:** 14px; UI densa entre **12–13.5px**.
- **Escala usada:** 16 (títulos de sección) · 14 (body) · 13.5 / 13 (controles, tabs) · 12.5 / 12 (labels) · 11.5 / 11 (metadata, captions).
- **Pesos:** 500 (default UI), 600 (énfasis/títulos), 700 (raro), 400 (texto largo).

### Spacing & radius
- **Radius:** `8px` por defecto (botones, inputs, tabs) · `12px` cards/contenedores · `6–7px` chips e icon-buttons · `999px` pills y toggles.
- **Spacing:** ritmo ajustado de producto; padding de controles ~`6–8px` vertical, `8–12px` horizontal.
- **Elevación:** sombras sutiles, ej. tab activa `0 1px 2px rgba(20,20,30,.08), 0 0 0 1px var(--border-default)`.

## Voz y tono
- Español, claro y directo; tono de producto fintech B2B (FinOps/contable).
- Labels accionables y cortos (ej: *"¿Cuándo notificar?"*, *"Solo al cierre"*, *"Todo el tiempo"*).
- Respetar glosario Simetrik (Conciliación, Fuente, Asiento contable, Período contable, Espacio de trabajo, Repositorio).
- Evitar jerga técnica en la UI; explicar el estado, no el mecanismo.

## Patrones de componentes
- **Shell:** sidebar de navegación (`nav-item`) + sub-panel (`panel-item`) + top tabs (`top-tab`) segmentadas.
- **Tabs segmentadas:** fondo `muted`, tab activa con fondo blanco + sombra/ring.
- **`sens-row`:** fila de configuración con label + control (slider/toggle/segmented) + resumen visual a la derecha. Patrón base de "¿Cuándo notificar?" y de sensibilidad por KPI.
- **Slider animado:** binario *Todo el tiempo* ↔ *Solo al cierre*; refleja la ventana de monitoreo.
- **Estados deshabilitados:** card de timing atenuada hasta encender un canal; usar `muted-foreground` y opacidad, no ocultar.
- **Hard limit por bound:** 3 modos (on/off + valor sugerido) replicando el patrón de system KPIs en user KPIs.
- **Chips / pills:** radius 999px, peso 500, alto ~22px.
- **Iconos:** Lucide vía CDN, tamaño consistente, color `text-tertiary`.

## Decisiones
- 2026-06-24 — Al encender un canal (Email/Slack) se despliega su panel de configuración dentro de la misma card (`.tm-notif-card.is-open`): Email pregunta los correos destino; Slack pregunta canales y a quién etiquetar (opcional). Destinatarios como chips removibles (`.tm-chip`, radius 999px). Razón: configuración progresiva — pedir el detalle del canal solo cuando se activa, evitando formularios siempre visibles. Color activo del toggle = `--primary` `#3D3BF5`.
- 2026-06-23 — Rediseño de "¿Cuándo notificar?" con patrón `sens-row` (slider animado + ventana de monitoreo como referencia visual) en vez de campos sueltos. Razón: feedback de reunión 23-jun; el resumen visual reduce error de configuración.
- 2026-06-23 — Card de timing deshabilitada hasta activar un canal (Email/Slack). Razón: configuración progresiva, evita estados inválidos.
- 2026-06-23 — 3 modos de hard limit por bound en user KPIs, replicando system KPIs. Razón: consistencia de patrón entre KPIs.
- 2026-06-23 — Tabs segmentadas e iconografía Lucide unificadas en toda la pantalla. Razón: coherencia visual con el shell de producto.
- 2026-06-22 — Tokens de color en HSL vía `:root` consumidos con `hsl(var(--token))`; acentos IA `--ai-purple` / `--ai-blue` para el monitoreo inteligente.
