# Plan — Notificaciones de incidentes (modelo de paquetes), filtros y cambios de UI

**Fuente:** sesión de feedback **30-jun-2026, 10:43 AM** · "Filtros de anomalías y configuración de notificaciones — épicas y cambios de UI"
**Prototipo afectado:** `notificaciones-resumen/index.html` (vista de Anomalías → Configuración → Notificaciones de incidentes + filtros de la vista de Gestión)
**Estado:** acuerdos para ejecutar · este plan **reemplaza** la parte de "Notificaciones de incidentes" del plan del 26-jun (`plan-alertas-vs-notificaciones-26jun.md`). La parte de **Alertas / KPI** de ese plan sigue vigente y **ya quedó resuelta**.
**Pendiente:** repaso con Cami (último día) y visto bueno antes de entregar a Edith.

---

## Cambio de paradigma — la notificación es un PAQUETE, no una config global

> Antes lo pensábamos como **una** configuración de notificaciones de incidentes (una sola pantalla, "mis incidentes"). **Cambió.** Ahora es un modelo de **paquetes / reglas de notificación**: el usuario crea **varios paquetes**, cada uno con su propio filtro + reglas. Un incidente se evalúa contra **todos los paquetes activos**; si machea varios, se notifica por todas esas vías.

Analogía del equipo (la misma de Gmail): *"Llega un incidente nuevo → tiene un montón de etiquetas (de qué dashboard, qué fuentes, qué severidad). Esas etiquetas se cruzan con el filtro de cada paquete. ¿Machea? Sí → notifica. No → no notifica."*

**Por usuario, no global.** Cada quien arma sus propios paquetes. Puedo ver los paquetes de mis compañeros y **sumar mi correo** a uno existente, o **crear el mío**. Default: quien configura el paquete es quien lo recibe (evitar spam: no auto-suscribir a terceros).

---

## Las épicas (separadas a propósito, para ejecución)

El equipo insistió en separarlas porque, mezcladas, los cambios chicos se pierden en desarrollo.

| # | Épica | Naturaleza | Estado |
|---|---|---|---|
| **1** | **Filtros de anomalías** (en la vista de Gestión) | ~100% frontend, algo de backend | Por hacer (rework) |
| **2** | **Paquetes de notificación de incidentes** | frontend + notificaciones + poco backend | Por hacer (rework del formulario) |
| **3** | **Resumen consolidado** | propiedad del paquete | Por hacer (mover dentro del paquete) |
| **4** | **Alertas en KPIs / Ingesta** (cambio de config) | ya resuelto en el lado del KPI | KPI ✅ · Ingesta pendiente |
| **UI** | **Cambios de UI** (épica aparte, enumerada) | frontend | Parcial |

> Andres lo resumió: *"Yo tengo filtros, la creación de notificaciones y la del resumen. En filtros se crean los filtros múltiples (concatenados) y los filtros recurrentes (guardados); eso se conecta con la creación de notificaciones porque uso esos filtros guardados para mi paquete."*

---

## ÉPICA 1 — Filtros de anomalías (vista de Gestión)

### 1a. Filtros múltiples con lógica correcta
- **Dentro de cada categoría → multiselect, unión con `O` (OR).** Ej: recurso ∈ {fuente A, fuente B, fuente C}.
- **Entre categorías distintas → `Y` (AND).** Ej: `recurso ∈ {...}` **Y** `tipo ∈ {...}` **Y** `estado ∈ {...}`.
- Cada vez que agrego una categoría nueva, se **concatena con `Y`**; las opciones dentro de una categoría se concatenan con `O`.
- ⚠️ **Producción hoy NO soporta multiselect dentro de cada filtro.** Es un cambio nuevo que hay que **documentar explícitamente** en el handoff/Figma (si no, no se ejecuta).
- En el prototipo: mostrar visualmente la lógica (ej. chip compuesto "Recurso: A o B o C" y entre chips se lee como Y).

### 1b. Filtros que se mantienen (catálogo)
Mantener **recurso, tablero, estado del incidente, tipo de incidente**. Conviene mantenerlo **sencillo** para entregar más funcionalidad.

- **Recurso** — multiselect (fuentes)
- **Tablero** — multiselect
- **Estado del incidente** — multiselect (creado/abierto/confirmado…)
- **Tipo de incidente** — multiselect (problem categories de BADS de Ingesta: Archivo faltante, fallido, vacío, duplicado, Variación de volumen)
- **Fecha** — se mantiene (rango temporal, naturaleza distinta)

> **QUITAR del filtro: Severidad.** Decisión del equipo: *"no pongas ese filtro hasta que el usuario pueda definir sus propios niveles de severidad."* Filtrar por una severidad que el usuario no puede configurar/calcular es contraproducente. **Severidad vuelve cuando sea configurable** (otra historia).

### 1c. Filtros recurrentes (guardados)
- Poder **guardar** un filtro para reutilizarlo (ej. "Incidentes Sergio" = solo incidentes de ciertos recursos).
- Es la misma personalización de la **vista** de incidentes: lo que guardo para ver, lo reutilizo para notificar.
- ⚠️ **Ojo, matiz importante:** en una iteración anterior quité "guardar filtros" porque Cloud lo había metido como automatización. **Ahora el equipo SÍ lo quiere**, pero como feature limpio y separado (feature 1 = crear+guardar filtros; feature 2 = armar paquetes que reusan esos filtros guardados). No es automatización de filtros; es guardar/nombrar un filtro.

---

## ÉPICA 2 — Paquetes de notificación de incidentes (rework del formulario)

> Reemplaza el formulario actual de `#anCfgNotif`. La pantalla debe verse como **una lista de tarjetas-paquete** (cada tarjeta = una regla de notificación), con un botón "Crear notificación / nuevo paquete". Cada paquete se compone de **3 bloques que NO se interfieren** + canales + (opcional) resumen.

### Bloque 1 — Scope ("Notifícame incidentes sobre…") — el filtro del paquete
> 💬 Ohana (cmt 3): *"notifícame incidentes sobre — cuál es el scope con `-o-` (es en forma de filtrar o parametrizar los valores que me interesan que se cumplan)."*
- Título en clave de copy: **"Notifícame incidentes sobre…"**
- Selecciono **fuentes / tableros / charts** (multiselect, unión `O`).
- Es literalmente **filtrar/parametrizar los valores que me interesan que se cumplan** — el scope ES un filtro.
- *"Si pasa algo en alguno de este conjunto de cosas → aplica."*
- **Reutiliza los filtros guardados de la Épica 1**: puedo traer "Incidentes Sergio" o armar uno nuevo aquí mismo.
- 💬 Ohana (cmt 2, sobre el ítem de nav): *"la configuración es la suma de los filtros que el usuario configure"* → el paquete entero se entiende como la suma de filtros.

### Bloque 2 — "¿En qué punto de la vida del incidente quieres ser notificado?"
> 💬 Ohana (cmt 4): *"en qué punto de vida de incidente quieres ser notificado."*
- Título en clave de copy: **"¿En qué punto de la vida del incidente quieres ser notificado?"**
- **2 opciones** (no checkboxes sueltos mezclados): **al crearse** / **al confirmarse**.

### Bloque 3 — ¿Updates?
- Toggle: **¿quieres recibir updates del incidente?** (reconfirmaciones, cambios de hipótesis, otros recursos afectados, sube severidad).

### (Posible 4º factor) — Severidad
- **Posponer.** Mismo motivo que el filtro: hasta que la severidad sea configurable por el usuario. No incluir aún.

### Canales (¿dónde notificar?)
- Correos + canales de Slack del paquete.
- **Anti-spam:** por default, quien configura el paquete es quien recibe. Sumar terceros es explícito (editar el paquete y agregar su correo).

### QUÉ QUITAR del formulario actual (lo que Cloud sobre-pintó)
El formulario que está hoy en `#anCfgNotif` mezcla cosas que el equipo descartó:

1. ❌ **"Cuando la severidad sea alta"** — fuera (severidad pospuesta).
2. ❌ **"Cuando no tenga responsable asignado"** — fuera de scope ahora.
3. ❌ **"Cuando me etiqueten"** — es otra clase de notificación (**flujo de la app**: "te asignaron / te etiquetaron un incidente"), con su propio template. **No se configura aquí.** El equipo decidió no apostar ese scope por ahora.
4. ❌ **"Qué incluir en la notificación" (Hipótesis / Acción recomendada / Resumen / narrativa)** — **fuera.** Eso va **directo en el template** que construimos (Block Kit / email), no es configurable por el usuario aquí.
5. ❌ **El "filtro reutilizado" como bloque informativo pasivo** ("ya sé que tienes un filtro, agrupo lo que tienes") — se reemplaza por el **Bloque 1 (scope) activo** que reusa filtros guardados.
6. ➡️ **Convertir** "¿Cuándo notificarme?" (5 checkboxes) en: 2 opciones de momento + toggle de updates (Bloques 2 y 3).

---

## ÉPICA 3 — Resumen consolidado (sección propia en el nav)

> 💬 **Ohana (cmt 0 + cmt 1):** *"esto va para resumen"* (sobre la tarjeta de Resumen consolidado del formulario actual) + *"crear uno nuevo de resumen"* (sobre el nav de Configuración).
>
> **Decisión de UI:** el Resumen consolidado **sale del formulario de Notificaciones** y pasa a ser un **ítem propio en el nav de Configuración** (junto a "Ingesta de datos" y "Notificaciones de incidentes").

- **Quitar** la tarjeta "Resumen consolidado" de `#anCfgNotif`.
- **Agregar** un ítem **"Resumen"** en `an-confnav` con su propia página de config.
- Por qué separado: es **otra cosa** que las notificaciones individuales — éstas son granularidad de evento (al crearse/confirmarse); el resumen es **1×día**. No deben mezclarse en el mismo formulario.
- Config del resumen: hora de llegada, zona horaria, e incluir ("solo abiertos y urgentes" / "todos mis incidentes").
- **Matiz con el modelo de paquetes:** conceptualmente el resumen sigue ligado al scope/paquete del usuario (es un resumen *de los incidentes que le importan*). En el UI, vive en su propia sección; al definirlo, reutiliza el mismo scope/filtros. (Reconcilia "propiedad del paquete" de Granola con "sección propia" de Ohana: misma data, entrada de nav separada.)

---

## ÉPICA 4 — Alertas en KPIs / Ingesta

- **KPI:** ya resuelto (reframe a "Alertas", ¿cuándo notificar?, sensibilidad). ✅
- **Ingesta:** pendiente — al activar el monitoreo de una fuente, poder **configurar sus alertas** (ventana + tipo). Vive en la vista de Ingesta de datos. (Pendiente del plan anterior, sigue válido.)
- Paradigma: **KPIs por su lado, incidentes por su lado.** Son distintos y no se mezclan.

---

## ÉPICA UI — Cambios de UI (enumerados, no se pueden saltar)

> El equipo fue enfático: **hay que enumerar cada cambio de UI explícitamente** (notas amarillas grandes en Figma / lista de criterios claros). Los cambios chicos pasan desapercibidos y no se ejecutan. El skill de handoff de Andres captura esto a medida que avanza.

Cambios ya hechos en el prototipo (confirmar que queden enumerados en el handoff):
- ✅ "Historial" → **"Alertas levantadas"** (+ columna "¿Notificada?").
- ✅ "Notificaciones" → **"Alertas"** en toda la vista del KPI.
- ✅ Botón **"Resumen de incidentes"** sacado del tablero → reubicado en Anomalías.
- ✅ Botón de **configuración** reubicado en la vista de Anomalías.
- ✅ Segmented Gestión · Historial(Alertas levantadas) · Configuración; iconos del top.

Cambios de UI por documentar/hacer:
- 🔲 **Multiselect dentro de cada filtro** (prod no lo soporta → cambio nuevo, documentar).
- 🔲 **Quitar filtro Severidad** (de la vista de Gestión y del paquete) hasta que sea configurable.
- 🔲 **Rework del formulario de notificaciones** → modelo de paquetes (lista de tarjetas); copy de bloques: "Notifícame incidentes sobre…" / "¿En qué punto de la vida del incidente…?".
- 🔲 **Resumen consolidado** → sacarlo del formulario y crear **ítem "Resumen" propio en el nav** de Configuración (Ohana cmt 0+1).
- 🔲 Revisar **tarjeta de incidente** en Gestión: hay diferencias con prod; si las hay, van como **épica de fixes de UI aparte** (cambiar aquí/allá, enumerado).
- ⛔ ~~Unificar construcción de títulos~~ → **fuera del prototipo**: se resuelve a nivel de la **respuesta del API/backend** (cómo se arma el título del incidente). No es UI.
- 🔲 Documentar **"qué hace hoy notificaciones y qué va a dejar de hacer"** (estado actual vs nuevo).

---

## Cómo se evalúa (para tener en mente, no es de este prototipo)

Los incidentes son eventos. Dos formas equivalentes:
1. **En tiempo real:** llega evento (creación / update) → se pasa por la lista de reglas de todos los paquetes → a quién machea, se notifica.
2. **Proceso por lotes (cada hora):** revisa qué hay por notificar y notifica.

Regla de oro de filtros: **las condiciones no pueden ser contradictorias** (si das condiciones que resultan en cero, no recibes nada — igual que un filtro de Gmail).

---

## Fuera de scope ahora (documentado para no perderlo)

- **Notificaciones de flujo de la app** ("te asignaron / te etiquetaron un incidente") — otro tipo de notificación, otro template. No se apuesta ese scope ahora.
- **Severidad** como filtro y como condición de notificación — vuelve cuando el usuario pueda definir sus propios niveles.
- **Preview "con esta config tendrías X notificaciones"** — idea buena pero deprioritizada (depende de cuántos incidentes haya; no tan disponible aún).
- **Asignación manual de incidentes** — hoy no existe asignar incidente a alguien.

---

## Preguntas abiertas / a validar

- **Visto bueno de Cami** (último día) antes de entregar a Edith — repaso ~3pm.
- **Lógica de evaluación** (tiempo real vs lote cada hora) — definición de eng (Ayed/Iván).
- ⚠️ **Heredado:** confirmación de incidente "al cierre de la ventana" vs **workflow runner** (validar con Iván).
- Filtros guardados: ¿alcance del backend? El equipo cree que es casi 100% frontend + poco backend; Ayed puede ayudar.

---

## Impacto sobre lo ya construido en este prototipo

| Elemento actual | Acción |
|---|---|
| `#anCfgNotif` (formulario de 4 tarjetas) | **Rework** → modelo de paquetes (lista de tarjetas-regla; 3 bloques + canales + resumen como propiedad) |
| Checkboxes "severidad alta / sin responsable / me etiqueten" | **Quitar** |
| Tarjeta "Qué incluir" (hipótesis/acción/narrativa) | **Quitar** (va en el template) |
| Filtros de Gestión | **Multiselect (O dentro / Y entre)** + **guardar filtros** + **quitar Severidad** |
| Resumen consolidado (tarjeta suelta en `#anCfgNotif`) | **Sacar** y crear **ítem "Resumen" en `an-confnav`** con su propia página (Ohana cmt 0+1) |
| Bloque scope / Bloque momento | Copy: **"Notifícame incidentes sobre…"** y **"¿En qué punto de la vida del incidente…?"** (Ohana cmt 3, 4) |
| Handoffs | Actualizar: enumerar cada cambio de UI; crear handoff de **paquetes de notificación** |
