# Handoff — Monitoreo de Ingesta de datos

> Spec implementable para el módulo de monitoreo de ingesta. Cada bloque de la
> experiencia tiene su propio documento con estados, anatomía, interacciones,
> data contracts y criterios de aceptación.

## Contexto general
- [`00-CONTEXT.md`](./00-CONTEXT.md) — Glosario, estados BADS (lifecycle de KPI / monitor),
  convenciones de copy, tokens de color y tamaños canónicos. **Leer primero.**

## Bloques de la experiencia
| # | Documento | Qué cubre |
|---|---|---|
| 01 | [Banner del tablero](./01-banner-tablero.md) | Banner promocional en el dashboard que invita a configurar monitoreo. |
| 02 | [Vista de monitoreo](./02-vista-monitoreo.md) | Pantalla con tabs (Ingesta · Calidad · Conciliación · Métricas) y subcomponentes. |
| 03 | [Banner monitorear tablero](./03-banner-monitorear-tablero.md) | Banner dentro del tab Ingesta que asegura que todo el tablero está monitoreado. |
| 04 | [Cards de monitores de ingesta](./04-cards-monitores-ingesta.md) | Grid de `tm-chart-card` por fuente, con estados Sin configurar / Aprendiendo / Monitoreado. |
| 05 | [Modal de configuración](./05-modal-configuracion.md) | Daysetup completo (Low / Family / High) + análisis inteligente. |
| 06 | [Activación masiva](./06-activacion-masiva.md) | Modal bulk de 3 stages: selecciona → revisa → activa. |

## Convenciones
- **Idioma**: español neutro, sin slang regional, sin em-dashes (`—`).
- **Glosario obligatorio**: `Fuente`, `Anomalía`, `Tablero`, `Espacio de trabajo`, `Conciliación`,
  `Dataset` (solo en Op Center), `KPI`, `Monitoreo`. Términos prohibidos: `dataset` (en
  conciliación), `dashboard`, `workspace`, `reconciliación`, `monitor` como verbo.
- **Motion**: duraciones canónicas 120ms / 200ms / 320ms ease-out. Microinteracciones
  pedagógicas, no decorativas.
- **Light mode** consistente. No mezclar dark + light en la misma vista.

## Prototipo
- HTML standalone: [`../index.html`](../index.html)
- URL GitHub Pages: `https://andresladino-design.github.io/Prototypes-HTML-/config-system-kpi/`

## Diseño previo
- Briefs y wireframes: [`../design/`](../design/)
- Figma: ver links en cada documento por bloque.
