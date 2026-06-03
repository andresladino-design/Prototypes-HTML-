# 03 · Wireframes low-fi

> Wireframes ASCII del modelo actual (modo + tabs). No buscan fidelidad visual, sino fijar estructura y posición. Fuente de verdad: `../index.html`.

## A · Modo Tablero (default)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ◇ Centro de Operaciones    [Tableros]  Incidentes  Pendientes  Almacenam.    │ ← "Tableros" activo
├──────────────┬──────────────────────────────────────────────────────────────┤
│ Tableros     │  Tablero de pruebas anomalías ✎   [↓][▦][⤴]  [Editar] [Monitoreo ● Sin configurar] │
│ ┌──────────┐ │  ───────────────────────────────────────────────────────────  │
│ │Tableros▾ │ │  Anomalías 1 │ Anomalías 2 │ Anomalías 3        ← páginas        │
│ 🔍 Buscar    │  ┌──────────┐ ┌──────────┐ ┌──────────┐                         │
│ ★ Favoritos  │  │  ▟▙ chart │ │  ╱╲ chart │ │  ▆▆ chart │                        │
│ ▸ Tablero..⋮ │  └──────────┘ └──────────┘ └──────────┘                         │
│ ▸ Test anom. │  (banner zero-state "Empezar a monitorear" si no hay monitoreo) │
└──────────────┴──────────────────────────────────────────────────────────────┘
```

El botón "Monitoreo" es el **último** del cluster de acciones (borde derecho) y lleva el badge de estado. El ⋮ de cada tablero en el panel abre un menú con un item "Monitoreo" (3ª entrada).

## B · Modo Monitoreo (misma entidad, otra lente)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ◇ Centro de Operaciones    [Tableros]  Incidentes  Pendientes  Almacenam.    │ ← SIGUE activo
├──────────────┬──────────────────────────────────────────────────────────────┤
│ Tableros     │  Tablero de pruebas anomalías                  [‹ Volver al tablero] │ ← header estable
│ ┌──────────┐ │ ░░░░░░░░░░░░░░░░░░░ glow azul (borde superior) ░░░░░░░░░░░░░░░░░  │ ← .tm-mode-glow
│ │Tableros▾ │ │                                                                │
│ 🔍 Buscar    │  ┌─ Conceptos clave ──────────────────────────────────[✕]─┐    │ ← banner (cerrable)
│ ★ Favoritos  │  │ Monitorea tu tablero · Ingesta / Métricas / Anomalías  │    │
│ ▸ Tablero..⋮ │  └────────────────────────────────────────────────────────┘    │
│  ↑ cambiar   │  Ingesta │ Calidad ᴾ │ Conciliación ᴾ │ Métricas   🔍Buscar [Activar N] │ ← tabs + acciones
│  de tablero  │  ─────────                                                     │
│  resetea a   │  ┌──────────────┬───────────────────────────┐                  │
│  Tablero     │  │ Fuentes      │ Detalle / monitor          │                  │
│              │  └──────────────┴───────────────────────────┘                  │
└──────────────┴──────────────────────────────────────────────────────────────┘

 Sin breadcrumb. El botón "Volver al tablero" (borde derecho) es la salida.
 Las acciones de tablero (Editar/Descargar/Compartir) se ocultan en este modo.
```

## C · Conmutación (qué cambia y qué no)

```
        Modo Tablero                         Modo Monitoreo
   ┌───────────────────────┐            ┌───────────────────────┐
   │ tab global "Tableros"  │  ═════►   │ tab global "Tableros"  │   (NO cambia)
   │ nombre del tablero     │            │ nombre del tablero     │   (NO cambia, header estable)
   │ [Editar][Descargar]    │            │ (acciones ocultas)     │   (cambia)
   │ [Monitoreo ●estado]    │            │ [‹ Volver al tablero]  │   (mismo botón, reetiquetado)
   │ páginas Anomalías 1..3 │            │ tabs Ingesta..Métricas │   (cambia el contenido)
   │ (sin glow)             │            │ glow azul superior     │   (señal de modo)
   └───────────────────────┘            └───────────────────────┘
```

## D · Barra de tabs con acciones (detalle)

```
 Ingesta de datos │ Calidad ᴾ │ Salud de conciliaciones ᴾ │ Métricas de gráficos     🔍 Buscar fuente   [⬡ Activar las 13]
 ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔                                                                    └──────── .tm-tabs-actions ────────┘
```

- Las **acciones viven al borde derecho de la barra de tabs** (`.tm-tabs-actions`), contextuales por etapa:
  - Ingesta → "Buscar fuente" + "Activar las N a la vez".
  - Métricas → "Buscar gráfico".
  - Calidad / Conciliación → sin acciones (Pronto).
- El contenido de cada tab conserva su título + descripción, pero **ya no** el buscador (subió a la barra de tabs).

## E · Configuración de una fuente (Ingesta)

Click en una card de fuente → (si está sin configurar) loader de activación ~2.9s → **modal Low/Family/High** con: ventana de tiempo, comportamiento por día, volumen de archivos, cantidad de registros, notas, grupos (High) y análisis IA. Detalle completo en `../handoff/05-modal-configuracion.md` y los contenedores `07`-`12`.

## Notas de motion

- Glow de modo: fade-in 500ms ease-out al entrar, fade-out 200ms al salir.
- Conmutación de contenido: instantánea; el header no se mueve (misma altura en ambos modos) para reforzar "mismo lugar".
- Banner conceptos: leave 200ms ease-in.
