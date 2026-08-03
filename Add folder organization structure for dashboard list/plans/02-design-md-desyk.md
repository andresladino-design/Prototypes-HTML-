# Etapa 2 — `design.md` estrictamente basado en desyk

**Objetivo:** una fuente de verdad de diseño para este prototipo, **derivada del código de desyk**, no de la memoria ni del ojo.
**Entregables:** `design.md` (raíz del proyecto) + `design/tokens.css` (tokens extraídos, consumibles por el HTML).
**Precondición:** Etapa 1 cerrada (las decisiones cambian qué componentes se documentan).

---

## Regla de oro

Todo token, componente y variante que entre al `design.md` debe poder señalarse en:

- `node_modules/@simetrikinc/desyk-components/dist/styles.css` → tokens
- `node_modules/@simetrikinc/desyk-components/skills/desyk/references/<componente>.md` → API y variantes
- `node_modules/@simetrikinc/desyk-components/skills/desyk/patterns/*.md` → patrones de listado
- `fe-solutions-mf/src/oc/features/dashboards/**` → cómo el producto **realmente** usa esos componentes hoy

Si algo no se puede señalar, **no entra** al design.md (o entra marcado como `⚠️ propuesta nueva`, que es justo lo que el handoff debe negociar con FE).

---

## 1. Extracción de tokens (mecánica, sin criterio)

Fuente: `dist/styles.css` (`:root`, HSL). Generar `design/tokens.css` con los mismos nombres de variable para que el prototipo use `hsl(var(--primary))` igual que el producto.

Confirmados en la lectura de la Etapa 0:

| Grupo | Tokens |
|-------|--------|
| Superficie | `--background 0 0% 100%` · `--card` · `--popover` |
| Texto | `--foreground 240 6% 10%` · `--muted-foreground 0 0% 55%` |
| Marca / acción | `--primary 240 94% 60%` · `--primary-foreground` |
| Estado | `--success 138 76% 36%` · `--warning 41 96% 40%` · `--info 221 83% 53%` · `--destructive 360 72% 51%` |
| Neutros de UI | `--secondary` · `--muted 240 5% 96%` · `--accent 240 5% 96%` (fondo de fila activa) |
| Bordes / foco | `--border 0 0% 85%` · `--input` · `--ring 221 83% 63%` |
| **Sidebar** (crítico acá) | `--sidebar-background 0 0% 98%` · `--sidebar-foreground 240 5% 26%` · `--sidebar-accent 240 6% 96%` · `--sidebar-accent-foreground` · `--sidebar-border 240 6% 90%` · `--sidebar-ring` |
| IA | `--ai-purple 280 100% 61%` · `--ai-blue 222 97% 66%` + `--ai-gradient-*` |
| Charts | `--chart-1` … `--chart-8` |
| Geometría | `--radius 0.5rem` |
| Tipografía | `Inter` (importada desde Google Fonts en `styles.css`) |

Incluir también el bloque `.dark` para no cerrarle la puerta al tema oscuro.

## 2. Escala tipográfica y de densidad — derivada del panel real

No inventar: leer las clases que ya usa el panel de Tableros y documentarlas.

- Fila de tablero: `text-sm` con `px-2 py-1.5`, nombre con `truncate`, iconos `h-3.5 w-3.5`.
- Header de sección: `SECTION_LABEL_CLASS` (en `DashboardList/constants.ts`) + contador entre paréntesis.
- Botones de acción en fila: `p-1` con glifo `!h-3 !w-3`, invisibles (`text-muted-foreground/0`) hasta `group-hover`.
- Empty states del panel: `text-xs` para título, `text-[11px]` para descripción; botón `h-7 text-xs`.
- Skeletons: `SidebarListSkeletonRow`, 3 filas en secciones, 5 en Tableros.

## 3. Componentes desyk que el prototipo debe replicar

| Necesidad | Componente desyk | Referencia |
|-----------|------------------|-----------|
| Contenedor de carpeta colapsable | `collapsible` | `references/collapsible.md` |
| Acciones de fila y de carpeta | `dropdown-menu` + `context-menu` (mismos ítems en ambos, como hoy) | `references/dropdown-menu.md`, `context-menu.md` |
| Crear / renombrar carpeta | `dialog` + `input` + `label` | `references/dialog.md`, `input.md` |
| Eliminar carpeta | `alert-dialog` (destructivo, patrón ya usado para eliminar tablero) | `references/alert-dialog.md` |
| Mover a carpeta | `dialog` con `command`/`combobox` si la lista de carpetas crece | `references/command.md`, `combobox.md` |
| Feedback | `sonner` (toast) | `references/sonner.md` |
| Vacío | `empty-state` | `references/empty-state.md` |
| Tooltips de iconos | `tooltip` | `references/tooltip.md` |
| Carga | `skeleton` | `references/skeleton.md` |
| Scroll del panel | `scroll-area` | `references/scroll-area.md` |
| Drag & drop (si D7 lo aprueba como secundario) | infra HTML5 propia del panel (`useDashboardCrossDrag` + `useHtml5Sortable`), **no** `@formkit` | §2.5 de la exploración |

## 4. Patrones de producto a documentar (criterio C6)

Documentar el patrón **tal como ya existe en el OC**, con su copy:

- **Crear:** botón en el contenedor (no en la fila) → diálogo con un solo campo → validación de duplicados inline → toast de éxito.
- **Renombrar:** ítem de menú → mismo diálogo en modo `rename` con el valor precargado y seleccionado → 409 del BE se muestra como error de duplicado.
- **Eliminar:** `AlertDialog` con el nombre en la descripción, botón `bg-destructive`, estado `Eliminando...`, y `Alert` de error inline si falla (no toast).
- **Estados de la sección:** `loading` (skeletons) · `error` (icono + mensaje + Reintentar) · `empty` (empty state con CTA) · `ready`.
- **Acciones en fila:** visibles solo en hover/focus, duplicadas en click derecho, la destructiva separada y en rojo.

## 5. Reglas de jerarquía visual para carpetas (criterio C4)

Esta es la parte de **criterio de diseño** del design.md, y hay que escribirla explícita porque es un criterio del issue:

- La carpeta debe leerse como un nivel **intermedio**: por debajo del header de sección ("Tableros"), por encima de la fila de tablero.
- Palancas disponibles, en orden de preferencia: **peso tipográfico** > **icono de carpeta + chevron** > **contador** > **indentación de los hijos** > fondo. Evitar sumar tamaño de fuente (rompe la densidad del panel).
- Los tableros sueltos van **después** de las carpetas, sin indentación, exactamente como se ven hoy → así la carpeta gana jerarquía sin degradar al suelto.
- Regla de contraste: mínimo 4.5:1 para texto, 3:1 para iconos y bordes.
- Nada de más de un acento de color por fila; el color ya está tomado por privacidad (`Globe` info / `Lock` muted) y por el badge de pendiente (warning).

## 6. Voz y tono

- Español, glosario Simetrik: **tablero** (nunca "dashboard" en UI), **carpeta** (alineado con Almacenamiento).
- Labels cortos y accionables; describir el estado, no el mecanismo.
- Reusar copy de `storage.main.json` cuando exista equivalente (ver Etapa 1). Divergir solo con razón escrita.

## 7. Estructura del `design.md`

```
# Design — carpetas en la lista de tableros
## Principios
## Tokens (color · tipografía · spacing · radius · sombras)   ← tabla + link a design/tokens.css
## Densidad y escala del panel
## Inventario de componentes desyk (con link a su reference)
## Patrones de producto (crear / renombrar / eliminar / mover / estados)
## Jerarquía visual de carpetas
## Voz y tono + glosario
## Accesibilidad (foco, teclado, aria, contraste)
## Decisiones (fecha — decisión — razón)
```

## 8. Definition of done

- [ ] `design/tokens.css` generado desde `dist/styles.css`, con `:root` y `.dark`.
- [ ] `design.md` con cada componente linkeado a su `references/*.md`.
- [ ] Sección de jerarquía visual con las palancas priorizadas y justificadas.
- [ ] Todo lo que **no** exista en desyk marcado `⚠️ propuesta nueva`.
- [ ] Registrar la decisión de reuso/divergencia de copy vs. Almacenamiento.

## 9. Riesgos

- **Inventar tokens** por comodidad del prototipo (p. ej. un gris intermedio) — si hace falta uno, marcarlo como propuesta, no camuflarlo.
- **Documentar desyk en abstracto** en vez de documentar *cómo el panel de Tableros usa desyk*: lo segundo es lo que hace el prototipo fiel.
- Que el `design.md` crezca hasta volverse ilegible. Corto y accionable, como el de `notificaciones-resumen`.
