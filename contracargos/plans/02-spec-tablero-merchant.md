# Spec 02 — Tablero de contracargos para merchant

**Estado:** propuesta para validar · **Depende de:** `00-plan-de-trabajo.md`, `design.md`
**Insumo:** el prototipo de Andrea (`Simetrik · Centro de Disputas — Operations Center.html`), reacotado al rol merchant
> ⚠️ **Actualizado el 26-ago con evidencia.** Ver `04-respuestas-preguntas-abiertas.md`.

## A quién sirve

El **operativo del marketplace**: la persona que cada mañana tiene que saber cuánto le debitaron, qué tarjetas bloquear y si la tasa se está acercando al umbral de la red. No es exploración, es una rutina diaria bajo presión.

La vista gerencial de pérdidas queda fuera de esta iteración (acuerdo del 26-ago).

**Dato clave a los 2 segundos:** cuánto se debitó desde el último corte y cuántas tarjetas quedan por bloquear. Hipótesis a confirmar con Andrea.

## Los tres estados del contracargo

Todo el tablero se organiza alrededor de esto, porque es la distinción que Andrea marcó como la más álgida:

| Estado | Qué significa para el merchant | Acción posible |
|---|---|---|
| **Notificado** | El adquirente avisó que va a debitar | Todavía se puede gestionar. Es prevención |
| **Debitado** | Ya descontó la plata | Pérdida consumada. Toca bloquear tarjetas y evitar que se repita |
| **Reversión** | El contracargo se revirtió a favor del merchant | Solo en algunos adquirentes |

⚠️ **No se agregan en un total único.** Un número que sume notificado + debitado no significa nada para el usuario.

## Estructura de la vista

```
┌─ Contracargos ────────────── 3 conjuntos de datos usados ──── [Contexto] [Monitoreo·Activado] [Editar] ─┐
│  Resumen · Notificados · Debitados · Controles                                                          │  ← UnderlineTabs
├─────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│  Filtros: Adquirente · Franquicia · País · Fecha · Moneda                                               │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│  ┌── Debitado en el período ──┐ ┌── Notificado sin gestionar ──┐ ┌── Tasa vs. umbral de red ─────────┐  │
│  │  $214.320 USD              │ │  $48.900 USD                 │ │  Visa      VAMP  ≤2.20%   1.84% ▲ │  │
│  │  1.284 contracargos        │ │  312 contracargos            │ │  Mastercard ECM  ≤1.50%   1.10% ✓ │  │
│  │  corte 26-ago 06:00        │ │  el más viejo: hace 9 días   │ │  faltan 0.36 pts para romper VAMP │  │
│  └────────────────────────────┘ └──────────────────────────────┘ └───────────────────────────────────┘  │
│                                                                                                          │
│  ┌── Composición por reason code ────────────┐  ┌── Serie diaria: notificado vs. debitado ────────────┐ │
│  │  barras apiladas, chart-1..8              │  │  dos series, semántico: warning / destructive       │ │
│  │  ◇ 13.1 no recibido +3.2σ vs. histórico   │  │                                                     │ │
│  └───────────────────────────────────────────┘  └─────────────────────────────────────────────────────┘ │
│                                                                                                          │
│  ┌── Requiere acción hoy ──────────────────────────────────────────────────────────────────────────┐   │
│  │  Franquicia │ ID │ Adquirente │ Fecha │ Monto │ Reason │ Estado │ Tarjeta │ Acción              │   │
│  │  Visa       │ …  │ …          │ …     │ …     │ 13.1   │Debitado│ ••••4821│ [Bloquear]          │   │
│  └──────────────────────────────────────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## KPIs

Tres, no más. Cada uno con su contexto auditable, nunca el patrón "número grande + flecha verde".

| KPI | Valor | Contexto que lo acompaña |
|---|---|---|
| **Debitado en el período** | monto + conteo | Fecha y hora del corte. Es la pérdida consumada |
| **Notificado sin gestionar** | monto + conteo | Antigüedad del más viejo. Es la ventana que todavía está abierta |
| **Tasa vs. umbral de red** | % por franquicia | Programa (VAMP / ECM), umbral, y **distancia en puntos para romperlo** |

El tercero no es un KPI numérico, es un semáforo. Verde bajo umbral, warning cerca, destructive roto. Los umbrales vienen pre-cargados del programa de red y son editables, como ya lo resolvió Andrea en su wizard.

> ⚠️ **Los umbrales del prototipo están vencidos.** Andrea pre-carga Visa VAMP en **2.20%** con la nota "→ 1.50% el 1-abr-2026". Esa fecha ya pasó: desde el 1 de abril de 2026 el umbral de merchant es **1.5%** en US, Canadá, UE y Asia-Pacífico. Mastercard ECM sigue en **1.5% con >100 CBK/mes**.
>
> Y llegan al mismo 1.5% por **fórmulas distintas**, lo que el prototipo no refleja:
>
> | Programa | Fórmula |
> |---|---|
> | Visa VAMP | (Fraude TC40 + Disputas TC15) / Transacciones liquidadas TC05 |
> | Mastercard ECM | Conteo puro de contracargos, con el mes anterior en el denominador |
>
> VAMP **incluye reportes de fraude**, no solo contracargos. Por eso el toggle "Por red / Agregado" no es cosmético: un agregado entre redes no significa nada para ninguna de las dos.

## Gráficos

Reglas de `design.md`: estados de negocio en color semántico, categóricas en `chart-1..8`, barras apiladas en vez de pie.

1. **Composición por reason code** — barras apiladas horizontales, con la anomalía marcada cuando una razón se dispara contra su histórico (el patrón `+3.2σ` que ya trae el prototipo de Andrea)
2. **Serie diaria notificado vs. debitado** — dos series, warning y destructive, para que se vea el gap de días entre el aviso y el débito
3. **Distribución por adquirente** — sirve para detectar que un adquirente concreto se disparó

## Los tres controles

Son la razón por la que el merchant abre esto. Van en su propia pestaña, cada uno como una lista accionable, no como un número.

| Control | Qué muestra | Acción |
|---|---|---|
| **Tarjetas por bloquear** | Las tarjetas de lo debitado que todavía no se bloquearon, enmascaradas a últimos 4 | Bloquear, individual y en lote |
| **Doble débito** | Contracargos descontados dos veces (liquidación + refund), agrupados por transacción original | Marcar para reclamo al adquirente |
| **Cruce con venta interna** | Contracargos sin match contra la venta interna | Ir a la conciliación |

El de doble débito es un **hallazgo**, no un estado: se marca con destructive sólido porque es plata recuperable que nadie está reclamando.

## Monitoreo

Se reutiliza el modelo de paquetes/reglas de notificaciones, no se diseña un sistema paralelo. Lo que la sesión del 26-ago dejó claro y hay que hacer visible en la UI:

**El monitoreo se activa sobre dos cosas a la vez:**

1. **La columna normalizada del dataset** — el dato de negocio calculado (el que dice si estoy perdiendo, cuánto y por qué). Sin esa columna no hay nada que alertar
2. **La fuente que alimenta el dataset** — porque una caída en el tablero puede ser una anomalía real o puede ser que el archivo no llegó, y sin monitorear la fuente no hay forma de saber la causa

En la UI esto **no es una decisión del usuario**, se activa solo. Pero tiene que ser visible: al activar monitoreo, el panel muestra las dos cosas que quedan vigiladas y por qué. Es lo que hace la diferencia entre "el tablero cayó" y "el archivo de notificados no llegó hoy".

### El contrato ya existe en producción

Verificado en `fe-solutions-mf/.../AnomalyMonitoringConfig/types.ts`. Una regla se ata a:

```ts
{ metric_field_id, metric_reference /* nombre real de la columna */,
  metric_aggregation, thresholds: [{ operator, value, series_value }] }
```

más `dateColumnId`, `categoryColumnNames[]`, `granularity`, `timezone`, `frequency`.

Tres consecuencias:

1. **`metric_reference` es literalmente el nombre de la columna.** Lo de la columna normalizada no era una hipótesis de diseño, es el contrato. Sin ella no hay nada que monitorear.
2. **El umbral por red ya se puede hacer sin features nuevas:** `categoryColumnNames: ["franquicia"]` y un `threshold.series_value` por cada red. Visa y Mastercard son dos filas de la misma regla.
3. **El monitoreo de la fuente también existe.** El Paso 9.3 del flujo del Brain documenta las anomalías de ingesta con acceso directo a Fuentes para recargar, reemplazar o corregir el mapeo. El loop que planteé en la sesión ya está resuelto en producto; no hay que diseñarlo, hay que conectarlo.

Queda para Santi: **quién materializa esa columna y en qué punto de la cadena.**

Tipos de regla que aplican acá:
- Distancia al umbral de red menor a X puntos
- Débito diario por encima del comportamiento aprendido
- Reason code disparado contra su histórico
- Fuente sin llegar en la ventana esperada

## Ciclo de vida del contracargo

El prototipo de Andrea trae un timeline (PAYIN → TC40/Verifi → Notificado → Debitado → 2ª Presentación) con el movimiento de fondos en cada nodo. Los implementadores lo pidieron y es valioso.

⚠️ **Bloqueado por una pregunta de data.** Los archivos llegan separados, así que encadenar la misma transacción a través de los tres estados depende de que sobrevivan llaves de cruce que hoy no sabemos si existen. El prototipo de Andrea asume ARN + código de autorización.

**Decisión de diseño:** el ciclo de vida se trata como **aditivo, no estructural**. El tablero funciona completo sin él. Si Santi confirma que la data lo permite, entra en el detalle del caso; si no, el detalle muestra solo los estados que sí se pueden probar. Ninguna otra parte del diseño depende de esa respuesta.

## Qué se conserva del prototipo de Andrea

| Elemento | Destino |
|---|---|
| Modelo conceptual: estados, reason codes reales, umbrales VAMP/ECM | ✅ Se conserva completo. Es el activo más valioso |
| Wizard de monitoreo con distancia al umbral | ✅ Se conserva la lógica, se reescribe sobre el modelo de paquetes |
| Línea de vida con movimiento de fondos | ⚠️ Condicionado a la data |
| Tabla de contracargos con reason code, SLA, cruce por ARN | ✅ Se conserva, reacotada a columnas de merchant |
| Bloques con narrativa y confianza del agente | ✅ Se conserva, con el patrón AI de desyk |
| Switch de 4 roles (Issuer / Merchant / PSP / Adquirente) | ❌ Colapsa a Merchant. Los otros quedan como demo comercial |
| Flujo agéntico de 8 pasos de cara al emisor | ❌ Fuera de alcance. Andrea: "no aplica para el merchant" |
| ChargeScore / win probability | ❌ Fuera. Es del mundo de disputas del emisor, no del merchant que recibe el débito |
| Win rate agregado y "recuperado" agregado | ❌ Descartados desde el 9-jul |
| Código (vanilla JS, SVG a mano, idioma mixto, `#3b63e6`) | ❌ Se rehace: Tailwind CDN + Alpine + tokens desyk, todo en español |

## Estados de la vista

> ⚠️ **Corregido el 28-ago (Andres):** el tablero **no tiene estado de configuración pendiente**. Instalado el template desde el Marketplace, queda usable. Para los marketplaces las fuentes de notificados y debitados ya están integradas en Simetrik, así que aplica el caso de fuentes preintegradas del Brain (UC-16): la instalación se completa sola y aterriza con datos reales.
>
> Se caen de esta spec: el empty state inicial, el patrón de mock data con banner "Pending Setup", los widgets `Locked` y toda la vinculación de fuentes. Siguen siendo el flujo general del producto para templates que sí piden archivos, pero **no son el caso de contracargos**.

1. **Recién instalado** — con datos reales desde el primer minuto. No hay estado intermedio que diseñar
2. **Detectado parcialmente** — el motor de inferencia clasificó al 30%. Banda con la confianza y la salida para corregir. Frecuente, no borde
3. **Poblado sin nada urgente** — el estado bueno. Debe leerse como "hoy estás bien", no como pantalla vacía
4. **Poblado con acción requerida** — el caso de todos los días
5. **Umbral de red roto** — el semáforo en destructive gana jerarquía sobre todo lo demás
6. **Fuente sin llegar** — anomalía de ingesta, con el corte desactualizado, la causa y el acceso directo a Fuentes. No un cero silencioso

## Preguntas abiertas

1. ¿El operativo es el usuario diario, o el manager también entra? (define densidad)
2. ¿El bloqueo de tarjeta se ejecuta desde Simetrik o solo se marca para ejecutarlo afuera? Cambia si es una acción o una lista de trabajo
3. ~~¿Los umbrales VAMP/ECM siguen vigentes?~~ **Resuelta: no.** VAMP bajó a 1.5% el 1-abr-2026 y hay que corregir el prototipo
4. ¿Las llaves de cruce permiten el ciclo de vida? (Santi)
5. ¿Se dice "monitoreo" o "agente" de cara al usuario?
6. **Nueva:** si el monitoreo puede venir pre-configurado dentro del template, ¿con qué umbrales sale de fábrica? ¿1.5% para las dos redes, o algo más conservador para que avise antes?
