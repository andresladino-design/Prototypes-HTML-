# 05 · Implementation summary — rediseño de navegación del monitoreo

> Cambios aplicados a `../index.html` en la sesión de rediseño de navegación. Todos in-place sobre el modelo de modo + tabs ya existente.

## Contexto

El disparador fueron dos reuniones (Granola, 01-jun) donde se detectó que la navegación al monitoreo se sentía como "irse a otra página" (breadcrumb intermedio `Tableros / {tablero} / Monitoreo`), entraba en fricción con los tabs globales y perdía contexto. La conclusión: **el monitoreo es un modo del tablero, no una página aparte** (ver `01` y `02`).

## Cambios aplicados

### 1 · Botón de modo contextual (reemplaza breadcrumb)
- Un solo botón en el header: dice **"Monitoreo"** (con badge "Sin configurar" / "Monitoreando") en modo Tablero, y **"Volver al tablero"** en modo Monitoreo.
- Anclado al **borde derecho** del cluster de acciones, para quedar fijo cuando las demás acciones se ocultan.
- Se eliminó el breadcrumb intermedio.

### 2 · Tab global "Tableros" activo en ambos modos
- Antes solo se marcaba activo con `currentView === 'dashboard'`; ahora también en `'tablero-monitoreo'`. Corrige el bug de "el sidebar se salía de Tableros".

### 3 · Header de entidad estable
- Clase `.entity-header` con `min-height` igualado entre Tablero y Monitoreo → el nombre del tablero no salta al conmutar.

### 4 · Acciones contextuales por modo
- En modo Monitoreo se ocultan "Editar tablero" / "Descargar" / "Compartir" (no aplican).

### 5 · Glow azul de modo (`.tm-mode-glow`)
- Sombra interna azul (`--info`) solo en el **borde superior** del área de contenido, **debajo del header** (`top: 65px`).
- Overlay fijo (no scrollea), `pointer-events: none`, fade-in 500ms (mismo timing que el `dashboard-edit-mode-glow` del producto real).
- Es la única señal de modo (se quitó un tinte de borde violeta que competía).

### 6 · Reset de modo por entidad
- Al elegir otro tablero en el panel izquierdo, `currentView` vuelve a `'dashboard'`.

### 7 · Banner "Conceptos clave" arriba de los tabs
- Se movió el banner (`.tm-concepts`) para que quede **encima** de la barra de tabs.

### 8 · Buscador + activación masiva a la barra de tabs (`.tm-tabs-actions`)
- El buscador y el botón "Activar las N a la vez" se movieron desde el header de cada tab (`.tm-tab-header-actions`) al **extremo derecho de la barra de tabs**, contextuales por etapa (Ingesta: buscar fuente + activar; Métricas: buscar gráfico).
- El contenido de cada tab conserva solo título + descripción.

## Decisiones de diseño (qué se probó y descartó)

El control de cambio de modo pasó por varias iteraciones antes de aterrizar en el botón contextual:

| Intento | Por qué se descartó |
|---|---|
| Segmented `[Tablero \| Monitoreo]` como fila propia | Sumaba una **tercera tira de tabs** (global + modo + etapas): demasiados tabs |
| Toggle switch on/off "Vista de monitoreo" | Leía como **activar/desactivar el feature**, no como cambiar de vista |
| Mode pill centrado / al borde (estilo Figma) | Mejor, pero seguía sin resolver el estado y generaba saltos al togglear |
| Subheader persistente sobre los tabs | Redundante con el banner de conceptos |
| **Botón contextual "Monitoreo ↔ Volver al tablero"** | **Adoptado**: es acción (no tab, no on/off), conserva el badge de estado, y la vuelta es el mismo botón reetiquetado |

## Lo que se mantuvo

- Modelo `currentView: 'dashboard' | 'tablero-monitoreo'` y `tmTab`.
- Tabs por etapa (Ingesta · Calidad · Conciliación · Métricas) y el modal Low/Family/High.
- Grid único de fuentes (sin secciones "Monitoreado / Sin monitoreo").
- Tokens y shell del Op Center.

## Pendientes / próximos pasos

- **Navegación por día + vista Resumen** dentro del detalle de fuente (pedido en las 2 reuniones): tab por día + panorama de patrones. No implementado aún.
- **Banner verde `tm-dash-secured`** ("monitoreado"): existe en CSS, sin markup. Decidir si se implementa o se descarta (hoy el estado vive en el badge del botón).
- **Alinear paddings**: el contenido bajo el header arranca a 24px en Tablero y 32px en Monitoreo (corrimiento de ~8px al conmutar). Pendiente menor.
- **Intensidad del glow**: validar si queda bien o conviene más sutil.

## Verificación

`open ../index.html` → entrar a un tablero → "Monitoreo" (glow aparece, "Tableros" sigue activo, sin breadcrumb) → recorrer tabs (buscador/acciones a la derecha) → "Volver al tablero" → cambiar de tablero (resetea a Tablero).
