# Diseño — Monitoreo de tableros (Nav Anomalías v3)

> Documentación de diseño del monitoreo de tableros en el Op Center de Simetrik. Refleja el **modelo actual**: el monitoreo es un **modo del tablero** (no una página aparte), organizado por etapas en tabs. Fuente de verdad: `../index.html`.

## Modelo en una frase

Monitorear un tablero no te lleva a otro lado: **enciende una lente sobre el mismo tablero**. Entras con un botón ("Monitoreo"), sales con el mismo botón ("Volver al tablero"), y mientras estás en modo monitoreo el contenido cambia a las etapas del proceso (Ingesta · Calidad · Conciliación · Métricas).

## Índice

| Doc | Qué cubre |
|---|---|
| [01-arquitectura-informacion.md](./01-arquitectura-informacion.md) | Jerarquía de navegación, el modelo de modo, dónde vive cada cosa |
| [02-user-flow.md](./02-user-flow.md) | Las 3 entradas al monitoreo, el flujo entrar/recorrer/volver |
| [03-wireframes-lowfi.md](./03-wireframes-lowfi.md) | Wireframes ASCII del header, el conmutador, el glow, los tabs + acciones |
| [04-copy-recomendaciones.md](./04-copy-recomendaciones.md) | Copy real del prototipo + remisión al glosario canónico |
| [05-implementation-summary.md](./05-implementation-summary.md) | Qué se construyó en el rediseño de navegación de esta sesión |
| [06-metricas-experiencia.md](./06-metricas-experiencia.md) | Métricas de UX para validar el rediseño (problema → solución → métrica), instrumentación y plan de medición |

## Relación con el handoff

`design/` es el **pensamiento de diseño** (por qué la navegación es así). La **especificación implementable** (componentes, estados, AC, contratos de datos) vive en [`../handoff/`](../handoff/README.md). Si hay conflicto, gana lo que diga el `index.html`; en segundo lugar, el handoff.

## Principios que guían este diseño

1. **El monitoreo es un modo, no una navegación con stack.** El usuario nunca "se va" del tablero; cambia de lente. Por eso el tab global "Tableros" sigue activo y no hay breadcrumb intermedio.
2. **Una sola señal de modo.** Un glow azul sutil en el borde superior comunica "estás en monitoreo", sin gritar.
3. **Las etapas son la narrativa.** Ingesta → Calidad → Conciliación → Métricas es el proceso que alimenta el tablero; los tabs lo hacen explícito.
4. **Densidad organizada.** Acciones contextuales (buscador, activación masiva) viven al borde derecho de la barra de tabs, no dispersas.
5. **Glosario Simetrik obligatorio** (ver `04` y `../handoff/00-CONTEXT.md`).

## Historial

La versión anterior de este diseño (Health Banner / landing "Estado del monitoreo" / sidebar de monitoreo / wizard de 5 pasos) está archivada en [`_archive/`](./_archive/README.md). Fue reemplazada por completo por el modelo de modo + tabs.
