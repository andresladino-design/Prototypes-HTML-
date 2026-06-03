# User flow — Configurar monitoreo del tablero

> 5 pasos del brief, materializados como flujo concreto sobre el prototipo.

## Flujo principal — Primera configuración

### Entrada al tablero

```
Cliente entra al tablero "Cobranzas Q2"
        ↓
Ve el banner de salud (persistente arriba):
  ◐ "Tu tablero todavía no tiene monitoreo activo"
        ↓
CTA "Configurar monitoreo"
        ↓
[ aterriza en la landing del monitoreo · vista "Estado del monitoreo" ]
```

### Landing → KPIs

```
Estado del monitoreo (landing)
  └─ Mensaje del agente IA:
     "Detecté 5 KPIs en este tablero y 12 Fuentes que los
      alimentan. ¿Querés que arme una configuración inicial?"
        ↓
     [Sí, propone una configuración]  [Configurar yo mismo]
        ↓
     (Si Sí) → la IA pre-llena Pasos 1-4 y lleva a Resumen
     (Si No) → entra a Paso 1 manual
```

## Paso 1 — Activar KPIs a monitorear

```
┌──────────────────────────────────────────────────┐
│ Paso 1 de 4 · ¿Qué KPIs querés vigilar?          │
├──────────────────────────────────────────────────┤
│                                                  │
│  🤖 La IA recomienda monitorear los 5 KPIs.      │
│                                                  │
│  [☑] Saldo neto día           ← analítico, alta  │
│      Frecuencia: diaria       crítico            │
│                                                  │
│  [☑] Conciliación bancaria    ← crítico          │
│  [☑] Cartera vencida          ← analítico        │
│  [☑] Asientos del día         ← analítico        │
│  [☐] Margen operativo         ← solo gerencial   │
│      ⚠ Dataset con 14 días de historial          │
│        (esperá 16 días para evitar falsos)       │
│                                                  │
│           [← Atrás]  [Siguiente: Dependencias →] │
└──────────────────────────────────────────────────┘
```

**Reglas**:
- Toggle on/off por KPI.
- Recomendación de la IA pre-marcada (toggle activado).
- KPIs con datasets inmaduros (<30 días) muestran inline el callout amarillo del Paso 5 del brief.

## Paso 2 — Dependencias auto-detectadas (lineage visual)

```
┌────────────────────────────────────────────────────────┐
│ Paso 2 de 4 · Estas Fuentes alimentan tus KPIs         │
├────────────────────────────────────────────────────────┤
│  🤖 La IA mapeó automáticamente el lineage:            │
│                                                        │
│  Mov. BBVA  ──┐                                        │
│              ├─► Conciliación bancaria ─┬─► Saldo neto │
│  Mov. Bcol. ──┘                          │             │
│                                          │             │
│  Cartera SAP ────► Cartera vencida ─────┘              │
│                                                        │
│  Plan cuentas ────► Asientos del día                   │
│                                                        │
│  ☑ Vigilar todas las Fuentes detectadas (4)            │
│  [Ajustar selección manualmente]                       │
│                                                        │
│           [← Atrás]  [Siguiente: Tipos de alerta →]    │
└────────────────────────────────────────────────────────┘
```

**Reglas**:
- Diagrama de lineage navegable (hover → highlight de la cadena).
- Auto-selección, opción manual escondida bajo "Ajustar".
- Si una Fuente alimenta varios KPIs, se marca como prioritaria.

## Paso 3 — Tipos de alerta a activar

```
┌─────────────────────────────────────────────────────────┐
│ Paso 3 de 4 · ¿Qué problemas querés que te avisemos?   │
├─────────────────────────────────────────────────────────┤
│  🤖 Recomendado para tu caso · todo activo              │
│                                                         │
│  Ingesta                                                │
│  [☑] Archivo faltante         "No llegó hoy"            │
│  [☑] Llegada tardía            "Llegó >2h tarde"        │
│                                                         │
│  Calidad                                                │
│  [☑] Volumen anómalo           "Llegaron muy pocas      │
│                                  filas vs lo normal"    │
│  [☑] Cambios estructurales     "Apareció/desapareció    │
│                                  una columna"           │
│                                                         │
│  Conciliación                                           │
│  [☑] Desalineación             "Diferencias inesperadas │
│                                  entre Fuentes"         │
│                                                         │
│  KPI                                                    │
│  [☑] Desvío del KPI            "El valor se aleja       │
│                                  del comportamiento     │
│                                  normal"                │
│                                                         │
│           [← Atrás]  [Siguiente: Notificaciones →]     │
└─────────────────────────────────────────────────────────┘
```

**Reglas**:
- Agrupado por etapa de pipeline (mismo orden visual del banner).
- Cada chequeo tiene **descripción en lenguaje de negocio** (frase entre comillas).
- Sin umbrales numéricos visibles — la IA los calcula.

## Paso 4 — Notificaciones y horarios

```
┌─────────────────────────────────────────────────────────┐
│ Paso 4 de 4 · ¿Quién y cómo recibe los avisos?         │
├─────────────────────────────────────────────────────────┤
│  Canales                                                │
│   [☑] Email a:                                          │
│       finanzas@empresa.com                              │
│   [☑] Slack a:                                          │
│       #cobranzas-alerts                                 │
│   [☐] Webhook custom        [Configurar]                │
│                                                         │
│  Horarios                                               │
│   No notificar entre las  [22:00] y [07:00]            │
│   Días sin avisos:  ☑ Sábado  ☑ Domingo                │
│                                                         │
│   ⓘ Los problemas críticos se notifican igual,         │
│     fuera de horario.                                   │
│                                                         │
│           [← Atrás]    [Revisar y activar →]            │
└─────────────────────────────────────────────────────────┘
```

## Paso 5 (cierre) — Disclaimer de madurez + activación

```
┌─────────────────────────────────────────────────────────┐
│ Casi listo — antes de activar                           │
├─────────────────────────────────────────────────────────┤
│  Vas a monitorear:                                      │
│  ✓ 4 KPIs                                               │
│  ✓ 4 Fuentes                                            │
│  ✓ 6 tipos de problema                                  │
│  ✓ 2 canales de notificación                            │
│                                                         │
│  ⚠ Tené en cuenta                                       │
│     Margen operativo no está incluido todavía:          │
│     su Fuente lleva 14 días recibiendo datos y el       │
│     monitoreo necesita 30 días para no generar          │
│     avisos falsos. Te lo recuerdo el 12 de junio.       │
│                                                         │
│  [☑] Empezar en modo prudente los primeros 7 días       │
│      (te avisamos sin enviar a Slack/Email hasta        │
│       validar que las alertas son precisas)             │
│                                                         │
│        [Volver a editar]    [Activar monitoreo]         │
└─────────────────────────────────────────────────────────┘
```

**Reglas**:
- Lista lo que se está activando en términos concretos del cliente (no jerga).
- Modo prudente (silencioso) para los primeros 7 días → reduce miedo, alineado con principio Simetrik "microinteracciones pedagógicas, reducen miedo".
- Disclaimer de madurez explícito sobre datasets inmaduros (Paso 5 brief).

## Flujo secundario — Editar override por caso específico

Desde la landing → click en un KPI específico → modal/Sheet lateral:

```
┌─────────────────────────────────────────────────────────┐
│ Saldo neto día — ajustes propios                        │
├─────────────────────────────────────────────────────────┤
│  Configuración general del tablero:                     │
│  · Notifica a finanzas@empresa.com                      │
│  · No notifica entre 22:00 y 07:00                      │
│                                                         │
│  Sobrescribir para este KPI:                            │
│  [☑] Notificar también a:  [cfo@empresa.com]            │
│  [☑] Notificar siempre, incluso fuera de horario        │
│      (es un KPI crítico para Tesorería)                 │
│                                                         │
│  [Quitar overrides]   [Cancelar]   [Guardar]            │
└─────────────────────────────────────────────────────────┘
```

**Reglas críticas** (alineado con "editar caso puntual sin perder configuración general"):
- Siempre muestra la regla heredada en gris.
- El override se marca visualmente como override (no se mezcla con la regla general).
- Botón "Quitar overrides" devuelve a la regla heredada.

## Flujo secundario — Ver incidentes filtrados del tablero

```
Banner del tablero → CTA "Ver incidentes (1)"
        ↓
Landing → Incidentes (panel intermedio)
        ↓
Lista filtrada SOLO por incidentes que afectan este tablero
        ↓
Click en uno → detalle (panel derecho)
  · ¿Qué pasó? (lenguaje natural)
  · ¿Qué KPIs afecta?
  · ¿Cuándo se resuelve?
  · CTA: Snooze · Resolver · Escalar
```

Diferencia con la vista global "Incidentes" del header principal: ahí ves todos los de la cuenta. Acá solo los del tablero activo. Persistencia visual: el breadcrumb muestra siempre `Tablero X › Incidentes`.

## Estados especiales

| Estado | Qué ve el cliente |
|---|---|
| Tablero **sin monitoreo activo** | Banner gris neutro + CTA grande "Configurar monitoreo" |
| Tablero en **modo prudente** (primeros 7 días) | Banner azul + chip "Aprendiendo · 4 días restantes" |
| Tablero **estable, todo verde** | Banner verde fino + "Listo para operar" |
| Tablero con **1 KPI en riesgo** | Banner amarillo + nombre del problema |
| Tablero con **incidente crítico activo** | Banner rojo + CTA prominente "Ver incidente" |
| Tablero con **Fuente inmadura** | Chip "Aprendiendo" en la stage Ingesta del pipeline |

## Transiciones

- Configuración inicial → confirmar → ir directo a la landing con banner verde.
- Edición de override → guardar → toast inferior + estado actualizado en la lista.
- Activación → modo prudente activo → countdown visible en banner.
