# Plan — Alertas (señales) vs Notificaciones de incidentes · separación y scope

**Fuente:** sesión de feedback **26-jun-2026, 4:42 PM** · "Notificaciones de señales e incidentes — configuración y scope"
**Prototipo afectado:** `notificaciones-resumen/index.html` (diálogo de monitoreo del KPI / chart)
**Estado:** acuerdos finales del equipo · plan para modificar el UI de este prototipo
**Decisión macro:** separar por completo **Alertas** (señales) de **Notificaciones de incidentes**. Hoy van mezcladas y eso confunde.

---

## TL;DR — el acuerdo en una frase

> Las **Alertas** (señales) se configuran **donde vive el KPI / la métrica / la ingesta** (este prototipo). Las **Notificaciones de incidentes** se configuran en la **vista de Anomalías**. Son dos features distintos, con distinto template, distinto propósito. **No se mezclan.**

Analogía del equipo: *"Signal = tu alarma (tipo Datadog monitors: si supera el umbral, mándame un Slack). Incidente = otra entidad, otro artefacto — es la relación chart↔dashboard. Configurar uno no debería disparar el otro."*

---

## Modelo y glosario (lo que se acordó)

| Concepto | Qué es | Dónde se configura | Template / output |
|---|---|---|---|
| **Alerta** (= señal de anomalía) | "El valor de un KPI salió de su rango esperado, fin." Definición idéntica a una *señal*: fuera del mín/máx + sensibilidad que el usuario definió. Trivial, para **mantenerte informado**. | **En el KPI / métrica** (este diálogo, desde el monitoreo del tablero) y **en Ingesta de datos / Fuentes** | Alerta simple (valor fuera de rango) |
| **Notificación de incidente** | Paquete "masticado": correlación, hipótesis, acción recomendada, narrativa IA, severidad. Es **gestión**. Una señal **no** crea siempre un incidente. | **En la vista de Anomalías** (página de configuración propia) | Notificación de incidente (rica, configurable) |

**Frases clave de la sesión:**
- *"Todo lo que el usuario configura en el monitoreo del KPI se entiende como **signals** → pongámosle el branding: **estas son tus alertas**."*
- *"Si quiero ser notificado de mis incidentes, es porque entré a mi vista de Anomalías → configuración → y ahí veo 'usted quiere ser notificado de esto que le mostramos'."*
- *"Una señal no necesariamente crea un incidente. Las alertas son el día a día para mantenerte informado; los incidentes son management."*

---

## Acuerdos finales

1. **Separación total.** En el KPI se configuran **Alertas (señales)**. Las **Notificaciones de incidentes** salen de aquí y viven en **Anomalías**.
2. **Quitar las notificaciones de incidentes que hoy se disparan desde el chart.** Hoy, al configurar monitoreo en un chart, el usuario **ya** empieza a recibir notificaciones de incidente sin haberlo pedido → está mal. **Por default, apagadas** aquí.
3. **Ingesta / Fuentes también configura alertas.** Al configurar la ingesta de una fuente se setea su **ventana de notificación** + tipo: *señales durante la ventana · señal al final · (recomendado) incidente*. Ojo: **las fuentes levantan incidentes antes que los charts** (una falla de fuente arma su incidente y luego la señal del KPI se asocia a ese incidente).
4. **El "Resumen diario / Resumen de incidentes" se MUEVE a Anomalías.** Es una notificación de incidentes, no una alerta. Sale de la tab de monitoreo del tablero.
5. **Renombrar "Historial" → "Alertas levantadas".** La ventana/tab que lista todos los KPIs que dispararon una alerta pasa a llamarse así (ya no "historial").
6. **Wording:** brandear lo del KPI como **"Alertas"**. Dejar claro que **una alerta no necesariamente crea una caja/incidente** en Anomalías.
7. **Updates de incidente** (reconfirmación, sube severidad, cambia hipótesis, otros recursos afectados): su toggle vive **en la config de incidentes** (Anomalías), **default off**. No en el KPI.
8. **La config de notificación de incidentes = un filtro sobre incidentes** (recursos/dashboards/KPIs impactados, "me etiquetan", severidad, sin asignar, estado…). Ese filtro define "mis incidentes" y esos son los que se notifican / resumen.

---

## Qué cambia EN ESTE PROTOTIPO (diálogo de monitoreo del KPI)

> Este prototipo es el lugar de las **Alertas**. Hay que reencuadrarlo y sacarle todo lo de incidentes.

### A. Reencuadrar "Notificaciones" → **"Alertas"**
- La sección de notificaciones del KPI pasa a ser **Alertas de este KPI** (señales): "avísame cuando este KPI salga de su rango esperado".
- **`¿Cuándo notificar?` = timing de la alerta**, en términos de **señal**, no de incidente:
  - **Durante la ventana** (cada señal mientras dura el horario)
  - **Solo al final de la ventana** (el estado de la señal al cierre)
  - **Nunca**
- ⚠️ **Replantear la barra-explicador:** hoy los marcadores muestran ciclo de **incidente** (abierto → reconfirmado → resuelto). Para Alertas deben representar **señales** (el KPI saliéndose de rango), no el ciclo de incidente. Ajustar marcadores/tooltips/copy.
- Quitar el eje "señal vs incidente" que exploramos en el preview: **aquí solo hay señales/alertas**.

### B. Sacar TODO lo de incidentes de este diálogo
- Eliminar la opción/idea de "notificar solo incidentes confirmados" como parte del KPI (eso ahora vive en Anomalías).
- Asegurar que configurar el monitoreo del KPI **no** implique notificaciones de incidente (default off / fuera de scope).

### C. Mover el "Resumen de incidentes" fuera
- El botón **"Resumen de incidentes"** + su popover (hoy en la tab de monitoreo del tablero) → **se reubica en Anomalías**. En este prototipo: removerlo de aquí (o marcarlo como "se va a Anomalías") para no mezclar.

### D. Renombrar "Historial" → "Alertas levantadas"
- Buscar la tab/ventana de "Historial" y renombrarla. Su contenido: todos los KPIs que dispararon una alerta.

### E. Wording / glosario
- Marca: **"Alertas"** en todo el bloque del KPI.
- Microcopy que aclare: *una alerta no crea necesariamente un incidente; los incidentes se gestionan en Anomalías*.
- Mantener la convención: nada de "agente/IA" de cara al usuario.

---

## Qué queda para la vista de Anomalías (NO en este prototipo — lo abordamos después)

> Andres lo definirá en una próxima sesión. Se documenta aquí para no perder el acuerdo.

- **Página de configuración de notificaciones de incidentes** (botón de config dentro del tab de Anomalías, análogo al de monitoreo en tableros).
- **¿Cuándo?**: cuando se creen incidentes nuevos, cuando se confirmen, por severidad (alta/media), cuando no tengan asignación, cuando me etiqueten, updates del incidente…
- **Filtro = definir "mis incidentes"** (recursos/dashboards/KPIs impactados, etc.). El mismo filtro de la **vista** de incidentes se reutiliza para la notificación.
- **Notificación agrupada / resumen consolidado** (1×día): "solo incidentes abiertos y urgentes", "todos los míos", etc. — **aquí vive el Resumen diario.**
- **Output configurable**: qué incluir (hipótesis, acción recomendada, resumen, narrativa).
- **Historias eng:** (1) historia de **filtros** en la vista de incidentes (endpoints) → reutilizable; (2) historia de **notificación de incidentes** que reusa esos filtros. "Matar dos pájaros con el mismo endpoint."

---

## Preguntas abiertas / a validar

- **¿Cuándo? de alertas:** ¿2 estados (Durante la ventana / Solo al final) o 3 con **Nunca**? (el eje de incidentes ya no aplica aquí).
- ¿Se conserva alguna opción per-KPI tipo *"avísame solo cuando este KPI entre en un incidente"*? Se mencionó al inicio, pero el consenso fue **separación limpia** (KPI = alertas). Confirmar.
- ⚠️ **Pendiente heredado:** confirmación de incidente "al cierre de la ventana" vs. confirmación por **workflow runner** (validar con Iván — viene de la sesión 26-jun am).
- Ingesta/Fuentes: ¿la config de alertas de fuente es otra vista/diálogo? (probablemente sí; fuera del scope de este prototipo).

---

## Impacto sobre lo ya construido en este prototipo

- El bloque **¿Cuándo notificar?** (3 estados de timing + barra-explicador con ciclo de incidente) → **se reencuadra a Alertas**: marcadores = señales, no incidentes; copy en clave de alerta.
- El **mini-dashboard de sensibilidad** sigue válido (la sensibilidad define el rango → la señal/alerta).
- El **"Resumen de incidentes"** → sale del prototipo (se va a Anomalías).
- **Handoffs** a actualizar tras implementar: `handoff-notificaciones-canales.md` (pasa a ser de Alertas), y crear uno nuevo para **Notificaciones de incidentes (Anomalías)** cuando se diseñe.
