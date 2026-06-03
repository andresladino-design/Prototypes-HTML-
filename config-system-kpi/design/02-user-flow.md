# 02 · User flow — entrar, recorrer, volver

> Cómo el usuario entra al monitoreo de un tablero, recorre sus etapas y vuelve. El monitoreo es un modo (ver `01`), así que "entrar" y "volver" son conmutar una lente, no navegar con stack.

## Las 3 entradas al monitoreo

Las tres dejan al usuario en `currentView = 'tablero-monitoreo'`, `tmTab = 'metricas'`, con el tab global "Tableros" aún activo y el glow azul encendido.

| # | Entrada | Dónde | Cuándo conviene |
|---|---|---|---|
| 1 | **Botón "Monitoreo"** (principal, persistente) | Borde derecho del header del tablero; lleva el badge de estado ("Sin configurar" / "Monitoreando") | Siempre disponible. Es la entrada/salida canónica |
| 2 | **Banner zero-state** (pedagógico, descartable) | Encima del grid de gráficos, solo si no hay monitoreo | Push de activación para quien nunca configuró |
| 3 | **Menú contextual ⋮** | Item "Monitoreo" del tablero en el panel izquierdo | Atajo desde la lista, sin abrir el tablero antes |

## Flujo principal

```
[Modo Tablero]
   │  click "Monitoreo" (o banner / menú ⋮)
   ▼
[Modo Monitoreo]  ── glow azul aparece (fade 500ms), acciones de tablero se ocultan,
   │                  el botón pasa a "Volver al tablero", "Tableros" sigue activo
   │
   ├─ aterrizo en Métricas (default). Leo el banner "Conceptos clave" (cerrable).
   ├─ recorro etapas con los tabs: Ingesta · Calidad(pronto) · Conciliación(pronto) · Métricas
   ├─ en Ingesta: buscador + "Activar las N a la vez" al borde derecho de los tabs
   │     └─ configuro una fuente → modal Low/Family/High (ver handoff/05)
   │
   │  click "Volver al tablero"
   ▼
[Modo Tablero]  ── glow desaparece, reaparecen acciones, el botón vuelve a "Monitoreo"
```

## Por qué "volver" es un botón y no un breadcrumb

El dolor del modelo anterior era *"¿cómo me devuelvo, dónde estoy?"*: el breadcrumb intermedio hacía sentir que el monitoreo era otra página. Al modelarlo como modo, la vuelta es el **mismo control** que la entrada, solo que reetiquetado. El botón vive anclado al **borde derecho** del header en ambos modos: al entrar a monitoreo, las demás acciones desaparecen *a su izquierda* y el botón se queda en su lugar, cambiando "Monitoreo" → "Volver al tablero". Eso comunica "es el mismo lugar, otra lente".

## Benchmark (resumen)

Para elegir el control de cambio de modo se compararon patrones reales:

| Patrón | Ejemplo | Veredicto para nuestro caso |
|---|---|---|
| **Mode switcher** (modo, no tab) | Figma Diseño/Dev Mode | El más cercano: misma entidad, otra lente, chrome teñido. **Adoptado** como concepto |
| View switcher (representación) | Linear List/Board, Notion | Medio: nuestras vistas no son la misma data en otro formato |
| Toggle on/off | settings | Descartado: lee como "activar el feature", no "cambiar de vista" |
| Tab más de la entidad | GitHub Code/Issues | Descartado: re-mezcla página con modo (el problema original) |

Implementación final: un **botón de modo contextual** ("Monitoreo" ↔ "Volver al tablero") con badge de estado, + glow azul como chrome. Es la forma más simple que cumple "no es página / no es on/off / no es tab".

## Flujos de borde

- **Cambiar de tablero mientras estoy en monitoreo** → vuelvo a Modo Tablero del nuevo tablero (reset de modo por entidad).
- **Cerrar el banner de conceptos** → no se pierde contexto: el modo sigue señalado por el botón y el glow; las etapas siguen en los tabs.
- **Etapa "Pronto"** (Calidad / Conciliación) → placeholder, sin acciones a la derecha.

## Estados de activación (resumen)

Una fuente puede estar **Sin configurar** → **Aprendiendo** (BADS recolectando) → **Monitoreado**. Detalle de estados y del modal de configuración en `../handoff/04-cards-monitores-ingesta.md` y `../handoff/05-modal-configuracion.md`.
