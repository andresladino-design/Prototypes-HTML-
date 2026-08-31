# Spec 01 — Cómo llega el merchant al tablero de contracargos

**Estado:** propuesta para validar · **Decide:** Vicky, vie 28-ago-2026 · **Depende de:** `00-plan-de-trabajo.md`
> ⚠️ **Actualizado el 26-ago con evidencia del Brain y del código de producción.** Ver `04-respuestas-preguntas-abiertas.md`. Los cambios de fondo: la ruta 4 queda confirmada, y la ruta 3 se parte en dos porque la mitad ya existe.

> 🔒 **Cerrada el 28-ago-2026.** La sesión con Andrea eligió la ruta del Marketplace y descartó la sugerencia en el Centro de operaciones. Las decisiones y los cambios que salieron de ahí están en [`05-cambios-post-sesion-28-ago.md`](05-cambios-post-sesion-28-ago.md). Este documento se conserva por el análisis de las cuatro rutas y los criterios; el prototipo A/B que menciona quedó archivado en `archivo-agosto-2026/`.

## La pregunta

El motor ya construye todo por detrás: identifica los recursos de contracargo, arma el diccionario canónico, genera el dataset y el tablero. Lo que no está resuelto es **el momento de entrada del usuario**: cómo un merchant se entera de que ese tablero existe y llega a él sin haber configurado nada.

Cuatro rutas salieron de la sesión del 26-ago. Las evalúo contra cuatro criterios y propongo una combinación, no una sola.

## Criterios de evaluación

| Criterio | Por qué importa |
|---|---|
| **Descubribilidad** | El merchant no sabe que esto existe. Si tiene que buscarlo, no llega |
| **Costo de construcción** | Cuánta UI nueva hay que inventar y cuánta ya existe |
| **Encaje conceptual** | Si el patrón contradice el modelo mental que el usuario ya tiene del producto, confunde |
| **Reversibilidad** | Qué tan fácil es cambiar de opinión después de shippear |

## Las cuatro rutas

### Ruta 1 — Comando por CLI

El implementador corre un comando y el tablero aparece en el espacio de trabajo del cliente.

- **Descubribilidad:** nula. El merchant nunca ve el CLI
- **Costo:** cero de UI, ya existe
- **Encaje:** correcto, pero responde a otra pregunta
- **Veredicto:** **no es una ruta de acceso, es una ruta de construcción.** Va en la spec del backend con Santi, no en la presentación a Vicky como alternativa de UX

### Ruta 2 — Simetrik Agent

El usuario le pide al agente "necesito un control de contracargos", le pasa los recursos y el agente construye hasta el tablero. Andrea ya lo probó y funciona hoy.

- **Descubribilidad:** baja. Exige que el usuario ya sepa que puede pedirlo y que sepa nombrarlo
- **Costo:** cero, ya existe
- **Encaje:** perfecto con la identidad agentizada del producto
- **Reversibilidad:** total
- **Veredicto:** **no sirve como descubrimiento, sirve como edición.** Es la salida natural para "quíteme esta fuente", "agrégueme esta franquicia". Se conserva en todas las alternativas, no compite con ellas

### Ruta 3a — Destacar el template en el Marketplace

**Ya existe y está construido.** El Marketplace Manager permite curar el catálogo: cuántos templates *featured* y *recommended* se muestran y cuáles, más banners y beneficios (Brain UC-01). En el código están `MarketplaceFeaturedSection`, `MarketplaceFeaturedCard`, `MarketplaceHeroCarousel` y el módulo `marketplace-admin` completo.

- **Descubribilidad:** media-alta. El merchant no lo busca, pero lo ve al entrar al Marketplace
- **Costo:** **cero UI.** Es configuración en un panel que ya existe
- **Encaje:** ✓ es literalmente para lo que se hizo
- **Veredicto:** **se suma a la ruta 4 sin costo.** No es una alternativa, es el acabado de la 4

### Ruta 3b — Detección proactiva en el Operation Center

En la lista de tableros aparece un bloque de sugerencia: "detectamos contracargos en tus fuentes, podemos armarte el tablero". Un clic dispara todo el flujo y muestra el resultado.

```
┌─ Tableros ─────────────────────────────────────────────┐
│ Favoritos                                         1/15 │
│  ⠿ Conciliación diaria                                 │
│                                                        │
│ ┌──────────────────────────────────────────────────┐   │
│ │ ◇ Sugerido                                       │   │  ← bloque AI
│ │ Encontramos contracargos en 3 de tus fuentes     │   │    (borde gradiente,
│ │ Rappi CO, Rappi MX, PedidosYa BR                 │   │     fondo ai-gray)
│ │ Confianza de la clasificación: 68%               │   │
│ │                    [ Ver qué detectamos ]  [ Armar tablero ] │
│ └──────────────────────────────────────────────────┘   │
│                                                        │
│ Tableros                                           155 │
│  ⠿ Adquirencia                                         │
└────────────────────────────────────────────────────────┘
```

- **Descubribilidad:** la más alta de las cuatro. Cero clics de búsqueda, aparece donde el usuario ya está
- **Costo:** alto. **Verificado: el patrón no existe.** El Brain (`Definicion - Navegacion y Home`) solo cubre persistencia de contexto y el Home como lanzador; el grep sobre `features/dashboards`, `datasets` y `anomalies` no devuelve nada de sugerencias. Hay que definir dónde vive, cuándo aparece, cuándo se descarta, si vuelve, y qué pasa con la lista de 155 tableros
- **Encaje:** consistente con la apuesta agentizada, pero introduce una categoría nueva en una lista que hoy solo tiene Favoritos y Tableros
- **Reversibilidad:** media. Una vez que hay "sugeridos", el patrón se vuelve expectativa
- **Veredicto:** es la mejor experiencia y la más cara. **Candidata fuerte, pero no como primera entrega**

### Ruta 4 — Template en el Marketplace

El merchant entra al Marketplace, ve el template "Contracargos", abre el preview con el mapa de recursos que necesita, instala, elige espacio de trabajo, y el tablero aparece en su Operation Center.

```
Marketplace                          Operation Center
┌───────────────────────┐            ┌──────────────────────┐
│ Contracargos          │            │ Tableros         156 │
│ ─────────────────     │  instalar  │  ⠿ Contracargos  ●   │
│ Preview del tablero   │ ─────────▶ │  ⠿ Adquirencia       │
│ Mapa de recursos:     │            │  ⠿ Conciliación      │
│  · notificados        │            └──────────────────────┘
│  · debitados          │
│  · transacciones      │
│ [ Instalar template ] │
└───────────────────────┘
```

- **Descubribilidad:** media. Exige que el usuario entre al Marketplace, pero es un destino que ya existe en el sidebar
- **Costo:** **el más bajo de las rutas visibles.** Todo el patrón existe: preview, mapa de recursos, selector de espacio de trabajo, instalación, aparición en el Operation Center. No se inventa UI
- **Encaje:** ✅ **confirmado, la duda estaba mal planteada.** Un Template *es* un dashboard del OC con todas sus dependencias, incluidas **anomalías** y **contexto AI** (Brain UC-25). El control de contracargos no se mete a la fuerza en un marketplace de otra cosa: el marketplace es un catálogo de controles empaquetados
- **Reversibilidad:** alta. Si no funciona, el template se despublica y no queda deuda de UI
- **Veredicto:** **la ruta principal.** Ya no está condicionada al encaje conceptual, sino a cinco restricciones operativas:
  1. **El catálogo es cross-account global.** No hay segmentación por cuenta: o lo ven todas las cuentas con el sub-flag `OperationCenter.modules.marketplace`, o no se publica
  2. No hay desinstalación ni rollback
  3. No hay update-in-place; cómo avisar de una versión nueva es un gap abierto en el propio Brain
  4. Cada instalación sufija los nombres con timestamp (`Contracargos_1756…`)
  5. Publicar requiere `MarketplaceAdmin`; instalar solo `oc:view` + el sub-flag

### Variante — Selector de tipo al crear tablero

Salió en la sesión como alternativa a la 4: en "Nuevo tablero" o en "Editar tablero", un campo "tipo de tablero" con la opción Contracargos, que configura todo.

- **Descubribilidad:** baja. Solo lo encuentra quien ya iba a crear un tablero
- **Costo:** bajo, es un campo en un formulario existente
- **Encaje:** ⚠️ dudoso. Convierte "contracargos" en un atributo del tablero, lo que abre la puerta a una taxonomía de tipos que nadie ha definido
- **Veredicto:** **descartada como ruta principal.** Se puede sumar después si la taxonomía de tipos llega a existir por otra razón

## Comparación

| Ruta | Descubribilidad | Costo | Encaje | Reversibilidad | Rol |
|---|---|---|---|---|---|
| 1 · CLI | ✗ | ninguno | ✓ | alta | Construcción, no acceso |
| 2 · Simetrik Agent | baja | ninguno | ✓✓ | alta | Edición, transversal |
| **3a · Destacado en Marketplace** | media-alta | **ninguno, ya existe** | ✓✓ | alta | **Acabado de la 4** |
| 3b · Detección proactiva en OC | ✓✓ | alto, patrón nuevo | ✓ con reservas | media | Fase 2 |
| **4 · Template Marketplace** | media | **ninguno, ya existe** | ✅ confirmado | alta | **Camino principal** |
| Variante · tipo de tablero | baja | bajo | ⚠️ | media | Descartada |

## Recomendación

**Ruta 4 + 3a como una sola entrega, ruta 3b como fase 2, ruta 2 siempre presente como salida de edición, ruta 1 fuera de la conversación de UX.**

La evidencia movió la recomendación de "propuesta razonable" a "camino evidente". La 4 no inventa nada: el Template *es* el artefacto, y trae dentro las anomalías y el contexto AI, así que el monitoreo de umbral de red puede venir **pre-configurado**. La 3a tampoco inventa nada: destacar el template en el catálogo es configuración en el Marketplace Manager. Juntas cuestan lo mismo que la 4 sola.

La 3b **ya no es más corta de forma significativa**: con las fuentes preintegradas, la 4 son 3 clics (abrir el template, instalar, listo) contra 2 de la 3b. El argumento de "menos pasos" que sostenía a la 3b se desinfló; lo que le queda es que el merchant no tiene que saber que el template existe, y eso sigue siendo real pero ya no compensa un patrón nuevo en esta iteración.

Una vez que existe el template, la 3b se vuelve barata: **la detección proactiva en el OC simplemente instala el template que ya está publicado.** No son dos construcciones, son la misma con dos puertas.

**Ya no hay plan B que presupuestar por riesgo conceptual.** El encaje quedó confirmado en el Brain. Lo que sí puede tumbar la ruta 4 es una restricción operativa, no conceptual: que el catálogo sea cross-account global y no se pueda ofrecer solo a los 11 marketplaces.

## Qué se prototipa para el viernes

✅ **Construido:** `prototypes/acceso-al-tablero-ab.html`, un solo HTML con switch A/B y recorrido paso a paso.

| Variante | Pasos | Muestra |
|---|---|---|
| **A · Marketplace** | 4 | Catálogo con el template destacado → detalle con vista previa → instalación → **tablero operando** |
| **B · Sugerencia en el OC** | 3 | Bloque de sugerido en la lista de tableros → revisión de qué se detectó con la confianza por recurso → tablero operando |

Las dos desembocan en **el mismo tablero** (`prototypes/contracargos-merchant.html`). Eso es parte del argumento: la puerta se decide después, el contenido no cambia.

> ⚠️ **Corregido el 28-ago (Andres):** una vez instalado el template, **el tablero queda usable, no hay que configurar nada**. Para los marketplaces las fuentes de notificados y debitados ya están integradas en Simetrik, así que aplica el caso de fuentes preintegradas del Brain (UC-16): la instalación se completa sola y aterriza con datos reales. Se cayeron los dos pasos de configuración que tenía la opción A.

**Se descartó la variante C (Agent) como pantalla propia.** La edición por chat vive en las dos y no compite con ellas como puerta de entrada; mostrarla como tercera opción confundía la decisión en vez de aclararla.

## Estados que el prototipo tiene que cubrir

1. **Sin detección** — el motor no encontró recursos de contracargo. Empty state con la forma del dato esperado (qué columnas debería traer un archivo de notificados) y la acción de conectar la fuente
2. **Detección parcial** — el motor acertó al 30%. Se muestra la confianza y la salida para corregir por dataset o por chat. Este es el caso más frecuente según Andrea, no el borde
3. **Instalado y poblado** — el caso feliz
4. **Instalado sin datos aún** — el template quedó instalado pero la fuente todavía no llega
5. **Ya instalado** — el usuario vuelve al Marketplace y el template ya está. No ofrecer instalar de nuevo

## Preguntas para el viernes

~~1. ¿Un control cabe conceptualmente en el Marketplace?~~ **Resuelta en el Brain: sí.** Se lleva como hallazgo, no como pregunta.

~~2. ¿El template se ofrece a los 11 marketplaces por defecto?~~ **Resuelta: hoy no se puede.** El catálogo es cross-account global y no existe segmentación por cuenta. Se convierte en la pregunta 1 de abajo.

Las que quedan vivas:

1. **El catálogo es global.** ¿Publicamos Contracargos para todas las cuentas habilitadas, o esperamos a que exista segmentación? Es la decisión de fondo del viernes
2. ¿Lo destacamos como *featured* en el Marketplace Manager desde el día uno?
3. ¿Vale la pena presupuestar la detección proactiva en el OC (3b), sabiendo que es patrón nuevo y que nadie más lo ha pedido todavía?
4. Los nombres sufijados con timestamp (`Contracargos_1756…`) van a quedar a la vista. ¿Se deja así o se arregla antes de publicar?
5. No hay update-in-place. Si mejoramos el template, los que ya lo instalaron se quedan con la versión vieja. ¿Aceptable para esta iteración?
