# Copy — Recomendaciones

> Microcopy que materializa la relación **KPI ↔ Dependencia ↔ Fuente ↔ Proceso** en lenguaje de negocio.
> Sigue el glosario obligatorio del skill `ux-writer` Simetrik. **Sin em-dashes (—)**. Sin "Powered by AI".

## 1 · Glosario aplicado a este flujo

| Concepto técnico (banned) | Término del cliente (usar) | Por qué |
|---|---|---|
| Recurso monitoreado | **Fuente** | "Recurso" es opaco. "Fuente" sí está en el glosario Simetrik y el cliente lo reconoce. |
| Dataset (en config de monitoreo) | **Fuente** | En el módulo Op Center "dataset" sí existe como término oficial, pero acá hablamos del nivel ingesta = Fuente. |
| Pipeline | **Cadena del tablero** | "Pipeline" es jerga. "Cadena" es metáfora natural ya que el flujo tiene etapas. |
| Stage | **Etapa** | Más natural en español. |
| Lineage | **Cómo se construye** | Cliente no piensa en "lineage". Sí piensa en "de dónde viene". |
| Anomalía | **Aviso** o **incidente** según severidad | Anomalía la usa el equipo Op Center, no el cliente. Cliente piensa en "algo raro pasó". |
| Threshold / umbral | **Margen** o **rango habitual** | "Umbral" suena técnico. "Margen" es de negocio. |
| Severity | **Importancia** o **prioridad** | Más legible. |
| Dismiss | **Marcar como esperado** | "Dismiss" no traduce. Cliente quiere decir "esto era esperable, no es problema". |
| Schedule / cron | **Horarios** | Plain. |
| Webhook | **Webhook** | Se mantiene (es término técnico que el integrador conoce). |
| Alert rule | **Aviso** | Como entidad: "configurar un aviso", "agregar otro aviso". |

## 2 · Banner del tablero

| Estado | Headline | Sub-line |
|---|---|---|
| Verde | **Tablero listo para analizar** | Última ingesta hace 12 min · 5 KPIs vigilados |
| Verde sin monitoreo | **Este tablero todavía no tiene monitoreo activo** | Activá el monitoreo para enterarte si una Fuente no llega o si un KPI se aleja de lo normal. |
| Amarillo (1 problema) | **1 KPI podría retrasarse hoy** | Falta una Fuente de Banco BBVA · esperada a las 06:30, sin recibir |
| Amarillo (N problemas) | **{N} KPIs podrían retrasarse hoy** | Falta una Fuente de Banco BBVA · esperada a las 06:30, sin recibir |
| Rojo (crítico) | **Tablero con incidente crítico** | El Asiento contable de Tesorería no se conciliará hoy si no llega Mov. BBVA |
| Aprendiendo | **Tu tablero está aprendiendo** | Modo prudente · 4 días para empezar a notificar al equipo |

**CTAs del banner**:
- Verde: `Ver historial` · `Configurar`
- Amarillo o rojo: `Ver incidentes ({N})` · `Configurar`
- Sin monitoreo: solo `Configurar monitoreo →` (grande)

**Pattern del sub-line**: siempre incluir **qué Fuente o KPI específico** está afectado. Nunca decir "hay problemas" sin nombrar.

## 3 · Pipeline visual — labels de cada etapa

| Etapa | Label corto | Sub-label (count) | Estado del cliente |
|---|---|---|---|
| Ingesta | **Ingesta** | "11 de 12 Fuentes ok" | Llegan los archivos del día |
| Calidad | **Calidad** | "1 problema" | Los archivos son válidos |
| Conciliación | **Conciliación** | "al día" | Las Fuentes cruzan bien entre sí |
| KPIs | **KPIs** | "2 de 5 en riesgo" | Tus números están sanos |

**Tooltip al hover de cada etapa** (educativo, no obligatorio leerlo):

- Ingesta: "Vigilamos que tus archivos lleguen a tiempo y con el volumen normal."
- Calidad: "Revisamos que los archivos tengan la estructura esperada y no traigan datos raros."
- Conciliación: "Cruzamos tus Fuentes entre sí para detectar diferencias inesperadas."
- KPIs: "Avisamos si un KPI se aleja del comportamiento normal."

## 4 · Wizard de configuración

### Paso 1 — Activar KPIs

- Título: **¿Qué KPIs querés vigilar?**
- Subtítulo: "Activá los que querés que monitoreemos. Podés ajustar después."
- Recomendación IA: **Te recomiendo monitorear los {N} KPIs de este tablero**.
- Por KPI: nombre + frecuencia ("se calcula cada día") + criticidad ("uso analítico" / "uso para Tesorería" / "uso gerencial").
- Disclaimer madurez: ⚠ **{Fuente} todavía está aprendiendo · 14 días de los 30 necesarios. Activar ahora puede generar avisos falsos.**

### Paso 2 — Dependencias detectadas

- Título: **Estas Fuentes alimentan tus KPIs**
- Subtítulo: "Detecté el lineage automáticamente. Si querés ajustarlo manualmente, podés."
- Diagrama: nombres de Fuentes → nombres de KPIs (sin "node", "edge", "vertex").
- Toggle: **Vigilar todas las Fuentes detectadas ({N})**.
- Link secundario: "Ajustar selección manualmente".

### Paso 3 — Tipos de aviso

- Título: **¿Qué problemas querés que te avisemos?**
- Subtítulo: "Cada aviso está en lenguaje claro · sin umbrales técnicos."
- Agrupado por etapa, una línea por aviso:

| Etapa | Aviso | Descripción que ve el cliente |
|---|---|---|
| Ingesta | Archivo faltante | "Una Fuente no llegó en el horario esperado" |
| Ingesta | Llegada tardía | "Una Fuente llegó más de {tiempo} tarde" |
| Calidad | Volumen anómalo | "Llegaron muy pocas filas comparado con lo normal" |
| Calidad | Cambios estructurales | "Apareció o desapareció una columna" |
| Conciliación | Desalineación | "Encontramos diferencias inesperadas entre dos Fuentes" |
| KPI | Desvío del KPI | "El valor se alejó del comportamiento habitual" |

### Paso 4 — Notificaciones

- Título: **¿Quién y cómo recibe los avisos?**
- Sub-sección "Canales": "Elegí por dónde llegan los avisos".
- Sub-sección "Horarios": "Configurá cuándo no avisar (los problemas críticos llegan igual)".
- Microcopy clave: **"Los problemas críticos se notifican igual, fuera de horario."** (transparente sobre que el silenciamiento tiene límite).

### Paso 5 — Resumen y activación

- Título: **Casi listo · antes de activar**
- Lista de lo que se activa en términos de cliente ("4 KPIs · 4 Fuentes · 6 tipos de aviso").
- Disclaimer madurez ⚠: "Margen operativo no se incluye todavía. Su Fuente lleva 14 días recibiendo datos y el monitoreo necesita 30 días para evitar avisos falsos. Te lo recuerdo el 12 de junio."
- Toggle "Empezar en modo prudente los primeros 7 días": "Te avisamos sin enviar a Slack o Email, mientras validamos que los avisos son precisos."

## 5 · Incidentes — copy del detalle

### Cabecera

```
{Fuente o KPI afectado} {verbo en presente o pretérito reciente}
```

Ejemplos:
- "Mov. BBVA no llegó hoy"
- "Saldo neto día se alejó del rango habitual"
- "Cartera SAP llegó con muy pocas filas"

### Bloques

**¿Qué pasó?** — explica el hecho concreto en 1-2 frases. Mencionar fecha/hora.
> El archivo de Movimientos BBVA debía llegar a las 06:30 y no llegó. Es la primera vez en 30 días.

**¿Qué KPIs afecta?** — lista de KPIs impactados con consecuencia esperada.
> · Saldo neto día · puede atrasarse
> · Conciliación bancaria · puede no completarse hoy

**¿Qué hacer?** — micro-playbook de 1-3 acciones contextuales, no genéricas.
> · Si sabés que el banco está caído, snoozeá 2h y reintentamos.
> · Si esperás carga manual, marcalo como resuelto cuando suba el archivo.

### Acciones (verbo + qué pasa)

| Botón | Tooltip / descripción |
|---|---|
| **Snooze 2h** | "Volvemos a avisarte si sigue el problema en 2h" |
| **Resolver** | "Marcalo como resuelto · queda en el historial" |
| **Escalar** | "Notifica a la persona responsable del tablero" |

## 6 · Overrides — copy clave

**Header del modal/Sheet**:
> {Nombre del KPI o Fuente} — ajustes propios

**Subtítulo**:
> Estos ajustes solo aplican a {nombre}. La configuración general del tablero sigue activa para el resto.

**Sección "Configuración heredada"** (en gris, no editable):
> Configuración general del tablero:
> · Notifica a finanzas@empresa.com
> · No notifica entre 22:00 y 07:00

**Sección "Sobrescribir para este KPI"** (editable, marca visualmente que es override):
> [☑] Notificar también a: cfo@empresa.com
> [☑] Notificar siempre, incluso fuera de horario
>     "Tesorería necesita saberlo en cualquier momento"

**Botón "Quitar overrides"**:
> Vuelve a la configuración general del tablero.

## 7 · Toasts y feedback

| Acción | Toast |
|---|---|
| Activar monitoreo | ✓ Monitoreo activado · empezamos a aprender |
| Activar en modo prudente | ✓ Monitoreo activado en modo prudente · 7 días |
| Guardar override | ✓ Override guardado para {nombre} |
| Quitar override | ✓ {nombre} vuelve a la configuración general |
| Snooze incidente | ✓ Snoozeado · te avisamos a las {hora} si sigue |
| Resolver incidente | ✓ Resuelto · queda en el historial |
| Escalar incidente | ✓ Notificamos a {persona/canal} |

## 8 · Empty states

| Vista | Headline | Sub-headline | CTA |
|---|---|---|---|
| Sin monitoreo activo | **Empezá a vigilar tu tablero** | El agente IA puede proponerte una configuración inicial en menos de un minuto. | "Configurar con la IA" / "Configurar yo mismo" |
| Sin KPIs vigilados | **No tenés KPIs vigilados todavía** | Activá los que querés que monitoreemos. | "Activar primer KPI" |
| Sin Fuentes vigiladas (KPIs vigilados) | **Aún no se detectaron Fuentes** | Mientras llegan los primeros archivos, no podemos mostrar dependencias. | (sin CTA) |
| Sin incidentes | **Sin incidentes · todo bajo control** | Cuando algo se salga de lo normal te lo mostramos acá. | "Ver historial" |
| Sin historial | **Tu tablero todavía no ha tenido incidentes** | Tu tablero estaba bien todo el período seleccionado. | (sin CTA) |

## 9 · Voz del agente IA

**Tono**: colaborador, no autoritario. Habla en primera persona ("yo detecté", "te recomiendo") cuando hace acciones específicas. Plural editorial ("vigilamos", "te avisamos") cuando habla del sistema.

**Cuándo aparece**:
- En recomendaciones de configuración: "Te recomiendo monitorear estos 5 KPIs."
- En explicaciones del lineage: "Detecté que esta Fuente alimenta 2 KPIs."
- En disclaimers de madurez: "Esta Fuente todavía está aprendiendo · 14 días de los 30 necesarios."

**Cuándo NO aparece**:
- En errores del sistema (eso es el sistema, no la IA).
- En confirmaciones de acciones del usuario ("Override guardado" no necesita IA voice).
- Como mascota / personaje. **No hay nombre de bot, no hay avatar de IA.**

**Banned phrases**:
- "Powered by AI"
- "Tu asistente inteligente"
- "Magia"
- "Inteligente" como adjetivo solo (todo es inteligente)
- "Smart alerts" / "Smart rules"
- Cualquier ✨ sparkle emoji
