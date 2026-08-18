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

Son independientes: se pueden implementar por separado.

## Alcance

Solo FE, un componente (`DashboardListItem`). No toca modelo de datos, API ni permisos.

## Documento

📄 [`handoff/01-ancho-util-de-la-fila.md`](./handoff/01-ancho-util-de-la-fila.md) —
problema medido, especificación con código, impacto, alcance de implementación y
las 4 preguntas a validar antes de aprobar.

## Prototipo

Vive dentro del prototipo de carpetas, porque ahí es donde se construyó:
[`../Add folder organization structure for dashboard list/prototypes/index.html`](../Add%20folder%20organization%20structure%20for%20dashboard%20list/prototypes/index.html)

Para verlo aislado de las carpetas: panel de demo → **«Antes / después» → Hoy (plano)**.
