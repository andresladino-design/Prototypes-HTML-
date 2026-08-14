# Benchmark acotado — Interacción de carpetas (SWAT-577)

**Fecha:** 2026-08-03
**Alcance:** cerrar las 6 preguntas de interacción I1–I6. El modelo ya estaba decidido ([`01-decisiones.md`](01-decisiones.md)).
**Método:** benchmark **interno** leyendo el código del producto (pesa más: criterio C6) + benchmark **externo** acotado a las preguntas que el producto no responde.

---

## Resumen de las 6 respuestas

| # | Pregunta | Respuesta |
|---|----------|-----------|
| **I1** | Disparador de "Nueva carpeta" | **Botón icono `FolderPlus` + tooltip en el header de la sección "Tableros"**, junto al toggle A→Z. Deshabilitado durante la búsqueda. Entrada secundaria dentro del selector de "Mover a carpeta". |
| **I2** | Default de expansión | **Colapsadas**, con 3 excepciones: se revela la carpeta del tablero activo · el estado se persiste en `localStorage` · si hay una sola carpeta, arranca expandida. |
| **I3** | Carpeta en resultados de búsqueda | **Segunda línea dentro de la fila** (icono de carpeta + nombre, `text-[11px] text-muted-foreground`), clickable para revelar la carpeta. Las carpetas que coinciden con el término se listan primero. |
| **I4** 🔄 | Jerarquía visual | Mismo `text-sm` que un tablero (la densidad no se toca) + **`font-medium`** + icono de carpeta **con estado (sin chevron, D13)** + contador del **subárbol** a la derecha + hijos indentados **12px** con guía de 1px. **Sin** fuente más grande, **sin** mayúsculas, **sin** color de acento. |
| **I5** | Cuántas carpetas | **Sin tope duro.** Objetivo de diseño 7 ± 2 · aviso suave al pasar de 15 · máximo técnico defensivo 50 por cuenta. |
| **I6** | ¿Reusar el `FolderNameDialog` de Almacenamiento? | **No reusar el componente ni su validación** — su regex rechaza acentos y `_`. Componente propio en `features/dashboards` que reusa las reglas de nombre de **tablero**. Sí se reusa el **léxico**. |

---

## ⚠️ Dos hallazgos que cambian decisiones previas

### 1. La validación de nombre de Almacenamiento **rompe el español**

`features/storage/utils/folderValidation.ts` valida con `NAME_PATTERN = /^[a-zA-Z0-9- ]+$/`:

| Nombre de carpeta | ¿Pasa la validación de Almacenamiento? |
|-------------------|----------------------------------------|
| `Cierre contable` | ✅ |
| `Conciliación diaria` | ❌ (tilde) |
| `Tesorería` | ❌ (tilde) |
| `Adquirencia_2026_06` | ❌ (guion bajo) |

Los tableros reales de la cuenta se llaman `Adquirencia_2026_06_04_...`, y el glosario Simetrik usa **Conciliación**. Reusar ese validador haría imposible nombrar una carpeta como el dominio la nombra.

**Regla correcta para carpetas de tableros** = la de los tableros (`utils/dashboardNameSchema.ts`): `trim`, mínimo 1, **máximo 100**, sin restricción de caracteres. Coherente además con que una carpeta agrupa tableros, no archivos.

### 2. En Almacenamiento, "Eliminar carpeta" **sí borra el contenido**. En tableros, no.

Copy real de Almacenamiento (`storage.main.json`):

> **¿Eliminar carpeta?**
> La carpeta "Ventas" se eliminará. Contiene 3 carpeta(s), 12 archivo(s).

Ese diálogo **advierte** sobre el contenido porque se destruye (`countFolderContents` cuenta descendientes para asustar, con razón). Nuestro D6 hace lo **opuesto**: desagrupa.

**Consecuencia:** el mismo botón, el mismo icono y casi el mismo título tendrán **consecuencias opuestas en dos partes del producto**. El copy de tableros tiene que **romper activamente** la expectativa, no solo omitir la advertencia:

> **¿Eliminar carpeta?**
> Se eliminará la carpeta «Adquirencia». Los **24 tableros** que contiene volverán a la lista de tableros; **no se eliminarán**.

Y nunca decir solo "Eliminar" en el menú de la carpeta (Almacenamiento dice `actions.delete: "Eliminar"`): en tableros debe decir **"Eliminar carpeta"**, para que jamás se lea como "eliminar tablero".

---

## I1 — Dónde vive "Nueva carpeta"

### Evidencia

| Fuente | Qué hace |
|--------|----------|
| **Almacenamiento** (`FilesView.tsx:1504-1517`) | `Button variant="outline" size="icon-default"` con icono `FolderPlus` y tooltip "Nueva carpeta", en la toolbar, **a la izquierda del botón primario** ("Subir archivos"). Y **`disabled={isSearching}`**. |
| **Paquetes de notificación** (`NotificationPackagesPanel.tsx:105`) | `Button` primario con `Plus` + label, arriba a la derecha del header de la vista. |
| **`FolderPicker`** (`components/shared/FolderPicker.tsx`) | Permite **crear carpeta inline dentro del selector**: botón `Plus` por nodo + input inline validado. |
| **desyk** `patterns/data-list.md` | El botón de crear va en la **toolbar del listado**, junto a la búsqueda y los filtros. |
| **Metabase** | "Click the **+** button in the left nav sidebar **at the top of the Collections section**" ([docs](https://www.metabase.com/docs/latest/exploration-and-organization/collections)). |
| **Panel de Tableros hoy** | El header de la sección ya aloja una acción: el toggle A→Z (`tablerosHeaderAction`, `DashboardList.tsx:325-349`). |

### Decisión

**Botón icono `FolderPlus` (variant outline o ghost, con tooltip "Nueva carpeta") en el header de la sección "Tableros", a la izquierda del toggle A→Z.**

Razones:

1. **Proximidad:** las carpetas viven dentro de esa sección (D4); el disparador va donde ocurre el efecto.
2. **El slot ya existe:** `DashboardSection` acepta `headerAction` y ya lo usa el toggle A→Z. Es aditivo, no una zona nueva.
3. **Doble respaldo:** replica el patrón de Almacenamiento (icono + tooltip) y el de Metabase (`+` en el header de la sección del sidebar).
4. **No degrada la acción más frecuente:** "Nuevo tablero" sigue siendo el botón primario ancho arriba del panel. Convertirlo en split-button metería una decisión (Hick) en el camino que más se recorre.

**Complementos:**

- **Entrada secundaria en el selector de "Mover a carpeta"** ("＋ Nueva carpeta"), como hace `FolderPicker`: si el usuario descubre que necesita una carpeta *mientras* mueve, no lo mandamos a empezar de nuevo.
- **Deshabilitado mientras hay búsqueda activa**, igual que Almacenamiento: en modo búsqueda la lista está aplanada y "crear acá" no tiene una ubicación clara.

**Descartado:** split-button en "Nuevo tablero" (Hick sobre el camino frecuente) · solo click derecho en el vacío (no descubrible; se suma como atajo, no como vía) · botón de texto ancho "Nueva carpeta" (compite visualmente con el primario y gasta 32 px de alto en un panel donde el objetivo es ver más filas).

**Riesgo aceptado (Fitts):** un icono de ~28 px es un target pequeño para la entrada principal de un feature nuevo. Mitigación: el empty state de la sección (cuando no hay carpetas) lleva un CTA de texto completo, así el primer uso no depende del icono.

---

## I2 — Colapsadas o expandidas por defecto

### Evidencia

- **Progressive disclosure:** un acordeón "typically starts in a collapsed state", pero con una advertencia explícita: *"users can't scan collapsed content, which means important information might stay hidden"* ([IxDF](https://ixdf.org/literature/topics/progressive-disclosure), [Primer](https://primer.style/ui-patterns/progressive-disclosure)).
- **Favoritos** (este mismo panel) está siempre visible y sin colapsar, porque es un atajo de ≤15 ítems.
- **Almacenamiento** no aplica: navega por niveles (drill-down), no expande in-place.
- **Grafana** operó con carpetas planas hasta v11.0.0 y solo después anidó ([issue #65604](https://github.com/grafana/grafana/issues/65604)).

### Decisión

**Colapsadas por defecto**, con tres excepciones:

1. **La carpeta que contiene el tablero activo se revela expandida** al cargar el panel. Sin esto, el usuario abre el OC y no ve dónde está parado.
2. **El estado de expansión se persiste** en `localStorage` por (cuenta, usuario). Es lo que hacen Notion, Linear y VS Code; colapsar todo en cada recarga se lee como un bug.
3. **Con una sola carpeta, arranca expandida.** Colapsarla no ahorra nada y esconde el 100 % del contenido organizado.

### 🔴 Hallazgo incómodo que sale de esta pregunta

Con el mock realista (4 carpetas + **111 tableros sueltos**), colapsar todo deja ~115 filas para escanear. **Las carpetas por sí solas no resuelven el problema si los sueltos no bajan.**

Esto no invalida el feature: lo condiciona. Implicaciones que se llevan a las Etapas 5 y 6:

- La métrica que importa no es "carpetas creadas" sino **"% de tableros dentro de una carpeta"**.
- El **onboarding** (HU-08) tiene que empujar a organizar, no solo a crear una carpeta vacía.
- Si la adopción se estanca, **la primera mejora a desbloquear es la multi-selección** ("mover 12 tableros de una vez"), hoy fuera de alcance por C7 pero explícitamente marcada como aditiva y reversible.

---

## I3 — Cómo se muestra la carpeta en un resultado de búsqueda

### Evidencia

| Fuente | Qué hace |
|--------|----------|
| **Almacenamiento** (`FilesView.tsx:778-803`) | En modo búsqueda cambia de tabla y agrega una **columna "Ubicación"**: icono de carpeta + nombre, `title` con la **ruta completa**, y **click navega a esa carpeta**. |
| **Almacenamiento** (`searchData`, línea 659) | La búsqueda recorre **todas** las carpetas e incluye **carpetas que coinciden** con el término, no solo archivos. |
| **Almacenamiento** (`DataToolbar`, `searchScope`) | Cuando estás dentro de una carpeta, la búsqueda queda **acotada a esa carpeta** y lo indica con un `Badge` "en: <carpeta>" dentro del input. |
| **Metabase** | *"The search results will display which collection each item is saved in"* ([Metabase Learn](https://www.metabase.com/learn/metabase-basics/getting-started/find-data)). |

### Decisión

En el sidebar no hay columnas, así que la columna "Ubicación" se traduce a una **segunda línea dentro de la fila**:

```
🌐 Adquirencia_2026_06_04_conciliacion
   📁 Adquirencia                        ← 11px, muted, clickable
```

- `text-[11px] text-muted-foreground`, icono de carpeta `h-3 w-3`.
- Click en esa línea → **revela la carpeta expandida** y limpia la búsqueda (equivalente al `navigateToFolder` de Almacenamiento).
- Los tableros **sin carpeta** no muestran segunda línea (evita ruido en 111 filas).
- Las **carpetas que coinciden** con el término se listan **primero**, antes de los tableros; click las abre. Es barato: la lista de carpetas está completa en el cliente (I5 la acota a decenas).

**Divergencia deliberada respecto a Almacenamiento:** allá la búsqueda se **acota** a la carpeta actual (badge "en: X"); acá **siempre cruza todas las carpetas** — es el criterio C5 del issue. No se copia el patrón de scope.

**Descartado:** chip a la derecha de la fila (compite con el pin y el `⋮`, y se trunca en 280 px) · agrupar los resultados por carpeta (contradice el objetivo de aplanar y obliga a escanear grupos para encontrar uno).

---

## I4 — Palancas de jerarquía visual (criterio C4)

### Evidencia (medida en el código, no a ojo)

| Elemento | Estilo real |
|----------|-------------|
| Header de sección | `SECTION_LABEL_CLASS = "text-xs font-medium text-muted-foreground"` → 12px, medium, gris |
| Fila de tablero | `text-sm` (14px) + `px-2 py-1.5`, iconos `h-3.5 w-3.5`, alto efectivo 32px (`SidebarListSkeletonRow` lo fija en `h-8`) |
| Fila activa | `bg-accent` + `font-medium` |
| Contador de Favoritos | `5/15` dentro del header, en el mismo `text-xs` muted |
| Botones de fila | `p-1` con glifo `!h-3 !w-3`, invisibles hasta `group-hover` |

El header de sección ya ocupa el registro "12px + medium + muted + mayúscula visual". Si la carpeta subiera de tamaño competiría con él; si bajara, se confundiría con metadata.

### Decisión — la fila de carpeta

> **🔄 Revisada el 2026-08-14** por D2 (3 niveles), D13 (el icono absorbe el chevron) y la
> corrección del ancho útil real del panel. La versión original está debajo, en «Lo que cambió».

```
Tableros (155)                    [🗀+] [↕A→Z]     ← 12px medium muted (header de sección)
▾ 🗀 Adquirencia              24                   ← 14px MEDIUM · SIN chevron (D13)
  │ ▸ 🗀 Visa                    8                 ← indentado 12px + guía 1px
  │ 🌐 ADQ-DASH                                    ← 14px normal
▸ 🗀 Cierre contable          12
  🌐 Adquirencia                                   ← suelto: 14px normal, sin indentar
```

Palancas, en orden de peso:

1. **`font-medium`** en el nombre de la carpeta vs. `font-normal` en el tablero. Es la palanca principal y no cuesta densidad.
2. **Icono `Folder` / `FolderOpen`** (`h-3.5 w-3.5`, `text-muted-foreground`) que **lleva el estado**. **Sin chevron** (D13): son 16px por fila y un elemento menos que procesar. `aria-expanded` se conserva en el botón.
3. **Contador** a la derecha, `text-xs text-muted-foreground` — mismo registro que el `5/15` de Favoritos. Muestra el **total del subárbol**, no los directos. Sin paréntesis (los paréntesis son del header de sección).
4. **Indentación de los hijos de 12px** + **guía vertical de 1px** (`border-l border-sidebar-border`), que es lo que hace legible el pertenecer. **12, no 16:** con 3 niveles de anidamiento, 16px por nivel dejaría el nombre en ~140px.
5. **Fondo:** ninguno en reposo. `bg-accent` está reservado para la fila activa y `hover:bg-muted` para el hover — no se toca.

### Lo que cambió respecto a la versión original

| | Antes (2026-08-03) | Ahora | Por qué |
|---|---|---|---|
| Chevron | `ChevronRight` / `ChevronDown` a la izquierda del icono | **no existe** | D13 — el icono lleva el estado; 16px recuperados |
| Indentación | ~16px | **12px** | D2 — con 3 niveles, 16px no cabe |
| Contador | tableros de la carpeta | **total del subárbol** | D2 — colapsada, «24» debe significar «hay 24 acá dentro» |
| Tamaño del contador | `text-[11px]` | `text-xs` (12px) | alineado con el resto de los contadores del panel |

**Corrección de un dato del benchmark original:** decía «el panel mide ~280px». El ancho real
disponible para una fila es **240px** — `w-72` (288px) menos `px-3` **dos veces**: en el
`<aside>` del layout (`OcContentLayout.tsx:171`) y otra vez en el cuerpo de la sección
(`DashboardSection`). Los cálculos de jerarquía y truncado se hacen sobre 240, no 280.

**Prohibido:** fuente más grande (rompe la densidad y compite con el header de sección) · mayúsculas (registro ya usado) · color de acento (los acentos ya están tomados: `text-info` en `Globe`, `warning` en el badge de pendiente, `destructive` en eliminar) · negrita 600+ (se lee como header).

**Verificación pendiente en el prototipo (Etapa 6):** que la fila de carpeta mantenga los 32px de alto. Si el contador la empuja a 36–40px, se pierde una fila visible por carpeta — y el feature se paga en el recurso que vinimos a ahorrar.

---

## I5 — Cuántas carpetas son demasiadas

### Evidencia

- **Miller:** 7 ± 2 chunks es el rango donde el reconocimiento es barato.
- **Favoritos** tiene tope **duro** de 15 (`FAVORITES_LIMIT`), verificado incluso contra la lista sin filtrar para que la búsqueda no lo evada.
- **Grafana** vivió con carpetas planas y terminó necesitando anidación cuando el número creció ([issue #65604](https://github.com/grafana/grafana/issues/65604)) — y la anidación trajo sus propias incompatibilidades ([issue #124158](https://github.com/grafana/grafana/issues/124158)).
- El panel muestra ~20 filas sin scroll.

### Decisión

**Sin tope duro**, a diferencia de Favoritos: un tope en Favoritos tiene sentido porque es un atajo de acceso rápido; un tope de carpetas bloquearía la organización de una cuenta grande, que es justo el caso que atendemos.

En su lugar:

| Umbral | Comportamiento |
|--------|----------------|
| 7 ± 2 | **Objetivo de diseño**, expresado en el copy del onboarding ("agrupa por contexto, no por tablero") |
| > 15 | **Aviso suave, no bloqueante**, sugiriendo consolidar. Nunca impide crear. |
| 50 | **Máximo técnico** por cuenta (defensivo: evita abuso y que la lista de carpetas necesite paginación) |

Y lo que realmente hay que vigilar no es el número de carpetas, sino el **% de tableros sueltos** (ver el hallazgo de I2).

---

## I6 — ¿Reusar el `FolderNameDialog` de Almacenamiento?

### Evidencia

- `features/storage/components/folders/FolderNameDialog.tsx` (95 líneas): `Dialog` + `Label` + `Input` + error inline, modos `create` | `rename`, valida contra `siblings`.
- `features/storage/utils/folderValidation.ts`: requerido · **máx 150** · **`/^[a-zA-Z0-9- ]+$/`** · duplicado case-insensitive.
- `features/dashboards/utils/dashboardNameSchema.ts`: `trim` · min 1 · **máx 100** · **sin patrón de caracteres**.
- `features/dashboards/components/DashboardNameField`: ya resuelve el caso completo (validación local + duplicado contra servidor + manejo de 409 + `serverDuplicateError`).

### Decisión

**Componente propio en `features/dashboards`**, reusando `DashboardNameField` como base y las reglas de nombre de **tablero** (máx 100, sin restricción de caracteres). No se importa nada de `features/storage`.

Razones:

1. **La validación de Almacenamiento es incorrecta para este dominio** — rechaza "Conciliación diaria" y "Tesorería" (ver hallazgo #1).
2. **Acoplamiento cross-feature:** que `features/dashboards` importe de `features/storage` crea una dependencia entre dos features de las que ninguna es dueña del componente.
3. **El patrón de duplicado ya existe acá** con manejo de 409 del servidor (`DashboardList.tsx:249-262`), que Almacenamiento no tiene.

**Propuesta para el handoff (deuda técnica, no bloqueante):** extraer un `shared/components/FolderNameDialog` parametrizable por validador, y migrar Almacenamiento después. Se propone, no se ejecuta en este alcance: tocar Almacenamiento es riesgo de regresión fuera del issue.

### Léxico: qué se reusa y qué no

| Copy de Almacenamiento | ¿Se reusa en tableros? |
|------------------------|------------------------|
| "Nueva carpeta" | ✅ Igual |
| "Crear carpeta" / "Renombrar carpeta" | ✅ Igual (títulos de diálogo) |
| "Nombre de la carpeta" | ✅ Igual (placeholder) |
| "Ya existe una carpeta con este nombre…" | ✅ Adaptado (sin "en esta ubicación": D2 = un nivel) |
| "¿Eliminar carpeta?" | ✅ Título igual, ⚠️ **descripción opuesta** (ver hallazgo #2) |
| "Carpeta creada correctamente." / "renombrada" / "eliminada" | ✅ Igual (toasts) |
| "Mover" (menú) | ❌ En tableros: **"Mover a carpeta"** (más explícito, sin jerarquía que desambiguar) |
| Validación `[a-zA-Z0-9- ]` máx 150 | ❌ **No** — usar reglas de nombre de tablero (máx 100) |
| Búsqueda acotada a la carpeta actual | ❌ **No** — C5 exige cruzar carpetas |
| "Ubicación" como columna | ➖ Traducido a segunda línea en la fila (I3) |

---

## Anti-patrones detectados (lo que no vamos a copiar)

1. **Doble semántica del verbo "eliminar"** entre Almacenamiento y Tableros. Lo mitigamos con copy explícito, pero conviene registrarlo como inconsistencia de producto.
2. **Validación de nombres que no soporta el idioma del producto** (Almacenamiento rechaza tildes). No replicarlo.
3. **Anidar antes de necesitarlo:** Grafana anidó y arrastró incompatibilidades con features que asumían un nivel ([#124158](https://github.com/grafana/grafana/issues/124158)). Refuerza D2.
4. **Multi-selección con checkboxes permanentes** (Metabase la usa para mover en lote): agrega una capa de modo a un panel de navegación. Queda fuera por C7, y si entra debe ser como acción temporal, no como columna de checkboxes siempre visible.
5. **Colapsar todo en cada carga:** se lee como pérdida de estado. Ver I2.

## ¿Aplica la metáfora de "explorador de archivos"?

El issue la cita (*"similar to a file explorer / desktop folder structure"*). Conclusión: **aplica el vocabulario, no la interacción.**

- ✅ Se toma: la palabra "carpeta", el icono, la idea de pertenencia exclusiva, el drag como atajo.
- ❌ No se toma: navegación por niveles con breadcrumb (el panel tiene **240 px útiles** y el gesto más frecuente es *cambiar de tablero*, que el drill-down encarece), doble click para abrir, panel de detalle, ni jerarquía profunda. **Confirmado con el A/B y cerrado en D16.**

Esto es lo que la Etapa 6 puso a prueba con el A/B: la **variante B** era la lectura literal de la metáfora, y la **variante A** esta conclusión.

> **✅ Cerrado el 2026-08-14 — ganó A (árbol in-place).** El A/B confirmó el análisis: el gesto más
> frecuente es cambiar de tablero y el drill-down le suma clics justo a eso. La variante B se
> eliminó del prototipo. Queda registrado en **D16**, con el trade-off que se acepta: el in-place
> paga 12px de indentación por nivel, algo que B no pagaba.
>
> Corrección de un dato de arriba: el panel no mide 280px sino **240px útiles** (`px-3` se aplica
> dos veces). Eso refuerza la conclusión, no la debilita.

---

## Fuentes

- [Collections | Metabase Documentation](https://www.metabase.com/docs/latest/exploration-and-organization/collections)
- [Find data | Metabase Learn](https://www.metabase.com/learn/metabase-basics/getting-started/find-data)
- [Organization overview | Metabase Documentation](https://www.metabase.com/docs/latest/exploration-and-organization/start)
- [NestedFolders: New Browse Dashboards · grafana/grafana#65604](https://github.com/grafana/grafana/issues/65604)
- [Dashboard list panel: include subfolders · grafana/grafana#124158](https://github.com/grafana/grafana/issues/124158)
- [What is Progressive Disclosure? — IxDF](https://ixdf.org/literature/topics/progressive-disclosure)
- [Progressive disclosure | Primer](https://primer.style/ui-patterns/progressive-disclosure)
- Código: `fe-solutions-mf` @ `8aebc1879` — `features/storage/components/{files/FilesView.tsx, folders/*, shared/{DataToolbar,FolderPicker}.tsx}`, `features/storage/utils/folderValidation.ts`, `features/dashboards/**`, `locales/es/storage.main.json`, `@simetrikinc/desyk-components@1.30.0-0` (`skills/desyk/**`)
