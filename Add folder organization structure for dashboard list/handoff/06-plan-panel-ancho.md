# Plan — El ancho del panel de Tableros (D17)

**Fecha:** 2026-08-19 · **Resuelve:** el hallazgo **H1** de [`00-spec.md`](00-spec.md) §13
**Estado:** ⚠️ **hay una decisión que tomar antes de escribir código.** Ver §4.

> **Este plan cambió D17.** Al revisar `@simetrikinc/desyk-components` apareció que **el design
> system ya tiene el componente y los tres tamaños** que D17 estaba inventando a mano. La buena
> noticia es que no hay que construirlo. La mala es que los tamaños de desyk son **porcentajes**,
> y todo el presupuesto de ancho de esta feature está calibrado en **píxeles fijos** — que es
> exactamente lo que pedía el feedback («medidas fijas»).

---

## 1. El hallazgo: no hay que construir nada, hay que adoptar `Panel`

D17 se diseñó asumiendo que había que hacer redimensionable un `<aside>` a mano. Eso era cierto
para el código actual, pero **no** para desyk.

```ts
// @simetrikinc/desyk-components/dist/components/ui/panel/types.d.ts
export type PanelVariant = "standard" | "embedded" | "collapsible";
export type PanelSize    = "M" | "L" | "XL";
export type PanelState   = "expanded" | "collapsed";
export type PanelBackground = "sidebar" | "white";
```

Lo que ya existe y coincide con lo que diseñamos:

| Lo que D17 inventó | Lo que desyk ya tiene |
|---|---|
| Tres anchos `sm` / `md` / `lg` | **`PanelSize = "M" \| "L" \| "XL"`** |
| Riel colapsado a mano (`w-14`) | **`COMPACT_PANEL_WIDTH = "w-12"`** |
| Estado colapsado + toggle | **`variant: "collapsible"`** · `collapsed` · `toggleCollapse()` |
| Botón de colapsar en el header | **`PanelHeaderCollapseButton`** |
| Fondo del panel | **`background: "sidebar" \| "white"`** |
| Anchos por breakpoint | **`SIZE_WIDTHS_2XL`** · **`SIZE_WIDTHS_3XL`** |

### Y esto resuelve H1

H1 decía: *desyk manda «Sidebar fija con ancho del producto → `Sidebar`, NO `Resizable` simulando
sidebar», y D17 hace redimensionable el panel.*

**H1 se disuelve, porque la premisa estaba mal.** El panel de Tableros **no es un `Sidebar`** —
esa regla habla de la navegación primaria del producto (el nav de plataforma, N1/N2). El panel de
Tableros es un **`Panel`**, según la propia definición de desyk:

> *«vista lateral persistente o colapsable que **convive** con el contenido principal sin
> ocultarlo»*

Que es literalmente lo que es. Así que:

- ❌ **No** usar `Resizable` (desyk lo prohíbe para esto, y con razón).
- ❌ **No** seguir con el `<aside>` a mano de `OcContentLayout.tsx:171`.
- ✅ **Adoptar `Panel`** con `variant="collapsible"` y `size`.

**Consecuencia buena:** el trabajo de D17 baja de «implementar un resize con snap, preview,
persistencia y colapso» a «migrar el `<aside>` a `Panel` y persistir el `size`».

---

## 2. El problema: porcentajes contra medidas fijas

`SIZE_WIDTHS` no son píxeles:

```js
SIZE_WIDTHS = { M: "w-[20%]", L: "w-[30%]", XL: "w-[40%]" }
```

**El feedback pedía lo contrario, y textualmente:** *«establecer anchos y máximos con medidas
fijas (sm-md-lg)»* (`cmt_mst640rv`).

No es una preferencia estética. **Todo el diseño de esta feature está calibrado en píxeles:** la
indentación de 12px por nivel, el tope de 3 niveles, el truncado al medio y el presupuesto de
nombre de D2 salen de que la fila mide 240px. Con porcentajes, ese número deja de existir.

### Qué da cada porcentaje, en píxeles reales

Contenedor = viewport − 256 (nav de plataforma) − 48 (`px-6`). Nombre de carpeta de nivel 1 =
panel − 48 (`px-3` dos veces) − 38 (`px-2` + icono + `gap`).

| viewport | contenedor | `M` 20% | `L` 30% | `XL` 40% |
|---:|---:|---:|---:|---:|
| **1440** | 1136 | 227 → **141px** | 341 → 255px | 454 → 368px |
| 1512 | 1208 | 242 → **156px** | 362 → 276px | 483 → 397px |
| 1728 | 1424 | 285 → 199px | 427 → 341px | 570 → 484px |
| 1920 | 1616 | 323 → 237px | 485 → 399px | 646 → 560px |
| 2560 | 2256 | 451 → 365px | 677 → 591px | 902 → **816px** |

*(panel → ancho disponible para el nombre)*

**Hoy, con 288px fijos: 202px.** Y el nombre más largo que genera el producto
(`Adquirencia_2026_06_04_conciliacion_master_v2`, 45 caracteres) necesita **329px**.

### Los tres problemas que salen de esa tabla

1. 🔴 **`M` es una regresión en el portátil más común.** A 1440px da **141px** de nombre contra
   los **202px** de hoy. Son 61px menos — y peor que los 182px que D2 ya llamaba un problema.
   **Adoptar `M` como default rompe algo que hoy funciona.**
2. 🔴 **El presupuesto de ancho deja de ser un número.** Va de 141px a 816px según la pantalla.
   No se puede calibrar el truncado, la indentación ni el tope de 3 niveles contra un rango así.
   D2, D17 y D18 quedan sin base.
3. ⚠️ **`XL` a 2560px son 902px de panel.** Para un inspector de detalle tiene sentido; para una
   lista de nombres, es desperdicio — y le come casi la mitad de la pantalla al tablero, que es
   lo que el usuario vino a ver.

**Por qué desyk lo diseñó así, y por qué no aplica acá:** `Panel` está pensado para
**inspectores** — un detalle que escala con la pantalla. Nuestro caso es una **lista de
navegación**, donde el ancho que importa es el que hace legible un nombre, y eso es una cantidad
absoluta de caracteres, no una fracción de la pantalla.

---

## 3. Tres caminos

### A · Adoptar `Panel` con `size` tal cual (porcentajes)

- ✅ Cero desviación del design system. Cero mantenimiento.
- ❌ Regresión a 1440px. Rompe el presupuesto de D2. **Contradice el feedback.**
- ❌ Habría que re-derivar el truncado y el tope de niveles «para el peor viewport», que es 1440
  — y ahí `M` no alcanza.

### B · Adoptar `Panel`, sobrescribir el ancho con medidas fijas ⭐ recomendado

Usar `Panel` para **todo** —estructura, colapso, `PanelHeaderCollapseButton`, tokens, a11y— y
sobrescribir solo `SIZE_WIDTHS` con los tres valores fijos derivados:

| | px | Clase | Por qué ese número |
|---|---|---|---|
| `M` | **288** | `w-72` | Lo de hoy. Default: no regresiona nada |
| `L` | **384** | `w-96` | El anidamiento deja de costar ancho: nivel 3 queda más ancho que un suelto en `M` |
| `XL` | **480** | `w-[30rem]` | El nombre de 45 caracteres entra entero hasta el nivel 3 |

- ✅ Respeta el feedback (medidas fijas) y conserva el presupuesto de D2.
- ✅ Se queda con el 90% de `Panel`: composición, colapso, estados, tokens.
- ⚠️ Desviación **documentada y acotada** a una constante. Hay que anotarla en `design.md` para
  que no parezca un descuido.

### C · Proponer a desyk que `Panel` soporte tamaños fijos

Que `PanelProvider` acepte `sizeMode: "fluid" | "fixed"`, o que `SIZE_WIDTHS` sea
sobrescribible por prop.

- ✅ Arregla el problema para todo el producto, no solo para nosotros.
- ❌ No desbloquea este issue: depende de otro equipo y otro release.
- **Recomendación: hacerlo igual, en paralelo, como issue aparte.** El caso «lista de navegación
  vs inspector» le va a pasar a otra feature. `/simetrik-ui extract` es el camino para proponerlo.

---

## 4. ⚠️ Lo que hay que decidir antes de escribir código

- [ ] **Camino A, B o C.** Recomendación: **B ahora + C en paralelo.**
- [ ] **Si es B: ¿la desviación se aprueba con el dueño de desyk?** Sobrescribir `SIZE_WIDTHS` es
      una decisión de design system, no de feature. **Es la conversación que hay que tener antes
      de implementar, no después del PR.**
- [ ] **¿El default se queda en `M` = 288px?** Debería: es lo que hay hoy, así que nadie pierde
      nada y quien quiera más ancho lo elige.
- [ ] **¿`COMPACT_PANEL_WIDTH` (48px) reemplaza el `w-14` (56px) actual?** Son 8px de diferencia
      en el riel colapsado. Adoptar el de desyk salvo que rompa el tab de iconos.

---

## 5. Plan de implementación

Tres fases. **La 1 no depende de la decisión de §4** y se puede empezar ya.

### Fase 1 — Migrar el `<aside>` a `Panel` *(no bloqueada)*

1. Envolver el layout del OC en `PanelProvider` con `variant="collapsible"`,
   `background="sidebar"`, `direction="left"`.
2. Reemplazar el `<aside className="w-72 min-w-72 …">` de `OcContentLayout.tsx:171` por `Panel`
   + `PanelHeader` / `PanelContent`.
3. Reemplazar el botón de colapsar propio por **`PanelHeaderCollapseButton`**.
4. Reemplazar el riel colapsado a mano por el estado `collapsed` de `Panel`.
5. **Conservar `restoreIfNoAutoCollapse`** (`:86`). Es lógica de producto —qué motivos colapsan
   automáticamente y cómo se restaura la preferencia— y `Panel` no la trae. Se conecta a
   `setCollapsed` del contexto en vez de a un `useState` local.
6. **Verificar que `oc_sidebar_collapsed` siga funcionando.** La preferencia persistida existe y
   no se debe perder en la migración.

**Criterio de aceptación:** el panel se ve y se comporta **igual que hoy**, con `Panel` por
debajo. Cero cambio visible. Si algo cambia visualmente en esta fase, es un bug.

### Fase 2 — El ancho como preferencia *(bloqueada por §4)*

1. Persistir el `size` elegido en **`oc_panel_size`**. Clave propia: **no unificar** con
   `oc_sidebar_collapsed`, que ya existe con la suya.
2. Leer la preferencia al montar y pasarla como `size` del `PanelProvider`.
3. Si es camino **B**: sobrescribir los tres anchos, en **un solo lugar** y comentado, con el
   link a este plan.
4. **Interacción con el colapso automático:** por debajo del umbral **gana el colapso**, y al
   reexpandir se recupera el `size` elegido. Ya resuelto por `restoreIfNoAutoCollapse` — el
   `size` es ortogonal al `collapsed`, así que no hay que coordinar nada nuevo.

### Fase 3 — El gesto de arrastrar

Acá va lo que ya está validado en el prototipo. **Lo único que `Panel` no trae.**

1. **Handle en el borde derecho**, hit area de **8px** (mínimo desyk).
2. **Snap** a los tres tamaños. El panel **no sigue al cursor**.
3. **Preview: sombrear solo la franja que se gana o se devuelve**, con línea de 2px en el borde
   destino y las tres paradas en 1px. Sombrear el panel entero taparía la lista.
   **El preview no puede vivir dentro del panel** (tiene `overflow-hidden` y tiene que dibujarse
   más ancho): va en el contenedor que envuelve panel + contenido.
4. **Sin rótulo `M`/`L`/`XL`.** No le dice al usuario hasta dónde va a llegar el panel.
   *(Nota: los nombres de desyk son `M`/`L`/`XL`, no `sm`/`md`/`lg`. Da igual: no se muestran.)*
5. **Teclado:** `role="separator"`, `aria-orientation="vertical"`, `aria-valuenow/min/max`,
   flechas ←/→, `Home`/`End`.
6. **Doble click en el handle → vuelve al default.** Convención desyk (`resizable.md`), 200ms
   `ease-out`. **Falta en el prototipo.**
7. **`user-select: none`** + `cursor: col-resize` en `body` durante el arrastre.
8. **Duraciones en canon:** 120 / 200 / 320. El prototipo usa `duration-150` y `duration-100`
   (hallazgo **H3**) — corregir al implementar.

**Criterio de aceptación:** arrastrar el borde cambia el tamaño; el tamaño sobrevive a una
recarga y a un ciclo de colapso; el gesto funciona con teclado; a `XL` el nombre de 45 caracteres
se lee entero en el nivel 3.

---

## 6. Qué NO hacer

- ❌ **`Resizable`.** desyk lo prohíbe para paneles laterales, y con `Panel` no hace falta.
- ❌ **Dejar el `<aside>` a mano y agregarle el resize encima.** Es el camino corto que deja
  deuda: duplica lo que `Panel` ya resuelve y se desincroniza en el próximo release de desyk.
- ❌ **Rótulos `S`/`M`/`L` visibles.** Ya se descartó con el feedback.
- ❌ **Unificar las claves de `localStorage`.** Producción ya persiste el colapso con su clave;
  unificar es migrar a cambio de nada.
- ❌ **Sombrear el panel entero durante el arrastre.** Tapa la lista y resalta lo que no importa.

---

## 7. Qué hay que corregir en el prototipo

El prototipo implementa el diseño validado, pero con `sm`/`md`/`lg` propios y sin `Panel`. Para
que quede alineado con este plan:

- [ ] Renombrar los tamaños a `M` / `L` / `XL`, para hablar el mismo idioma que desyk.
- [ ] Agregar **doble click en el handle → default** (**H2**).
- [ ] Corregir `duration-150` → `120` y `duration-100` → `120` (**H3**).
- [ ] Anotar en el panel de demo que el riel colapsado real es de **48px**, no 56.

Ninguno cambia el diseño: son alineaciones de vocabulario y de canon.

---

## 8. Lo que este plan deja resuelto y lo que no

| | |
|---|---|
| ✅ **H1 resuelto** | El panel es un `Panel`, no un `Sidebar`. La regla de `Resizable` no aplica |
| ✅ **Menos trabajo** | `Panel` ya trae los tres tamaños, el colapso y el riel |
| ✅ **H2 y H3** | Incorporados a la Fase 3 y a §7 |
| ⚠️ **Decisión pendiente** | Porcentajes vs fijos (§4). **Bloquea la Fase 2, no la Fase 1** |
| ⚠️ **Conversación con desyk** | Si es camino B, la desviación se aprueba antes de implementar |
| ❌ **Fuera de este plan** | El truncado al medio y los botones en hover: son [`ancho-util-lista-tableros/`](../../ancho-util-lista-tableros/), y D17 es su tercera palanca |
