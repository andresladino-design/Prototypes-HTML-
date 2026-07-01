# Handoff 1 — Filtros en la vista de incidentes

**Prototipo:** `notificaciones-resumen/index.html` → Anomalías → **Gestión** (barra "Filtrar / Ordenar / Guardados").
**Fuente:** sesiones Granola **30-jun-2026** (am: épicas y cambios de UI · pm: design review con ingeniería) + comentarios de Ohana.
**Registro:** Interno / Operation Center. **Plataforma:** Desktop (shell de OC).
**Qué cubre:** los filtros de la lista de incidentes en Gestión (Recurso, Tablero, Estado, Tipo, Fecha), su lógica de combinación, el multiselect por categoría y los filtros guardados reutilizables.
**Qué NO cubre:** el editor de notificación y su alcance "Entidades afectadas", los paquetes de notificación y el resumen consolidado (todo eso es Handoff 3); la configuración de detección y las alertas del KPI (Handoff 2). La severidad no entra en scope (system-assigned, ver más abajo).

> **Regla del equipo:** donde un cambio de UI no se enumere explícitamente, no se ejecuta en desarrollo. Por eso este handoff lista **cada** cambio, incluso los chicos.

---

## 1. Contexto y objetivo

La vista **Anomalías → Gestión** es la cola de incidentes que el operador de Operation Center revisa varias veces al día, a menudo bajo presión. Encima de la lista hay una barra con tres acciones: **Filtrar**, **Ordenar** y **Guardados**.

El objetivo del slice de filtros es que el operador pueda acotar la cola combinando varios valores (por ejemplo "confirmados de Adquirencia de tipo archivo faltante") y **guardar** esa combinación con un nombre para volver a ella en un clic, sin rearmarla cada vez.

Un incidente en esta vista es la entidad `incident` de BADS (agrupa señales/alertas con causa raíz). La lista y sus filtros operan siempre sobre **incidentes**, no sobre señales atómicas (`anomaly_signal`, que viven en la vista del KPI / Alertas levantadas).

---

## 2. Cambios de UI (enumerados)

Ubicación: Anomalías → Gestión → barra "Filtrar / Ordenar / Guardados".

1. **Multiselect dentro de cada categoría.** Al abrir Recurso / Tablero / Estado / Tipo, se pueden marcar **varios valores**. Cada opción muestra un **check** al elegirse; el submenú **no se cierra** al marcar (footer con "Limpiar" y "Listo").

2. **Lógica de combinación O / Y.** Dentro de una misma categoría los valores se unen con **`o`** (OR); entre categorías distintas, con **`Y`** (AND). En los chips aplicados: el valor se lee como `A o B`; entre chips de categorías distintas aparece un conector **"Y"**. La lógica O/Y debe quedar legible en los chips (el operador entiende qué está viendo en pocos segundos).

3. **Quitar el filtro "Severidad".** Eliminado del menú. Motivo: no exponer severidad hasta que el usuario pueda **definir sus propios niveles**. La severidad hoy la asigna el sistema (ver guía de implementación). Vuelve cuando sea configurable.

4. **Filtros que quedan:** **Recurso**, **Tablero**, **Estado**, **Tipo** y **Fecha**.
   - **Recurso y Tablero van SEPARADOS**, como dos categorías independientes. No se unifican en esta vista (ver Nota crítica).
   - **Fecha** = rango **estático** ("Últimos 30 días"), valor único. El rango dinámico t-n que se probó fue **revertido**; el t-n vive solo en el período del resumen del paquete (Handoff 3), no acá.
   - **Tipo** = problem categories reales de BADS (Ingesta): Archivo faltante, Archivo fallido, Archivo vacío, Archivo duplicado, Variación de volumen.

5. **Filtros guardados (recurrentes).**
   - Botón **"Guardar filtro"** en el panel de chips aplicados → nombrar inline (por ejemplo "Incidentes de Sergio").
   - Botón **"Guardados"** en la barra: **solo ícono** (bookmark), con **tooltip / aria-label**. Abre un menú con los filtros guardados para **cargar** o **eliminar**.
   - Sin automatizaciones: solo guardar y reutilizar. Estos filtros guardados son los que el editor de notificación reutiliza vía su botón "Aplicar un filtro guardado" (Handoff 3).

---

## 3. Historia de UX — HU-1 · Filtrar incidentes por varios valores y guardar ese filtro

**Usuario:** operador que revisa la cola de incidentes varias veces al día.
**Contexto:** entra a Gestión con una pregunta concreta ("¿qué hay confirmado en Adquirencia hoy?"); no quiere rearmar el filtro cada vez.

**Historia:** como operador que vuelve a la misma vista todo el día, quiero acotar los incidentes combinando varios valores y **guardar** esa combinación con un nombre, para entrar directo a "lo mío" sin reconstruir el filtro y sentir que la herramienta me conoce.

### Estados de interfaz
- **Inicial:** lista completa de incidentes; barra Filtrar / Ordenar / Guardados.
- **Eligiendo:** submenú por categoría (Recurso, Tablero, Estado, Tipo) con **multiselect** (check por opción, no se cierra), footer Limpiar / Listo.
- **Aplicado:** panel gris con un **chip compuesto por categoría** ("Tipo: Archivo faltante o Archivo duplicado"), conector **"Y"** entre categorías, más "Guardar filtro" / "Quitar filtros".
- **Guardando:** input inline para nombrar ("Incidentes de Sergio") → aparece en "Guardados".
- **Vacío post-filtro:** si la combinación da 0 resultados, mostrarlo explícito (no una lista en blanco muda).

### Interacción / motion
- Marcar una opción = feedback inmediato (check + recálculo de la lista), 120 ms.
- Los chips entran y salen sin saltar el scroll de la lista.

### Criterios
- **[F]** Dentro de una categoría los valores se combinan con **O**; entre categorías con **Y**.
- **[F]** Estado → `incident.status`, Tipo → `incident.problem_category` (ver guía BADS).
- **[F]** Un filtro guardado se puede cargar y eliminar; es reutilizable por las notificaciones.
- **[X]** Reconstruir un filtro frecuente toma **1 clic** (Guardados), no rearmarlo.
- **[X]** En 2 s el operador entiende qué está viendo (la lógica O/Y es legible en los chips).

### a11y
- [ ] Opciones del menú navegables por teclado; el check expone estado (`aria-checked`).
- [ ] Chip "Quitar filtro" con `aria-label`.
- [ ] Botón "Guardados" (icon-only) con `aria-label` y tooltip.

---

## 4. Copy (glosario aplicado)

- **Categorías del menú:** Recurso · Tablero · Estado · Tipo · Fecha.
- **Estados (Tipo Estado):** En observación · Abierto · Confirmado · Resuelto.
- **Tipos (categoría Tipo):** Archivo faltante · Archivo fallido · Archivo vacío · Archivo duplicado · Variación de volumen.
- **Conectores en chips:** valores dentro de una categoría se leen con "o"; entre categorías se muestra "Y".
- **Fecha:** "Últimos 30 días".
- **Acciones:** "Guardar filtro", "Quitar filtros", "Limpiar", "Listo", "Guardados".
- **Vacío post-filtro:** mensaje explícito de que la combinación no arrojó incidentes (qué pasó y cómo ajustar), no una lista en blanco.

Vocabulario: **monitoreo** (nunca "agente" / "Agente IA" / "IA" de cara al usuario), **incidente**, **señal / alerta**, **KPI**, **Tablero**, **Recurso**.

---

## 5. Guía de implementación (slice de filtros)

Aterriza el prototipo contra el modelo real de **BADS** (Brain v2.8) y los componentes **desyk** de `fe-solutions-mf`.

### Mapeo a BADS

**Filtro "Estado" → `incident.status`:**

| Label UI (proto) | `incident.status` |
|---|---|
| En observación | `WATCHING` |
| Abierto | `OPEN` |
| Confirmado | `CONFIRMED` |
| Resuelto | `RESOLVED` |
| (terminales no mostrados) | `AUTO_CLOSED` · `USER_CLOSED` · `CLOSED` · `MERGED` |

(`UNDER_INVESTIGATION` reservado.)

**Filtro "Tipo" → `incident.problem_category`** (catálogo cerrado de Ingesta):

| Label UI | enum BADS |
|---|---|
| Archivo faltante | `MISSING_FILE` |
| Archivo fallido | `FAILED_FILE` |
| Archivo vacío | `UNEXPECTED_EMPTY_FILE` |
| Archivo duplicado | `DUPLICATED_FILE` |
| Variación de volumen | `VOLUME_VARIATION` |

- Los **nombres del catálogo** son exactos (Brain). Los constantes enum `MISSING_FILE` / `FAILED_FILE` / `VOLUME_VARIATION` están **inferidos del patrón** (`UNEXPECTED_EMPTY_FILE` / `DUPLICATED_FILE` sí verbatim) → **confirmar el string exacto con backend BADS**.
- `ALL_OK` es interno (auto-cierra el incidente) → **no se muestra**.
- Catálogos de Data Quality (M4), Conciliación (M5) y Accounting (M10) están pendientes → el filtro Tipo hoy solo refleja Ingesta.

**Por qué NO hay filtro Severidad:** la severidad es un enum `URGENT` / `REQUIRES_ATTENTION` **asignado por el workflow runner de BADS (D-13), no configurable por el usuario**. Por eso se quitó el filtro Severidad (y la condición "severidad alta" del editor). Vuelve cuando exista severidad configurable por el usuario.

### Lógica de filtros (scope)

- **Dentro de una categoría: OR. Entre categorías distintas: AND.**
- **Filtros de Gestión (lista):** `recurso ∈ {...} AND tablero ∈ {...} AND estado ∈ {...} AND tipo ∈ {...}` (cuatro categorías separadas, cada una con OR interno).
- **Fecha:** rango **estático** ("Últimos 30 días"), valor único. El t-n dinámico se probó y se **revirtió**.
- **Multiselect dentro de cada filtro: producción NO lo soporta hoy.** Es un cambio nuevo de endpoints/UI → documentarlo como **historia de eng**. Según el equipo: casi 100% frontend + poco backend (Ayed puede apoyar).
- **Filtros guardados:** entidad propia reutilizable. Se crean en Gestión con el vocabulario Recurso / Tablero / Estado / Tipo. Al aplicarlos en el editor de notificación, Tablero/Recurso se colapsan a "Entidad" y Estado se descarta (`pkgScopeKeep`); eso pertenece al Handoff 3, acá el filtro guardado conserva las cuatro categorías.

### Mapeo a componentes desyk (`@simetrikinc/desyk-components`)

Refs: `fe-solutions-mf/.../skills/desyk/references/`.

| Patrón del proto | Componente desyk | Nota |
|---|---|---|
| Menús de Filtrar / Ordenar / Guardados | **`Popover`** | |
| Tooltip de íconos | **`Tooltip`** | para el botón "Guardados" icon-only y demás íconos |
| Multiselect por categoría / chips aplicados | **`Combobox`** + render de chips | desyk **no** tiene token-input dedicado; Combobox con búsqueda + chips custom |
| Estado / severidad como chip | **`Badge`** (variants success/warning/info/destructive) | severidad no se filtra, pero puede mostrarse como badge en la tarjeta |
| Botón icon-only ("Guardados") | **`Button`** con `size=icon-*` | requiere `aria-label` + `Tooltip` |

### Motion y a11y (specs)
- Durations canónicas **120 / 200 / 320 ms**, ease-out `cubic-bezier(0.22,1,0.36,1)`. Solo `transform` / `opacity`.
- Marcar opción = 120 ms; chips entran/salen sin saltar el scroll.
- **Skeleton con forma** sobre spinner para la carga de la lista; empty state activo (no "Sin resultados" plano) para el vacío post-filtro. Light mode.
- `@media (prefers-reduced-motion: reduce)` desactiva animaciones.
- Componentes desyk (`Combobox`, `Button`) traen roles/aria; chips con `aria-label="Quitar"`; check expone `aria-checked` — **obligatorio en la implementación**.

---

## 6. Nota crítica para ingeniería + edge cases

⚠️ **Recurso y Tablero van SEPARADOS en la vista de Gestión.** No confundir con el editor de notificación (Handoff 3), donde Tablero + Recurso se **unifican** en un solo bloque "Entidades afectadas" (OR). Esa unificación es **solo del editor de notificación**, porque ahí sirven para definir una regla y las condiciones tablero∧recurso podían volverse imposibles (un recurso que no pertenece al tablero elegido → nunca notifica). En Gestión, en cambio, la lista es para **navegar**, no para definir una regla: Recurso y Tablero se quedan como **dos categorías independientes** (AND entre ellas, OR dentro de cada una). Son features distintos; no mezclar la lógica.

⚠️ **Producción HOY no soporta multiselect dentro de cada filtro.** El multiselect por categoría es un cambio nuevo de endpoints/UI → documentarlo como historia de ingeniería propia. ~100% frontend + poco backend.

### Edge cases
- **Combinación sin resultados:** mostrar vacío post-filtro explícito (qué pasó, cómo ajustar), nunca lista en blanco muda.
- **Fecha estática:** "Últimos 30 días" es valor único; no exponer selector t-n en esta vista.
- **Severidad:** no exponer como filtro ni columna filtrable (system-assigned por BADS).
- **Strings de `problem_category`:** los enums `MISSING_FILE` / `FAILED_FILE` / `VOLUME_VARIATION` están inferidos → confirmar con backend antes de cablear el filtro Tipo.
- **Filtro guardado importado al paquete:** cambia de forma (colapsa Tablero/Recurso a Entidad, descarta Estado); ese comportamiento es del Handoff 3, no de esta vista.

---

## 7. Checklist pre-implementación

- [ ] Confirmar strings exactos de `incident.problem_category` con backend BADS (`MISSING_FILE`, `FAILED_FILE`, `VOLUME_VARIATION`).
- [ ] Enlazar filtro "Estado" a `incident.status` con el mapeo de labels de la tabla.
- [ ] Documentar como historia de ingeniería el **multiselect por categoría** (endpoints nuevos; producción no lo soporta hoy).
- [ ] Implementar lógica de combinación: **OR dentro de categoría, AND entre categorías**, con la lectura de chips ("A o B" + conector "Y").
- [ ] Mantener **Recurso y Tablero como categorías separadas** (no unificar en "Entidades afectadas" — eso es solo del editor, Handoff 3).
- [ ] Fecha como **rango estático** "Últimos 30 días" (no t-n dinámico).
- [ ] Quitar el filtro **Severidad** del menú (system-assigned; vuelve cuando sea configurable).
- [ ] Filtros guardados: "Guardar filtro" (nombrar inline) + botón "Guardados" **icon-only** con `aria-label` + tooltip; cargar / eliminar.
- [ ] Empty state post-filtro explícito (no "Sin resultados" plano); skeleton con forma en carga.
- [ ] a11y: navegación por teclado en menús, `aria-checked` en checks, `aria-label` en chips "Quitar" y en el botón "Guardados".
- [ ] Motion: 120 / 200 / 320 ms, ease-out `cubic-bezier(0.22,1,0.36,1)`; respetar `prefers-reduced-motion`.
- [ ] Mapear componentes a desyk: `Popover`, `Tooltip`, `Combobox` + chips, `Badge`, `Button` icon-only.
