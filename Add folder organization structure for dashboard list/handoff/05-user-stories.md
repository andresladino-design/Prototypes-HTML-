# User stories UX — Carpetas en la lista de tableros (SWAT-577)

**Fecha:** 2026-08-03 · **Audiencia:** diseño · FE · BE · QA
**Base:** [`01-decisiones.md`](01-decisiones.md) (D1–D7) · [`01-benchmark.md`](01-benchmark.md) (I1–I6) · [`04-userflows.md`](04-userflows.md) (F1–F7) · [`../design.md`](../design.md)

---

## Contexto de diseño (aplica a las 8 historias)

**Usuario:** analista de conciliación, lead de FinOps o admin de cuenta del Centro de operaciones. Nivel técnico medio-alto (vienen de Excel y de herramientas de BI), conocen el dominio contable.

**Contexto de uso:** escritorio, en medio de una tarea concreta — revisar el cierre del período, verificar una conciliación, mirar por qué se disparó una anomalía. **No están explorando: están buscando algo específico.**

**Estado emocional:** con prisa y con una pregunta en la cabeza. El panel es un medio, no un destino. Cuando aparece fricción acá, la fricción se siente doble porque interrumpe otra tarea.

**Éxito desde el punto de vista del usuario:** llegar al tablero **reconociendo** en lugar de recordando, en pocos segundos, sin tener que escribir un nombre que no recuerda con exactitud (`Adquirencia_2026_06_04_conciliacion_visa`).

**Plataforma:** desktop. El panel mide `w-72` (288px) y **auto-colapsa cuando el contenedor baja de 1200px** (`COLLAPSE_WIDTH_THRESHOLD` en `OcContentLayout.tsx`). No hay experiencia mobile del OC hoy.

**Restricciones de diseño:** desyk 1.30.0 · el panel ya existe con 3 secciones · densidad de 32px por fila · los patrones de crear/editar/eliminar ya establecidos.

### Comportamiento responsivo (común)

| Punto de quiebre | Comportamiento |
|---|---|
| Contenedor > 1200px | Panel expandido (288px). Experiencia completa: carpetas, contadores, acciones en hover. |
| Contenedor ≤ 1200px | El panel **auto-colapsa a 56px** (comportamiento existente). Las carpetas **no se ven** en modo colapsado: el rail solo muestra los iconos de Tableros/Datasets. ⚠️ Pregunta abierta transversal: ¿el rail colapsado debería dar acceso a las carpetas? Ver PA-1. |
| Mobile | Fuera de alcance: el OC no tiene experiencia mobile. |

### Accesibilidad (línea base común)

- [ ] Contraste AA: 4.5:1 en texto, 3:1 en iconos y bordes. **Verificar** `text-muted-foreground` (`0 0% 55%`) sobre `--sidebar-background` (`0 0% 98%`) en el tamaño 11px del contador y de la segunda línea.
- [ ] Toda tarea se completa **solo con teclado**. El drag & drop es atajo, nunca requisito (D7).
- [ ] La fila de carpeta es un `CollapsibleTrigger` con `aria-expanded`; `Enter` y `Espacio` alternan.
- [ ] **El área de toggle es la fila completa (32px de alto), no el chevron.** Expandir no puede depender de un target de 12px → ver hallazgo 🔴 C1.
- [ ] El contador va en el nombre accesible ("Adquirencia, 24 tableros"), no solo visual.
- [ ] **Semántica de lista:** los hijos de una carpeta van en una lista (`ul`/`li` o `role="group"`) para que el lector de pantalla anuncie posición ("3 de 24") → ver 🔴 C3.
- [ ] **`Escape` cierra todo diálogo** (salvo mientras guarda), el foco queda atrapado dentro mientras está abierto y **vuelve al disparador** al cerrar → ver 🔴 C2.
- [ ] Los errores en diálogos se anuncian (`role="alert"` / `aria-live`), no solo se pintan en rojo.
- [ ] Los controles que aparecen en `hover` aparecen también en `focus-visible` — el panel ya lo hace.
- [ ] Foco visible siempre; nunca `outline: none` sin reemplazo.
- [ ] Nada se comunica **solo** por color: la carpeta se distingue por icono + peso + chevron, no por tinte.
- [ ] La animación de expandir/colapsar respeta **`prefers-reduced-motion`**.
- [ ] Espaciado mínimo de 8px entre targets adyacentes: la fila de carpeta **no** apila tres icon-buttons juntos.

---

## HU-01 · Reconocer mis tableros agrupados en lugar de escanear 159

**Usuario:** analista que entra al OC varias veces al día
**Contexto:** llega al panel con una pregunta concreta; hoy encuentra una lista plana de 159 nombres casi idénticos
**Flujo:** F7 · **Criterio:** C4

### Historia

Como analista que entra al panel con una pregunta concreta y no recuerda el nombre exacto del tablero,
quiero ver mis tableros **agrupados por contexto y con los grupos cerrados**,
para reconocer de un vistazo dónde mirar en vez de escanear una lista infinita y sentir que empiezo perdido.

### Estados de interfaz

- **Inicial:** carpetas **colapsadas**, ordenadas A→Z, seguidas del bloque "Sin carpeta". La carpeta que contiene el **tablero activo** aparece expandida (si no, el usuario no ve dónde está parado). Con una sola carpeta, arranca expandida.
- **Carga:** los skeletons actuales (`SidebarListSkeletonRow`, 5 filas). Las carpetas no tienen skeleton propio: aparecen con la lista.
- **Activo:** al expandir, los hijos entran indentados 16px con guía vertical de 1px; el chevron rota.
- **Error:** el error de la sección "Tableros" ya existe (icono + mensaje + Reintentar) y cubre también las carpetas.
- **Éxito:** no aplica — navegar no genera confirmación.
- **Vacío post-interacción:** carpeta expandida **sin** tableros → ver HU-08.

### Interacción y movimiento

- **Transición:** expandir/colapsar con la animación `accordion-down` / `accordion-up` de desyk (0.2s ease-out). Nada custom.
- **Feedback:** `hover:bg-muted` en la fila de carpeta; la fila del tablero activo mantiene `bg-accent`.
- **Persistencia:** el estado de expansión se guarda en `localStorage` por (cuenta, usuario). **Precedente en el mismo archivo:** `SIDEBAR_COLLAPSED_KEY = "oc_sidebar_collapsed"` ya persiste el colapso del panel.

### Criterios de aceptación

- [ ] Con 4 carpetas colapsadas + los sueltos, el usuario ve **menos filas** que en la lista plana equivalente.
- [ ] La fila de carpeta mide **32px**, igual que una fila de tablero (medir en el prototipo).
- [ ] Se distingue una carpeta de un tablero **sin leer el texto** (icono + peso + chevron).
- [ ] Se distingue una carpeta del **header de sección** "Tableros" sin ambigüedad.
- [ ] Al recargar la página, las carpetas que el usuario había expandido **siguen expandidas**.
- [ ] Al entrar con un tablero activo dentro de una carpeta, esa carpeta se ve expandida y la fila activa marcada.
- [ ] El toggle A→Z ordena carpetas entre sí y tableros dentro de cada una (D5).
- [ ] Un tablero puede estar en una carpeta **y** en Favoritos, y en Favoritos no muestra su carpeta.

### Preguntas abiertas

- **PA-2:** ¿el bloque "Sin carpeta" necesita un separador con label, o alcanza con la ausencia de indentación?
- **PA-3:** con 111 sueltos, ¿mostramos el conteo en el separador ("Sin carpeta · 111") para hacer visible el trabajo pendiente de organizar?

### Evidencia

- **Ley de Miller:** chunks de 5–9 reconocibles en vez de una lista de 159.
- **Reconocer antes que recordar** (Nielsen #6): es el objetivo declarado del issue.
- **Visibilidad del estado del sistema** (Nielsen #1): revelar la carpeta del tablero activo.
- Progressive disclosure con su advertencia: *"users can't scan collapsed content"* → de ahí las tres excepciones al colapsado.

---

## HU-02 · Crear una carpeta sin abandonar lo que estaba haciendo

**Usuario:** analista o lead que decide ordenar · **Flujo:** F1 · **Criterio:** C1

### Historia

Como usuario que ya no encuentra nada en una lista de 159 tableros,
quiero crear una carpeta en dos clics y con un solo campo,
para empezar a ordenar sin sentir que entro a una configuración larga.

### Estados de interfaz

- **Inicial:** disparador = botón icono `FolderPlus` con tooltip "Nueva carpeta", en el header de la sección "Tableros", a la izquierda del toggle A→Z (I1).
- **Carga:** botón "Crear" en estado `Creando...` con `LoaderCircle animate-spin`; el campo queda deshabilitado.
- **Activo:** `Dialog` con un solo campo, enfocado y seleccionado al abrir. `Enter` confirma.
- **Error:** duplicado → mensaje inline bajo el campo (`text-xs text-destructive`), no toast solo. Fallo de red → `Alert variant="destructive"` inline.
- **Éxito:** la carpeta aparece **vacía y expandida** en la lista + `toast.success("Carpeta creada")`.
- **Vacío post-interacción:** la carpeta recién creada está vacía → HU-08.

### Interacción y movimiento

- El disparador está **deshabilitado mientras hay búsqueda activa** (igual que Almacenamiento): en modo búsqueda la lista está aplanada y "crear acá" no tiene ubicación clara.
- Entrada secundaria: "＋ Nueva carpeta" **dentro** del selector de mover (HU-03), para no obligar a empezar de nuevo si la necesidad aparece a mitad de camino.

### Criterios de aceptación

- [ ] Crear una carpeta toma **un clic + un nombre + Enter**.
- [ ] La carpeta nace **vacía**: el diálogo no pide seleccionar tableros (C7).
- [ ] Validación: `trim` · mínimo 1 · **máximo 100** · **sin restricción de caracteres** — acepta "Conciliación diaria" y "Cierre_contable".
- [ ] El duplicado se detecta local (mientras escribe) **y** contra el servidor (409), y ambos se ven en el mismo lugar.
- [ ] Se completa con teclado: el disparador es alcanzable por `Tab` y tiene nombre accesible.
- [ ] Tras crear, el foco vuelve a un lugar predecible (la carpeta nueva o el disparador), no al `<body>`.

### Preguntas abiertas

- **PA-4:** ¿un icono de 28px es suficiente para la entrada principal de un feature nuevo? Mitigación actual: el empty state lleva CTA de texto completo. **A validar en la demo.**
- **PA-5:** ¿hace falta un aviso suave al pasar de 15 carpetas (I5) o se deja para una v1.1 con datos reales?

### Evidencia

- **Fitts:** un target chico en hover es riesgoso para la entrada principal → de ahí el CTA de respaldo.
- **Hick:** no convertir "Nuevo tablero" en split-button; es la acción más frecuente del panel.
- Precedentes: `FilesView.tsx:1504` (icono + tooltip en toolbar) · Metabase (`+` en el header de la sección del sidebar).

---

## HU-03 · Mover un tablero a una carpeta sin miedo a romper nada

**Usuario:** cualquier usuario con acceso al tablero · **Flujo:** F2 · **Criterio:** C2

### Historia

Como usuario que acaba de crear una carpeta y quiere llenarla,
quiero mover un tablero desde su propio menú y ver confirmado a dónde fue,
para no dudar si el tablero sigue existiendo ni dónde quedó.

### Estados de interfaz

- **Inicial:** ítem "Mover a carpeta" en el menú `⋮` **y** en el menú de clic derecho.
- **Carga:** el movimiento es **optimista** (la fila salta a la carpeta de inmediato); si falla, vuelve a su lugar con toast de error.
- **Activo:** `Dialog` con lista simple de carpetas (D2 = un nivel, sin árbol) + buscador si hay más de 7 + "＋ Nueva carpeta".
- **Error:** rollback visible + `toast.error`.
- **Éxito:** `toast("Tablero movido a «Adquirencia»", { action: "Deshacer" })`.
- **Caso especial:** si ya estaba en otra carpeta, un paso de **confirmación** ("saldrá de «Cierre contable»") porque la pertenencia es exclusiva (D3).

### Interacción y movimiento

- **Atajo:** arrastrar la fila sobre la carpeta. Debe funcionar con la carpeta **colapsada** (highlight `bg-info/5` + `border-info/50`) y con **autoscroll** del panel.
- Una fila arrastrada **no** debe activar a la vez el drop target de Favoritos y el de carpetas → MIME propio `DASHBOARD_TO_FOLDER_MIME`.
- El menú pasa de 5 a 6 ítems: verificar que siga escaneable (Hick) y si hace falta un separador.

### Criterios de aceptación

- [ ] "Mover a carpeta" aparece en `⋮` **y** en clic derecho, con el mismo copy.
- [ ] El copy dice **"Mover a carpeta"**, nunca "Agregar a" (no es acumulativo).
- [ ] Mover un tablero que ya estaba en otra carpeta **pide confirmación** y nombra ambas carpetas.
- [ ] Todo lo que se logra arrastrando se logra por menú **y** por teclado.
- [ ] El toast permite **Deshacer** y deshacer devuelve el tablero a su carpeta anterior (no a "Sin carpeta").
- [ ] El selector se navega con flechas y se confirma con `Enter`.
- [ ] Mover un tablero **no** cambia su estado de favorito ni sus permisos.

### Preguntas abiertas

- **PA-6:** ¿expandir la carpeta al hacer hover ~700ms durante un drag, o solo hacer drop directo sobre la fila colapsada?
- **PA-7:** ¿el drag entra en la v1 o se corta a v1.1? Regla ya acordada: si el alcance aprieta, **se corta el drag, no el menú**.

### Evidencia

- Metabase documenta las dos vías: *"Click and drag it onto the destination collection, or click the three-dot menu (…) and select Move."*
- La infra de DnD HTML5 ya existe en este panel (`useDashboardCrossDrag`, usada por Favoritos).

---

## HU-04 · Sacar un tablero de una carpeta sabiendo que no lo estoy borrando

**Usuario:** cualquier usuario con acceso · **Flujo:** F3 · **Criterio:** C3

### Historia

Como usuario que se equivocó al clasificar un tablero,
quiero quitarlo de la carpeta con una acción reversible y sin diálogos que me asusten,
para corregir sin la duda de si acabo de eliminar trabajo de alguien.

### Estados de interfaz

- **Inicial:** ítem "Quitar de la carpeta" en el menú, solo visible cuando el tablero **está** en una carpeta.
- **Carga:** optimista, igual que HU-03.
- **Activo:** la fila se mueve al bloque "Sin carpeta".
- **Error:** rollback + toast.
- **Éxito:** `toast("Tablero quitado de la carpeta", { action: "Deshacer" })`.
- **Vacío post-interacción:** si era el último tablero, la carpeta queda vacía → HU-08.

### Criterios de aceptación

- [ ] **Sin diálogo de confirmación** (es reversible y de bajo riesgo).
- [ ] La palabra "Eliminar" **no aparece** en ningún punto de este flujo.
- [ ] El toast ofrece "Deshacer" y funciona.
- [ ] El ítem no aparece si el tablero no está en una carpeta (nada de acciones inertes).
- [ ] Tras quitarlo, el tablero sigue abierto si estaba abierto (no se pierde el contexto de trabajo).

### Preguntas abiertas

- ~~**PA-8:** ¿cuánto dura el toast con Deshacer?~~ **Resuelta por el checklist de calidad del OC:** *"Toast de undo aparece después de cualquier acción destructiva, disponible ~1 minuto"*. Se adopta **~60s** para mover y quitar.

### Evidencia

- **Control y libertad del usuario** (Nielsen #3): "deshacer" en vez de "confirmar" para acciones reversibles.
- **Prevención de errores** (Nielsen #5) aplicada al *lenguaje*: el riesgo real es que el usuario **crea** que borra.

---

## HU-05 · Renombrar una carpeta cuando el nombre dejó de servir

**Usuario:** quien organizó la cuenta · **Flujo:** F4 · **Criterio:** C1

### Historia

Como usuario que nombró una carpeta apurado y ahora no la entiende,
quiero renombrarla en el mismo diálogo con el nombre ya escrito,
para corregir sin volver a escribir todo.

### Estados de interfaz

- **Inicial:** ítem "Renombrar carpeta" en el menú `⋮` de la carpeta.
- **Carga:** botón `Guardando...` con spinner.
- **Activo:** el mismo diálogo de HU-02 en modo `rename`, con el valor **precargado y seleccionado**.
- **Error:** duplicado (409) inline + toast.
- **Éxito:** nombre actualizado en la lista + `toast("Carpeta renombrada")`.

### Criterios de aceptación

- [ ] El campo llega precargado y seleccionado: escribir reemplaza (patrón del rename de tableros).
- [ ] Confirmar con el **mismo nombre** cierra sin llamar al servidor.
- [ ] El 409 se muestra **inline en el diálogo**, además del toast.
- [ ] Misma validación que HU-02 (máx 100, sin restricción de caracteres).
- [ ] La carpeta **conserva su estado de expansión** y sus tableros después del renombrado.

### Preguntas abiertas

- **PA-9:** ¿rename inline en la fila (doble clic) como atajo, o solo por diálogo? El repo tiene `useInlineRename` disponible pero el panel usa diálogo para tableros — divergir crearía dos patrones.

---

## HU-06 · Eliminar una carpeta sin perder los tableros que contiene

**Usuario:** quien reorganiza la cuenta · **Flujo:** F5 · **Criterios:** C1, D6
**⚠️ La historia de mayor riesgo del feature.**

### Historia

Como usuario que quiere deshacer una agrupación que no funcionó,
quiero eliminar la carpeta y que el diálogo me diga **exactamente** qué pasa con los tableros que hay dentro,
para no quedarme con la duda de si acabo de borrar 24 tableros de mi equipo.

### Estados de interfaz

- **Inicial:** ítem "Eliminar carpeta" (nunca "Eliminar" a secas), en `text-destructive`, tras un separador.
- **Carga:** botón `Eliminando...` con spinner.
- **Activo:** `AlertDialog` — **no** se descarta clickeando fuera.
- **Error:** `Alert variant="destructive"` **dentro** del diálogo (no toast), el diálogo permanece abierto.
- **Éxito:** los 24 tableros aparecen en "Sin carpeta" + `toast("Carpeta eliminada")`.
- **Caso vacío:** si la carpeta no tiene tableros, el copy cambia a "Está vacía".

### Copy (verbatim, es el corazón de la historia)

> **¿Eliminar carpeta?**
> Se eliminará la carpeta «Adquirencia». Los **24 tableros** que contiene volverán a la lista de tableros; **no se eliminarán**.

### Criterios de aceptación

- [ ] La descripción incluye el **número real** de tableros afectados.
- [ ] La descripción afirma explícitamente que **no se eliminarán** (no basta con omitir la advertencia).
- [ ] Eliminar la carpeta **jamás** elimina un tablero — verificable en BE con `ON DELETE SET NULL`.
- [ ] Tras eliminar, los tableros aparecen en "Sin carpeta" y siguen abribles.
- [ ] Si falla, el error se ve **dentro** del diálogo y nada se elimina.
- [ ] El botón destructivo no es el foco por defecto al abrir el diálogo.
- [ ] **Prueba de QA obligatoria:** eliminar una carpeta con 24 tableros y verificar que los 24 existen después.

### Preguntas abiertas

- **PA-10:** ¿ofrecemos "Deshacer" también acá (recrear la carpeta y reasignar)? Encarece el BE; la alternativa es que el diálogo sea suficientemente claro.
- **PA-11:** en Almacenamiento, eliminar carpeta **sí** borra el contenido. ¿Vale la pena abrir un ticket para alinear el lenguaje del producto, o convivimos con la divergencia?

### Evidencia

- Copy real de Almacenamiento: *"La carpeta "Ventas" se eliminará. Contiene 3 carpeta(s), 12 archivo(s)."* → allá se advierte **porque se destruye**. Mismo botón, consecuencia opuesta.
- **Prevención de errores** (Nielsen #5) + **coincidencia con el mundo real** (#2): en un explorador de archivos, borrar una carpeta borra el contenido. Estamos rompiendo esa expectativa a propósito y hay que decirlo.

---

## HU-07 · Encontrar un tablero esté donde esté, y saber dónde está

**Usuario:** quien busca por nombre parcial · **Flujo:** F6 · **Criterio:** C5

### Historia

Como usuario que recuerda un fragmento del nombre pero no en qué carpeta quedó,
quiero que el buscador me devuelva resultados de **todas** las carpetas y que cada uno me diga en cuál está,
para encontrarlo sin adivinar y aprender dónde vive para la próxima.

### Estados de interfaz

- **Inicial:** el buscador actual, sin cambios de aspecto.
- **Carga:** el debounce de 300ms ya existente; skeletons si la respuesta tarda.
- **Activo:** lista **aplanada**; las carpetas que coinciden van primero; cada tablero en carpeta muestra su carpeta como **segunda línea** (11px, muted, clickable).
- **Error:** el error de carga existente.
- **Vacío:** "No se encontraron tableros para «xyz»" (copy actual, sin cambios).
- **Al limpiar:** el panel **recupera el estado de expansión anterior**, no colapsa todo.

### Criterios de aceptación

- [ ] La búsqueda devuelve tableros de cualquier carpeta y también los sueltos.
- [ ] Cada resultado que está en una carpeta la muestra; los sueltos **no** muestran segunda línea (evita ruido en 111 filas).
- [ ] Clic en la carpeta del resultado **revela esa carpeta expandida** y limpia la búsqueda.
- [ ] Al limpiar la búsqueda, la expansión previa se restaura.
- [ ] Sigue funcionando el scroll infinito sobre resultados filtrados.
- [ ] La búsqueda **no** se acota a una carpeta (divergencia deliberada con Almacenamiento).
- [ ] El texto de 11px de la segunda línea cumple contraste AA.

### Preguntas abiertas

- **PA-12:** la fila de resultado pasa a **dos líneas** (~44px). ¿Es aceptable cuando el usuario está escaneando resultados, o vale un chip de una línea? **A validar en la demo.**

### Evidencia

- Almacenamiento resuelve esto con una **columna "Ubicación"** clickable, con la ruta completa en el `title` (`FilesView.tsx:778`). En 288px no hay columnas → segunda línea.
- Metabase: *"The search results will display which collection each item is saved in."*

---

## HU-08 · Entender qué son las carpetas la primera vez que las veo

**Usuario:** cualquiera, en su primer contacto · **Flujo:** F1 (empty) · **Criterio:** C8
**Es la historia que decide la adopción del feature.**

### Historia

Como usuario que abre el panel y ve carpetas por primera vez,
quiero entender en una línea qué ganan y cómo empezar,
para no ignorar el feature y seguir scrolleando como siempre.

### Estados de interfaz

- **Sin carpetas (cuenta nueva al feature):** `EmptyState` en la sección "Tableros", **arriba** de la lista plana:
  > **Agrupa tus tableros**
  > Crea carpetas por contexto para encontrarlos más rápido.
  > `[＋ Nueva carpeta]` ← CTA de **texto completo**, no solo el icono.
- **Carpeta recién creada y vacía:**
  > **Sin tableros**
  > Mueve tableros a esta carpeta desde su menú de opciones.
- **Carga / error:** heredan los de la sección.
- **Éxito:** el empty state desaparece cuando existe la primera carpeta con al menos un tablero.

### Criterios de aceptación

- [ ] El empty state es visible **sin scrollear** al abrir el panel.
- [ ] No bloquea ni empuja la lista fuera de la vista: convive con los 159 tableros.
- [ ] Explica el **beneficio** ("encontrarlos más rápido"), no el mecanismo.
- [ ] La carpeta vacía dice **cómo** llenarla (apunta al menú del tablero).
- [ ] Se puede descartar o desaparece solo tras crear la primera carpeta (no reaparece para siempre).
- [ ] No usa la palabra "dashboard" ni jerga técnica.

### Preguntas abiertas

- **PA-13:** ¿el empty state se descarta manualmente y se recuerda por usuario, o desaparece solo al crear la primera carpeta?
- **PA-14 (la más importante):** con **111 tableros sueltos**, crear 4 carpetas no resuelve el problema. ¿El onboarding debería empujar a **mover en lote**? Eso reabriría la multi-selección, hoy fuera de alcance por C7. Alternativa: medir y decidir con datos.

### Evidencia

- Hallazgo de I2: colapsar carpetas con 111 sueltos deja ~115 filas → **el feature depende de que los sueltos bajen**, no de que existan carpetas.
- Por eso la métrica principal no es "carpetas creadas" sino **% de tableros dentro de una carpeta**.

---

## Métricas de éxito y telemetría

La hipótesis es: *si navegar funciona, se busca menos y se llega antes*.

| Métrica | Cómo se lee |
|---------|-------------|
| **% de tableros dentro de una carpeta**, por cuenta | La métrica principal. Si queda bajo, el feature existe pero no resuelve (PA-14). |
| % de cuentas con ≥1 carpeta a los 30 días | Adopción básica. |
| Búsquedas por sesión, **antes vs. después** | Debería **bajar**: navegar reemplaza recordar. |
| Tiempo hasta abrir el primer tablero de la sesión | Debería bajar. |
| Abandonos en el diálogo de eliminar carpeta | Señal de copy confuso (HU-06). |
| Uso de "Deshacer" en mover/quitar | Si es alto, el selector no comunica bien el destino. |
| Ratio menú vs. drag al mover | Valida o descarta el atajo (PA-7). |

**Eventos a instrumentar con el feature** (no después): `folder_created` · `folder_renamed` · `folder_deleted` (con `dashboard_count`) · `dashboard_moved_to_folder` (con `method: menu | drag`) · `dashboard_removed_from_folder` · `move_undone` · `folder_expanded` / `folder_collapsed` · `search_used` (con `had_folders: bool`) · `search_result_folder_clicked`.

---

## Preguntas abiertas transversales

- **PA-1:** el panel auto-colapsa a ≤1200px y en modo colapsado **las carpetas no existen**. ¿Se acepta, o el rail colapsado necesita acceso a carpetas?
- **PA-15:** ¿el feature sale detrás de feature flag? El panel es la navegación principal del OC.

---

## Revisión heurística

Checklist de evaluación UX (universal + items específicos del Operation Center), corrido sobre las 8 historias.

```
ARTEFACTO: 8 historias UX · carpetas en la lista de tableros (SWAT-577)
FECHA: 2026-08-03

CRÍTICOS: 3
IMPORTANTES: 3
MEJORAS: 1
PREGUNTAS CERRADAS POR EL CHECKLIST: 1 (PA-8)

VEREDICTO: listo para prototipar, con los 3 críticos incorporados a la línea base de a11y.
PRIORIDAD #1: el área de toggle de la carpeta debe ser la fila completa, no el chevron.
```

### 🔴 C1 · Targets por debajo del umbral de escritorio (40×36px)

El umbral de Fitts para escritorio es **40×36px**. Medido en el código:

| Control | Tamaño real | ¿Pasa? |
|---------|-------------|--------|
| Chevron de la carpeta | `h-3 w-3` ≈ 12px | ❌ |
| `⋮` de fila (existente) | `p-1` + glifo 12px ≈ 20px | ❌ |
| Botón pin (existente) | ≈ 20px | ❌ |
| Botón `FolderPlus` de crear | `p-1.5` + glifo 16px ≈ 28px | ❌ |

**El panel ya viola este umbral hoy** — no es algo que introduzca el feature, es el precio de la densidad de 32px. Pero sí condiciona cómo se diseñan los controles nuevos:

- **Fix aplicado:** el área de toggle de la carpeta es **toda la fila** (288px × 32px), no el chevron. Expandir es la acción más frecuente del feature y no puede depender de un target de 12px.
- **Fix aplicado:** el disparador de crear tiene un CTA de texto completo en el empty state como camino descubrible (ya estaba, ahora con razón explícita).
- **Aceptado con razón:** `⋮` de la carpeta se mantiene en ~20–28px por consistencia con las filas de tablero existentes. Divergir crearía dos tamaños de icon-button en el mismo panel.
- **Regla nueva:** la fila de carpeta **no** apila tres icon-buttons (contador + chevron + `⋮` pegados) — mínimo 8px entre targets.

### 🔴 C2 · Rutas de escape sin especificar

Ninguna historia decía qué pasa con `Escape` ni dónde queda el foco al cerrar un diálogo. Con 4 diálogos nuevos, es un riesgo de trampa de teclado.

**Fix aplicado (línea base de a11y):** `Escape` cierra todo diálogo salvo mientras guarda · el foco queda atrapado dentro mientras está abierto · al cerrar **vuelve al disparador**, no al `<body>`.

### 🔴 C3 · Semántica de lista ausente

Las historias especificaban `aria-expanded` en la carpeta, pero no cómo se anuncian los hijos. Sin semántica de lista, un lector de pantalla lee 24 filas sin decir cuántas hay ni en qué posición va.

**Fix aplicado:** los hijos van en una lista (`ul`/`li` o `role="group"`) para que se anuncie "3 de 24". El contador viaja en el nombre accesible de la carpeta.

### 🟡 I1 · La segunda línea de 11px está bajo el umbral de legibilidad

El mínimo para texto de cuerpo es 14px. La carpeta como segunda línea en resultados de búsqueda (I3) va en **11px + `muted-foreground`** — doble riesgo: tamaño y contraste a la vez.

**Mitigación:** es metadata, no cuerpo, y reusa el registro `text-[11px]` que ya existe en el panel. Pero se agrega verificación explícita de contraste y **se evalúa subirla a 12px en el prototipo**. Refuerza PA-12.

### 🟡 I2 · `prefers-reduced-motion` no contemplado

La animación de acordeón (0.2s) no tenía excepción para usuarios que piden movimiento reducido. **Fix aplicado** en la línea base.

### 🟡 I3 · Campo requerido sin marcar

El diálogo de nombre tiene un solo campo obligatorio y no estaba marcado como tal. Se resuelve con el botón deshabilitado + validación inline, pero conviene el `aria-required`.

### 🟢 E1 · Duración de la animación: 120 vs 200ms

El checklist del OC pide micro-animaciones de toggle de **120ms**; el acordeón de desyk usa **200ms** (`accordion-down` / `accordion-up`). **Se adopta desyk (200ms)** por consistencia con el resto del producto, y se registra la desviación.

### Items que pasan sin observaciones

Protección de acciones destructivas (HU-06) · estados de error, vacío y carga en todas las historias · mensajes de error en lenguaje natural · confirmación de éxito · validación inline · feedback bajo 400ms (optimistic updates) · ubicación actual indicada · independencia del color · consistencia terminológica ("Eliminar carpeta" ≠ "Quitar de la carpeta" son acciones distintas, no sinónimos mezclados) · sin breadcrumbs porque D2 dejó un solo nivel · acciones reversibles separadas visualmente de las irreversibles.

---

## Trazabilidad

| Historia | Flujo | Criterio del issue | Riesgo |
|----------|-------|--------------------|--------|
| HU-01 Reconocer agrupado | F7 | C4 | Medio — la jerarquía tiene que leerse sin instrucciones |
| HU-02 Crear carpeta | F1 | C1 | Medio — descubribilidad del disparador (PA-4) |
| HU-03 Mover a carpeta | F2 | C2 | Medio — el drag suma complejidad (PA-6, PA-7) |
| HU-04 Quitar de la carpeta | F3 | C3 | Bajo |
| HU-05 Renombrar carpeta | F4 | C1 | Bajo |
| HU-06 Eliminar sin perder tableros | F5 | C1, D6 | **Alto** — el copy es la única barrera contra el malentendido |
| HU-07 Buscar cross-carpeta | F6 | C5 | Medio — filas de dos líneas (PA-12) |
| HU-08 Entender la primera vez | F1 | C8 | **Alto** — decide la adopción (PA-14) |

Los 8 criterios del issue quedan cubiertos: **C1** → HU-02/05/06 · **C2** → HU-03 · **C3** → HU-04 · **C4** → HU-01 · **C5** → HU-07 · **C6** → todas (vía `design.md`) · **C7** → todas (un diálogo por tarea) · **C8** → HU-08 + la ayuda de usuario del handoff.
