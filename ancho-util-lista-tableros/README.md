# Ancho útil en las filas del panel de Tableros

Mejora **independiente** del panel lateral del Centro de operaciones: recuperar
ancho para el nombre de cada tablero, y hacer que los caracteres visibles sean
los que de verdad distinguen una fila de otra.

> Se descubrió prototipando SWAT-577 (carpetas), pero **no depende de las carpetas**
> ni forma parte de ese issue. Aplica a la lista tal como está hoy en producción.

## El problema en una imagen

La fila mide 240px. El ⋮ se lleva 20 de ellos sin ser visible, y el truncado corta
por donde los nombres se parecen:

```
hoy                              propuesto
─────────────────────────        ─────────────────────────
Adquirencia_2026_06_04_c…        Adquirencia_2026_06_04_conciliacion…_visa
Adquirencia_2026_06_04_c…        Adquirencia_2026_06_04_conciliaci…_master
Adquirencia_2026_06_18_c…        Adquirencia_2026_06_18_conciliacion…_visa
   ↑ dos filas idénticas            ↑ se distinguen sin abrir
```

## Las dos propuestas

| # | Cambio | Gana |
|---|---|---|
| 2.a | Los botones de fila aparecen en hover en vez de reservar espacio siempre | +20px en Tableros · +40px en Favoritos |
| 2.b | Truncado al medio, fijando el último segmento del nombre | Los caracteres visibles pasan a ser los que desambiguan |
| **2.c** | **El ancho del panel es una preferencia: `sm` 288 · `md` 384 · `lg` 480** (D17, 2026-08-18) | **+96px** a `md` · **+192px** a `lg` |

Son independientes: se pueden implementar por separado, y se refuerzan. A `lg` con los botones
en hover, el nombre de un tablero pasa de 182px a **394px**.

> **2.c salió del feedback del prototipo de SWAT-577.** Se documenta acá porque **no depende de
> carpetas** — igual que las otras dos. El default se queda en 288px, así que nada regresiona.

## Alcance

Solo FE. **2.a** y **2.b** son un componente (`DashboardListItem`); **2.c** es otro
(`OcContentLayout`) más una clave de `localStorage`. No toca modelo de datos, API ni permisos.

> **🔴 Antes de implementar 2.c, verificar el umbral de colapso.**
> `COLLAPSE_WIDTH_THRESHOLD = 1200` se compara contra el ancho del **contenedor**, no de la
> ventana, así que se dispara alrededor de los **1504px**: en un portátil de 1440px el panel
> arranca colapsado. Un panel que no se muestra no tiene ancho que discutir.

## Documento

📄 [`handoff/01-ancho-util-de-la-fila.md`](./handoff/01-ancho-util-de-la-fila.md) —
problema medido, especificación con código, impacto, alcance de implementación y
las 4 preguntas a validar antes de aprobar.

## Prototipo

Vive dentro del prototipo de carpetas, porque ahí es donde se construyó:
[`../Add folder organization structure for dashboard list/prototypes/index.html`](../Add%20folder%20organization%20structure%20for%20dashboard%20list/prototypes/index.html)

Para verlo aislado de las carpetas: panel de demo → **«Antes / después» → Hoy (plano)**.
