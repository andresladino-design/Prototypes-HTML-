# Plan 05 — Cambios al prototipo tras la sesión del 28-ago

**Fecha de la sesión:** 28-ago-2026 · **Con:** Andrea Giraldo · **Escrito:** 31-ago-2026
**Fuente:** [Marketplace Chargeback Dashboard Integration](https://notes.wisprflow.ai/shared/-MdZziEBcOF1vXDTHyOp_7qT7BvEBj-uXex5BD1aB9o) (Wispr Flow, transcript completo)
**Depende de:** `01-spec-acceso-al-tablero.md` — esta sesión la cierra
**Estado:** ✅ aprobado el 31-ago-2026 · ver «Lo aprobado» abajo

---

## Lo aprobado — 31-ago-2026

| Decisión | Qué se aprobó |
|---|---|
| **Archivos** | **Camino 2.** `contracargos-merchant.html` es el tablero destino; sobre `acceso-al-tablero-ab.html` se rehace el camino del Marketplace. El HTML de 400 KB de la presentación se archiva |
| **Opción B** | **Se borra.** Fuera del prototipo entera. El porqué del descarte vive en este documento, no en la interfaz |
| **Tarjetas por actor** | **Las 4 visibles, solo merchant navega.** El catálogo muestra adquirente / PSP / emisor / merchant; solo merchant tiene detalle e instalación reales |
| **Flujo del emisor** | **Se borra.** No se extrae a un HTML aparte. El respaldo es `plans/archivo-julio-2026/proto-andrea-original-2026-06-30.html`, que lo conserva intacto |

> **Consecuencia a manejar:** al archivar el HTML de la presentación cambia el link que hoy está publicado en Pages. Hay que reapuntar `contracargos/index.html` y el `index.html` de la raíz al nuevo prototipo principal.

---

## Lo que la sesión decidió

Cinco cosas quedaron cerradas. Las cuatro primeras cambian el prototipo; la quinta lo confirma.

| # | Decisión | Cita que la sostiene |
|---|---|---|
| **D1** | **Se va por la opción A: Marketplace.** La opción B (sugerencia proactiva en el centro de operaciones) queda descartada | *"Si el Marketplace ya tiene resuelto cómo instalar un template o algo literalmente prefabricado en Symmetry, pues me parece que sería lo correcto irse por ahí"* — Andrea: *"Sí, total. Tienes toda la razón"* |
| **D2** | **Una tarjeta por tipo de actor** en el catálogo: adquirente, PSP, emisor, merchant. El usuario instala la que aplique | *"Crear una tarjeta para cada caso, y que instale el que es de su caso de uso"* — Andrea: *"Bueno, me gusta" / "Mucho mejor, me parece"* |
| **D3** | **El selector de rol dentro del tablero se elimina.** El actor lo define el template que se instaló, no un switch en la vista | *"Esto de issuer, merchant, PSP más bien lo dejamos como trigger desde la configuración, que yo elija Contracargos PSP"* |
| **D4** | **La pestaña Disputas desaparece** y se convierte en un widget/gráfico dentro del tablero | *"Sería quitar esa página. Eso no haría falta"* — Andrea, sobre convertirlo en gráfico: *"Como un gráfico puede ser, sí, para que no se vaya a otro lado, mejor"* |
| **D5** | **El flujo del emisor (step by step tipo Mastercard) queda fuera del alcance** | Andrea: *"Ese flujo está direccionado a otro tipo de actor que todavía no hemos tocado, que es el emisor"* — *"No, no, no, eso no va"* |

### Por qué gana el Marketplace, en una línea

**Economía de lógica, no preferencia estética.** El Marketplace ya resuelve separar casos de uso, elegir espacio de trabajo, mostrar el árbol de dependencias de recursos, manejar el error de fuente faltante y crear el dataset por detrás. Al ser un dataset normal, el tablero hereda gratis anomalías, alertas y notificaciones por incidente y por resumen del Operation Center. Nada de eso hay que inventarlo.

**El riesgo vivo:** no está confirmado que todos los clientes vean el Marketplace. Si los permisos lo bloquean, la opción B vuelve a la mesa. Por eso *descartada* aquí significa *no se construye*, no *se borra el argumento*.

### Por qué se cae la opción B

Dos razones, las dos de Andrea y mías en la sesión:

1. **Le quita visibilidad al usuario.** B depende de que el motor corra primero. Si el motor dice "no puedo", el merchant nunca se entera de que existía la posibilidad ni de qué fuente le faltaba cargar. A le muestra el abanico completo desde el principio.
2. **Riesgo de spam.** Si el usuario cierra la sugerencia, hay que inventar cómo se la devolvemos. Más rutas, más lógica.

---

## La pregunta previa: sobre qué archivo se hace esto

Es lo primero a resolver, porque cambia el tamaño del trabajo por un factor de cinco.

Hoy hay tres archivos y **los cambios D3, D4 y D5 ya están hechos en uno de ellos**:

| Archivo | Qué tiene hoy | Frente a las decisiones |
|---|---|---|
| `Simetrik · Centro de Disputas — Operations Center.html` (400 KB) | El proto de Andrea íntegro + la capa A/B encima (prefijo `pz-`) | Conserva el switch de 4 roles, la pestaña Disputas, el flujo agéntico de 8 pasos y las dos opciones. **Le falta todo** |
| `prototypes/contracargos-merchant.html` (39 KB, tokens desyk reales) | Roles colapsados a merchant, sin flujo agéntico, sin pestaña Disputas, subtabs reacotados | **D3, D4 y D5 ya cumplidos.** Le falta el camino del Marketplace |
| `prototypes/acceso-al-tablero-ab.html` (45 KB, tokens desyk) | Las dos experiencias en limpio | Le falta D1 y D2 |

Esto abre dos caminos, y hay que elegir uno antes de tocar nada:

**Camino 1 — Operar sobre el archivo de la presentación.** Se le quitan roles, pestaña Disputas y flujo agéntico, y se le multiplican las tarjetas del catálogo. Ventaja: es el archivo que ya está publicado y el que Andrea reconoce. Costo: es cirugía sobre 2.506 líneas donde el markup original y la capa `pz-` están entrelazados, y el resultado es borrar la mitad del archivo para llegar a donde el otro ya está.

**Camino 2 — Promover los limpios.** `contracargos-merchant.html` pasa a ser el tablero destino y sobre `acceso-al-tablero-ab.html` se rehace el camino del Marketplace con las cuatro tarjetas. Ventaja: tokens desyk reales, un quinto del peso, y tres de las cinco decisiones ya vienen aplicadas. Costo: el archivo publicado hoy deja de ser el bueno y hay que reapuntar los links y el índice.

> **Recomendación: camino 2.** El archivo de la presentación era el vehículo para mostrarle a Andrea *dos* opciones. Ya no hay dos. Lo que queda que mostrar —una tarjeta por actor, la instalación, el tablero— es exactamente lo que los archivos limpios hacen mejor. El de 400 KB se archiva junto al original de Andrea, no se borra.

---

## Los cambios

Numerados para poder aprobarlos uno por uno. La columna *dónde* apunta al archivo de la presentación; si se aprueba el camino 2, cambia el archivo pero no el cambio.

### C1 · Sacar la opción B del recorrido — D1

Deja de ser un A/B. El panel de presentación pierde el segmentado, los atajos `A`/`B` y el copy *"Dos experiencias. Las dos terminan en el mismo tablero"*.

- **Dónde:** `OPC.b` (l. 2228-2236), `#pzSeg` (l. 2254), `#pzSug` en la lista de tableros (l. 2395-2400), vista `#pzDetect` "Esto es lo que encontramos" (l. 2360-2386), handler de teclado
- **A decidir:** ¿la opción B se borra, o queda accesible marcada como *descartada, y por qué*? A favor de conservarla: el argumento del descarte es justo lo que hay que contarle a Pedro Marota y a Vicky. A favor de borrarla: un prototipo con una opción muerta adentro confunde a quien lo abra solo
- **Nota:** la pantalla `#pzDetect` (clasificación de recursos con confianza) **no es exclusiva de B.** El motor de inferencia sigue corriendo en A al instalar. Vale la pena reubicarla dentro del flujo de instalación en vez de eliminarla

### C2 · Una tarjeta por actor en el catálogo — D2

Hoy hay una sola tarjeta `Contracargos`, repetida en la sección *Tarjetas* y en *Recién agregados*. Pasa a ser **Contracargos adquirente · Contracargos PSP · Contracargos emisor · Contracargos merchant**.

- **Dónde:** `#pzMkt`, clase `pzTplCbk`, l. 2295 y 2297
- **Por qué importa que sea el usuario quien elige:** Andrea propuso que el backend infiriera el actor por la industria del cliente. Se descartó al ver que hay clientes multi-industria — *"Melin, porque tiene Mercado Pago que es como un PSP, y tiene Marketplace"*, *"DLocal también tiene como cuatro tipos de industria"*. Ese cliente instala varias tarjetas
- **A decidir:** ¿las cuatro navegables, o las cuatro visibles y solo merchant con detalle e instalación reales? Solo merchant tiene contenido de verdad hoy
- **Ojo:** el template de **adquirencia** y la categoría *contracargos* **ya existen en dev**, creados por Daiver Doria. La tarjeta de adquirente no se inventa: se refina la que hay

### C3 · Quitar el selector de rol del tablero — D3

Fuera los botones Issuer / Merchant / PSP / Adquirente y la nota que cambia con cada uno.

- **Dónde:** `#roles` (l. 817-822), `#rolenote` (l. 834), y `renderCanvas(role)` / `DATA[role]` / `curRole` quedan fijos en merchant
- **Riesgo técnico:** `LAYOUT` y `DATA` están indexados por rol; hay que fijar el rol sin romper el render de widgets
- **Ya hecho en** `contracargos-merchant.html`

### C4 · La pestaña Disputas pasa a widget — D4

La pestaña con la flor de IA desaparece del header del tablero. El pipeline de disputas baja a ser un gráfico más del canvas.

- **Dónde:** subtab `data-view="flow"` (l. 811), vistas `#flowview` y `#disputasView` (l. 838-1006), `#caseView` (l. 1021)
- **A decidir:** el widget, ¿al hacer clic abre la cola de disputas en tabla, o se queda como gráfico y punto? La sesión no lo cerró. Andrea solo pidió *"que no se vaya a otro lado"*, lo que empuja a que sea gráfico sin navegación
- **Ya hecho en** `contracargos-merchant.html`, donde además se verificó que **el OC real no tiene pestaña Disputas**: tiene Tableros, Anomalías, Pendientes, Almacenamiento y Asientos contables

### C5 · Archivar el flujo del emisor — D5

Los 8 pasos (Dispute Filed → Network Decision), el rail de win probability, el ChargeScore y el OPEX saved salen del prototipo.

- **Dónde:** `#flowview` completo (l. 838-878), rail `#fa-rail`, `#fa-next`, guion de pasos en el JS
- **A decidir:** ¿archivar en un HTML aparte o borrar? **Recomiendo archivar.** Pedro Marota llega a la sesión desde una propuesta que ya le hicieron a un cliente sobre este mismo terreno; tener el flujo del emisor a mano sirve para marcar la frontera de alcance, aunque no se construya
- **Es el bloque más grande del archivo.** Sacarlo es lo que más adelgaza

### C6 · Afinar la instalación con lo que dijo la sesión — refuerza D1

El flujo ya está en el prototipo y fue lo que más le gustó a Andrea: *"esta visual me gusta mucho porque desde ahí le muestra qué es todo lo que va a hacer"*. Le faltan cuatro detalles que salieron del recorrido en vivo por el Marketplace de dev:

1. **Elegir espacio de trabajo antes de instalar** — *"¿en qué espacio de trabajo lo va a crear?"*
2. **El árbol de dependencias de recursos** visible en el detalle, junto a qué hace y qué obtiene
3. **La fuente faltante no bloquea.** El copy debe ser *"necesito que cargues una fuente de este tipo para poder continuar"*, no un error. El prototipo ya avisa *"faltan configurar 2 fuentes"*; falta la salida para resolverlo
4. **Salidas de corrección:** desde el Simetrik Agent o yendo al dataset a cambiar la query — *"si no es así, pues cámbialo desde el Symmetry Agent o vete al dataset y cambia la query"*

### C7 · Decir en el detalle que hereda el Operation Center — refuerza D1

El detalle del template debe decir con todas las letras que al instalarse quedan funcionando anomalías, alertas y notificaciones por incidente y por resumen, porque por detrás es un dataset como cualquier otro. Es el argumento que sostiene la decisión y hoy no está escrito en ninguna pantalla.

- **Dónde:** bloque `.pz-ben` "Beneficios y características" (l. 2346-2355)

---

## Lo que no cambia

- El tablero destino: KPIs de notificado y debitado separados, semáforo con distancia al umbral, los tres controles operativos
- Los umbrales VAMP 1,50% y ECM 1,50%, y la razón de que el ratio vaya por red y no agregado
- El wizard de monitoreo
- Que el prototipo se llame **contracargos** y no *disputas* en el copy de cara al usuario

---

## Lo que no es trabajo de prototipo

De la misma sesión, y sin lo primero nada de esto se sostiene:

| Pendiente | De quién | Estado |
|---|---|---|
| Averiguar los permisos de acceso al Marketplace por tipo de cliente | Andres | ⚠️ **Bloqueante.** Si no todos ven el Marketplace, se reabre la opción B |
| Refinar los templates de contracargos que ya están en dev (Daiver Doria) | Andres | Pendiente |
| Sesión con Pedro Marota (Gen Factory) para alinear y no pisarse | Andrea agenda | Lunes 31-ago, 11:00 |
| Sesión con Vicky: encaje estratégico del Marketplace | Andrea coordina | Pendiente |

Pedro va a montar controles de contracargos desde el Simetrik Agent, y ya venía preguntando cómo se había imaginado el tema. La sesión es para ver si se solapa con esto o lo complementa.

---

## Orden propuesto

0. **Decidir el camino de archivos** (camino 1 o 2) — bloquea todo lo demás
1. C1 y C2 juntos: son la decisión de producto y lo que se muestra afuera
2. C3, C4 y C5: limpieza del tablero. Gratis si se va por el camino 2
3. C6 y C7: el acabado del argumento
4. Actualizar `prototypes/README.md` y `01-spec-acceso-al-tablero.md`, que hoy describen un A/B que ya no existe
