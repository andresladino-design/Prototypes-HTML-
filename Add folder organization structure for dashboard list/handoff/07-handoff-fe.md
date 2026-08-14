# Handoff FE — Carpetas en la lista de tableros (SWAT-577)

**Repo:** `fe-solutions-mf` · `src/oc/features/dashboards/` · verificado en `8aebc1879`
**Alcance:** solo el panel de Tableros (D10). El tab **Datasets no se toca**.
**Prototipo:** [`prototypes/index.html`](../prototypes/index.html) · baseline «antes»: [`prototypes/00-baseline-tableros.html`](../prototypes/00-baseline-tableros.html)
**Forma de navegar:** **árbol in-place** (D16). El drill-down por niveles se descartó y se quitó del prototipo.

Decisiones que gobiernan este documento: [`01-decisiones.md`](01-decisiones.md).
Contrato de API: [`07-handoff-be.md`](07-handoff-be.md).

---

## 0. Dos cosas antes de empezar

### 0.1 El prototipo miente en un punto, a propósito

Construye el árbol **en cliente** sobre los 159 tableros en memoria. Producción carga
20 y va pidiendo más (D15). **La estrategia de datos correcta está en §1** y no es la
del prototipo. Todo lo demás —interacción, copy, jerarquía, estados— sí se replica.

### 0.2 Parte de la mejora visual que se ve NO es de este issue

El prototipo tiene activos el **truncado al medio** y los **botones de fila en hover**
(D14). Son un issue aparte: [`ancho-util-lista-tableros/`](../../ancho-util-lista-tableros/).

Al comparar capturas, tenerlo presente. Si ese issue se implementa primero —que es la
recomendación—, la fila ya viene con ~20px más de ancho y este feature los aprovecha.

---

## 1. Estrategia de datos (D15) — decidida, no delegada

```
1. Al montar el panel   → GET /dashboards/folders          (todas, sin paginar)
2. Al montar el panel   → GET /dashboards?unfiled=true     (paginado, scroll infinito)
3. Al expandir carpeta  → GET /dashboards?folder_id={id}   (paginado, scroll infinito)
4. Al buscar            → GET /dashboards?search=…         (plano, cruza todo, con folder.path)
```

**Los contadores vienen del BE.** `subtree_count` es el número que se muestra;
`direct_count` alimenta el tooltip. **No contar en cliente** — con paginación contarías
solo lo que bajaste.

Esto encaja con lo que ya existe: las carpetas arrancan **colapsadas** (I2), así que en
el primer render solo se piden las carpetas y los sueltos. Es *menos* trabajo que hoy.

### Cómo pintar el árbol — lección medida en el prototipo

Aplanar la estructura en filas con `depth` y pintar **una sola lista**, en vez de
componentes recursivos por nivel. Y que **cada fila lleve ya calculado** su `path`,
contador y estado.

La versión ingenua —llamar `countSubtree()` / `folderPath()` desde el render de cada
fila— costaba **60 recorridos de la colección por render (~13.000 accesos)** contra
**3** de la versión de una pasada. En el prototipo eso bloqueaba los clics con el árbol
abierto. Con React y datos del servidor el mecanismo es distinto, pero la forma correcta
es la misma: **calcular una vez, arriba, y bajar datos planos a las filas.**

---

## 2. Componentes nuevos

| Componente | Rol |
|-----------|-----|
| `FolderTree/` | Aplana carpetas + tableros en filas con `depth` y pinta una lista. Orden por nivel: **subcarpetas primero, tableros después** (convención de explorador de archivos). |
| `FolderRow/` | Fila de carpeta · 32px: icono con estado (D13, **sin chevron**) + nombre + `subtree_count` + `⋮`. |
| `CreateFolderWizard/` | 2 pasos (D8): elegir tableros → nombre. Muestra `Dentro de: <ruta>` cuando hay madre. |
| `DashboardPicker/` | Selector múltiple compartido (D8 paso 1 + D9). **Tope de 10 filas visibles**, resto en scroll. |
| `FolderNameDialog/` | Solo renombrar. **No** reusar el de storage: su validación rechaza tildes y `_`. |
| `DeleteFolderDialog/` | `AlertDialog` diciendo **a dónde sube** el contenido (D6). |
| `MoveToFolderDialog/` | **Árbol de destinos con ruta**, no lista simple. Sirve para mover tableros *y* carpetas. |
| `services/dashboards/folders/` | `queriesFn` · `queryKeys` · `schemas` · `types`, siguiendo el patrón exacto de `services/dashboards/favorites/`. |

## 3. Componentes modificados

| Archivo | Cambio |
|---|---|
| `DashboardList.tsx` | Composición árbol + sueltos; diálogos nuevos como **instancia única** (como ya hace con rename/delete/access); modo búsqueda aplanado con ruta. |
| `DashboardListItem.tsx` | Ítems nuevos en `renderActionItems` (aparecen en `⋮` **y** en click derecho automáticamente); ruta de carpeta en modo búsqueda; drag source. |
| `DashboardSection.tsx` | **Colapsable** (D12), manteniendo `loading` / `error` / `empty` / `dropTarget`. |
| `dashboards/schemas.ts` + `types.ts` | Campo `folder: { id, name, path } \| null`; params `folder_id` / `unfiled`. |
| `locales/{es,en,pt}/dashboards.main.json` | Keys nuevas bajo `dashboardsMain.sidebar.folders.*`. |

---

## 4. Jerarquía visual (C4 · I4 revisada)

```
Tableros (155)                          🗀+  ↕A→Z    ← 12px medium muted (header de sección)
▾ 🗀 Adquirencia                     24              ← 14px MEDIUM · SIN chevron (D13)
  │ ▸ 🗀 Visa                          8             ← indentado 12px + guía 1px
  │ 🌐 ADQ-DASH
▸ 🗀 Cierre contable                 12
  Sin carpeta                        100             ← con chevron (D12)
  🌐 Adquirencia_2026_06_04…                         ← suelto: sin indentar
```

**Palancas, en orden de peso** (I4 revisada):

1. **`font-medium`** en la carpeta vs. `font-normal` en el tablero. La principal, y no cuesta densidad.
2. **Icono `Folder` / `FolderOpen`** (`h-3.5 w-3.5`) que **lleva el estado** — sin chevron (D13). `aria-expanded` se conserva en el botón.
3. **Contador** a la derecha, `text-xs muted`, con `subtree_count`. Sin paréntesis (esos son del header de sección).
4. **Indentación de 12px por nivel** + guía vertical de 1px (`border-l border-sidebar-border`). **12, no 16 ni 19** — ver D2.
5. **Fondo:** ninguno en reposo. `bg-accent` es de la fila activa, `hover:bg-muted` del hover.

**Prohibido:** fuente más grande · mayúsculas · color de acento · negrita 600+. Todos esos
registros ya están tomados y competirían con el header de sección.

**Verificar en implementación:** que la fila de carpeta mantenga **32px** de alto. Si el
contador la empuja a 36–40px, se pierde una fila visible por carpeta — y el feature se paga
en el recurso que vino a ahorrar.

---

## 5. Secciones colapsables (D12)

Las 4 secciones llevan chevron: `Configuraciones pendientes`, `Favoritos`, `Tableros`,
`Sin carpeta`.

**Dos claves de `localStorage` separadas, y la distinción importa:**

| Clave | Guarda | Por qué |
|---|---|---|
| carpetas expandidas | **lo abierto** | el default es colapsado (I2) |
| secciones colapsadas | **lo colapsado** | el default es abierta — si guardara lo abierto, una sección nueva aparecería cerrada para todos los usuarios existentes |

Precedente en el repo: `SIDEBAR_COLLAPSED_KEY = "oc_sidebar_collapsed"`.

**Durante la búsqueda** «Tableros» pasa a ser «Resultados»: el toggle se **deshabilita** y el
chevron se oculta. Ahí no es una sección, es el resultado de una consulta.

---

## 6. Puntos técnicos a cerrar

1. **Query keys e invalidación.** Seguir el mapa fino que ya existe para favoritos.
   ⚠️ **Mover una carpeta invalida el subárbol entero**, no una key: los `path` de todos sus
   descendientes cambiaron.
2. **Optimistic updates.** Mover un *tablero* debe sentirse instantáneo — molde en
   `utils/favoriteOptimisticUpdates.ts` (mutate → rollback → settled). Mover una *carpeta*
   probablemente **no** conviene optimista: reescribe paths y los contadores del subárbol.
3. **Transaccionalidad del lote (D8/D9).** Con 1+N llamadas, una falla parcial deja la carpeta
   a medio llenar y el "Deshacer" deja de ser confiable. **El punto de negociación con BE.**
4. **Revelar después de actuar.** Al crear, mover, agregar o renombrar: abrir **toda la cadena
   de ancestros**, scroll hasta la carpeta y resaltarla ~2s. Con anidamiento esto es más crítico
   que antes — expandir la hoja sin expandir la madre **no revela nada**. Fue hallazgo de las
   pruebas: sin esto el usuario queda buscando su propio resultado.
5. **Drag & drop (D7).** Reusar `useDashboardCrossDrag` con un MIME nuevo
   (`DASHBOARD_TO_FOLDER_MIME`); **no** traer `@formkit/drag-and-drop`. A resolver:
   - drop sobre carpeta **colapsada** sin expandirla
   - autoscroll al arrastrar hacia una carpeta fuera del viewport
   - que una fila arrastrada no active a la vez el drop target de Favoritos **y** el de carpetas
   - **arrastrar una carpeta** sobre otra respeta ciclo y tope de 3

   Equivalente por menú y teclado **obligatorio**. Si el alcance aprieta, **se corta el drag,
   no el menú**.
6. **Feature flag.** El panel es la navegación principal del OC; un flag reduce el riesgo.

---

## 7. Estados y guardas en la UI

| Situación | Comportamiento |
|---|---|
| Carpeta en el nivel 3 | «Nueva subcarpeta» **deshabilitada** con etiqueta `máx 3` y tooltip. **No ocultarla**: si desaparece, el usuario la busca porque la vio en otras carpetas |
| Destino inválido en «Mover a» (ciclo o tope) | **No se lista.** Prevenir por ausencia, no dejar elegir y fallar. El BE valida igual |
| Drag hacia destino inválido | Toast de aviso — ahí no se puede prevenir por ausencia |
| Carpeta vacía | Botón outline punteado de 32px con `⊕ Agregar tableros` (D9) |
| Sin carpetas todavía | Empty state con «Agrupa tus tableros» + CTA (HU-08) |
| Búsqueda sin resultados | `No se encontraron tableros para «xyz»` |
| Tablero sin acceso | `opacity-60`, no navegable — igual que hoy. Cuenta en el contador de la carpeta |

---

## 8. Accesibilidad

- `role="tree"` en la lista, `role="treeitem"` + `aria-level` en las filas de carpeta.
- `aria-expanded` en el botón de la carpeta — **imprescindible**, es lo que reemplaza al chevron (D13).
- `aria-label` de la carpeta con **la ruta legible**: `«Visa, dentro de Adquirencia, 8 tableros»`.
- Toda acción de `⋮` alcanzable por teclado. Los botones de fila que aparecen en hover deben
  abrirse también con `focus-within` — y **no** usar `display:none`, que los saca del orden de
  tabulación. (Esto es de D14, pero afecta a las filas de carpeta de este issue.)
- El foco vuelve al disparador al cerrar cualquier diálogo.
- `prefers-reduced-motion`: sin animación de acordeón ni de rotación de icono.

---

## 9. Copy (es) — el que se probó en el prototipo

| Situación | Texto |
|---|---|
| Crear carpeta | `Nueva carpeta` / `Nueva subcarpeta` |
| Contexto de madre | `Dentro de: Adquirencia / Visa` |
| Paso 1 / paso 2 | `Elige los tableros` / `Ponle nombre` |
| Confirmar creación | `Crear con 12 tableros` · `Crear vacía` |
| Menú de carpeta | `Agregar tableros` · `Nueva subcarpeta` · `Renombrar carpeta` · `Mover carpeta a…` · `Eliminar carpeta` |
| Menú de tablero | `Mover a carpeta` · `Quitar de la carpeta` |
| Nombre duplicado | `«Adquirencia» ya tiene una carpeta con este nombre` |
| Tope de profundidad | `Máximo 3 niveles de carpeta` |
| Ciclo | `No se puede mover una carpeta dentro de sí misma` |
| **Eliminar (el más delicado)** | `Se eliminará la carpeta «Visa». Sus 8 tableros y 1 subcarpeta suben a «Adquirencia»; no se eliminan.` |
| Destino raíz en «Mover a» | `Primer nivel (sin carpeta madre)` |
| Separador de sueltos | `Sin carpeta` |
| Toast de mover | `Tablero movido a «Adquirencia / Visa»` + `Deshacer` |

**Regla de léxico:** «Eliminar carpeta» ≠ «Eliminar tablero». Nunca mezclar los verbos. Y
nunca «agregar a carpeta» para un tablero (sugiere acumulación y D3 es exclusiva) — es
**«mover a»**.

---

## 10. Telemetría

`folder_created` · `subfolder_created` · `folder_moved` · `folder_renamed` · `folder_deleted`
· `dashboard_moved_to_folder` · `dashboard_removed_from_folder` · `folder_expanded` ·
`section_collapsed` · `search_used`

**Incluir `depth` en todos los de carpeta.** Es el dato que va a responder si 3 niveles
alcanzan o si alguien necesita un cuarto — la pregunta abierta de D2.

Métrica principal del feature: **% de tableros dentro de una carpeta** (no el número de
carpetas). Es lo que dice si el feature se adoptó.

---

## 11. Definition of done

- [ ] Árbol de hasta 3 niveles con carga perezosa al expandir; contadores del BE.
- [ ] Crear carpeta y subcarpeta, renombrar, mover, eliminar — con «Deshacer» en las cuatro.
- [ ] Mover tablero por menú **y** por drag, con paridad de teclado.
- [ ] Búsqueda cruza todo el árbol y muestra la ruta completa.
- [ ] Las 4 secciones colapsan y persisten (D12), con las dos claves separadas.
- [ ] Fila de carpeta en **32px**, indentación de **12px**, sin chevron (D13).
- [ ] Guardas de ciclo y de tope: destinos inválidos **no ofrecidos**.
- [ ] i18n es/en/pt completo.
- [ ] Telemetría con `depth`.
- [ ] Revisión visual lado a lado contra el baseline.
