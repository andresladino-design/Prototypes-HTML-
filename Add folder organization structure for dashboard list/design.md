# Design — Carpetas en la lista de tableros (SWAT-577)

> Fuente de verdad del diseño de este prototipo. Ohana y Claude lo leen para mantener consistencia.
> **Regla de oro:** todo lo que está acá se puede señalar en el código. Si no se puede señalar, va marcado `⚠️ PROPUESTA`.

**Basado en:** `@simetrikinc/desyk-components@1.30.0-0` · `fe-solutions-mf` @ `8aebc1879`
**Decisiones que lo gobiernan:** [`handoff/01-decisiones.md`](handoff/01-decisiones.md) (D1–D7) · [`handoff/01-benchmark.md`](handoff/01-benchmark.md) (I1–I6)
**Última actualización:** 2026-08-03

---

## Principios

1. **Fidelidad antes que belleza.** El panel de Tableros existe; esto es una extensión, no un rediseño. Cualquier píxel que se vea distinto al producto es un error, no una mejora.
2. **La densidad es el recurso escaso.** El feature existe para que quepan más tableros reconocibles en pantalla. Todo lo que suba el alto de fila trabaja contra el objetivo.
3. **Jerarquía por peso, no por tamaño.** El panel ya tiene tres registros tipográficos ocupados (header de sección 12px, fila 14px, metadata 11px). Las carpetas se distinguen con `font-medium`, no con una cuarta escala.
4. **Una tarea a la vez.** Cada acción abre exactamente un diálogo y resuelve exactamente una cosa (criterio C7).
5. **Nada destructivo sin decirlo con números.** Eliminar una carpeta no borra tableros, y el copy tiene que afirmarlo explícitamente (D6).
6. **Reconocer antes que recordar.** El objetivo del feature; si algo obliga a recordar un nombre, está mal resuelto.
7. **Velocidad sobre perfección** en el prototipo: Tailwind CDN + Alpine + Lucide, sin build.

---

## Tokens

Extraídos a [`design/tokens.css`](design/tokens.css) desde `dist/styles.css`, con los mismos nombres de variable que el producto.
Mapeo token → clase de Tailwind en [`design/tailwind.desyk.js`](design/tailwind.desyk.js), derivado de `dist/tailwind-preset.cjs`.

### Color — los que este feature usa

| Token | HSL | Uso en este feature |
|-------|-----|--------------------|
| `--sidebar-background` | `0 0% 98%` | Fondo del panel |
| `--sidebar-border` | `240 6% 90%` | Guía vertical de los hijos de una carpeta, separadores |
| `--foreground` | `240 6% 10%` | Nombre de tablero y de carpeta |
| `--muted-foreground` | `0 0% 55%` | Header de sección, contador de carpeta, iconos secundarios, segunda línea de búsqueda |
| `--muted` | `240 5% 96%` | **Hover** de fila y de icon-buttons |
| `--accent` | `240 5% 96%` | **Fondo de fila ACTIVA** — reservado, no usar para hover |
| `--info` | `221 83% 53%` | Icono `Globe` (tablero público) · línea de inserción y tinte de drop target |
| `--warning` | `41 96% 40%` | Badge de instalación pendiente (`bg-warning/15` + glifo `text-warning`) |
| `--destructive` | `360 72% 51%` | Acción "Eliminar carpeta" y su botón de confirmación |
| `--primary` | `240 94% 60%` | Botón primario ("Nuevo tablero"), foco |
| `--border` | `0 0% 85%` | Bordes de inputs y de botones `outline` |
| `--ring` | `221 83% 63%` | Anillo de foco |
| `--radius` | `0.5rem` | `rounded-lg`; las filas usan `rounded-md` = `radius − 2px` |

**Convención:** el valor se declara en HSL sin función y se consume con `hsl(var(--token))`, lo que permite modular opacidad — `bg-warning/15`, `bg-info/5`, `border-muted-foreground/20`. Mantener esa indirección.

### 🔴 `--muted-foreground` no cumple AA — medido, no estimado

| Par | Contraste | Requiere | |
|-----|-----------|----------|---|
| `muted-foreground` sobre `sidebar-background` | **3.22:1** | 4.5:1 | ❌ |
| `muted-foreground` sobre `background` | **3.36:1** | 4.5:1 | ❌ |
| `sidebar-foreground` sobre `sidebar-background` | **10.01:1** | 4.5:1 | ✅ |
| `foreground` sobre `sidebar-background` | **16.97:1** | 4.5:1 | ✅ |
| `sidebar-border` sobre `sidebar-background` (guía de 1px) | **1.22:1** | 3:1 | ❌ (decorativo) |

`--muted-foreground` (`0 0% 55%` = `#8C8C8C`) **falla AA para texto normal en las dos superficies del producto**, y hoy se usa en todo el panel: el header de sección, los contadores, los iconos secundarios. **Es una deuda de accesibilidad preexistente**, no algo que introduzca este feature.

**Regla para este feature:** todo texto que **lleve información** usa `--sidebar-foreground` (10:1), no `--muted-foreground`. Aplica al contador de la carpeta, a la segunda línea con la carpeta en resultados de búsqueda y al separador "Sin carpeta". `--muted-foreground` queda solo para elementos **decorativos o transitorios** (iconos que aparecen en hover, placeholders).

La **guía vertical de 1px** en 1.22:1 es aceptable porque es decorativa: la pertenencia la comunica la indentación, no la línea. La línea nunca puede ser el único indicio de anidación.

**⚠️ Trampa detectada:** el preset de desyk mapea `tooltip: hsl(var(--tooltip))`, pero **el token `--tooltip` no está definido** ni en `dist/styles.css` ni en el `globals.css` del OC. No usar `bg-tooltip` / `text-tooltip-foreground`.

**Modo oscuro:** desyk **no** redefine `--success` / `--warning` / `--info` en `.dark` (heredan de `:root`). Si el prototipo suma tema oscuro, revisar contraste de esos tres.

### Tipografía

- **Familia:** `Inter` (importada en `styles.css`), fallback `ui-sans-serif, system-ui, -apple-system…`.
- **Escala real del panel** (medida en el código, no elegida):

| Registro | Clase | Dónde |
|----------|-------|-------|
| 14px | `text-sm` | Fila de tablero y fila de carpeta |
| 12px medium muted | `text-xs font-medium text-muted-foreground` | Header de sección (`SECTION_LABEL_CLASS`) |
| 12px | `text-xs` | Títulos de empty state, botones chicos |
| 11px | `text-[11px]` | Contador de carpeta, segunda línea de búsqueda, descripciones de empty state |

- **Pesos:** `font-normal` (nombre de tablero) · `font-medium` (carpeta, fila activa, header de sección) · nunca 600+ en el panel: se lee como header.

### Densidad y geometría

| Medida | Valor | Fuente |
|--------|-------|--------|
| Ancho del panel | ~280px | Captura de producción |
| Alto de fila | **32px** (`h-8`) | `SidebarListSkeletonRow` lo fija explícitamente para que el swap skeleton→real no mueva nada |
| Padding de fila | `px-2 py-1.5` | `DashboardListItem` |
| Gap entre filas | `gap-0.5` (2px) | `DashboardSection` |
| Padding horizontal de sección | `px-3` | `DashboardSection` |
| Iconos de fila | `h-3.5 w-3.5` | privacidad, carpeta |
| Glifos de icon-button | `!h-3 !w-3` con `p-1` | pin, `⋮`, chevron |
| Radio de fila | `rounded-md` | `DashboardListItem` |

> **Invariante del feature:** la fila de carpeta debe medir **32px igual que un tablero**. Si el contador la empuja a 36–40px, se pierde una fila visible por carpeta y el feature se paga en el recurso que vino a ahorrar. (El chevron ya no está — D13.) Verificar en la revisión visual.

---

## Inventario de componentes desyk

Cada uno con su doc en `fe-solutions-mf/node_modules/@simetrikinc/desyk-components/skills/desyk/references/<componente>.md` — la columna **Ref** nombra ese archivo.

### Ya usados por el panel (replicar tal cual)

| Componente | API que importa | Ref |
|-----------|-----------------|-----|
| `button` | `variant`: default · destructive · **outline** · secondary · ghost · link · `size`: default · lg · **icon-default** · icon-lg · icon-sm · `shape`: square · circle | `button.md` |
| `dialog` | `Dialog` · `DialogContent` · `DialogHeader` · `DialogTitle` · `DialogDescription` · `DialogFooter` | `dialog.md` |
| `alert-dialog` | `AlertDialog` · `AlertDialogContent` · `AlertDialogHeader/Title/Description` · `AlertDialogFooter`. **No se cierra clickeando fuera** | `alert-dialog.md` |
| `dropdown-menu` | `DropdownMenu` · `DropdownMenuTrigger asChild` · `DropdownMenuItem` · `DropdownMenuSeparator` | `dropdown-menu.md` |
| `context-menu` | Misma API; `ContextMenuTrigger` **envuelve** el área de click derecho | `context-menu.md` |
| `empty-state` | `EmptyState` · `EmptyStateContent` (icono o acción) · `EmptyStateTitle` · `EmptyStateDescription` | `empty-state.md` |
| `sonner` | `toast()` · `.success` · `.error` · `.warning` · `.info` · **`action: { label, onClick }`** ← el "Deshacer" | `sonner.md` |
| `tooltip` | `Tooltip` · `TooltipTrigger asChild` · contenido vía wrapper del OC | `tooltip.md` |
| `input` / `label` | Campo del diálogo de nombre | `input.md` |
| `skeleton` | `SidebarListSkeletonRow` (icono + barra de ancho variable) | `skeleton.md` |
| `scroll-area` | Scroll del panel, con `[data-radix-scroll-area-viewport]` | `scroll-area.md` |
| `alert` | `Alert variant="destructive"` inline dentro de diálogos cuando falla la acción | `alert.md` |

### Nuevos para este feature

| Componente | Para qué | Ref |
|-----------|----------|-----|
| `collapsible` | La carpeta. `Collapsible` (`open` / `onOpenChange`) + `CollapsibleTrigger asChild` + `CollapsibleContent` | `collapsible.md` |
| `command` | Buscador dentro del selector "Mover a carpeta" cuando hay > 7 carpetas: `CommandInput` · `CommandList` · `CommandEmpty` · `CommandItem onSelect` | `command.md` |
| `stepper` | Wizard de creación en 2 pasos (D8): `Stepper currentStep` · `StepperItem` · `StepperIndicator state` · `StepperLabel` | `stepper.md` |
| `checkbox` | Selección de tableros en el paso 1 del wizard | `checkbox.md` |
| `badge` | Solo si el prototipo necesita el chip "en: carpeta" — **descartado en I3** a favor de la segunda línea | `badge.md` |

### Infra propia del panel (no traer librerías nuevas)

| Hook | Qué hace |
|------|----------|
| `hooks/useDashboardCrossDrag.ts` | `useDashboardDragSource` / `useDashboardDropTarget({ acceptMime, onDrop })` con MIME types. Para carpetas: **MIME nuevo** `DASHBOARD_TO_FOLDER_MIME` |
| `shared/hooks/useHtml5Sortable.ts` | Reorder vertical con línea de inserción `before`/`after` |
| `utils/favoriteOptimisticUpdates.ts` | Molde de optimistic update: `onMutate` → `onError` rollback → `onSettled` invalidate |

**No usar** `@simetrikinc/desyk-components/drag-and-drop` (`@formkit`): el panel ya tiene DnD HTML5 propio y probado.

**Nota de implementación (solo repo, no prototipo):** en el OC **no** se importan los `*Content` de desyk directamente sino los wrappers de `@oc/shared/components/desyk-components-with-portals` (`SolutionsDialogContent`, `SolutionsAlertDialogContent`, `SolutionsDropdownMenuContent`, `SolutionsContextMenuContent`, `SolutionsTooltipContent`…). Resuelven el portal dentro del Shadow DOM del microfrontend. Omitirlos rompe el scroll.

---

## Patrones de producto

Los tres patrones ya existen en el panel; las carpetas los siguen sin inventar nada.

### Crear (2 pasos · D8)

Disparador (**I1**) → **paso 1: elegir tableros** (buscador + checkboxes, sueltos primero) → **paso 2: nombre + resumen de lo que se guarda** → validación de duplicado **inline** → la carpeta se **revela** (scroll + resalte ~2s) → `toast` con Deshacer.

Usa `stepper` de desyk. Precedentes en el producto: `CreateConnectionWizard` y `TemplateFormDialog/steps`.

- Disparador: `Button` icono `FolderPlus` con `Tooltip`, en el `headerAction` de la sección "Tableros", a la izquierda del toggle A→Z.
- **Deshabilitado mientras hay búsqueda activa** (como `FilesView` en Almacenamiento).
- El campo se enfoca y selecciona al abrir (`requestAnimationFrame` + `select()`, como el rename de tableros).
- `Enter` confirma; el botón queda deshabilitado con el campo vacío o mientras guarda (`Guardando...` + `LoaderCircle animate-spin`).

### Renombrar

Ítem de menú → **el mismo diálogo** en modo `rename` con el valor precargado → 409 del servidor se muestra como error de duplicado inline **y** toast.

### Eliminar

`AlertDialog` (no `Dialog`: no se descarta clickeando fuera) → nombre entre comillas en la descripción → botón `bg-destructive text-destructive-foreground hover:bg-destructive/90` → estado `Eliminando...` → si falla, `Alert variant="destructive"` **inline** (no toast).

### Estados de sección

`DashboardSection` ya los resuelve; las carpetas heredan:

| Estado | Render |
|--------|--------|
| `loading` | 3 skeletons en secciones, 5 en Tableros |
| `error` | `AlertCircle` + mensaje `text-destructive` + descripción 11px + botón "Reintentar" (`RefreshCw`, `h-7 text-xs`) |
| `empty` | `EmptyState` con CTA |
| `ready` | `flex flex-col gap-0.5` de filas + `afterList` (sentinel de scroll infinito) |

### Acciones en fila

- Invisibles en reposo (`text-muted-foreground/0`), visibles en `group-hover` y en `focus-visible`.
- **Duplicadas en click derecho** vía `ContextMenu` con exactamente los mismos ítems (el panel lo hace con una función `renderActionItems(Item, Separator)` compartida — seguir ese patrón).
- La destructiva va última, tras `Separator`, en `text-destructive focus:text-destructive`.

---

## Jerarquía visual de carpetas (criterio C4)

Resuelto en **I4**. La carpeta es un nivel **intermedio**: por debajo del header de sección, por encima de la fila de tablero.

> **🔄 Revisado el 2026-08-14** por D2 (3 niveles), D13 (el icono absorbe el chevron) y la
> corrección del ancho útil real del panel.

**El ancho disponible para una fila es 240px, no 288.** `w-72` (288px) menos `px-3` **dos veces**:
en el `<aside>` del layout (`OcContentLayout.tsx:171`) y otra vez en el cuerpo de la sección
(`DashboardSection`). Todos los cálculos de jerarquía y truncado se hacen sobre **240**.

```
Tableros (155)                    [🗀+] [↕A→Z]   ← 12px medium muted
▾ 🗀 Adquirencia               24                ← 14px MEDIUM · SIN chevron · contador 12px
  │ ▸ 🗀 Visa                     8               ← subcarpeta · indent 12px · guía 1px
  │ 🌐 ADQ-DASH                                   ← 14px normal
▸ 🗀 Cierre contable           12
  🌐 Adquirencia                                  ← suelto: 14px normal, sin indentar
```

Palancas, en orden de peso:

1. **`font-medium`** en la carpeta vs. `font-normal` en el tablero. Palanca principal, no cuesta densidad.
2. **Icono** `Folder` / `FolderOpen` (`h-3.5 w-3.5 text-muted-foreground`) que **lleva el estado**. **Sin chevron** (D13): son 16px por fila y un elemento menos que procesar al escanear. `aria-expanded` se conserva en el botón — lo que se fue es solo el glifo.
3. **Contador** a la derecha, `text-xs text-muted-foreground`, **sin paréntesis** (los paréntesis son del header de sección: "Tableros (155)"). Muestra el **total del subárbol**, no los directos; el desglose va en el `title`.
4. **Indentación** de los hijos de **12px** + **guía vertical de 1px** `border-l border-sidebar-border`, una guía por ancestro.
5. **Fondo:** ninguno en reposo. `hover:bg-muted` para hover, `bg-accent` reservado para la fila activa.

**Por qué 12px y no 16.** Con 3 niveles de anidamiento (D2), 16px por nivel dejaría el nombre de
un tablero de nivel 3 en ~140px, y los nombres reales tienen 40 caracteres. A 12px el peor caso
es **166px** para el tablero y **158px** para la carpeta. Es el número que sostiene la decisión:

| | nivel 1 | nivel 2 | nivel 3 |
|---|---|---|---|
| Nombre de carpeta | 182px | 170px | **158px** |
| Nombre de tablero dentro | 190px | 178px | **166px** |

**Dónde SÍ se conserva el chevron:** solo en los encabezados de sección colapsables (D12), que
no tienen icono que pueda cargar el estado. Eso deja una distinción limpia:
**chevron = sección del sistema · icono con estado = carpeta del usuario**.

El árbol es **in-place** y no navega por niveles (D16), así que no hay ningún lugar donde el
chevron signifique «entrar».

**Prohibido:** fuente mayor a 14px · mayúsculas · color de acento en la carpeta (los acentos están tomados: `text-info` en `Globe`, `warning` en pendiente, `destructive` en eliminar) · peso 600+.

### Drop target (drag como atajo, D7)

Reusar el vocabulario visual que ya existe en `DashboardSection`:

- Variante `subtle`: `bg-primary/5` cuando se está encima (la usa hoy la sección Tableros).
- Variante `dashed`: borde punteado + `border-info/50 bg-info/5` al encima, `bg-destructive/10 ring-1 ring-destructive` si el drop es inválido (la usa Favoritos).
- Para carpetas: **highlight de la fila de carpeta** (`bg-info/5` + `border-info/50`), que funcione **con la carpeta colapsada**.

---

## Patrón: «Panel de recursos del OC»

Los paneles de Tableros, Anomalías y Pendientes hacen lo mismo —listar recursos de la cuenta para
navegarlos— pero hoy divergen en **10 de 10 slots**, incluida la altura del buscador. Las carpetas
tienen que aterrizar en los tres, así que sin un patrón común el componente se implementa tres veces.

### El eje que ordena todo: artefacto vs. evento

Antes de los slots, la regla que explica las diferencias legítimas:

| | **Artefacto** — tableros, datasets, conciliaciones | **Evento** — anomalías |
|---|---|---|
| Qué es | algo que el usuario **crea y conserva** | algo que **llega solo** y no deja de llegar |
| Unidad de fila | **32px**, densa | **card** multilínea (~110px) |
| Ancho del panel | **288px** (`w-72`) | **425px** (`w-[425px]`) — lo pide la card |
| Fin de lista | **scroll infinito** (lo explorás) | **paginación numerada** (con 3054, necesitás saltar y saber dónde estás) |
| Acción de crear | **sí** | no existe |
| **Carpeta** | **declarada** | **heredada** |

**Es un solo eje, no dos reglas.** El mismo criterio que decide la membresía de carpeta (D10) decide
la anatomía del panel. Cuando aparezca una entidad nueva, se clasifica una vez y todo lo demás se
deriva.

### Los 9 slots, en orden fijo

| # | Slot | Siempre | Especificación |
|---|------|---------|----------------|
| 1 | **Header** | ✅ | Título `text-sm font-semibold` + **contador como badge** `rounded-full bg-secondary text-[11px]` + botón colapsar `ghost icon-lg` con `ChevronLeft` |
| 2 | **Modo** | — | Tabs segmentadas `h-10 rounded-xl bg-muted p-1`, triggers `h-8 rounded-lg`. Labels visibles si caben; con 3+ tabs en 425px, solo la activa muestra label y toma `flex-1` |
| 3 | **Crear** | solo artefactos | `Button variant=outline` `h-10` a ancho completo, icono `Plus` + "Nuevo {singular}" |
| 4 | **Buscar** | ✅ | `Input h-10 rounded-[0.625rem]`, icono `Search` a la izquierda, placeholder **"Buscar {qué}"** |
| 5 | **Filtros** | — | Fila de pills `h-9` outline. La destructiva/limpiar va como link, no como pill |
| 6 | **Fijados** | — | Sección con contador `n/máx` y drop target punteado |
| 7 | **Organizar** | ✅ (lo nuevo) | Carpetas. Si la vista **ya tiene** otra agrupación, se ofrece como toggle "Agrupar por" (SD-7), nunca como nivel extra |
| 8 | **Lista** | ✅ | Fila 32px o card, según el eje |
| 9 | **Pie** | ✅ | Scroll infinito o paginación, según el eje |

**El slot 7 es el que este feature agrega.** Si los slots 1–6 no están alineados, el 7 hereda tres
comportamientos distintos.

### Qué se corrige y qué no

**Accidental → se unifica** (no cambia funcionalidad, solo consistencia):

| Qué | Antes | Ahora |
|---|---|---|
| Contador | `(155)` en el header de sección · `1-20 de 3054` al pie · badge junto al título | **badge junto al título** en los tres (slot 1) |
| Buscador en Anomalías | no existía | **"Buscar por recurso"** — con 3054 incidencias y 153 páginas, filtrar exigía armar un filtro |
| Altura del buscador | `h-9` en Pendientes, `h-10` en Tableros | **`h-10`** en los tres |
| Contenedor de Anomalías | dos cards con gap | **una card con `border-r`**, como los otros dos |

**Semántico → se documenta la regla, no se unifica:** unidad de fila, ancho, fin de lista y acción de
crear. Se derivan del eje artefacto/evento.

### Inconsistencias que quedan abiertas

- **SD-8 · "Favoritos" vs "Fijados".** Tableros dice "Favoritos (5/15)" y Pendientes "Fija o arrastra
  conciliaciones aquí" — **mismo mecanismo (`Pin`), dos nombres**. Unificar es una decisión de producto
  con impacto en copy establecido y en el tope de 15; no se toca sin acuerdo.
- **Tabs de modo.** Tableros muestra label en las dos; Anomalías solo en la activa. La regla propuesta
  ("labels si caben") lo explica, pero conviene verificar si las tres de Anomalías caben en 425px.
- **Acción primaria en Pendientes.** No tiene "Nueva conciliación" aunque es un artefacto. Puede ser
  correcto (se crean en otro flujo) o un hueco. A confirmar.

## Voz y tono

- Español. Glosario Simetrik: **tablero** (nunca "dashboard" en UI), **carpeta** (alineado con Almacenamiento), **Conciliación**, **Fuente**.
- Labels cortos y accionables. Describir el estado, no el mecanismo.
- **"Mover a carpeta"**, nunca "Agregar a carpeta" (D3: la pertenencia es exclusiva, no acumulativa).
- **"Eliminar carpeta"**, nunca "Eliminar" a secas (tiene que ser imposible leerlo como "eliminar tablero").
- **"Quitar de la carpeta"** para sacar un tablero sin eliminarlo.

### Copy (fuente para las keys de i18n)

| Situación | Copy |
|-----------|------|
| Botón crear (tooltip / aria-label) | Nueva carpeta |
| Título del wizard (D8) | Nueva carpeta |
| Paso 1 · título / ayuda | Elige los tableros · *Marca los tableros que quieres agrupar. Podrás mover más después.* |
| Paso 1 · atajos | Seleccionar los {{count}} visibles · Limpiar · **{{count}} seleccionados** |
| Paso 1 · aviso | Algunos ya están en otra carpeta: se moverán a esta. |
| Paso 2 · título | Ponle nombre |
| Label / placeholder del campo | Nombre de la carpeta |
| Ayuda del campo | Acepta tildes, espacios y guion bajo. Máximo 100 caracteres. |
| Paso 2 · resumen | Se creará con **{{count}} tableros** · Se creará vacía |
| Paso 2 · volver a elegir | Cambiar la selección |
| **Botón de confirmación (D8)** | Crear con {{count}} tableros · **Crear vacía** si no hay selección — nunca solo "Crear" |
| Navegación del wizard | Siguiente · Atrás · Cancelar |
| Error de duplicado | Ya existe una carpeta con este nombre |
| Título diálogo renombrar | Renombrar carpeta |
| Descripción renombrar | Cambia el nombre de la carpeta. Los tableros que contiene no se mueven. |
| **Menú de carpeta** | Agregar tableros · Renombrar carpeta · Eliminar carpeta |
| Menú de tablero | Mover a carpeta · Quitar de la carpeta |
| **Carpeta vacía (D9)** | Botón outline punteado: **⊕ Agregar tableros** — ofrece la acción, no describe el mecanismo |
| Título "Agregar tableros" (D9) | Agregar tableros a «{{nombre}}» |
| Ayuda de "Agregar tableros" | Marca los tableros que quieres mover a esta carpeta. |
| Botón de "Agregar tableros" | Agregar {{count}} tableros |
| Título eliminar | ¿Eliminar carpeta? |
| **Descripción eliminar** | Se eliminará la carpeta «{{nombre}}». Los **{{count}} tableros** que contiene volverán a la lista de tableros; **no se eliminarán**. |
| Descripción eliminar (vacía) | Se eliminará la carpeta «{{nombre}}». Está vacía. |
| Toasts | Carpeta «{{nombre}}» creada con {{count}} tableros · Carpeta «{{nombre}}» creada · está vacía · Carpeta renombrada a «{{nombre}}» · Carpeta «{{nombre}}» eliminada · {{count}} tableros en la lista · Tablero movido a «{{nombre}}» · Tablero quitado de la carpeta · {{count}} tableros agregados a «{{nombre}}» · {{count}} salió de otra carpeta |
| Acción de deshacer | Deshacer *(disponible ~60s, estándar del OC)* |
| Sin carpetas (primer uso) | Agrupa tus tableros · Crea carpetas por contexto para encontrarlos más rápido. |
| Separador de sueltos | Sin carpeta |

**Validación del nombre** (I6): `trim` · mínimo 1 · **máximo 100** · **sin restricción de caracteres**, siguiendo `dashboardNameSchema.ts`.
⚠️ **No** usar la validación de Almacenamiento (`/^[a-zA-Z0-9- ]+$/`): rechaza "Conciliación diaria" y "Tesorería".

---

## Accesibilidad

- **Teclado completo:** toda tarea se completa sin mouse. El drag es atajo, nunca requisito (D7).
- La fila de carpeta es un `CollapsibleTrigger` con `aria-expanded`; `Enter`/`Espacio` alternan.
- Contador anunciado en el nombre accesible ("Adquirencia, 24 tableros"), no solo visual.
- Contraste: 4.5:1 en texto, 3:1 en iconos y bordes. Ojo con `text-muted-foreground` (`0 0% 55%`) sobre `--sidebar-background` (`0 0% 98%`) en 11px — verificar en el prototipo.
- Foco visible siempre (`focus-visible`), nunca `outline: none` sin reemplazo.
- Los botones que aparecen en hover deben aparecer también en `focus-visible` (el panel ya lo hace).
- `aria-disabled` en vez de `disabled` cuando el click debe seguir dando feedback (patrón del botón de pin al llegar al tope).

---

## Decisiones

- **2026-08-03 — Tokens extraídos, no transcritos a ojo.** `design/tokens.css` sale de `dist/styles.css` y `design/tailwind.desyk.js` de `dist/tailwind-preset.cjs`, para que el HTML use los mismos nombres de utilidad que el TSX y el prototipo sea comparable 1:1 con el repo. Razón: la Etapa 3 (vista espejo) solo tiene valor si es indistinguible del producto.
- **2026-08-03 — La jerarquía de carpeta se resuelve con peso, no con escala** (I4). Razón: los tres registros tipográficos del panel ya están ocupados; una cuarta escala o competiría con el header de sección o se leería como metadata.
- **2026-08-03 — Alto de fila de carpeta = 32px, invariante.** Razón: el feature existe para ganar filas visibles; una carpeta de 40px se come el beneficio.
- **2026-08-03 — Validación de nombre de carpeta = la de tablero, no la de Almacenamiento.** Razón: el regex de Almacenamiento rechaza tildes y `_`, es decir el propio glosario Simetrik y los nombres reales de los tableros.
- **2026-08-03 — `--accent` queda reservado para la fila activa**; el hover de carpetas usa `muted`. Razón: es la convención vigente del panel y romperla haría ambiguo qué tablero está abierto.
- **2026-08-03 — El texto informativo secundario usa `--sidebar-foreground`, no `--muted-foreground`.** Razón: medido, `muted-foreground` da 3.22:1 sobre el fondo del panel y falla AA. Es deuda preexistente del producto; el feature no la hereda.
- **2026-08-03 — Toda la fila de carpeta es el área de toggle** (288 × 32px), no el chevron de 12px. Razón: hallazgo 🔴 C1 de la revisión heurística — expandir es la acción más frecuente del feature y el umbral de Fitts para escritorio es 40×36px. El `⋮` se mantiene chico a propósito, por consistencia con las filas de tablero.
- **2026-08-03 — La carpeta en resultados de búsqueda va en 12px (`text-xs`), no 11px.** Razón: hallazgo 🟡 I1 — 11px queda lejos del mínimo de legibilidad y esa línea **lleva información** que el usuario necesita. Sube a 12px y a contraste 10:1. Queda por validar en la demo si la fila de dos líneas molesta al escanear (PA-12).
- **2026-08-03 — La animación de expandir respeta `prefers-reduced-motion`** y usa el acordeón de desyk (200ms), no los 120ms que pide el checklist del OC para toggles. Razón: consistencia con el resto del producto; desviación registrada.
- **2026-08-03 — Crear carpeta pasa a ser un wizard de 2 pasos** (elegir tableros → nombre), y toda acción sobre una carpeta la **revela** con scroll + resalte de ~2s. Razón: al probar el prototipo, crear una carpeta cerraba el diálogo y dejaba al usuario buscando su propio resultado entre 4 carpetas y 100 sueltos; y una carpeta vacía no es un resultado verificable. Ver D8 en `handoff/01-decisiones.md`.
- **2026-08-03 — El botón de confirmación nombra la consecuencia:** "Crear con 12 tableros" en vez de "Crear". Razón: el label es el último lugar donde el usuario puede verificar qué está guardando.
- **2026-08-04 — Los estados vacíos ofrecen la acción, no la describen.** La carpeta vacía lleva un **botón outline punteado** de 32px (`border-dashed border-border`, hover `border-info/60 bg-info/5`) con `⊕ Agregar tableros`, en vez del texto "mueve tableros desde su menú de opciones". Razón: describir el mecanismo obliga al usuario a traducirlo en pasos; el punteado comunica "acá falta contenido" sin competir con las filas reales. Ver D9.
- **2026-08-04 — Se documenta el patrón «Panel de recursos del OC»** con 9 slots en orden fijo, y el eje **artefacto vs. evento** como criterio que deriva la anatomía. Razón: los tres paneles divergían en 10 de 10 slots y las carpetas tienen que aterrizar en los tres; sin patrón común, el componente se implementa tres veces. Se unifica lo accidental (contador, buscador, alturas) y se documenta como regla lo semántico (fila, ancho, paginación).
- **2026-08-04 — Anomalías gana buscador de texto** ("Buscar por recurso"). Razón: era el único panel sin slot 4, y con 3054 incidencias en 153 páginas encontrar las de un recurso exigía construir un filtro.
