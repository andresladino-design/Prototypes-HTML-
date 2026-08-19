# Etapa 9 — Feedback del prototipo (revisión de Andrés en Ohana)

**Objetivo:** cerrar los hallazgos de la revisión del prototipo, en el orden en que
no obliga a medir dos veces.
**Entregables:** decisiones D17–D19 en `design-record/01-decisiones.md` · prototipo actualizado ·
`handoff/07-*` re-sincronizado **cuando** se confirmen los valores de ancho.
**Precondición:** ninguna. **② bloqueaba a ③** (ver §Orden).

> **Origen:** 5 comentarios en Ohana del 2026-08-14. Fue la **revisión visual que faltaba**
> de las Etapas 3 y 6 — la hizo Andrés usando el prototipo, no yo (la extensión de Chrome
> nunca conectó, y sigue sin conectar).
>
> **Falta el complemento:** Andrés dijo tener más cosas registradas fuera de Ohana. Este plan
> se abre asumiendo que van a entrar hallazgos nuevos.

## Estado · 2026-08-18

| # | Hallazgo | Estado |
|---|---|---|
| ② | Resize del panel | ✅ **Cerrado.** Mecanismo decidido (arrastrar el borde, franja del delta sombreada) y **los tres valores confirmados por Andrés el 2026-08-18: 288 · 384 · 480.** Queda re-sincronizar los docs. |
| ③ | Quitar el contador | ✅ **Quitado** (D18). El total se muda al `title` y al `aria-label`. Corregido el 2026-08-18: la primera lectura fue mía y estaba mal. |
| ~~①~~ | ~~Límites de tableros por carpeta~~ | ⛔ **Fuera del plan por ahora** (Andrés, 2026-08-18). El hueco de I5 sigue abierto, pero no se resuelve en esta etapa. |
| ④ | Permisos al eliminar carpeta | ✅ **D20 · flujo y prototipo listos.** Política: solo quien la creó, con `oc:manage_access` como escape. Falta confirmar con BE. |
| ~~⑤~~ | ~~Acordeón exclusivo~~ | ⛔ **Fuera del plan** (Andrés, 2026-08-18). D12 se queda como está: secciones independientes. |

---

## Orden propuesto, y por qué

**② fue primero.** No era preferencia: el ancho del panel es la variable de la que dependen
las tres mitigaciones de D2 (indentación de 12px, truncado al medio, tope de 3 niveles).
Haberlo resuelto primero es lo que dejó ③ decidido con un número en vez de una opinión.

```
② resize del panel  ──┬──▶ ③ quitar contador   ✅ quitado (el motivo era ancho,
                      │                          pero el pedido era quitarlo)
                      └──▶ recalcular D2 · D13 · D16 · design.md · 01-frontend
                             ⏸ pendiente de que se confirmen los valores

① límites por carpeta ─── independiente
④ permisos (D1.b)    ─── independiente · necesita BE
```

---

## ② Resize del panel — anchos fijos sm / md / lg

> *«explorar un resize del panel · podemos aumentar el ancho · establecer anchos y máximos
> con medidas fijas (sm-md-lg)»* — `cmt_mst640rv`, anclado en el `<aside>`

**Estado en producción, verificado:** el panel **no** es redimensionable. `w-72 min-w-72`
fijo (`OcContentLayout.tsx:171`), con colapso automático a `w-14` cuando el viewport baja
de `COLLAPSE_WIDTH_THRESHOLD = 1200`. No hay handle de resize ni preferencia guardada.

### Por qué esto es lo más importante de los cinco

El ancho útil de una fila es **240px** (288 menos `px-3` dos veces). Sobre ese número están
calibradas:

| Decisión | Depende del ancho |
|---|---|
| **D2** · indentación de 12px por nivel | a 19px el nombre no cabía en el nivel 3 |
| **D2** · tope de 3 niveles | el peor caso queda en 158px |
| **D14** · truncado al medio | la cola se pierde porque no hay ancho |
| **D16** · árbol in-place sobre drill-down | se aceptó pagar 12px/nivel |

Con un panel de 320px (`md`) el presupuesto sube ~80px y **las cuatro se reabren**. Con 400px
(`lg`), el drill-down deja de tener siquiera el argumento del ancho.

### ✅ Lo que se produjo

**Tabla de presupuesto, parametrizada y viva.** La cuenta de D2 dejó de estar copiada a mano:
vive en el prototipo (`get budget()`) y se recalcula al cambiar de tamaño. A 288px reproduce
**exacto** los números de D2 (carpeta 182/170/158 · tablero 190/178/166), que es la prueba de
que es la misma cuenta y no una nueva.

**Los tres valores, derivados en vez de elegidos.** Cada uno responde a una pregunta:

| | px | Clase | Por qué ese número |
|---|---|---|---|
| `sm` | **288** | `w-72` | Lo de hoy. Es el default: elegirlo no cambia nada de producción. |
| `md` | **384** | `w-96` | **El anidamiento deja de costar ancho.** Un tablero en el nivel 3 pasa a 262px — 60px *más* que un tablero suelto hoy (202px). Bajar un nivel deja de pagarse con nombre. |
| `lg` | **480** | `w-[30rem]` | **El peor caso real entra entero.** `Adquirencia_2026_06_04_conciliacion_master_v2` (45 caracteres ≈ 329px) se lee completo hasta el nivel 3. |

Progresión de +96px, dos de los tres en la escala Tailwind por defecto. Se descartó la
propuesta de arranque del plan (288/360/440): 360 y 440 no salían de ningún criterio, y 440
se queda **3px corto** para el peor caso al nivel 3 — o sea que habría prometido algo que no
cumple.

> El peor caso son **45 caracteres, no 40**. La cuenta original de D2 usaba
> `Adquirencia_2026_06_04_conciliacion_visa`, pero el propio `build()` genera nombres con
> sufijo `_v2` y `_master`, que son más largos. El presupuesto estaba calibrado contra un
> peor caso optimista.

**Mecanismo: ✅ A · arrastrar el borde** (decidido el 2026-08-18). Se prototiparon los dos
porque el comentario pide dos cosas a la vez («explorar un resize» y «medidas fijas»):

- **A ✅ · handle de arrastre con snap.** Cuesta 0px del header. `role="separator"` + flechas
  (patrón WAI-ARIA *window splitter*), paridad por teclado sin control extra — mismo criterio
  que D7 con el drag.
- **B ⛔ · control discreto S/M/L** en el header. Se descubre solo, pero se come ~72px del
  **slot 1** y obliga a interpretar `S/M/L`.

### El feedback del arrastre es espacial, no textual

**Esto lo corrigió Andrés**, y de paso mató el rótulo en los dos mecanismos. `S/M/L` es
vocabulario de diseñador: no dice **hasta dónde va a llegar el panel**, que es la única
pregunta que tiene el usuario mientras arrastra. Mi primera versión de A tenía el mismo defecto
mudado de lugar — un badge que escribía «MD · 384px» durante el arrastre. **Escribir el tamaño
es admitir que no se ve.**

Ahora al arrastrar se sombrea **solo la franja que el panel gana o devuelve**, con una línea
azul que marca dónde queda el borde y las tres paradas en líneas tenues.

**Se sombrea el delta, no el panel entero** — segunda corrección de Andrés, y va en la misma
dirección que la primera. Pintar los 288px completos tapa la lista que estás leyendo, y resalta
lo que no importa: la pregunta no es «cuánto va a medir» sino **«cuánto gano»**. Funciona en los
dos sentidos: creciendo, azul sobre lo que se suma; encogiendo, gris sobre lo que se devuelve al
contenido. Si el destino es el tamaño de partida, la franja mide 0 y no se dibuja nada.

Resuelve dos cosas más de una:

1. **El snap deja de sentirse como un bug.** El panel no sigue al cursor —salta entre tres
   valores— y eso se leía como que la interfaz no responde. Ahora lo que se mueve es la zona,
   y el salto se lee como intención.
2. **Las medidas fijas se enseñan sin nombrarlas.** Ver tres paradas comunica «hay tres
   anchos» mejor que tres letras.

El rótulo se fue de todo lo que ve el usuario: badge, tooltip del riel colapsado y `aria-label`
del separador (ahí el número lo dan `aria-valuenow`/`min`/`max`, que es lo que corresponde).
Detalle de oficio que faltaba: durante el arrastre se suprime la selección de texto, porque si
no el gesto va seleccionando los nombres de la lista al pasar.

**Persistencia.** Clave propia `swat577_panel_width` (`oc_sidebar_width` en producción).
**No se unifican** las tres claves: producción ya persiste el colapso en
`oc_sidebar_collapsed` con su propia clave, así que el ancho va en paralelo. Unificar sería
migrar algo que ya existe, a cambio de nada.

**Interacción con el colapso automático: ya estaba resuelta en producción.** No hubo que
inventar nada — `OcContentLayout.tsx:86` tiene `restoreIfNoAutoCollapse()`, que separa la
*preferencia del usuario* de los *motivos de colapso automático* y restaura cuando el motivo
desaparece. El ancho se cuelga del mismo mecanismo: **gana el colapso, y al reexpandir se
recupera el tamaño elegido.** El prototipo ahora lo modela (riel colapsado incluido) para
poder demostrarlo.

**El truncado al medio no hay que recalibrarlo.** Es CSS puro (`truncate` en la cabeza +
`shrink-0` en la cola), sin medir en JS, así que se adapta solo a cualquier ancho. Una de
las cuatro decisiones que ② «reabría» no necesitaba tocarse.

### Hallazgo colateral — ✅ cerrado el 2026-08-19

**El umbral de colapso mide el contenedor, no la ventana.**
`COLLAPSE_WIDTH_THRESHOLD = 1200` (`OcContentLayout.tsx:56`) se compara contra
`entry.contentRect.width` del contenedor del OC (`:127`) — y `contentRect` **excluye el
padding**, así que del ancho de ventana ya se descontaron el nav de plataforma y el `px-6`. El
panel se colapsa **antes** de lo que «1200» sugiere.

**Andrés lo revisó: los umbrales están bien.** No se cambia nada. Queda escrito porque es
contraintuitivo al leer el código y al probar en distintos tamaños, no porque haya algo que
arreglar.

Lo que sí queda de esto para D17: por debajo del umbral **gana el colapso** y el tamaño elegido
se recupera al reexpandir — ya resuelto reusando `restoreIfNoAutoCollapse`.

### Lo que queda abierto

- [x] ~~Que Andrés elija mecanismo.~~ **A · arrastrar el borde**, sombreando la franja del delta.
- [x] ~~Confirmar los tres valores.~~ **288 · 384 · 480 confirmados** el 2026-08-18.
- [ ] **Re-sincronizar los docs** — ya está desbloqueado. Ver la lista al final de esta sección.
- [ ] **¿Es de SWAT-577 o es el segundo spin-off?** Argumento para separarlo: beneficia al
      panel **exista o no** el feature de carpetas, igual que D14 — y es la **tercera palanca
      de ancho** del mismo problema que `ancho-util-lista-tableros/`. Recomendación: que las
      tres viajen juntas en ese issue.
- [ ] **Validar contra el área de contenido.** A `lg` en una pantalla de 1920px el grid de
      2 columnas del tablero baja a ~543px por gráfico, y los mocks se dibujan a 560px. Es
      el costo real de `lg`, y es el argumento más fuerte para que el default siga en `sm`.

### Re-sincronizar — ✅ desbloqueado (valores confirmados el 2026-08-18)

Se hace en la **fase de cierre** de esta etapa, junto con los flujos, según el orden que pidió
Andrés: primero terminar el feedback (④), después flujos y handoff.

`design-record/01-decisiones.md` (D2 · D13 · D16) · `design-record/02-benchmark.md` (I4) · `design.md` ·
`handoff/01-frontend.md` §4 · la tabla de `ancho-util-lista-tableros/`.

✅ **Hecho el 2026-08-19.** Re-sincronizados: `01-decisiones.md` (D2 · D13 · D16),
`design-record/02-benchmark.md` (I4), `design.md`, `handoff/01-frontend.md` (§4 + §4.a ancho + §4.b permisos),
`handoff/02-backend.md` (§6.b permisos + `created_by` en el response) y los dos docs de
`ancho-util-lista-tableros/` (entra como palanca **2.c**).

El peor caso de D2 quedó corregido en los cuatro lugares donde estaba mal: son **45**
caracteres, no 40.

---

## ③ Quitar el contador de las subcarpetas — ✅ quitado (D18)

> *«QUitar este contador»* — `cmt_mst64r43`, anclado en `span.flex` de un `li` con una guía
> de indentación antes → es el contador de una carpeta de **profundidad 1**

**El contador sale de la fila.** El total del subárbol se muda al `title` y al `aria-label`,
que cuestan 0px.

> **⚠️ Corrección de rumbo (2026-08-18).** La primera versión de esta sección decidió lo
> contrario —que el contador se quedaba— con este argumento: el motivo era ancho, y ② devuelve
> 96px donde el contador devolvía 20.
>
> **Contestaba una pregunta que nadie hizo.** El comentario era una instrucción; el motivo
> explicaba *por qué*, no *si*. Andrés lo marcó al revisar el proto: «el panel sigue mostrando
> el contador, algo que en el feedback se comentó que ya no iba».
>
> La resta sigue siendo válida para lo que sí decidía —que **quitarlo no era la forma de
> recuperar ancho**, y por eso ② igual valía la pena— pero se quita, porque el ancho no era la
> única razón.

**Lo que gana la fila:** +20px en cada carpeta, y una propiedad nueva — **una carpeta y un
tablero a la misma indentación ahora miden lo mismo.** La fila deja de tener dos presupuestos
según el tipo.

| | Con contador (D2) | Sin contador |
|---|---|---|
| Carpeta nivel 1 / 2 / 3 | 182 / 170 / **158** | 202 / 190 / **178** |

**Lo que se pierde, y hay que decirlo:** una carpeta **cerrada** ya no dice cuánto tiene
adentro. Era la única señal de volumen sin expandir, y es el caso donde más servía —decidir si
vale abrirla. Queda en el `title` y el `aria-label`, pero un dato que exige un gesto no es un
dato que se escanea.

- [ ] **A validar en la próxima revisión:** si se extraña el volumen de una carpeta cerrada. Si
      se extraña, la salida **no** es volver al contador en todas las filas, sino mostrarlo
      **solo en las colapsadas**.

**Los contadores de sección no se tocan** — «Tableros», «Configuraciones pendientes (8)»,
«Favoritos (5/15)» y «Sin carpeta» existen en producción y no eran de lo que hablaba el
comentario.

---

## ④ Permisos: ¿solo elimino las carpetas que yo creé? — ✅ D20

> *«Al eliminar el tablero debería validar quien es el creador · ¿solo elimino las carpetas
> que yo creo?»* — `cmt_mst66vz6`

**Decisión de Andrés (2026-08-18): opción (b), solo quien la creó** — con el escape por admin
diseñado. Va contra mi recomendación, que era (c); el escape cierra la objeción que yo tenía.

**Qué se restringe, y qué no.** La línea es: **restringir lo que altera la carpeta de otro, no
lo que la usa.**

| Restringido al autor | Libre |
|---|---|
| Renombrar · Mover a… · Eliminar | Agregar tableros · Nueva subcarpeta · mover un tablero |

Sin esa segunda columna, «solo el autor» se vuelve un candado que impide colaborar en la
ubicación compartida que definió D1.

**El escape es lo que hace viable a (b).** `oc:manage_access` puede gestionar cualquier
carpeta — reusa un permiso que ya existe, y resuelve que la carpeta de alguien que se fue del
equipo no quede inmanejable para siempre. El proto lo modela con una huérfana real (`2025`,
creada por alguien `inactive`) y un toggle para simular el permiso.

**El copy cambia con el motivo**, porque las salidas son distintas:

- Sigue en la cuenta → *«Solo María, que creó esta carpeta, puede renombrarla…»*
- Se fue → *«Lucía ya no está en la cuenta. Solo alguien que gestione accesos puede…»*

Mandar a pedirle a Lucía cuando Lucía no está es un callejón sin salida. Un mensaje de permisos
tiene que **nombrar la salida**, no solo la puerta cerrada.

**La autoría no va en la fila.** Gastaría el ancho que D17 acaba de recuperar. Vive en el
`title`, en el `aria-label` y en el pie del menú — los tres cuestan 0px. Y los ítems se
**deshabilitan, no se ocultan**: mismo criterio que el tope de 3 niveles.

### Dos trampas que aparecieron al implementarlo

1. **Una carpeta recién creada tiene que ser gestionable por quien la creó.** Si `createdBy` no
   se asigna al crear, la creás y no la podés ni renombrar. Había **cuatro** rutas de creación
   en el proto; ahora las cuatro asignan autor.
2. **«Deshacer» un borrado restaura al autor original**, no a quien deshace — si no, eliminar +
   deshacer sería una forma de apropiarse de la carpeta de otro.

### Lo que queda

- [ ] **Confirmar con BE.** D20 respeta la letra de D1.b (no hay permiso nuevo) pero **agrega
      una comprobación de autoría que hoy no existe**. Lo que habilitó el cambio es que **D6
      debilitó la premisa**: eliminar ya no lo garantiza el motor de base de datos.
- [ ] **BE tiene que devolver `created_by` en el listado** — el dato existe pero **no viaja**.
- [ ] **Validar en el endpoint, no solo en la vista.** Un permiso que solo vive en el FE no es
      un permiso.
- [ ] Aclarar en el ticket que el comentario dice «eliminar el tablero» pero pregunta por
      carpetas. Los tableros ya tienen su regla (`hasAccess`) y no se tocan.

---

## ~~⑤ Acordeón exclusivo~~ — ⛔ fuera del plan

> *«dejar priorizado el colapsable que se abre y cerrer los otros»* — `cmt_mst69j96`

**Andrés lo sacó del plan el 2026-08-18.** No se diseña. **D12 se queda como está:** las
cuatro secciones del panel colapsan de forma **independiente**, y las carpetas del árbol
también.

Se conserva el registro porque el comentario sigue `open` en Ohana y conviene que quede
escrito por qué no se hizo, no solo que no se hizo.

---

## Pendientes que vienen de antes

- [x] ~~**PR #54 sin mergear.**~~ **Mergeado el 2026-08-18** (`91e4e44`). Pages ya publica la
      Etapa 7. La Etapa 9 arranca en rama propia desde `main`:
      `feat/swat-577-feedback-prototipo`.
      🔗 https://github.com/andresladino-design/Prototypes-HTML-/pull/54
- [ ] **Capturas antes/después** de `handoff/05-antes-despues.md` §8 — lo único que queda
      abierto de la Etapa 7.
- [x] ~~**Push:** la credencial activa es `amladinon94-source` y da 403.~~ **Resuelto:**
      `gh auth switch --user andresladino-design`. Ojo, no es permanente — hay que
      re-verificarlo al empezar cada sesión.
- [ ] **El complemento de Andrés:** hallazgos registrados fuera de Ohana, todavía sin recibir.

---

## Riesgos de esta etapa

- ✅ **Resolver ③ antes que ②** — *evitado.* Se hizo ② primero y ③ se cerró con una resta
  (20px vs 96px) en vez de con una opinión. Era exactamente el riesgo que describía el plan.
- ⚠️ **Tratar ② como ajuste de UI.** Sigue vivo, con el signo invertido: los docs **todavía no
  se re-sincronizaron**, y eso es deliberado (los valores no están confirmados). El riesgo
  ahora es *olvidarse* de hacerlo cuando se confirmen. La lista está en §②.
- 🔴 **Que D20 se implemente solo en el FE.** Un permiso que vive en la vista no es un permiso.
  Y BE hoy **no devuelve `created_by`** en el listado, así que sin eso el FE no puede ni
  pintar los estados deshabilitados.
- **Decidir ④ sin BE.** Es política de permisos; elegirla en UX y descubrir en implementación
  que el permiso no existe con ese alcance cuesta un rediseño.
- **Que ② y ① se metan en SWAT-577.** Ninguno depende de carpetas. Igual que D14, probablemente
  merecen issue propio — si no, el ticket vuelve a crecer sin control, que es lo que ya pasó
  una vez con D10.
