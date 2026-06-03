# 01 · Arquitectura de información

> Cómo se estructura la navegación del monitoreo de tableros y por qué. El concepto central: **monitoreo = modo de la entidad tablero**, no una sección hermana.

## Jerarquía de navegación

```
N1  Rail global (Op Center)            icon rail oscuro, persistente
      └ Centro de Operaciones
N2  Nav global (header superior)       Tableros · Incidentes · Pendientes · Almacenamiento
      └ "Tableros" activo
N3  Panel de tableros (268px, izq.)    lista de Tableros / Conjuntos de datos  → cambia de ENTIDAD
N4  Entidad {Tablero}                  header estable + 2 MODOS:
      ├─ Modo Tablero (default)        acciones (Editar/Descargar) + páginas (Anomalías 1/2/3) + grid de gráficos
      └─ Modo Monitoreo                tabs por etapa + contenido de la etapa
N5  Etapa del monitoreo (tabs)         Ingesta · Calidad(pronto) · Conciliación(pronto) · Métricas
N6  Detalle / configuración            modal de config por fuente (Low/Family/High) · split master-detail por gráfico
```

## La decisión clave: monitoreo es un modo, no una página

El monitoreo **no es una entidad relacionada** del tablero (como sí lo son sus páginas o sus gráficos). Es **otra forma de ver la misma entidad** — una lente. Esto evita el anti-patrón que teníamos antes: presentarlo como una página separada con su propio breadcrumb (`Tableros / {tablero} / Monitoreo`), lo que hacía sentir al usuario que "se había ido a otro lado" y entraba en fricción con los tabs globales.

Implicaciones de modelarlo como modo:

- **El tab global "Tableros" se mantiene activo** en ambos modos (`currentView: 'dashboard' | 'tablero-monitoreo'`). No se pierde la ubicación de nivel N2.
- **No hay breadcrumb intermedio.** La vuelta es un botón explícito ("Volver al tablero"), no un nivel de migas.
- **El header de la entidad es estable** entre modos (`.entity-header`, altura igualada para que no salte el nombre del tablero al conmutar).
- **Las acciones se ocultan por modo**: en Monitoreo no aplican "Editar tablero" / "Descargar" / "Compartir", así que desaparecen.
- **Una señal de chrome** marca el modo: un glow azul (`.tm-mode-glow`) en el borde superior del contenido, debajo del header.

> Referencia de patrón: es el mismo modelo que el "Dev Mode" de Figma (misma entidad, otra lente, conmutador prominente, chrome teñido), no un toggle on/off ni un tab más. Ver `02` (benchmark resumido) y `_archive/` para el modelo descartado.

## Single source of truth de navegación

| Pregunta del usuario | Lo responde |
|---|---|
| ¿A dónde puedo ir? | Nav global (N2) + panel de tableros (N3) |
| ¿Dónde estoy? | El tab "Tableros" activo + el nombre del tablero en el header + el botón de modo |
| ¿En qué modo estoy? | El botón ("Monitoreo" vs "Volver al tablero") + el glow azul |
| ¿Qué etapa estoy viendo? | Los tabs (N5) |

## Cambio de entidad vs cambio de modo

Son dos ejes ortogonales:

- **Cambiar de tablero** (panel izquierdo, N3) **resetea el modo a Tablero** (`currentView = 'dashboard'`). Cada tablero abre en su lente default. Decisión: lo más predecible es que entrar a una entidad nueva no herede el modo de la anterior.
- **Cambiar de modo** (botón) mantiene la entidad.

## Etapas del monitoreo (N5)

El monitoreo cubre el proceso que alimenta el tablero, en orden:

1. **Ingesta de datos** — las fuentes que alimentan el tablero (disponible).
2. **Calidad de datos** — *Pronto*.
3. **Salud de conciliaciones** — *Pronto*.
4. **Métricas de gráficos** — las series de cada gráfico (disponible).

Default al entrar: **Métricas** (`tmTab = 'metricas'`). Las etapas "Pronto" se muestran con un badge gris y un placeholder.

## Glosario aplicado (resumen)

Fuente / Dataset, Monitoreo, Anomalía, Incidente, Tablero. Definiciones completas y reglas de uso en `../handoff/00-CONTEXT.md` y `04-copy-recomendaciones.md`.
