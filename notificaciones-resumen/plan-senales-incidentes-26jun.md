# Plan de ajustes — Notificaciones y monitoreo (señales, incidentes y sensibilidad)

**Fuente:** sesión de feedback del **26-jun-2026** · "Notificaciones y monitoreo — configuración de señales, incidentes y sensibilidad"
**Prototipo:** `notificaciones-resumen/index.html` (diálogo de monitoreo del KPI)
**Estado:** 🟡 en ejecución · bloque "¿Cuándo notificar?" reconstruido (sesión 26-jun pm) · resto pendiente
**Participantes clave del feedback:** Iván (notificaciones/backend), Vicky (incidentes), Andres (diseño)

> **Avance al 26-jun (cierre de sesión de diseño):** ver sección [Construido esta sesión](#construido-esta-sesión-26-jun-pm) al final. En corto: el bloque ¿Cuándo notificar? se rehízo con un eje de timing de 3 estados + barra explicadora + empty state. Los P0 #2 y #3 quedan cubiertos en la UI; el P0 #1 se **reenfocó** (no dos bloques, sino un eje único). P1/P2 siguen pendientes.

---

## TL;DR

El gran tema de la sesión es que **hoy todo se configura sobre "señales" en un solo panel, y el usuario no entiende cómo eso se relaciona con los incidentes**. La UI funciona cuando alguien la explica de viva voz, pero "configurando esto, no me imaginaría que el sistema de notificación funciona así" (Iván). Hay que:

1. **Separar la configuración de señales de la de incidentes** (lo más importante).
2. **Hacer explícito el modelo mental señal → incidente → cierre de ventana** en la propia pantalla.
3. **Notificar el ciclo de vida completo** del incidente, no solo el primer trigger.
4. Pulir destinatarios (internos vs externos + duplicados), wording de "Resumen diario", feedback visual de la sensibilidad y, a futuro, **sacar la config del modal a página completa**.

---

## Modelo mental acordado (la base de todo)

Esto es lo que el sistema hace, y lo que la UI debe comunicar:

```
KPI monitoreado
   └─ genera SEÑALES (alertas tempranas, ruidosas: "subió", "faltó", "se arregló")
        └─ N señales se agrupan en un INCIDENTE
             └─ el incidente se CONFIRMA solo al cerrar la ventana de monitoreo
                  (si al cerrar el problema sigue activo → incidente confirmado)
```

- **Señales** = alertas tempranas, más ruidosas. Siempre se generan y se ven en el monitor in-app; solo se notifican vía Email/Slack si el usuario lo activa.
- **Incidente** = el paquete completo ("te faltan archivos de tal fuente, impacta tal tablero"). Se confirma **al cierre de la ventana**, no antes.
- Hoy el panel de notificaciones **solo configura las señales del KPI**. Falta la pata de incidentes.

---

## Ajustes priorizados

### 🔄 P0 — Separar señales e incidentes en dos configuraciones · **REENFOCADO (no se hará así)**

> **Decisión 26-jun:** en el discovery se descartó hacer dos bloques. Se optó por **un solo eje de timing** (Nunca / Solo al final / En tiempo real) donde **señales e incidentes van siempre juntos**; lo que cambia es el *cuándo*, no el *qué*. Esto resuelve la confusión de raíz (el usuario ya no configura "solo señales") sin partir la UI en dos. **Quedaron fuera** (no se diseñaron): los criterios de incidente por *severidad* y *antigüedad >1 día*, y el control "notificar solo cuando se confirme el incidente / apagar señales". Si el equipo quiere recuperarlos, vuelven a ser pendientes.

**Feedback:** "esa separación entre señales e incidentes... acá solamente estás configurando la tabla individual de las señales. Hay que separarlo en que incidentes tenga su propia configuración también."

**Estado actual:** ~~`¿Cuándo notificar?` (Nunca / Solo al cierre / Todo el tiempo) gobierna todo desde un solo bloque~~ → reemplazado por el eje de timing de 3 estados (Nunca / Solo al final / En tiempo real); señales+incidentes unificados.

**Propuesta:**
- Dos bloques de configuración claramente rotulados:
  - **Señales (alertas tempranas)** → "más ruidosas; actívalas solo en KPIs muy puntuales que te interesan". Toggle on/off + frecuencia (Todo el tiempo / Solo al cierre / Nunca).
  - **Incidentes (confirmados)** → criterios de cuándo notificar: *cuando se confirme*, *cuando la severidad sea alta*, *cuando lleve más de un día abierto*, etc.
- **Opción puente:** un control tipo "Notificar solo cuando se confirme el incidente" que **automáticamente apaga las señales** ("eso ya le mata las señales").
- Lógica clara: si no notificas incidentes → solo recibes señales; si no notificas señales → solo recibes el incidente confirmado.

**Owner sugerido:** Diseño (estructura) + PM (criterios de incidente).

---

### ~~🔴 P0 — Hacer explícito el modelo señal → incidente → cierre~~ · ✅ HECHO (26-jun)

> **Resuelto en la UI:** la **barra de la ventana de monitoreo es el explicador** — cada notificación es un punto ubicado a la hora en que llegaría, con tooltip (Señal / Incidente abierto / Reconfirmado / Resuelto). Más una **línea descriptiva por modo** debajo de la barra. El contraste visual (1 punto en "Solo al final" vs varios en "En tiempo real") enseña el modelo mostrando el resultado, no la teoría.

**Feedback:** "todo eso queda claro de vos explicándolo, pero configurando esto no me imaginaría que funciona así."

**Propuesta (✅ implementada):**
- ~~Microcopy / diagrama corto que explique la cadena señal → incidente → confirmación al cierre.~~ → barra con marcadores + tooltips + línea por modo.
- Significado de cada modo en términos del ciclo de vida:
  - ~~**Todo el tiempo**~~ → **En tiempo real**: "cada cambio de estado, a medida que ocurre" (stream completo).
  - ~~**Solo al cierre**~~ → **Solo al final**: "el estado final al cerrar la ventana; si se resolvió antes, no llega nada."
- ~~Conectar visualmente con la **ventana de monitoreo**~~ → la barra ES la ventana, con badges (Diario · 08–20 · Bogota) y acceso a Programación.

**Owner:** Diseño + UX Writing (copy fino pendiente de pulir).

---

### ~~🔴 P0 — Notificar el ciclo de vida completo del incidente~~ · 🟡 CASI (falta 1 microcopy)

> **Resuelto en la representación de los modos:** "En tiempo real" muestra el stream completo (apertura → reconfirmado → resuelto); "Solo al final" muestra el estado final al cierre. El ciclo de vida ya se ve en los marcadores/tooltips de la barra.
> **Falta:** actualizar el microcopy de las tarjetas Email/Slack (~L2181, L2203) que aún dice "cuando el monitoreo detecte un incidente" (sugiere disparo único). ⚠️ **Validar con Iván** qué estado reporta BADS al cierre (confirma por workflow runner, no estrictamente al cerrar).

**Feedback:** "hoy la notificación solo se envía en el primer trigger... si se resuelve a las dos horas, el usuario nunca recibió el cambio."

**Propuesta:**
- ~~Modo **Todo el tiempo** = stream de updates (apertura, reconfirmación, resolución).~~ ✅ "En tiempo real"
- ~~Modo **Solo al cierre** = un único aviso con el estado final.~~ ✅ "Solo al final"
- ~~La **confirmación del incidente ocurre solo al cerrar la ventana**~~ ✅ reflejado en copy ⚠️ a validar con Iván
- ⬜ Ajustar microcopy de las tarjetas Email/Slack (~L2181, L2203) para reflejar updates, no un único disparo. **(pendiente)**

**Owner sugerido:** Diseño (copy/estados) + Ingeniería (comportamiento backend).

---

### 🟡 P1 — Destinatarios: internos vs externos + duplicados

**Feedback:** hoy solo hay **externos** (tipear email, pegar canal de Slack). Iván propone que en "Notificar" se pueda elegir **usuario de la plataforma / correo / canal de Slack**:
- Usuario interno → el sistema resuelve su email + in-app según las preferencias del propio usuario (modelo tipo Facebook: el usuario decide dónde recibir cada tipo).
- Riesgo: si agrego un usuario interno **y además** su correo a mano → **doble notificación** ("se envían por dos cajas distintas; esa validación no existe").

**Estado actual:** solo externos — `Destinatarios` (email, ~L2187) y `Canales` Slack + tag por ID (~L2208).

**Propuesta:**
- Explorar agregar **"usuario de la plataforma"** como tercer tipo de destinatario (combo del workspace; no hay que saber su email).
- Mostrar **aviso/validación de duplicados** cuando un email coincida con el de un usuario interno ya seleccionado.
- ⚠️ **Bloqueante de diseño:** confirmar con Ingeniería cómo se almacena hoy (email/Slack se guardan separado "para que no se pise") antes de cablear la UI de internos. Por ahora puede quedar solo externo, pero dejar el espacio previsto.

**Owner sugerido:** Diseño + Ingeniería (verificación técnica primero).

---

### ~~🟡 P1 — Wording de "Resumen diario"~~ · ✅ HECHO (26-jun)

> **Resuelto:** botón corto = **"Resumen de incidentes"** (la cadencia y el alcance viven en el menú). Popover: título "Resumen diario de incidentes" + subtítulo "Todos los días, **a la hora que elijas**, recibes un resumen de los incidentes **de este tablero** que siguen abiertos, por los canales donde ya recibes avisos." Glosario aplicado (Incidente), sin copy de IA/agente, y sin "cada mañana" (la hora es configurable).

**Feedback:** "el 'Resumen diario' parece como que es del tablero. Hay que poner un poco mejor el wording" — es el resumen de **anomalías/incidentes abiertos**, no del tablero.

**Estado actual:** ~~botón `Resumen diario`~~ → **Resumen diario de incidentes** (botón ~L1765, popover ~L1773).

**Propuesta:**
- Renombrar para dar contexto de monitoreo, p. ej. **"Resumen diario de incidentes"** o **"Resumen diario de monitoreo"**.
- Mantener el subtítulo que explica: aviso al inicio del día con los incidentes que siguen abiertos del día anterior.
- Nota: el resumen **no lo genera una IA** (decisión deliberada para no interferir); reutiliza los textos ya generados de cada incidente. No introducir copy que implique "agente/IA" (consistente con la convención del proyecto).

**Owner sugerido:** UX Writing.

---

### 🟡 P1 — Sensibilidad: reforzar el feedback visual en la gráfica

**Feedback:** Iván entendió el contador de abajo ("hubieras recibido N señales") pero **no vio que la línea/banda de la gráfica también se movía** al arrastrar el slider.

**Estado actual:** slider de sensibilidad + gráfica (`#sens-chart` ~L2290) + footer de impacto. Funciona, pero el cambio en la gráfica pasa desapercibido.

**Propuesta:**
- Hacer **evidente** el cambio en la gráfica al mover el slider (animar el umbral punteado / resaltar los puntos que entran-salen, transición visible).
- Mantener el contador derivado y, si se puede, marcar visualmente los puntos que habrían disparado señal.
- Reafirmar en copy: **sensibilidad 0 = alarma estándar de umbral fijo** (solo notifica si supera el máximo); a mayor sensibilidad, más adaptativo. Hacer explícito que 0 = hard limit (no es obvio en la UI).

**Owner sugerido:** Diseño (interacción) + Frontend.

---

### 🟢 P2 — Sacar la configuración del modal a página completa

**Feedback:** "¿por qué un modal? Aprovechemos la pantalla. Me mostraste el feed y ni me imaginé que abajo había un control por cada serie." La sensibilidad por serie queda oculta por scroll dentro del modal.

**Estado actual:** toda la config vive en un modal que escaló más allá de lo que aguanta.

**Propuesta:**
- A futuro: al hacer clic en la tarjeta del KPI, **reemplazar la lista por el contenido de configuración en página completa**; al cerrar, volver a la lista (misma experiencia, más espacio).
- **No bloquea el release actual** ("queda modal por ahora"), pero queda como principio: no ir por modal como primera opción cuando la config escala.

**Owner sugerido:** Diseño (próxima iteración).

---

### 🟢 P2 — Etiquetado @ en Slack (contexto técnico)

**Feedback:** para @mencionar en Slack hace falta el **Slack user ID** (`U0...`) vía Block Kit; el sistema no tiene el mapping usuario-plataforma ↔ usuario-Slack. Escribir `@nombre` a mano llega como texto y no notifica.

**Estado actual:** ya resuelto en el prototipo — campo "Etiquetar a personas" pide el ID con helper de cómo obtenerlo (~L2216). ✅

**Acción:** ninguna de diseño; mantener. Si a futuro se quiere @mención por nombre, requiere que Ingeniería guarde el ID de Slack al integrar (fuera de alcance ahora).

---

## Temas fuera del prototipo (registrar, no diseñar aquí)

- **Integración Slack/Webhooks/Jira** se hace desde **Manage** (admin). Hoy solo admins entran a Manage; hay que revisar (tema con Tony) que ciertos usuarios necesiten acceso a Manage sin ser admins plenos. → Producto/permisos.
- Email viene por defecto (CES propio); webhooks y Jira a futuro vía el mismo patrón de integración.

---

## Resumen de acciones

| # | Ajuste | Prioridad | Estado | Owner |
|---|--------|-----------|--------|-------|
| 1 | ~~Separar config de señales vs incidentes~~ → eje único de timing | 🔴 P0 | 🔄 Reenfocado (criterios severidad/antigüedad fuera) | Diseño + PM |
| 2 | Hacer explícito el modelo señal→incidente→cierre | 🔴 P0 | ✅ Hecho (barra explicadora) | Diseño + UX Writing |
| 3 | Notificar ciclo de vida completo del incidente | 🔴 P0 | 🟡 Casi (falta microcopy Email/Slack + validar Iván) | Diseño + Ing |
| 4 | Destinatarios internos + validación de duplicados | 🟡 P1 | ⬜ Pendiente | Diseño + Ing (verif. técnica) |
| 5 | ~~Wording "Resumen diario"~~ → "Resumen diario de incidentes" | 🟡 P1 | ✅ Hecho | UX Writing |
| 6 | Feedback visual de sensibilidad + copy "0 = umbral fijo" | 🟡 P1 | ⬜ Pendiente | Diseño + FE |
| 7 | Migrar config de modal a página completa | 🟢 P2 | ⬜ Futuro | Diseño (próx. iter.) |
| 8 | Tag @ Slack por ID | — | ✅ Hecho | — |
| 9 | **Empty state de primer ingreso** (no estaba en el plan) | extra | ✅ Hecho | Diseño |

### Qué falta (lista corta)
- ⬜ **Microcopy** de las tarjetas Email/Slack (ciclo de vida, no disparo único) — P0 #3.
- ⚠️ **Validar con Iván**: estado real que reporta BADS al cierre (afecta copy "estado final").
- ⬜ **P1**: destinatarios internos + duplicados · feedback visual de sensibilidad. (~~wording "Resumen diario"~~ ✅ hecho)
- ⬜ **P2**: modal → página completa.
- ❓ **Decidir**: si se recuperan los criterios de incidente (severidad / antigüedad) que quedaron fuera del eje único.

---

## Construido esta sesión (26-jun pm)

Bloque **¿Cuándo notificar?** reconstruido en `index.html` (diálogo de monitoreo → Notificaciones):

- **Selector de 3 estados de timing** con íconos de campana: Nunca (`bell-off`) · Solo al final (`bell`, recomendado) · En tiempo real (`bell-ring`). El ícono del estado activo aparece también en el botón del selector.
- **Barra de la ventana de monitoreo como explicador**: cada notificación es un punto sobre la línea de tiempo, ubicado a su hora, con tooltip al hover. Reusa `winrec-*`.
- **Línea descriptiva por modo** debajo de la barra.
- **Empty state de primer ingreso** (`whenMode='unset'`): "Aún no configuras las notificaciones" + CTA "Configurar notificaciones" (configura con el recomendado "Solo al final"). Hasta configurar, ¿Dónde?/Idioma quedan atenuados.
- **En "Nunca"** se ocultan barra y Programación; queda solo la explicación.
- **Caja** con el mismo gris clarito de Email/Slack (`hsl(var(--muted)/0.5)`, sin borde).
- Limpieza: se eliminó el contador "N avisos", la leyenda (su info pasó a tooltips), y CSS/JS muerto (`winrec-fill`, `winrecPulse`, etc.).

Archivo de apoyo usado para iterar: `preview-cuando-notificar.html` (sandbox; se puede borrar).

---

## Cadencia acordada
> "Esta semana dejamos andando, la otra semana ejecutamos." → Cerrar P0/P1 de diseño esta semana para handoff la próxima.
