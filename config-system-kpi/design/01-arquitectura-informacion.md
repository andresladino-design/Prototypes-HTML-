# Arquitectura de información — Config monitoreo "tablero-first"

> Reframe del prototipo `config-system-kpi/index 2.html`. Punto de partida: **el tablero/KPI**, no "recursos monitoreados".

## Mapa conceptual

```
Tablero (entidad raíz para el cliente)
│
├── [Vista analítica del tablero]                ← donde ya vive (gráficos)
│   └── Banner de salud (persistente)            ← NUEVO: nace en el header
│
└── [Estado de monitoreo del tablero]            ← NUEVA landing dedicada
    │
    ├── Cadena de proceso (pipeline visual)      ← Ingesta → Calidad → Conciliación → KPIs
    │
    ├── KPIs monitoreados (1)
    │   └── KPI individual
    │       ├── Estado actual
    │       ├── Dependencias que lo alimentan
    │       └── Reglas y overrides propios
    │
    ├── Dependencias monitoreadas (2)
    │   ├── Fuentes (archivos que entran)        ← antes: "Recursos"
    │   ├── Calidad de los datos
    │   └── Conciliación entre Fuentes
    │
    ├── Notificaciones y horarios (3)
    │   ├── Canales (Slack, Email, Webhook)
    │   ├── Horarios de silencio
    │   └── Por quién recibe qué
    │
    ├── Overrides (4)                            ← excepciones a la regla general
    │   ├── por KPI
    │   └── por Fuente
    │
    └── Incidentes de este tablero               ← lista filtrada, NO global
```

## Decisiones IA

### D1 · El tablero es la entidad raíz, no la cuenta

**Cambio**: la vista de monitoreo se accede **desde dentro del tablero** (sub-navegación), no desde un módulo global "Configuración de anomalías".

**Por qué**: el cliente piensa en su tablero (un objeto que ya conoce y opera). "Configuración de anomalías" es un módulo abstracto que no conecta con su mental model.

**Implementación**: la nav lateral del tablero (`anomalies-nav-panel`) deja de llamarse "Anomalías" y pasa a ser **"Monitoreo del tablero"** con dos secciones:

| Sección | Items |
|---|---|
| Operación | Estado del monitoreo · Incidentes · Historial |
| Configuración | KPIs · Dependencias · Notificaciones · Overrides |

### D2 · Pipeline visual como columna vertebral

**Decisión**: la "cadena de proceso" deja de ser texto explicativo y se convierte en **componente visual persistente** en 3 lugares:

1. **Banner del tablero** (mini, horizontal, 4 chips colored) → siempre visible en la vista analítica.
2. **Landing de monitoreo** (full, con counts y estados) → protagonista.
3. **Detalle de KPI** (sub-pipeline propio del KPI) → solo las stages que lo alimentan, con badges de problema.

**Por qué**: materializa el principio "monitoreo como historia de proceso" del brief. El cliente ve dónde nace el problema y a qué KPI llega.

### D3 · "Recursos monitoreados" muere como concepto top-level

**Cambio**:
- "Recursos monitoreados" (label actual, abstracto) → desaparece del header.
- En su lugar viven 3 conceptos concretos en **Dependencias**:
  - **Fuentes** (archivos que entran al sistema — antes "recursos")
  - **Calidad** (validación de los archivos)
  - **Conciliación** (cruce entre Fuentes)

**Por qué**: el brief dice literalmente "recursos monitoreados se siente demasiado abstracto". La cadena de proceso tiene 3 etapas técnicas; nombrarlas explícitamente es más claro que esconderlas en una palabra paraguas.

**Glosario obligatorio**: "Recursos" → **Fuentes** (alineado con desyk-design-laws Simetrik).

### D4 · Separación dura: ver vs configurar

**Cambio**: dos affordances de entrada distintos en el banner de salud del tablero:

- **"Ver incidentes de este tablero"** → lleva a la lista filtrada.
- **"Configurar monitoreo"** → lleva a la landing.

**Por qué**: el brief separa explícitamente "crear gráficos" de "activar/configurar monitoreo". No deben mezclarse en un mismo CTA ni en una misma pantalla.

### D5 · Configuración a nivel tablero, overrides por excepción

**Patrón**: una sola regla general aplica a todo el tablero. Cualquier ajuste fino vive en la sección **Overrides** y no contamina el flujo general.

**Por qué**: el brief lo pide explícitamente ("aplicar a todo el tablero" + "overrides por caso específico"). Resuelve el "no quiero entrar gráfico por gráfico".

### D6 · La IA recomienda, el humano confirma

**Rol del agente**: al activar un KPI, el agente IA pre-llena:
- Qué dependencias vigilar (las que alimentan ese KPI, deducido del lineage).
- Qué tipos de problema activar (deducidos del tipo de Fuente).
- Qué umbrales son sensatos (basados en histórico del dataset).

**El humano nunca llena desde cero**. Solo confirma o ajusta. Esto es el patrón agentizado Simetrik.

### D7 · Disclaimer de madurez en setup

Si el dataset que alimenta un KPI tiene menos de 30 días de historial, la UI muestra un **callout amarillo** antes de activar:

> "Esta Fuente todavía está aprendiendo. Activar monitoreo ahora puede generar avisos falsos. Recomendado: esperar 14 días más o usar solo alertas de archivo faltante."

Con dos opciones: "Activar de todas formas" o "Activar solo alertas básicas".

## Navegación final del tablero

```
┌─────────────────────────────────────────────────────────┐
│ Op Center  ›  Tableros  ›  Tablero pruebas anomalías    │
├─────────────────────────────────────────────────────────┤
│  [Banner de salud — persistente]                        │
│  ◐ 2 KPIs en riesgo · Falta Fuente BBVA                 │
│  ✓Ingesta ⚠Calidad ✓Conciliación ◐KPIs                 │
│  [Ver incidentes (1)]  [Configurar monitoreo]           │
├─────────────────────────────────────────────────────────┤
│  Tabs: │ Vista analítica │ Monitoreo │                  │
└─────────────────────────────────────────────────────────┘
```

Cuando el usuario hace clic en "Monitoreo" o en "Configurar monitoreo", entra a la landing con sidebar:

```
Operación
  · Estado del monitoreo  ← landing (default)
  · Incidentes (1)
  · Historial

Configuración
  · KPIs monitoreados
  · Dependencias
    · Fuentes
    · Calidad
    · Conciliación
  · Notificaciones
  · Overrides
```

## Lo que NO cambia (compatibilidad)

- Estructura del shell Op Center (sidebar dark 48px + header con tabs principales).
- Lista de tableros del panel izquierdo (`width:268px`).
- Componentes desyk usados (Button, Tabs, Sheet, Popover).
- Tokens HSL (`--primary`, `--success`, `--warning`, etc).
- AI gradient (--ai-purple → --ai-blue) cuando el agente IA aparece.
