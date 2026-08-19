# Handoff — Carpetas en la lista de tableros (SWAT-577)

**Fecha:** 2026-08-19 · **Origen:** `prototypes/index.html` validado + D1–D20
**Registro:** Op Center (interno) · **Patrón de presentación:** árbol in-place en el panel lateral
**Issue:** [SWAT-577](https://linear.app/simetrik/issue/SWAT-577/enhancement-dashboards-add-folderorganization-structure-for-dashboard)

> **Este archivo es el punto de entrada.** Es autocontenido para decidir *qué* construir. Los
> anexos tienen el detalle de *cómo*:
>
> | | |
> |---|---|
> | [`01-frontend.md`](01-frontend.md) | Componentes, estados, a11y, telemetría, DoD |
> | [`02-backend.md`](02-backend.md) | Modelo, endpoints, `path` materializado, permisos |
> | [`03-flujos.md`](03-flujos.md) | Los 13 user flows con sus ramas |
> | [`04-historias.md`](04-historias.md) | Historias y criterios de aceptación |
> | [`05-antes-despues.md`](05-antes-despues.md) | Diff contra producción |
>
> El **porqué** de cada decisión no vive acá: está en [`../design-record/`](../design-record/).
> Si vas a discutir una decisión, empezá por [`01-decisiones.md`](../design-record/01-decisiones.md).

---

## 1. Contexto y objetivo

Los usuarios del OC acumulan **tableros** en una lista plana. La cuenta de referencia tiene
**155**, y el buscador exige **recordar** el nombre. Falta un mecanismo de **reconocimiento**.

**Objetivo:** bajar el tiempo de encontrar un tablero reduciendo carga cognitiva — chunks de
5–9 en vez de una lista de 155 (Ley de Miller).

**Qué se construye:** carpetas de hasta **3 niveles** dentro de la sección «Tableros» del panel
lateral, navegables como **árbol in-place** (expandir, no navegar).

**Qué NO se construye:** carpetas en Datasets, Anomalías ni Pendientes · etiquetas ·
pertenencia múltiple · orden manual · colores de carpeta · reasignar autoría.

## 2. Usuario y registro

**Op Center — registro interno.** Analistas y ops que entran **todos los días** y cuyo gesto más
frecuente es **cambiar de tablero**. Eso es lo que decidió el patrón: el árbol in-place expande
sin navegar, porque un drill-down por niveles le sumaría clics justo a lo que más se hace (D16).

Densidad alta permitida. Fila de **32px**, `text-sm`, sin fuentes grandes ni acentos decorativos.

## 3. Historias de usuario

Ocho historias con criterios de aceptación en [`04-historias.md`](04-historias.md). El resumen:

| | Historia |
|---|---|
| HU-01 | Crear una carpeta eligiendo tableros (wizard de 2 pasos) |
| HU-02 | Mover un tablero a una carpeta |
| HU-03 | Quitar un tablero sin eliminarlo |
| HU-04 | Renombrar una carpeta |
| HU-05 | Eliminar una carpeta **sin perder tableros** |
| HU-06 | Buscar cruzando todas las carpetas |
| HU-07 | Navegar el árbol y que el estado persista |
| HU-08 | Primer uso: no hay carpetas todavía |

## 4. Arquitectura de componentes desyk

**Todo es desyk. Cero componentes custom nuevos** salvo la composición del árbol.

| Elemento de la UI | Componente desyk | Notas |
|---|---|---|
| Panel lateral | `Sidebar` (ya existe) | `OcContentLayout.tsx` — se le agrega ancho variable, ver §7 |
| Secciones colapsables | `Collapsible` | Las 4: Pendientes · Favoritos · Tableros · Sin carpeta |
| Fila de carpeta | composición propia sobre `Button variant="ghost"` | icono `Folder`/`FolderOpen` + nombre. **Sin chevron** (D13), **sin contador** (D18) |
| Menú de la fila | `DropdownMenu` | Disparador `⋮`, visible en hover/focus |
| Menú por click derecho | `ContextMenu` | **Mismos ítems que el DropdownMenu**, sin excepción |
| Renombrar | `Dialog` + `Input` | 1 input → Dialog es correcto por el árbol de overlays |
| Eliminar | `AlertDialog` | Destructivo. **No** `Dialog`: no se descarta clickeando fuera |
| Crear carpeta (2 pasos) | `Dialog` + `Checkbox` + `Stepper` | ⚠️ ver hallazgo **H4** en §13 |
| Mover a carpeta | `Dialog` con árbol | ⚠️ ver hallazgo **H5** en §13 |
| Avisos con «Deshacer» | `Sonner` | Todo lo reversible va acá, **no** a un diálogo |
| Tooltips | `Tooltip` | Motivo del tope de 3 niveles, nombre completo truncado |
| Carga | `Skeleton` | **Nunca spinner** |
| Sin carpetas | `EmptyState` | Con CTA, ver §5 |
| Contadores de sección | `Badge` | Solo de **sección**; la fila de carpeta no lleva |
| Handle de ancho | convenciones de `Resizable` | ver §7 y hallazgo **H1** |

## 5. Estados

| Estado | Comportamiento |
|---|---|
| **Loading** | `Skeleton` con la **forma** de la lista (filas de 32px), no spinner. Al expandir una carpeta, skeleton dentro de ella |
| **Empty · sin carpetas** | `EmptyState`: «Agrupá tus tableros» + CTA `Nueva carpeta`. Es el estado de primer uso (HU-08) |
| **Empty · carpeta vacía** | Botón outline **punteado** de 32px dentro de la carpeta: `⊕ Agregar tableros` (D9) |
| **Empty · búsqueda** | `No se encontraron tableros para «xyz»` |
| **Error** | Fallo al crear/renombrar: **inline en el diálogo** (`Alert variant="destructive"`), no toast. Fallo al mover/eliminar: toast |
| **Partial** | Lista paginada de 20 con scroll infinito (D15). El árbol se pide aparte y completo |
| **Success** | `Sonner` con «Deshacer» + la carpeta afectada se **revela** con scroll y resalte |
| **Sin permiso** | Ítems del `⋮` **deshabilitados** con `aria-disabled` + motivo al pie del menú (D20). **Nunca ocultarlos** |
| **Tope de 3 niveles** | «Nueva subcarpeta» deshabilitada con etiqueta `máx 3` + tooltip |
| **Destino inválido al mover** | **No se lista.** Prevenir por ausencia, no dejar elegir y fallar |

## 6. Copy

Completo en [`01-frontend.md`](01-frontend.md) §9. **Glosario verificado: 0 violaciones** —
las 60 apariciones de «dashboard» en los anexos son identificadores de código, y la prosa usa
**tablero** en los 29 casos de cara al usuario.

Los dos strings que más importan:

**Eliminar una carpeta** — tiene que **romper activamente** la expectativa de Almacenamiento,
donde el mismo botón **sí** borra el contenido:

> Se eliminará la carpeta «Visa». Sus **8 tableros y 1 subcarpeta** suben a «Adquirencia»;
> **no se eliminan**.

**Sin permiso** — el copy cambia según si el autor sigue en la cuenta, porque las salidas son
distintas:

| Autor | Mensaje |
|---|---|
| Activo | `Solo María, que creó esta carpeta, puede renombrarla, moverla o eliminarla.` |
| Inactivo | `Lucía ya no está en la cuenta. Solo alguien que gestione accesos puede renombrarla, moverla o eliminarla.` |

Mandar a «pedile a Lucía» cuando Lucía no está es un callejón sin salida. **Un mensaje de
permisos nombra la salida, no la puerta cerrada.**

**Regla de léxico:** «Eliminar carpeta» ≠ «Eliminar tablero», nunca mezclar los verbos. Y nunca
«agregar a carpeta» para un tablero (sugiere acumulación, y D3 es exclusiva): es **«mover a»**.

## 7. Microinteracciones

Canon Simetrik: **120 / 200 / 320 ms `ease-out`**.

| Interacción | Duración | Qué anima |
|---|---|---|
| Expandir/colapsar carpeta o sección | **200ms** `ease-out` | `height` (el `accordion-down`/`up` de desyk) |
| Rotación del chevron de sección | **200ms** `ease-out` | `transform` |
| Aparición del `⋮` en hover | **120ms** `ease-out` | `width` + `opacity` |
| Cambio de ancho del panel al soltar | **200ms** `ease-in-out` | `width` — ver nota |
| Preview de la franja al arrastrar | **120ms** `ease-out` | `width` + `left` |
| Resalte al revelar una carpeta | **320ms** `ease-out` | `background` + `ring`, y se apaga |

**Nota sobre el ancho del panel:** usa `ease-in-out`, no `ease-out`, porque **replica la
transición que ya tiene `OcContentLayout` para el colapso**. Es una desviación deliberada del
canon a favor de la consistencia con producción.

### El gesto de redimensionar (D17)

- **Handle en el borde derecho**, hit area de **8px** (mínimo desyk), visualmente sutil.
- **Snap a tres anchos fijos**: 288 (`sm`, default) · 384 (`md`) · 480 (`lg`).
- **El panel NO sigue al cursor.** Durante el arrastre se sombrea **solo la franja que se gana o
  se devuelve**, con una línea de 2px en el borde destino y las tres paradas marcadas en 1px.
  Sombrear el panel entero taparía la lista que el usuario está leyendo.
- **Sin rótulo `S`/`M`/`L`:** es vocabulario de diseñador, no le dice al usuario hasta dónde va a
  llegar el panel.
- **`user-select: none`** en `body` durante el arrastre, o el gesto va seleccionando nombres.
- **Teclado:** `role="separator"` + `aria-valuenow/min/max`, flechas ←/→, `Home`/`End`.
- **Doble click en el handle → vuelve al default** (288) en 200ms `ease-out`. Convención desyk.
- **Persistencia:** `oc_sidebar_width`, clave propia. **No unificar** con `oc_sidebar_collapsed`.
- **Colapso automático:** reusar `restoreIfNoAutoCollapse` (`OcContentLayout.tsx:86`). **Gana el
  colapso**, y al reexpandir se recupera el tamaño elegido. No inventar mecanismo.

## 8. AI integration

**Esta feature no tiene IA, y es deliberado.** Organizar tableros es una decisión del usuario
sobre su propio espacio: no hay nada que resumir antes, sugerir durante ni validar después.

**No agregar** `AiChat`, sugerencias de agrupación automática ni badges de IA. Si más adelante
la telemetría muestra que nadie organiza, la conversación es *sugerir carpetas a partir de los
nombres* — y sería un issue aparte, con su propio discovery.

## 9. Endpoints esperados

Contrato completo en [`02-backend.md`](02-backend.md). Lo que el FE necesita:

```
GET    /dashboards/folders                → árbol completo, sin paginar
GET    /dashboards?folder_id={id}         → tableros de una carpeta (paginado, 20)
GET    /dashboards?search=…               → plano, cruza todo, con folder.path
POST   /dashboards/folders                → crear (+ asignar tableros en el mismo call)
PATCH  /dashboards/folders/{id}           → renombrar
PATCH  /dashboards/folders/{id}/parent    → mover carpeta
DELETE /dashboards/folders/{id}           → disolver un nivel
PATCH  /dashboards/{id}/folder            → mover un tablero
PATCH  /dashboards/folder                 → lote
```

**Tres cosas que hoy NO existen y bloquean el FE:**

1. **`created_by` no viaja** en el listado de carpetas. Sin él no se pueden pintar los estados
   deshabilitados de D20.
2. **`can_manage`** calculado por el servidor. Que el FE compare ids duplica la política.
3. **`subtree_count` y `direct_count`** siguen siendo necesarios — cambió *dónde* se pintan
   (`title` y `aria-label`), no que se pidan.

> **El árbol no se puede resolver en cliente** (D15). La lista es paginada con `search` y `sort`
> server-side. Cualquier diseño que asuma la colección completa en memoria no es implementable.
> **El prototipo lo hace en cliente solo porque es un prototipo.**

## 10. Edge cases y validaciones

| Caso | Esperado |
|---|---|
| Nombre duplicado | **Entre hermanas**, no global: `Adquirencia / 2026` y `Cierre contable / 2026` conviven |
| Tildes y `_` en el nombre | **Permitidos.** No reusar el validador de Almacenamiento: rechaza `/^[a-zA-Z0-9- ]+$/` |
| Mover una carpeta dentro de su propio subárbol | No se ofrece el destino. El BE valida igual (guarda por prefijo de `path`) |
| Mover algo que superaría los 3 niveles | El destino no se lista |
| Eliminar una carpeta de primer nivel | Su contenido queda suelto — caso particular de «sube un nivel» |
| Nombre de 45 caracteres | Se trunca **al medio** conservando la cola. Solo entra completo en `lg` |
| Carpeta con 60 tableros | Scroll infinito dentro de la carpeta |
| Carpeta huérfana (autor inactivo) | Solo `oc:manage_access` puede gestionarla |
| Crear carpeta y querer renombrarla | `created_by` **tiene que quedar seteado al crear**, o queda inmanejable |
| Eliminar + «Deshacer» | Restaura la carpeta, el `parent_id` de las hijas, el `folder_id` de los tableros **y el `created_by` original** |
| Tablero sin acceso dentro de una carpeta | `opacity-60`, no navegable. **Sí** cuenta en `subtree_count` |
| Búsqueda activa | «Nueva carpeta» deshabilitado; la sección pasa a ser «Resultados» y no colapsa |

## 11. Test cases sugeridos

**Obligatorios** (si uno falla, no se mergea):

1. **Eliminar una carpeta NO elimina ningún tablero.** Es criterio del issue y ya no lo garantiza
   el motor de base de datos (D6): es lógica de servicio en una transacción.
2. **El contenido sube a la carpeta madre, no a la raíz.**
3. **Unicidad entre hermanas**, no global.
4. **Guarda de ciclos:** mover «Adquirencia» dentro de «Adquirencia / Visa» falla.
5. **Tope de 3 niveles** respetado también por *mover* (no solo por crear).
6. **Sin permiso, los tres endpoints devuelven 403** — no solo se deshabilita en la vista.
7. **`created_by` queda seteado** en las cuatro rutas de creación.
8. **«Deshacer» un borrado restaura el autor original**, no a quien deshace.

**Del FE:** el árbol pinta con `depth` en una sola lista (no recursión) · el estado de expansión
persiste entre recargas · la cadena de ancestros del tablero activo se revela completa · el
`⋮` es alcanzable por teclado · el ancho elegido sobrevive al colapso automático.

## 12. Tokens

Solo tokens desyk, **cero hex**. Los que aplica esta feature:

`--sidebar-foreground` · `--sidebar-border` (guías de indentación) · `--border` · `--background` ·
`--muted` (hover de sección) · `--accent` (fila activa) · `--secondary` (badges de sección) ·
`--info` (drop target, handle activo, preview de ancho) · `--destructive` (eliminar) ·
`--warning` (instalación pendiente) · `--muted-foreground`

> ⚠️ `--muted-foreground` **no cumple AA** — medido, está registrado en `design.md`. No usarlo
> para texto que haya que leer, solo para glifos y elementos secundarios.

**Medidas que no son negociables:** fila de **32px** · indentación de **12px** por nivel (no 16
ni 19) · guía de **1px** · hit area del handle de **8px**.

## 13. Revisión contra las leyes Simetrik

Corrida con `/simetrik-ui handoff` el 2026-08-19.

### Pasa

- **Glosario:** 0 violaciones (verificado excluyendo código y URLs).
- **`DropdownMenu` con `ContextMenu` equivalente** — el árbol de overlays lo exige.
- **`AlertDialog` para eliminar**, `Sonner` con «Deshacer» para lo reversible.
- **Deshabilitar en vez de ocultar** — coincide con el criterio del skill.
- **Empty states activos** con forma y CTA, no ilustraciones vacías.
- **Skeleton, nunca spinner.**
- **Light mode** consistente, sin mezcla.
- **Sin bans:** cero sparkles, cero «Powered by AI», cero gradient text, cero hex, cero
  side-stripes, cero chat flotante.
- **Hit area del handle = 8px**, el mínimo que pide desyk.
- **Persistencia con clave propia por contexto.**

### Hallazgos

| # | Hallazgo | Severidad |
|---|---|---|
| **H1** | **desyk dice «Sidebar fija con ancho del producto → `Sidebar`, NO `Resizable` simulando sidebar».** D17 hace redimensionable el panel, así que hay tensión con esa regla. El argumento a favor: no estamos *simulando* un sidebar con `Resizable`, estamos dando ancho variable a uno que ya existe, y los nombres reales de 45 caracteres no caben en 240px. **Hay que decidirlo explícitamente con FE o lo van a frenar en review.** | 🔴 |
| **H2** | **Faltaba el doble click en el handle para volver al default.** Es convención desyk. Ya está incorporado en §7, falta en el prototipo. | 🟡 |
| **H3** | **`duration-150` y `duration-100` no son canon** (120/200/320). El prototipo usa 150 en seis lugares y 100 en dos. Corregir a 120 al implementar. | 🟡 |
| **H4** | **El wizard de crear es un `Dialog`, y por el árbol de overlays debería ser `Sheet`.** `Dialog` es para «tarea modal corta, 1–3 inputs». El wizard tiene dos pasos y multi-selección sobre 155 tableros — y además el usuario está eligiendo *de la lista que queda detrás*, que es el caso de uso de `Sheet`. | 🟡 |
| **H5** | **`MoveToFolderDialog` con árbol de destinos, mismo caso que H4.** Es un picker sustantivo, no 1–3 inputs. | 🟡 |
| **H6** | **Los anexos no declaraban microinteracciones.** El §7 de este archivo es nuevo: antes no había duraciones especificadas en ninguna parte del handoff. | 🟡 |

**H4 y H5 no los cambio por mi cuenta:** D8 y D7 eligieron `Dialog` con argumentos propios y son
decisiones cerradas. Quedan como recomendación del skill para revisar, no como cambio aplicado.

## 14. Checklist pre-PR

- [ ] Componentes desyk, sin custom innecesarios
- [ ] Glosario aplicado en todos los strings de cara al usuario
- [ ] Estados completos: loading (skeleton) · empty (con CTA) · error (inline en diálogos) · sin permiso
- [ ] Duraciones en canon 120/200/320 (**H3**)
- [ ] Light mode consistente
- [ ] A11y: `role="tree"`/`treeitem`/`aria-level` · `aria-expanded` · focus trap y retorno al
      disparador en los diálogos · el `⋮` alcanzable por teclado · `aria-disabled` con motivo
- [ ] La guarda de permisos está en el **handler**, no solo en el `disabled` — el click derecho y
      el teclado llegan sin pasar por el botón
- [ ] Los 8 tests obligatorios de §11 verdes
- [ ] Fila de 32px · indentación de 12px · handle de 8px
- [ ] `created_by` y `can_manage` en el response del BE (**bloqueante**)
- [ ] Validación de permisos en el endpoint, no solo en la vista (**bloqueante**)
- [ ] **H1 resuelto** con FE antes de implementar el resize
