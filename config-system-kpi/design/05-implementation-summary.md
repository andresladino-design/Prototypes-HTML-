# 05 · Implementation summary — rediseño de navegación del monitoreo

> Cambios aplicados a `../index.html` en la sesión de rediseño de navegación. Todos in-place sobre el modelo de modo + tabs ya existente.

## Contexto

El disparador fueron dos reuniones (Granola, 01-jun) donde se detectó que la navegación al monitoreo se sentía como "irse a otra página" (breadcrumb intermedio `Tableros / {tablero} / Monitoreo`), entraba en fricción con los tabs globales y perdía contexto. La conclusión: **el monitoreo es un modo del tablero, no una página aparte** (ver `01` y `02`).

## Cambios aplicados

### 1 · Botón de modo contextual (reemplaza breadcrumb)
- **Problema que resuelve:** el breadcrumb intermedio (`Tableros / {tablero} / Monitoreo`) hacía sentir que el monitoreo era *otra página* y dejaba al usuario preguntándose "¿cómo me devuelvo, dónde estoy?".
- Un solo botón en el header: dice **"Monitoreo"** (con badge "Sin configurar" / "Monitoreando") en modo Tablero, y **"Volver al tablero"** en modo Monitoreo.
- Anclado al **borde derecho** del cluster de acciones, para quedar fijo cuando las demás acciones se ocultan.
- Se eliminó el breadcrumb intermedio. La entrada y la salida son el mismo control reetiquetado: refuerza "es el mismo lugar, otra lente".

### 2 · Tab global "Tableros" activo en ambos modos
- **Problema que resuelve:** al entrar a monitoreo el tab "Tableros" se apagaba, así que la nav global decía que ya no estabas en Tableros (perdías la ubicación de nivel N2 y entraba en fricción con el modelo de modo).
- Antes solo se marcaba activo con `currentView === 'dashboard'`; ahora también en `'tablero-monitoreo'`. Corrige el bug de "el sidebar se salía de Tableros".

### 3 · Header de entidad estable
- **Problema que resuelve:** los dos modos eran headers distintos de alturas distintas, así que al conmutar el nombre del tablero "saltaba" (~3px) y rompía la sensación de seguir en el mismo lugar.
- Clase `.entity-header` con `min-height` igualado entre Tablero y Monitoreo → el nombre del tablero no salta al conmutar.

### 4 · Acciones contextuales por modo
- **Problema que resuelve:** mostrar "Editar tablero" / "Descargar" / "Compartir" dentro del monitoreo ofrecía acciones que no se pueden ejecutar ahí (ruido y confusión sobre qué hace cada modo).
- En modo Monitoreo se ocultan "Editar tablero" / "Descargar" / "Compartir" (no aplican).

### 5 · Glow azul de modo (`.tm-mode-glow`)
- **Problema que resuelve:** al sacar el breadcrumb y el badge del header, nada indicaba de forma persistente que estabas en modo monitoreo; al cerrar el banner de conceptos se perdía el contexto. El glow es la señal de modo que siempre está.
- Sombra interna azul (`--info`) solo en el **borde superior** del área de contenido, **debajo del header** (`top: 65px`).
- Overlay fijo (no scrollea), `pointer-events: none`, fade-in 500ms (mismo timing que el `dashboard-edit-mode-glow` del producto real).
- Es la única señal de modo (se quitó un tinte de borde violeta que competía).

### 6 · Reset de modo por entidad
- **Problema que resuelve:** si el modo se mantenía al cambiar de tablero, abrías un tablero nuevo directamente en monitoreo sin haberlo pedido (comportamiento impredecible).
- Al elegir otro tablero en el panel izquierdo, `currentView` vuelve a `'dashboard'`. Cada tablero abre en su lente default.

### 7 · Banner "Conceptos clave" arriba de los tabs
- **Problema que resuelve:** el onboarding del monitoreo quedaba por debajo de los tabs, separado de la narrativa de etapas que justamente explica.
- Se movió el banner (`.tm-concepts`) para que quede **encima** de la barra de tabs, presentando los conceptos antes de las etapas.

### 8 · Buscador + activación masiva a la barra de tabs (`.tm-tabs-actions`)
- **Problema que resuelve:** las acciones de cada etapa vivían dispersas dentro del contenido de cada tab, empujando hacia abajo y restando jerarquía; costaba encontrarlas y la vista ganaba alto innecesario.
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
