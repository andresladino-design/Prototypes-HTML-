# Etapa 9 — Feedback del prototipo (revisión de Andrés en Ohana)

**Objetivo:** cerrar los hallazgos de la revisión del prototipo, en el orden en que
no obliga a medir dos veces.
**Entregables:** decisiones D17–D19 en `handoff/01-decisiones.md` · prototipo actualizado ·
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
| ② | Resize del panel | ✅ **Resuelto en el proto** · valores derivados + los dos mecanismos en A/B. Falta que Andrés elija mecanismo y confirme los valores. |
| ③ | Quitar el contador | ✅ **Cerrado sin quitarlo.** El motivo era (c) ancho, y ② devuelve 96px donde el contador devolvía 20. |
| ① | Límites de tableros por carpeta | ⬜ Independiente, sin bloqueos. |
| ④ | Permisos al eliminar carpeta | ⬜ Independiente · necesita BE. |
| ~~⑤~~ | ~~Acordeón exclusivo~~ | ⛔ **Fuera del plan** (Andrés, 2026-08-18). D12 se queda como está: secciones independientes. |

---

## Orden propuesto, y por qué

**② fue primero.** No era preferencia: el ancho del panel es la variable de la que dependen
las tres mitigaciones de D2 (indentación de 12px, truncado al medio, tope de 3 niveles).
Haberlo resuelto primero es lo que dejó ③ decidido con un número en vez de una opinión.

```
② resize del panel  ──┬──▶ ③ quitar contador   ✅ cerrado: el motivo era ancho
                      └──▶ recalcular D2 · D13 · D16 · design.md · 07-handoff-fe
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

**Los dos mecanismos, en A/B.** El comentario pide dos cosas a la vez («explorar un resize»
y «medidas fijas»), así que están los dos y se eligen en el panel de demo:

- **A · handle de arrastre con snap.** El gesto es continuo, el resultado siempre cae en
  sm/md/lg. Un badge muestra a qué medida va a caer, porque si el ancho siguiera libre al
  cursor y después saltara, el snap se leería como un bug. `role="separator"` + flechas
  (patrón WAI-ARIA *window splitter*), así que hay paridad por teclado sin control extra
  — mismo criterio que D7 con el drag. **Cuesta 0px del header.**
- **B · control discreto S/M/L** en el header del panel. Se descubre solo, pero se come
  ~72px del **slot 1**, que ya tiene el título y el contador de tableros.

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

### 🔴 Hallazgo nuevo, y es más grave que ②

**El umbral de colapso mide el contenedor, no la ventana.**
`COLLAPSE_WIDTH_THRESHOLD = 1200` (`OcContentLayout.tsx:56`) se compara contra
`entry.contentRect.width` del contenedor del OC (`:127`) — y `contentRect` **excluye el
padding**, así que del ancho de ventana ya se descontaron el nav de plataforma y el `px-6`.

Con el nav en 256px (lo que replica el prototipo), el colapso se dispara alrededor de los
**1504px de ventana**. Es decir: **en un portátil de 1440px el panel arranca colapsado y el
árbol de carpetas no se ve nunca.**

- [ ] **Verificar el ancho real del nav de plataforma.** No vive en `fe-solutions-mf`, así
      que los 256px son el supuesto del prototipo, no un dato medido. El número exacto
      cambia, la dirección no: el umbral se dispara **antes** de lo que «1200px» sugiere.
- [ ] Si se confirma, esto es **más importante que elegir entre 384 y 480**: un panel que no
      se muestra no tiene ancho que discutir. Y le pega a la premisa de D16 (árbol in-place)
      y de D2, que asumen el panel expandido.

### Lo que queda abierto

- [ ] **Que Andrés elija mecanismo** (A o B) y confirme los tres valores.
- [ ] **¿Es de SWAT-577 o es el segundo spin-off?** Argumento para separarlo: beneficia al
      panel **exista o no** el feature de carpetas, igual que D14 — y es la **tercera palanca
      de ancho** del mismo problema que `ancho-util-lista-tableros/`. Recomendación: que las
      tres viajen juntas en ese issue.
- [ ] **Validar contra el área de contenido.** A `lg` en una pantalla de 1920px el grid de
      2 columnas del tablero baja a ~543px por gráfico, y los mocks se dibujan a 560px. Es
      el costo real de `lg`, y es el argumento más fuerte para que el default siga en `sm`.

### Cuando se confirmen los valores, re-sincronizar

**Todavía no se tocó nada de esto, a propósito:** escribirlo antes de que los valores estén
confirmados haría que el handoff afirme algo indeciso — el mismo problema del que salimos.

`handoff/01-decisiones.md` (D2 · D13 · D16) · `handoff/01-benchmark.md` (I4) · `design.md` ·
`handoff/07-handoff-fe.md` §4 · la tabla de `ancho-util-lista-tableros/`.

Lo único que hay que arreglar **pase lo que pase** es el peor caso: D2 dice 40 caracteres
y son 45.

---

## ③ Quitar el contador de las subcarpetas — ✅ cerrado sin quitarlo

> *«QUitar este contador»* — `cmt_mst64r43`, anclado en `span.flex` de un `li` con una guía
> de indentación antes → es el contador de una carpeta de **profundidad 1**

**Motivo confirmado por Andrés (2026-08-18): (c) roba ancho al nombre.**

Y con el motivo en la mano, la respuesta se decide con una resta en vez de con una opinión:

| | Devuelve al nombre |
|---|---|
| Quitar el contador | **+20px** — y se pierde el total del subárbol |
| Subir de `sm` a `md` | **+96px** — y no se pierde nada |

**El contador se queda.** ② devuelve casi cinco veces más ancho sin sacrificar información,
así que pagar con el contador es un mal negocio. D2 sigue en pie, y con él la lección de
Grafana ([#124158](https://github.com/grafana/grafana/issues/124158)): el número significa
siempre lo mismo — total del subárbol, desglose en el `title`.

**En el prototipo** quedó un toggle *«Sin contador de subárbol»* en el panel de demo. **No es
una alternativa de diseño: es el instrumento con el que se midió.** Sirve para ver los 20px
al lado de los 96 y comprobar que la resta es real.

---

## ① Límites de tableros dentro de una carpeta

> *«definir limites de tableros dentro de carpetas»* — `cmt_mst60djq`

**Hueco real.** **I5** definió cuántas *carpetas* caben (objetivo 7±2 · aviso suave >15 ·
tope técnico 50) pero nunca cuántos *tableros* caben dentro de una. Es la pregunta espejo.

- [ ] ¿Tope **duro** (como los 15 de Favoritos) o **aviso suave** (como las carpetas)?
      Favoritos tiene tope duro porque es un atajo; una carpeta es una ubicación, y una
      ubicación que rechaza contenido es rara. **Recomendación: aviso suave.**
- [ ] Definir el número. Referencia útil: hoy «Adquirencia» tiene 24 y ya se siente larga —
      que es justamente lo que motivó D2 (subcarpetas).
- [ ] **La salida natural del límite es crear una subcarpeta**, no rechazar. Copy sugerido:
      *«Esta carpeta tiene 40 tableros. Considerá agruparlos en subcarpetas.»* con acción
      directa a «Nueva subcarpeta».
- [ ] ¿Se valida en BE o solo se avisa en UI? Si es aviso, **no** hace falta BE.
- [ ] Métrica que lo respalda: la telemetría ya manda `depth`; agregar el **tamaño de carpeta**
      para saber si el límite propuesto tiene base en el uso real.

---

## ④ Permisos: ¿solo elimino las carpetas que yo creé?

> *«Al eliminar el tablero debería validar quien es el creador · ¿solo elimino las carpetas
> que yo creo?»* — `cmt_mst66vz6`

**Reabre D1.b**, que había quedado explícitamente aplazada:

> *«no se introduce un permiso nuevo. Crear / renombrar / eliminar carpeta usa el mismo umbral
> que crear un tablero. (A confirmar con BE en la Etapa 7; si el equipo prefiere atarlo a
> `oc:manage_access`, es un cambio de una línea en la vista, no del modelo.)»*

**Nunca se confirmó.** El dato ya existe: el modelo guarda `created_by` (§1.1 del handoff BE).
Falta la política.

- [ ] Elegir entre tres:
      **(a)** cualquiera con acceso a Tableros — lo que dice D1 hoy;
      **(b)** solo quien la creó;
      **(c)** el permiso `oc:manage_access`, que ya existe y ya gobierna «Gestionar acceso».
- [ ] **Tensión a resolver antes de elegir (b):** D1 argumentó que ninguna acción de carpetas
      es destructiva y todo tiene «Deshacer», y por eso no hacía falta permiso. **Pero D6
      cambió**: eliminar ya no lo garantiza el motor de base de datos, es lógica de servicio.
      La premisa que sostenía la apertura se debilitó.
- [ ] **Contra-argumento a (b):** si solo el creador puede eliminar, una carpeta de alguien
      que se fue del equipo queda huérfana para siempre. Necesitaría un escape por admin.
- [ ] **Recomendación tentativa: (c).** Reusa un permiso que ya existe, no inventa modelo, y
      evita el huérfano. **Confirmar con BE.**
- [ ] Distinguir en el ticket: el comentario dice «eliminar el tablero» pero pregunta por
      carpetas. Los tableros ya tienen su propia regla (`hasAccess`) y no se toca.

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
- [ ] **Capturas antes/después** de `handoff/07-antes-despues.md` §8 — lo único que queda
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
- 🔴 **Que el umbral de colapso quede sin verificar.** Si en 1440px el panel arranca
  colapsado, discutir 384 vs 480 es discutir el ancho de algo que no se muestra.
- **Decidir ④ sin BE.** Es política de permisos; elegirla en UX y descubrir en implementación
  que el permiso no existe con ese alcance cuesta un rediseño.
- **Que ② y ① se metan en SWAT-577.** Ninguno depende de carpetas. Igual que D14, probablemente
  merecen issue propio — si no, el ticket vuelve a crecer sin control, que es lo que ya pasó
  una vez con D10.
