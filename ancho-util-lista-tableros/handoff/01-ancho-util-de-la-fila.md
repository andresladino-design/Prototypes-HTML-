# Recuperar ancho útil en las filas del panel de Tableros

> **Este documento no es parte de SWAT-577 (carpetas).** Es una mejora independiente
> del panel lateral del Centro de operaciones que se puede implementar sola, sin
> carpetas de por medio, y que beneficia a la lista tal como está hoy en producción.
> Se descubrió mientras se prototipaban las carpetas, pero el problema ya existe.

**Estado:** propuesta con prototipo funcionando · pendiente de issue en Linear
**Alcance:** solo FE · no toca modelo de datos, API ni permisos
**Componente:** `DashboardListItem` (`fe-solutions-mf`)

---

## 1. El problema

El panel lateral mide `w-72` (288px) y aplica `px-3` dos veces: una en el `<aside>`
del layout y otra en el cuerpo de cada sección. **El ancho real de una fila es 240px.**

Sobre esos 240px, cada fila gasta espacio fijo en cosas que no son el nombre:

| Sección | Estructura fija | Queda para el nombre |
|---|---|---|
| Tableros · Pendientes | `px-2` 16 + icono 14 + `gap-2` 8 + **⋮ 20** | **182px** |
| Favoritos | + grip 12 + **pin 20** | **150px** |

Dos problemas distintos se suman ahí.

### 1.a · El ⋮ reserva espacio permanentemente para algo que solo sirve en hover

El botón de opciones nunca se desmonta: vive con `text-muted-foreground/0` y solo
cambia de color en `group-hover`. Es decir, **está invisible pero ocupa sus 20px
en todas las filas, todo el tiempo.** En Favoritos son 40px entre el pin y el ⋮.

### 1.b · El truncado corta justo por donde los nombres se distinguen

Los nombres reales del OC se desambiguan en la **cola**, no en la cabeza:

```
Adquirencia_2026_06_04_conciliacion_visa
Adquirencia_2026_06_04_conciliacion_master
Adquirencia_2026_06_18_conciliacion_visa
```

Con `truncate` (que es `text-overflow: ellipsis` al final), a 182px se ven ~25
caracteres y las tres filas quedan así:

```
Adquirencia_2026_06_04_c…
Adquirencia_2026_06_04_c…
Adquirencia_2026_06_18_c…
```

**Dos de las tres son literalmente idénticas en pantalla.** El usuario tiene que
abrir el tablero o pasar el mouse para leer el `title` y saber cuál es cuál.
Esto no es un caso extremo inventado: es el patrón de nombres por defecto que
genera el propio producto.

---

## 2. Propuesta

Dos cambios independientes entre sí. Se pueden implementar por separado, aunque
juntos se refuerzan.

### 2.a · Los botones de fila aparecen en hover y empujan el texto

El contenedor de acciones arranca en `w-0` y se abre en hover o foco.

```html
<div class="flex w-0 shrink-0 items-center justify-end overflow-hidden opacity-0
            transition-[width,opacity] duration-150
            group-hover:w-6 group-hover:opacity-100
            group-focus-within:w-6 group-focus-within:opacity-100">
  <button class="shrink-0 rounded-md p-1 text-muted-foreground
                 transition-colors hover:bg-muted hover:text-foreground">
    <EllipsisVertical className="!h-3 !w-3" />
  </button>
</div>
```

Anchos exactos (el botón mide `p-1` 4 + icono 12 + `p-1` 4 = 20px):

| Sección | Botones | Ancho abierto |
|---|---|---|
| Tableros · Pendientes | ⋮ | `w-6` (24px) |
| Favoritos | pin + ⋮ | `w-11` (44px) |

**Tres decisiones dentro de esto que importan:**

**Empujar, no superponer.** La alternativa habitual (Linear, Notion, GitHub) es
flotar los botones sobre el borde derecho con un degradado. Acá **no sirve**:
taparían exactamente la cola del nombre, que es lo que el punto 2.b viene a
rescatar. Al empujar, el texto se encoge pero la cola sigue visible.

**`w-0`, no `hidden`.** Con `display:none` el botón sale del orden de tabulación
y un usuario de teclado no puede alcanzarlo nunca. Con `w-0` + `overflow-hidden`
sigue siendo enfocable, y `group-focus-within` abre el contenedor al llegar con
Tab — mismo comportamiento que con el mouse.

**El costo, explícito:** el texto se reacomoda al pasar el mouse. Al recorrer la
lista de arriba abajo, cada fila reajusta su truncado al entrar. Es el trade-off
central de esta propuesta y hay que verlo antes de aprobarlo (ver §5).

### 2.b · Truncado al medio, fijando el último segmento

En vez de truncar al final, se corta la cabeza y se ancla la cola:

```
Adquirencia_2026_06_04_conciliacion…_visa
Adquirencia_2026_06_04_conciliaci…_master
Adquirencia_2026_06_18_conciliacion…_visa
```

Se resuelve con **CSS puro**, sin medir en JS: dos `<span>` dentro de un flex,
uno que trunca y otro que no encoge.

```tsx
<span className="flex min-w-0 flex-1 items-center">
  <span className="truncate">{head}</span>
  <span className="shrink-0">{tail}</span>
</span>
```

Regla de corte (implementada y probada en el prototipo):

```ts
// El último segmento tras _ — o " " si no hay _.
// Si el segmento es largo (>14) o no hay separador, se fijan los últimos 6 caracteres.
function tail(name: string): string {
  const i = Math.max(name.lastIndexOf("_"), name.lastIndexOf("—"), name.lastIndexOf(" "));
  const t = i > 0 && name.length - i <= 14 ? name.slice(i) : name.slice(-6);
  return t.length >= name.length ? "" : t;   // nombres cortos no se parten
}
const head = (name: string) => name.slice(0, name.length - tail(name).length);
```

> **Nota:** esto **no** resuelve el caso `_04` vs `_18`, que está en el medio del
> nombre. Ninguna estrategia de truncado lo resuelve; ahí lo que ayuda es el
> ancho recuperado en 2.a. Los dos cambios se complementan por eso.

---

## 3. Impacto

| Sección | Nombre hoy | Con 2.a (reposo) | Ganancia |
|---|---|---|---|
| Tableros · Pendientes | 182px | **202px** | +20px (~3 caracteres) |
| Favoritos | 150px | **190px** | +40px (~6 caracteres) |

Y con 2.b, los caracteres que sobreviven pasan a ser los que **distinguen** una
fila de otra, que es la métrica que de verdad importa: no cuántos se ven, sino
si alcanzan para elegir sin abrir.

---

## 4. Alcance de implementación

Un solo componente concentra casi todo:

| Archivo | Qué cambia |
|---|---|
| `src/oc/features/dashboards/components/DashboardListItem/DashboardListItem.tsx` | El contenedor de acciones (pin + ⋮) pasa a `w-0`/hover; el nombre se parte en head/tail |

Consideraciones:

- La fila es **la misma** para Tableros, Favoritos y Pendientes (`isFavorite` y
  `hidePinButton` solo derivan variantes), así que un cambio cubre las tres secciones.
- El `title` del botón principal ya existe y **debe conservarse**: es el fallback
  para leer el nombre completo.
- El `AwaitingDataDot` (6px + gap) vive dentro del botón principal, después del
  nombre. Al partir el nombre en dos spans hay que dejarlo fuera del bloque que
  trunca, o se lo come el `overflow`.
- `prefers-reduced-motion`: la transición de `width` debe anularse. En el
  prototipo ya está cubierto por la regla global.

---

## 5. Qué hay que validar antes de aprobar

| # | Pregunta | Por qué importa |
|---|---|---|
| 1 | ¿El reflow del texto en hover molesta al recorrer la lista? | Es el costo directo de 2.a. Se juzga con los ojos, no en el código |
| 2 | ¿El «…» en el medio estorba al escanear rápido? | 2.b cambia la forma de la palabra; puede leerse peor aunque informe más |
| 3 | ¿Fijar el último segmento es la regla correcta? | Está calibrada para nombres tipo `Adquirencia_..._visa`. Habría que mirarla contra nombres de cuentas reales |
| 4 | ¿Hay usuarios en pantallas donde el panel se colapsa a `w-14`? | Ahí la fila es un icono y nada de esto aplica |

---

## 6. Lo que NO entra acá

**El chevron de las carpetas.** En el prototipo de SWAT-577 el icono de carpeta
absorbe la función del chevron (`folder` cerrada ↔ `folder-open` abierta), lo que
libera otros 16px. Eso **sí** pertenece a SWAT-577, porque solo tiene sentido si
existen carpetas. Está documentado allá.

---

## 7. Dónde verlo

Prototipo: [`Add folder organization structure for dashboard list/prototypes/index.html`](../../Add%20folder%20organization%20structure%20for%20dashboard%20list/prototypes/index.html)

Ambos comportamientos están activos en todas las filas del panel. Para aislarlos
del ruido de las carpetas, en el panel de demo (abajo a la derecha) poner
**«Antes / después» → Hoy (plano)**: eso deja la lista plana como producción,
con el truncado al medio y los botones en hover ya aplicados.

Las preguntas 1 y 2 de §5 están anotadas como **D13** y **D12** en la sección
«Qué queremos decidir con esta demo» del mismo panel.
