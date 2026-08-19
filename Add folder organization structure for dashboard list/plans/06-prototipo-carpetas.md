# Etapa 6 — Prototipo HTML con carpetas

**Objetivo:** un prototipo navegable que demuestre que agrupar baja el tiempo de encontrar un tablero, con dos alternativas de jerarquía comparables lado a lado.
**Entregable:** `prototypes/index.html` (con switch A/B + nota de feedback)
**Precondición:** Etapas 2 (design.md), 3 (baseline), 4 (flows) y 5 (historias).

---

## 1. Punto de partida

Se construye **sobre** `prototypes/00-baseline-tableros.html`: mismo shell, mismos tokens, mismos 155 tableros mock.
La única diferencia debe ser la organización — así la demo aísla la variable y el "antes/después" es honesto.

## 2. Las dos alternativas (A/B con switch, según la forma de trabajo del equipo)

> **Ambas variantes comparten el modelo ya decidido** (`design-record/01-decisiones.md`): carpetas **por cuenta**,
> **un solo nivel**, pertenencia **exclusiva**, eliminar **desagrupa**, mover por **menú + drag**.
> El A/B no pone en juego el modelo: pone en juego **I2** (default de expansión) e **I4** (jerarquía visual y forma de navegar).

### Variante A — Carpetas colapsables in-place (acordeón en el panel)

```
Tableros (155)                          ↕A→Z
▸ 📁 Adquirencia            (24)
▾ 📁 Cierre contable        (12)
     🌐 Cierre junio 2026
     🔒 Cierre mayo 2026
▸ 📁 Conciliación diaria     (8)
  ── sin carpeta ──
  🌐 Adquirencia
  🌐 Adquirencia_2026_06_04...
```

- Todo en un nivel visual; los sueltos quedan **debajo** de las carpetas.
- Ventaja: el usuario ve carpetas y sueltos a la vez; cero navegación; reversible con un click.
- Riesgo: si hay 20 carpetas expandidas, vuelve la lista larga → el estado por defecto (colapsado) importa.

### Variante B — Navegación por niveles (drill-down con breadcrumb)

```
Tableros                                 ← Adquirencia          (24)
📁 Adquirencia          (24) ›              🌐 ADQ-DASH
📁 Cierre contable      (12) ›              🌐 Adquirencia_2026_06_04...
📁 Conciliación diaria   (8) ›              ...
── 111 sin carpeta ──
```

- Un nivel a la vez, con breadcrumb de vuelta — el patrón de Almacenamiento y de `DashboardTreeFilter`.
- Ventaja: máxima reducción de carga cognitiva por pantalla (Miller en su forma más pura); consistente con Almacenamiento.
- Riesgo: cambiar de tablero entre dos carpetas cuesta más clicks; el sidebar deja de mostrar todo el contexto.

**Recomendación a defender en la demo:** A como default (el panel es de navegación rápida y siempre visible; el drill-down suma clicks al gesto más frecuente, que es cambiar de tablero), con la nota de que B es más consistente con Almacenamiento — y que esa tensión es exactamente lo que la demo debe resolver con feedback.

## 3. Contenido del prototipo

### Interacciones a implementar (una tarea a la vez, según flows F1–F7)

| # | Interacción | Implementación |
|---|-------------|----------------|
| 1 | Crear carpeta | Disparador definido en F1 → `Dialog` con un campo → validación de duplicado inline → toast |
| 2 | Renombrar carpeta | `⋮` de la carpeta → mismo diálogo en modo rename |
| 3 | Eliminar carpeta | `AlertDialog` destructivo con el conteo de tableros que se desagrupan |
| 4 | Mover tablero a carpeta | `⋮` de la fila → "Mover a carpeta" → selector (con buscador si > 7 carpetas y opción "Nueva carpeta") |
| 5 | Quitar de la carpeta | `⋮` de la fila → acción directa + toast con "Deshacer" |
| 6 | Colapsar / expandir | Estado por carpeta, persistido en `localStorage` |
| 7 | Buscar cross-carpeta | Lista aplanada, cada resultado con su carpeta como metadato; al limpiar vuelve el estado previo |
| 8 | Arrastrar tablero a carpeta | Atajo de la v1 (D7): drop target por carpeta con highlight, **incluyendo carpeta colapsada** y autoscroll del panel |
| 9 | Abrir tablero | Marca la fila activa (`bg-accent` + `font-medium`) |

### Estados a cubrir

- Panel **sin carpetas** (empty state que explica el concepto y ofrece crear la primera) → cubre HU-08.
- Carpeta **vacía** (tras crear, antes de mover) con su propio mensaje y CTA.
- Búsqueda **sin resultados** con carpetas presentes.
- Carga (skeletons) y error (Reintentar), heredados del baseline.
- Carpeta con **muchos** tableros (60+) → demostrar que el scroll infinito sigue vivo dentro de la carpeta.
- Tablero **sin acceso** dentro de una carpeta (atenuado, no navegable).

### Comparador antes / después

Un toggle **"Ver estado actual"** que vuelve al baseline plano dentro del mismo prototipo. Es el argumento de venta del feature en una sola pantalla y el insumo directo del handoff.

## 4. Nota de feedback (requisito de la demo)

Un panel fijo, discreto, con:

- Las **2 variantes** y qué pregunta responde cada una.
- Las decisiones abiertas que la demo busca cerrar (disparador de crear, default colapsado, drag sí/no, alcance del sort).
- Espacio para que la audiencia deje comentarios (o el link a comentarios de Ohana).

## 5. Datos mock

Carpetas verosímiles derivadas de los nombres reales de la captura: `Adquirencia` (24) · `Cierre contable` (12) · `Conciliación diaria` (8) · `Pruebas y QA` (15) · y **111 sueltos** → deja ver que el problema no desaparece solo por crear 4 carpetas, lo cual es honesto y útil para discutir el onboarding.

## 6. Definition of done

- [ ] `prototypes/index.html` autocontenido, abre sin build, usa `design/tokens.css`.
- [ ] Switch A/B funcional; ambas variantes con las 9 interacciones (las que apliquen).
- [ ] Toggle antes/después.
- [ ] Todos los estados de §3 alcanzables.
- [ ] Copy final igual al de las historias (Etapa 5) — el prototipo es la fuente del copy para i18n.
- [ ] Navegable **solo con teclado** de punta a punta.
- [ ] Jerarquía visual de carpetas conforme al `design.md` (C4) y sin tokens inventados.
- [ ] README del proyecto actualizado + entrada en el índice del repo y en el `index.html` raíz.
- [ ] Publicado en GitHub Pages vía PR (flujo del repo).

## 7. Riesgos

- **Que la variante B se construya a medias** y el A/B quede sesgado. Si no alcanza el tiempo para las dos completas, hacer B como *estático* de 2 pantallas y decirlo en la nota, en vez de dejarla rota.
- **Mock demasiado ordenado:** si en el mock todos los tableros ya están en carpetas, el prototipo no muestra el problema real (111 sueltos) ni cómo se ve el camino intermedio.
- **Agregar features de paso** (multi-selección, colores de carpeta, anidación): rompen C7 y contaminan el feedback.
