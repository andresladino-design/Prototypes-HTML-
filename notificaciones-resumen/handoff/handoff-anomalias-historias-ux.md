# Historias de UX — Anomalías: filtros, notificaciones de incidentes y resumen

**Complementa:** `handoff-anomalias-filtros-notificaciones.md` (cambios de UI + guía de implementación BADS/desyk).
**Registro:** Interno — **Operation Center**. **Plataforma:** Desktop (shell de OC).
**Persona base:** *operador de Operation Center* (analista/ops de Simetrik) que vigila incidentes de **varios clientes** a la vez. Uso **frecuente**, a menudo **bajo presión** (algo se rompió y hay que decidir rápido). Su miedo: **perderse algo importante** o, al revés, **ahogarse en ruido**.

> Criterios marcados **[F]** = funcional (sí/no), **[X]** = de experiencia.

---

## HU-1 · Filtrar incidentes por varios valores y guardar ese filtro

**Usuario:** operador que revisa la cola de incidentes varias veces al día.
**Contexto:** entra a Gestión con una pregunta concreta ("¿qué hay confirmado en Adquirencia hoy?"); no quiere rearmar el filtro cada vez.

### Historia
Como operador que vuelve a la misma vista todo el día,
quiero acotar los incidentes combinando varios valores y **guardar** esa combinación con un nombre,
para entrar directo a "lo mío" sin reconstruir el filtro y sentir que la herramienta me conoce.

### Estados de interfaz
- **Inicial:** lista completa de incidentes; barra Filtrar / Ordenar / Guardados.
- **Eligiendo:** submenú por categoría (Recurso, Tablero, Estado, Tipo) con **multiselect** (check por opción, no se cierra), footer Limpiar / Listo.
- **Aplicado:** panel gris con un **chip compuesto por categoría** ("Tipo: Archivo faltante o Archivo duplicado"), conector **"Y"** entre categorías, + "Guardar filtro" / "Quitar filtros".
- **Guardando:** input inline para nombrar ("Incidentes de Sergio") → aparece en "Guardados".
- **Vacío post-filtro:** si la combinación da 0, mostrarlo explícito (no lista en blanco muda).

### Interacción / motion
- Marcar opción = feedback inmediato (check + recálculo de la lista). 120 ms.
- Los chips entran/salen sin saltar el scroll de la lista.

### Criterios
- **[F]** Dentro de una categoría los valores se combinan con **O**; entre categorías con **Y**.
- **[F]** Estado→`incident.status`, Tipo→`incident.problem_category` (ver guía BADS).
- **[F]** Filtro guardado se puede cargar y eliminar; es reutilizable por las notificaciones.
- **[X]** Reconstruir un filtro frecuente toma **1 clic** (Guardados), no rearmarlo.
- **[X]** En 2 s el operador entiende qué está viendo (la lógica O/Y es legible en los chips).

### a11y
- [ ] Opciones del menú navegables por teclado; check expone estado (`aria-checked`).
- [ ] Chip "Quitar filtro" con `aria-label`.

---

## HU-2 · Crear mi primera notificación (first-run, sin partir de cero)

**Usuario:** operador que nunca ha configurado notificaciones.
**Contexto:** llega a Configuración → Notificaciones de incidentes y no tiene nada; no quiere leer un manual.

### Historia
Como operador que entra por primera vez y no sabe qué se puede configurar,
quiero **ver de qué se trata** y empezar desde una plantilla razonable,
para tener una notificación útil en segundos y entender el modelo de paso.

### Estados de interfaz
- **Vacío / first-run:** título + explicación corta + **"Vista previa"** (diagrama ilustrativo: una notificación → Email y Slack, no clickeable) + **plantillas** ("Incidentes confirmados", "Archivos faltantes o fallidos") + CTA **"Crear notificación"**. (No "Sin resultados".)
- **Desde plantilla:** abre el editor **pre-llenado** (nombre + alcance + momento) listo para ajustar.
- **Desde cero:** editor en blanco.
- **Guardado:** vuelve a la **lista** con la tarjeta ya creada.

### Interacción / motion
- En la vista previa, **pulso de flujo** por los wires enseña la dirección (incidente → canales); entrada escalonada. Respeta `prefers-reduced-motion`.
- El diagrama es ilustración (`pointer-events:none`), separado de plantillas/CTA (que sí son accionables).

### Criterios
- **[F]** "Usar" plantilla pre-llena alcance + momento del editor.
- **[X]** El operador entiende, sin instrucciones, que **una notificación llega por varios canales**.
- **[X]** Nunca enfrenta un formulario en blanco como primera opción.

---

## HU-3 · Definir el alcance de una notificación ("¿qué incidentes te interesan?")

**Usuario:** operador que solo quiere enterarse de cierto subconjunto.
**Contexto:** le importan los incidentes confirmados de sus tableros; el resto es ruido.

### Historia
Como operador que no quiere recibir todo,
quiero describir **qué incidentes me importan** combinando filtros (o reusando uno guardado), elegir **en qué momento** del ciclo de vida me avisan y **por dónde**,
para recibir solo lo relevante y confiar en que no me llega spam ni se me escapa lo urgente.

### Estados de interfaz (editor)
- **Bloque 1 · "¿Qué incidentes te interesan?":** botón **Filtrar** (mismo menú multiselect, inline) **o** select "aplica un filtro guardado"; abajo "Tu alcance" como chips. Alcance vacío = "Todos mis incidentes".
- **Bloque 2 · "¿En qué punto de la vida del incidente…?":** Cuando se cree / Cuando se confirme.
- **Bloque 3 · "¿Recibir actualizaciones?":** toggle.
- **Canales:** tarjetas activables **Email** / **Slack**; Slack incluye **Etiquetar por ID de usuario** con su nota.
- **Inválido:** si no hay momento o no hay canal, **aviso** "Esta notificación no avisaría de ningún incidente" y no guarda.

### Criterios
- **[F]** Momento ↔ eventos BADS (creación / `status_changed→CONFIRMED`); updates ↔ `status_changed` posteriores.
- **[F]** Canal apagado no se envía; mención por **ID de Slack** (no `@nombre`).
- **[F]** Guardar bloqueado si falta momento o canal.
- **[X]** El operador percibe el paquete como **una regla suya** ("a mí, esto, así").

### a11y
- [ ] Toggles como `Switch` (rol/estado), checkboxes con label asociado, hint como `Alert info`.

---

## HU-4 · Mantener mis notificaciones (lista, editar, duplicar, pausar, eliminar)

**Usuario:** operador con varias reglas ya creadas.
**Contexto:** quiere ajustar una, clonar una parecida o pausar temporalmente sin perder la config.

### Historia
Como operador que ya tiene varias notificaciones,
quiero verlas de un vistazo y **editar / duplicar / pausar / eliminar** cada una,
para mantener mis avisos al día sin rehacer trabajo.

### Estados de interfaz
- **Lista:** tarjeta por notificación con nombre, resumen del alcance, **toggle activo/inactivo**, tags (momento · actualizaciones · canales) y acciones **Duplicar · Editar · Eliminar** (íconos en footer).
- **Inactiva:** tarjeta atenuada, toggle off.
- **Duplicar:** crea "… (copia)" y abre el editor (clonar una existente es la vía para reutilizar).

### Criterios
- **[F]** Toggle activa/pausa sin entrar al editor.
- **[F]** Duplicar copia alcance, momento, updates y canales.
- **[X]** "Me gusta esta config, me la copio" se resuelve en 1 clic (Granola).
- **[X]** Sin concepto de dueño/equipo: se ven todas las configuradas, en una lista plana.

---

## HU-5 · Activar y mantener mi resumen consolidado diario

**Usuario:** operador que no quiere notificaciones sueltas todo el día.
**Contexto:** prefiere un único consolidado a una hora fija.

### Historia
Como operador que se satura con avisos sueltos,
quiero un **único resumen al día** de los incidentes que me importan, a la hora que elija,
para mantenerme al tanto sin interrupciones constantes.

### Estados de interfaz (3 estados)
- **First-run (apagado):** intro + **Vista previa** (diagrama: incidencias → agrupadas en un resumen → Email + Slack) + **"Activar resumen diario"**.
- **Editando:** formulario con **defaults** ya puestos (alcance, "solo abiertos y urgentes", 08:00, CO·Bogotá, mi correo).
- **Guardado / activo:** banner **"Tu resumen diario está activo"** + tarjeta read-only con la config (llega 8:00 · CO; incluye; alcance; canales) + **Editar** (ícono) + toggle para **pausar**.

### Interacción
- Activar → revela config; Guardar → estado activo; Pausar (toggle off) → vuelve al first-run; Cancelar → vuelve a lo guardado (o al vacío si nunca se guardó).

### Criterios
- **[F]** El resumen es **distinto** de las notificaciones por evento: es **1×día** (no por `status_changed`).
- **[F]** Reutiliza el mismo patrón de alcance y de canales (incl. ID de Slack).
- **[X]** El operador entiende, en la vista previa, que **muchas incidencias se agrupan en un solo aviso**.
- **[X]** El patrón "Editar" es **consistente** con las tarjetas de notificación (mismo ícono/posición).

---

## Notas transversales (todas las historias)
- **Glosario:** incidente, anomalía/señal, tablero, KPI; **no** "agente/IA" de cara al usuario.
- **Severidad** no se expone (la asigna BADS) hasta que sea configurable.
- **Desktop-only** (shell de Operation Center). Columna de lista de Anomalías ~384px; el detalle a la derecha.
- **Loading/empty/error** de datos reales: skeleton con forma (no spinner); empty states activos (ya definidos); error con mensaje que diga qué pasó y qué hacer.
