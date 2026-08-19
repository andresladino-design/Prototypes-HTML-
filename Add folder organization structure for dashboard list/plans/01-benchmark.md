# Etapa 1 — Benchmark acotado

**Objetivo:** resolver las **6 preguntas de interacción** (I1–I6) con evidencia, dentro del modelo ya decidido.
**Entregable:** `design-record/02-benchmark.md` con matriz comparativa + una recomendación por pregunta.
**Precondiciones:** `design-record/03-exploracion-fe-be.md` ✅ · `design-record/01-decisiones.md` ✅ (D1–D7 cerradas)

> **Cambio de foco respecto al plan original.** D1–D7 se cerraron el 2026-08-03 sin necesidad del benchmark
> (la evidencia del propio issue y de los precedentes internos alcanzó). Esta etapa ya **no decide el modelo**:
> el modelo es *carpetas por cuenta, un nivel, pertenencia exclusiva*. Lo que queda es **cómo se ve y cómo se opera** — y eso
> hace el benchmark más barato y más útil, porque se mira con una pregunta concreta en mano.

---

## Las 6 preguntas a cerrar

| # | Pregunta | Por qué importa |
|---|----------|----------------|
| **I1** | ¿Dónde vive el disparador de **"Nueva carpeta"**? | Es el punto de entrada del feature; si no se encuentra, el feature no existe. Candidatos: header de la sección "Tableros" · menú desplegable junto a "Nuevo tablero" · click derecho en el vacío · dentro del selector de "Mover a carpeta". |
| **I2** | ¿Colapsadas por defecto? ¿Se recuerda el estado? | Define si el panel se siente más corto (el objetivo) o igual de largo. |
| **I3** | ¿Cómo se muestra la carpeta en un **resultado de búsqueda**? | Criterio C5. Candidatos: chip a la derecha · texto secundario bajo el nombre · resultados agrupados por carpeta. |
| **I4** | ¿Qué palancas dan la **jerarquía visual** de la carpeta? | Criterio C4, explícito en el brief. Candidatos: peso tipográfico · icono + chevron · contador · indentación de hijos · fondo. |
| **I5** | ¿Cuántas carpetas son demasiadas? | Si una cuenta crea 30 carpetas, volvimos a la lista larga (y D2 dejó fuera la anidación). |
| **I6** | ¿Reusar el `FolderNameDialog` de Almacenamiento o crear uno propio? | Coherencia de producto vs. acoplamiento entre features. Decisión conjunta con FE. |

---

## 1. Benchmark interno primero (pesa más que el externo)

Coherencia con el producto es el criterio C6, así que esto va antes que las referencias externas.

| Precedente | Qué responde |
|-----------|-------------|
| **Almacenamiento › Archivos y carpetas** (`features/storage/components/folders/`) | **I1, I3, I6** + todo el copy ya traducido en `storage.main.json` (ver inventario en la exploración §2.6). Es el único lugar del producto donde ya existe la palabra "carpeta" de cara al usuario. |
| **Favoritos** (`FavoritesSection`) | **I2, I4** — cómo se ve una sección con contador, tope y drop target punteado dentro de este mismo panel. Y el molde de drag & drop que la v1 reusa (D7). |
| **`DashboardTreeFilter`** (anomalías) | **I3, I4** — jerarquía en poco espacio, navegación por niveles dentro de un popover. |
| **Paquetes de notificación** | **I1, I5** — precedente reciente de "agrupar cosas en un contenedor con nombre" y de dónde se pone su botón de crear. |
| **desyk** `patterns/data-list.md` + `data-table-rules.md` | **I1** — reglas oficiales de dónde van las acciones de un listado (toolbar vs. fila). |
| **desyk** `references/collapsible.md` | **I2, I4** — API real del componente con el que se construye la carpeta. |

## 2. Benchmark externo, con foco

Ya no hace falta la ronda completa de 8 productos: solo los que aportan a I1–I4.

| Producto | Para qué mirarlo |
|----------|-----------------|
| **Metabase — Collections** | I1 (botón "＋" en el header del sidebar) · I3 (cómo indica la colección en resultados de búsqueda) · I4 (jerarquía carpeta/ítem). |
| **Grafana — Folders** | I2 (default colapsado) · I5 (qué pasa cuando hay muchas carpetas). |
| **Notion / Linear (sidebar)** | I1 (`＋` que aparece en hover del header) · I2 (persistencia del estado de expansión) · I4 (la barra de calidad de jerarquía en un sidebar denso). |
| **Looker Studio** | I3 (resultados de búsqueda con ubicación). |
| **Finder / Explorer** | I4 — **verificar si la metáfora aplica** a un panel de 280 px, o si solo aplica el vocabulario. El issue la cita; hay que confirmarla o descartarla con argumento. |

Para cada uno: 1–2 screenshots en `handoff/assets/benchmark/` + la respuesta puntual a la pregunta que le toca. Nada de fichas genéricas.

## 3. Leyes de UX como criterio de corte

- **Miller** → I2 e I5: ¿cuántos ítems visibles a la vez deja el default? Si el panel abre con 30 filas visibles, el default está mal.
- **Reconocer > recordar** → I3: el resultado de búsqueda tiene que mostrar la carpeta, no obligar a recordarla.
- **Hick** → I1: el menú de fila pasa de 5 a 6–7 ítems; el de carpeta nace con 3. Verificar que sigan escaneables (y si hacen falta separadores).
- **Jakob** → I4: los usuarios que ya usan Metabase/Grafana esperan una convención concreta; desviarse necesita razón.
- **Fitts** → I1: el disparador de crear no puede ser un target de 16 px que aparece solo en hover si es la entrada principal al feature.

## 4. Actividades

1. Recolectar las respuestas internas (leer el código y capturar pantallas del producto).
2. Recolectar las externas, solo para las preguntas asignadas.
3. Matriz: preguntas I1–I6 en filas, referencias en columnas.
4. Cerrar cada pregunta con: recomendación · razón · referencia de respaldo · qué se descarta.
5. Inventario del copy reutilizable de `storage.main.json` con decisión explícita de reusar o divergir (alimenta I6 y el `design.md`).
6. Anotar los **anti-patrones** encontrados (lo que se ve mal en las referencias y no vamos a copiar).

## 5. Definition of done

- [ ] `design-record/02-benchmark.md` con la matriz I1–I6.
- [ ] Screenshots en `handoff/assets/benchmark/`.
- [ ] **I1–I6 cerradas**, cada una con razón y respaldo.
- [ ] Inventario de copy reusable vs. copy nuevo.
- [ ] Sección de anti-patrones.
- [ ] Verificado si la metáfora de "explorador de archivos" aplica al panel o solo al vocabulario.

## 6. Riesgos

- **Volver a abrir D1–D3** porque una referencia hace las cosas distinto. Ya están cerradas con razón escrita; si aparece evidencia fuerte en contra, se documenta como nota en `01-decisiones.md` — no se rehace el modelo a mitad de camino.
- **Sesgo de "file explorer"**: el issue lo sugiere, pero un sidebar de 280 px no es Finder. Validar, no asumir.
- **Benchmark que se infla**: 6 preguntas concretas contestadas valen más que 20 fichas de producto.
