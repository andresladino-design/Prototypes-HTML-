# Wireframes low-fi — 4 vistas

> ASCII low-fi. La intención es validar **layout, jerarquía y narrativa**, no el visual final.
> Tokens: ✓ = ok · ⚠ = alerta · ◐ = en riesgo · ✕ = error · • = neutro

---

## Vista 1 — Estado del tablero (banner persistente en vista analítica)

Esta es la **cabecera del tablero** que el cliente ve cuando entra a operarlo. Reemplaza el actual "2 datasets usados | Recursos monitoreados" del prototipo.

### 1a · Estado verde (todo listo)

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│  ←  Cobranzas Q2                                              [Editar] [···]    │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ✓  Tablero listo para analizar                                                  │
│     Última ingesta hace 12 min · 5 KPIs vigilados                                │
│                                                                                  │
│  ✓ Ingesta ─── ✓ Calidad ─── ✓ Conciliación ─── ✓ KPIs                           │
│  12 Fuentes    todas ok       al día              5 estables                     │
│                                                                                  │
│                                            [Ver historial]  [Configurar]        │
├──────────────────────────────────────────────────────────────────────────────────┤
│  │ Vista analítica │ Monitoreo │                                                 │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### 1b · Estado con alerta (2 KPIs en riesgo)

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│  ←  Cobranzas Q2                                              [Editar] [···]    │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ◐  2 KPIs podrían retrasarse hoy                                                │
│     Falta una Fuente de Banco BBVA · esperada a las 06:30, sin recibir          │
│     Afecta: Saldo neto día · Conciliación bancaria                              │
│                                                                                  │
│  ✓ Ingesta ─── ⚠ Calidad ─── ✓ Conciliación ─── ◐ KPIs                           │
│  11 de 12      1 problema     al día              2 de 5 en riesgo               │
│  Fuentes ok    (BBVA mov.)                                                       │
│                                                                                  │
│                                       [Ver incidentes (1)]  [Configurar]        │
├──────────────────────────────────────────────────────────────────────────────────┤
│  │ Vista analítica │ Monitoreo │                                                 │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### 1c · Estado sin monitoreo (tablero recién creado)

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│  ←  Cobranzas Q2                                              [Editar] [···]    │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  •  Este tablero todavía no tiene monitoreo activo                               │
│     Activá el monitoreo para enterarte si una Fuente no llega                    │
│     o si un KPI se aleja de lo normal.                                           │
│                                                                                  │
│                                              [Configurar monitoreo →]            │
│                                                                                  │
├──────────────────────────────────────────────────────────────────────────────────┤
│  │ Vista analítica │                                                             │
└──────────────────────────────────────────────────────────────────────────────────┘
```

**Decisiones de jerarquía**:
- Status pill arriba, con verbal narrative en 1-2 líneas (no "All systems operational" abstracto).
- Pipeline horizontal con 4 stages igualmente espaciadas, cada una con icono + label + count.
- CTAs alineadas a la derecha del banner; primaria = "Configurar", secundaria = "Ver incidentes".
- Si no hay incidentes, la CTA secundaria es "Ver historial". Si hay, es "Ver incidentes (N)".

---

## Vista 2 — Configuración general del monitoreo (landing)

Esta es la pantalla a la que se entra desde "Configurar monitoreo". Es el detail-pane principal con sidebar de navegación.

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│  ←  Cobranzas Q2  ›  Monitoreo                                          [···]    │
├──────────────────┬─────────────────────────────────────────────────────────────────┤
│                  │                                                                 │
│  Operación       │  Estado del monitoreo                                           │
│  ▸ Estado        │  ─────────────────────────                                      │
│    Incidentes(1) │                                                                 │
│    Historial     │  ◐ 2 de 5 KPIs en riesgo hoy                                    │
│                  │     Falta Fuente BBVA · esperada 06:30                          │
│  Configuración   │     [Ver incidente]                                             │
│  · KPIs          │                                                                 │
│  · Dependencias  │  Cadena de tu tablero                                           │
│    · Fuentes     │  ──────────────────────                                         │
│    · Calidad     │                                                                 │
│    · Conciliación│   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐    │
│  · Notificaciones│   │ Ingesta  │──►│ Calidad  │──►│Conciliac.│──►│   KPIs   │    │
│  · Overrides     │   │ ✓ 11/12  │   │ ⚠ 1 prob.│   │ ✓ al día │   │ ◐ 2 risk │    │
│                  │   └──────────┘   └──────────┘   └──────────┘   └──────────┘    │
│                  │                                                                 │
│                  │  KPIs monitoreados (5)                       [+ Activar otro]   │
│                  │  ──────────────────────                                         │
│                  │  ◐  Saldo neto día           Fuente BBVA en problema           │
│                  │     5 dependencias · 2 reglas    [override] [↗]                │
│                  │  ◐  Conciliación bancaria    Fuente BBVA en problema           │
│                  │     3 dependencias · 1 regla                  [↗]              │
│                  │  ✓  Cartera vencida          al día                            │
│                  │     2 dependencias                            [↗]              │
│                  │  ✓  Asientos del día         al día                            │
│                  │     1 dependencia                             [↗]              │
│                  │  ✓  Margen operativo         al día                            │
│                  │     2 dependencias · prudente 4d              [↗]              │
│                  │                                                                 │
└──────────────────┴─────────────────────────────────────────────────────────────────┘
```

**Decisiones**:
- Sidebar de monitoreo a la izquierda (240px), reemplaza el actual `anomalies-nav-panel`.
- "Estado" es el item activo por default (landing).
- "KPIs monitoreados" lista cards horizontales escaneables, no grid.
- Cada KPI muestra: estado · dependencias en problema · contador de overrides si los tiene.
- "+ Activar otro" en el header del bloque, no como botón flotante.

---

## Vista 3 — Configuración de un tipo de alerta (Dependencias → Fuentes)

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│  ←  Cobranzas Q2  ›  Monitoreo  ›  Dependencias  ›  Fuentes                       │
├──────────────────┬─────────────────────────────────────────────────────────────────┤
│                  │                                                                 │
│  Operación       │  Fuentes que alimentan tu tablero                               │
│  · Estado        │  ─────────────────────────────────                              │
│  · Incidentes(1) │                                                                 │
│  · Historial     │  4 Fuentes vigiladas · 1 con problema                           │
│                  │                                                                 │
│  Configuración   │  ┌─────────────────────────────────────────────────────────┐  │
│  · KPIs          │  │ Aplicar a todas las Fuentes del tablero          ▼    │  │
│  ▸ Dependencias  │  │                                                         │  │
│    ▸ Fuentes     │  │ ☑ Avisar si una Fuente no llega a tiempo                │  │
│    · Calidad     │  │   Margen de espera:  ●─────────●─── 2h                  │  │
│    · Conciliación│  │                                                         │  │
│  · Notificaciones│  │ ☑ Avisar si llega con muy pocas filas                   │  │
│  · Overrides     │  │   Comparado contra:  ▾ media de los últimos 30 días     │  │
│                  │  │                                                         │  │
│                  │  │ ☑ Avisar si cambia la estructura                        │  │
│                  │  │   (columnas nuevas o que desaparezcan)                  │  │
│                  │  │                                                         │  │
│                  │  │ 🤖 Esta configuración la propuso el agente IA basado    │  │
│                  │  │    en el comportamiento histórico de tus Fuentes.       │  │
│                  │  └─────────────────────────────────────────────────────────┘  │
│                  │                                                                 │
│                  │  Fuentes (4)                                                    │
│                  │  ─────────────                                                  │
│                  │  ⚠ Mov. BBVA          │ alimenta 2 KPIs │ 14 días histórico   │
│                  │      No llegó hoy a las 06:30          [Ver detalle ↗]         │
│                  │  ✓ Mov. Bancolombia   │ alimenta 2 KPIs │ 8 meses histórico    │
│                  │  ✓ Cartera SAP        │ alimenta 1 KPI  │ 14 meses             │
│                  │  ✓ Plan cuentas       │ alimenta 1 KPI  │ 24 meses             │
│                  │                                                                 │
│                  │  ─────────────  Overrides activos (1)  ─────────────             │
│                  │  Mov. BBVA · margen extendido a 4h por Andrés · ayer            │
│                  │                                          [Quitar override]      │
│                  │                                                                 │
└──────────────────┴─────────────────────────────────────────────────────────────────┘
```

**Decisiones**:
- Header del bloque: "Aplicar a todas las Fuentes del tablero" — comunica visualmente que la regla es a nivel tablero.
- Lista de Fuentes abajo muestra estado individual, sirve para detectar quién tiene override o quién está atípico.
- Overrides activos aparecen como una sección colapsable al final, con CTA "Quitar".
- Mensaje del agente IA con tono colaborativo, no autoritario.

---

## Vista 4 — Incidentes filtrados por tablero

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│  ←  Cobranzas Q2  ›  Monitoreo  ›  Incidentes                          [Filtros]  │
├──────────────────┬───────────────────────┬─────────────────────────────────────────┤
│                  │                       │                                         │
│  Operación       │  Incidentes (1)       │  Mov. BBVA no llegó hoy                 │
│  · Estado        │  ──────────────       │  ──────────────────────                 │
│  ▸ Incidentes(1) │                       │                                         │
│  · Historial     │  ┌─────────────────┐ │  Abierto · hace 38 min                  │
│                  │  │ ◐ Mov. BBVA     │ │  Severidad: alta · Crítico para         │
│  Configuración   │  │   no llegó hoy  │ │  Tesorería                              │
│  · KPIs          │  │                 │ │                                         │
│  · Dependencias  │  │ Hace 38 min     │ │  Qué pasó                               │
│  · Notificac.    │  │ ───────────     │ │  El archivo de Movimientos BBVA debía   │
│  · Overrides     │  │ Afecta:         │ │  llegar a las 06:30 y no llegó. Es la   │
│                  │  │  · Saldo neto   │ │  primera vez en 30 días.                │
│                  │  │  · Conciliación │ │                                         │
│                  │  └─────────────────┘ │  Qué KPIs afecta                        │
│                  │                       │   ◐ Saldo neto día · puede atrasarse    │
│                  │                       │   ◐ Conciliación bancaria · idem        │
│                  │                       │                                         │
│                  │                       │  ¿Qué hacer?                            │
│                  │                       │  · Si sabés que el banco está caído,    │
│                  │                       │    snoozeá 2h.                          │
│                  │                       │  · Si esperás carga manual, marcalo     │
│                  │                       │    como resuelto cuando suba el archivo.│
│                  │                       │                                         │
│                  │                       │  [Snooze 2h]  [Resolver]  [Escalar]     │
│                  │                       │                                         │
│                  │                       │  Línea de tiempo                        │
│                  │                       │  06:30 · esperado                       │
│                  │                       │  07:08 · IA detecta atraso              │
│                  │                       │  07:08 · notificado a #cobranzas-alerts │
│                  │                       │                                         │
└──────────────────┴───────────────────────┴─────────────────────────────────────────┘
```

**Decisiones**:
- Tres paneles (igual que el prototipo actual de anomalías) pero con contenido filtrado por tablero.
- Breadcrumb persistente arriba: `Cobranzas Q2 › Monitoreo › Incidentes`.
- Detalle del incidente con sección "Qué pasó" (en lenguaje natural, no jerga técnica) + "Qué KPIs afecta" + "¿Qué hacer?".
- Acciones primarias: Snooze · Resolver · Escalar (la severa no se "dismissea", se resuelve o escala).
- Timeline al final, no expandido por default si no hay más eventos.

---

## Pipeline visual — Anatomía del componente

El pipeline horizontal aparece en 3 lugares:

### Mini (banner del tablero) — 56px de alto
```
✓ Ingesta ─── ⚠ Calidad ─── ✓ Conciliación ─── ◐ KPIs
12 Fuentes    1 problema     al día              2 de 5 en riesgo
```

### Full (landing del monitoreo) — 120px de alto
```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   Ingesta    │──►│   Calidad    │──►│ Conciliación │──►│    KPIs      │
│     ✓        │   │      ⚠       │   │      ✓       │   │      ◐       │
│ 11/12 ok    │   │ 1 problema   │   │   al día     │   │ 2 en riesgo  │
│ últ. 12 min │   │ Mov. BBVA    │   │              │   │ Saldo neto   │
└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
```

### Sub-pipeline (detalle de un KPI) — 48px, solo las stages relevantes
```
Saldo neto día depende de:  ⚠ Ingesta → ✓ Calidad → ✓ Conciliación → este KPI
```

**Reglas**:
- Stages siempre en mismo orden (Ingesta → Calidad → Conciliación → KPIs).
- Color del chip = peor estado de esa stage (rojo > amarillo > verde > neutro).
- Click en una stage = filtra la vista actual a esa stage.
- Hover = tooltip con el conteo.
- Las 4 stages se mantienen incluso si una no aplica (placeholder "no requerido" en gris).

## Empty states

| Vista | Estado vacío |
|---|---|
| Estado del monitoreo | "Configurá tu primer KPI para empezar" + ilustración + CTA grande |
| KPIs monitoreados | "No tenés KPIs vigilados todavía" + lista de KPIs disponibles del tablero |
| Dependencias › Fuentes | "Activá un KPI primero — las Fuentes se detectan automáticamente" |
| Incidentes | "Sin incidentes activos · todo bajo control" + ilustración tranquila |
| Historial | "Tu tablero todavía no ha tenido incidentes" |
