# Plan de trabajo — Contracargos (merchant)

**Fecha:** 26-ago-2026 · **Con:** Andrea Giraldo (Product Engineering Manager) · **Backend:** Santi · **Decisor de producto:** Vicky
**Proyecto Ohana:** `contracargos/` · **Prototipo insumo:** `Simetrik · Centro de Disputas — Operations Center.html` (2.011 líneas, autocontenido, vanilla JS)

## Fuentes

| Fuente | Qué aporta |
|---|---|
| Sesión "Ladi - Andre chargebacks", 26-ago-2026 (Wispr Flow) | Reacote de alcance a merchant, flujo notificado/debitado, las 4 rutas de acceso, los compromisos |
| `Simetrik · Centro de Disputas — Operations Center.html` | Modelo conceptual completo de Andrea: pipeline, reason codes, umbrales VAMP/ECM, ciclo de vida, ChargeScore, wizard de monitoreo |
| `plans/archivo-julio-2026/00..07` | Los 7 planes de julio. Siguen válidos salvo donde el reacote los superó (ver abajo) |
| `design.md` | Tokens desyk 1.30.0-0 y patrones de este prototipo |
| Brain, commit `ae66cd5` (30-jun) | Redefinición de templates de Marketplace, relevante para la ruta de acceso 4 |

## Contexto

Los ~11 marketplaces de Simetrik (Rappi, PedidosYa, iFood, Falabella, entre otros) reciben contracargos de sus adquirentes y hoy **no tienen dónde verlos**. Los implementadores construyen el control y lo entregan como export a un dataset que el cliente tiene que bajar y moler en otra herramienta. Nadie llega a una pantalla y ve que tiene 8.000 débitos y 8.000 tarjetas por bloquear. Mientras no lo vea, sigue perdiendo plata y la marca sigue sancionando.

**El flujo del dato.** El adquirente manda archivos por SFTP: uno `notificados` ("le voy a debitar esto") y días después uno `debitados` ("le debité esta plata"). En algunos clientes, como el local, no vienen separados: llega una columna de estado dentro de una sola base. En Simetrik ya viven esos recursos y ya generan conciliaciones.

**Lo que ya existe del lado de ingeniería.** Motor de inferencia que identifica qué recursos del cliente son contracargos (acierta entre 30% y 70% según qué tan raros sean los nombres) → diccionario canónico para unificar llaves de cruce → dataset automático → tablero. Todo eso pasa por detrás; el cliente solo ve el resultado.

**Los tres controles que el merchant hace a mano hoy:** bloquear tarjetas de lo debitado (prevención de fraude), conciliar venta interna contra lo del adquirente, y cazar el doble débito (el mismo contracargo descontado dos veces, en la liquidación y en el refund).

## El problema a resolver esta semana

> "Tengo construido este proto, pero no sé dónde meterle el cómo llegar a esa mierda del tablero."
> — Andrea, 26-ago

No es rediseñar el centro de disputas. **Es resolver el acceso**: cómo un merchant llega a un tablero de contracargos armado sin haber hecho un solo clic de configuración. Cuatro rutas sobre la mesa, detalladas en `01-spec-acceso-al-tablero.md`.

## Qué cambió respecto a los planes de julio

La reunión del 9-jul dejó cinco decisiones en `plans/archivo-julio-2026/06-analisis-prototipo-andrea.md`. El reacote del 26-ago toca una:

| # | Decisión de julio | Estado tras el 26-ago |
|---|---|---|
| 1 | Emisor fuera de alcance | ✅ **Vigente y reforzada.** Andrea: el flujo de cara al emisor "no aplica para el merchant" |
| 2 | Sin win rate agregado | ✅ Vigente |
| 3 | Sin "recuperado" agregado en el tablero | ✅ Vigente. Se suma: la vista gerencial de pérdidas también queda fuera del alcance inicial |
| 4 | **Rol primario = PSP adquirente**, merchant como receptor | ⚠️ **SUPERADA.** El alcance se acotó a los merchants/marketplaces. El rol primario ahora es el merchant |
| 5 | Monitoreo reutiliza el modelo de notif-resumen | ✅ Vigente, y ahora con detalle técnico: hacen falta **dos monitoreos**, sobre la columna normalizada y sobre la fuente |

**Consecuencia práctica:** el switch de 4 roles del prototipo (Issuer / Merchant / PSP / Adquirente) colapsa a Merchant. Los otros tres quedan como material de demo comercial, no de producción.

> ✅ **Decidido el 26-ago por Andres: el merchant reemplaza al PSP como rol primario.** Ya no es un supuesto. El switch de 4 roles colapsa a Merchant y los KPIs se rearman en notificado / debitado / doble débito / bloqueo de tarjetas. Queda comunicárselo a Andrea, no consultárselo.

## Alcance

**Dentro:**
- Tablero de contracargos para merchant, con notificado y debitado como lecturas separadas
- Los tres controles operativos: bloqueo de tarjetas, conciliación, doble débito
- Semáforo de tasa contra umbrales de red (VAMP, ECM) con distancia al umbral
- Activación de monitoreo: sobre la columna normalizada del dataset **y** sobre la fuente
- La ruta de acceso al tablero (el entregable del viernes)

**Fuera:**
- Vista gerencial de pérdidas. Se retoma cuando esté más pulido
- Todo el flujo de cara al emisor (recopilar evidencia y postear en Mastercard)
- Los roles Issuer, PSP y Adquirente como vistas de producción
- El ciclo de vida completo de la transacción **hasta confirmar que la data lo permite** (ver riesgos)

## Entregables

| # | Entregable | Archivo | Para |
|---|---|---|---|
| 1 | Plan de trabajo | `plans/00-plan-de-trabajo.md` | Este documento |
| 2 | Spec de acceso al tablero | `plans/01-spec-acceso-al-tablero.md` | La presentación a Vicky del viernes |
| 3 | Spec del tablero merchant | `plans/02-spec-tablero-merchant.md` | Base del prototipo y del handoff a Santi |
| 4 | Sistema de diseño | `design.md` | Tokens desyk reales, ya listo |
| 5 | Prototipo con las alternativas | `prototypes/` | Demo A/B con switch, para el viernes |
| 6 | Handoff implementable | `handoff/` | Después de que Vicky decida |

## Cronograma

| Cuándo | Qué | Quién |
|---|---|---|
| Mié 26-ago | Plan + specs + `design.md` (este bloque) | Ladi |
| Mié 26-ago | Recibir de Andrea el prototipo y el flujo | Andrea ✅ prototipo recibido |
| Jue 27-ago | Prototipo A/B de las rutas de acceso sobre el HTML de Andrea | Ladi |
| Jue 27-ago | Alineación con Santi: documentación del backend del skill | Ladi + Santi |
| **Vie 28-ago** | **Presentación de alternativas a Vicky**, incluida la pregunta de si el tablero encaja en el Marketplace | Andrea + Ladi |
| Post-viernes | Handoff de la ruta elegida | Ladi |

## Preguntas abiertas

> **Estado al 26-ago:** 5 resueltas con evidencia (Brain v2.8, código de `fe-solutions-mf`, reglas de red). Ver `04-respuestas-preguntas-abiertas.md`. Las que siguen abajo con ⏳ necesitan a un humano.

**Para Andrea:**
1. ✅ **Resuelta por Andres: el merchant reemplaza al PSP.** Se le comunica a Andrea, no se le pregunta.
2. ⏳ ¿Quién usa esto todos los días: el operativo que bloquea tarjetas, o el manager? La sesión dijo que son dos consumos distintos y que el gerencial queda fuera, así que asumo el operativo. Confirmar.
3. ⏳ ¿Qué tiene que haber absorbido esa persona en los primeros 2 segundos? Mi hipótesis: cuántos débitos nuevos hay y cuántas tarjetas quedan por bloquear.
4. ⏳ ¿"Monitoreo" o "agente"? En notificaciones se acordó no decir "agente" de cara al usuario. Conflicto con el glosario de `simetrik-ui`, que sí lista "Agente IA".

**Para Santi:**
5. ⏳ ¿La data permite encadenar notificado → debitado → reversión de una misma transacción? De esto depende si el ciclo de vida se dibuja o no.
6. ⏳ ¿Qué llaves de cruce sobreviven al diccionario canónico? El prototipo de Andrea asume ARN + código de autorización.
7. ✅ **¿Cómo se expone la columna normalizada?** Resuelta: el contrato es `metric_reference` (nombre real de la columna) + `metric_aggregation` + `thresholds[]`, con `categoryColumnNames` para segmentar por red. Queda solo: ⏳ quién la materializa y en qué punto de la cadena.

**Para Vicky:**
8. ✅ **¿Un control cabe en el Marketplace?** Resuelta en el Brain: sí, un Template *es* un dashboard del OC con datasets, recursos, **anomalías** y contexto AI. La duda estaba mal planteada. Pero aparecen cinco restricciones operativas, la mayor: el catálogo es **cross-account global**, no hay segmentación por cuenta.
9. ✅ **¿El OC puede tener "sugerido"?** Resuelta: en el OC no existe. Pero en el **Marketplace sí**, y está construido (featured / recommended vía Marketplace Manager). La ruta 3 se parte en 3a (ya existe, cero costo) y 3b (patrón nuevo en el OC).

**Extra resuelta:** los umbrales VAMP del prototipo (2.20%) están **vencidos**. Desde el 1-abr-2026 son 1.5%, y VAMP y ECM usan fórmulas distintas para llegar ahí.

## Riesgos y dependencias

| Riesgo | Impacto | Mitigación |
|---|---|---|
| La data no permite encadenar los tres estados | El ciclo de vida del prototipo de Andrea no se puede construir | Diseñar el tablero para que funcione sin él; el ciclo de vida es aditivo, no estructural |
| El motor de inferencia acierta solo 30% en algunos clientes | El tablero llega incompleto y el usuario no confía | Mostrar la confianza de la clasificación y dar la salida de corregir por dataset o por chat |
| "Control" dentro de "Marketplace" no le hace sentido a Vicky | Cae la ruta 4, la más barata | Llevar la ruta 3 como plan B, ya especificada |
| El equipo está en reestructuración y la priorización está en pausa | El trabajo se puede volver a detener | Los entregables son autocontenidos y quedan escritos, no en la cabeza de nadie |

## Organización

✅ **Consolidado el 26-ago en `contracargos/`.** La carpeta `Disputas/` ya no existe. Se migró:

- Los 7 planes de julio y su `design.md` → `plans/archivo-julio-2026/`
- El board de Moka (4 flujos, 34 pantallas) → `.ohana/flow.json`
- Los 7 comentarios de Ohana anclados al prototipo → `.ohana/findings.json`

Respaldo del estado previo en el scratchpad de la sesión (`Disputas-backup-2026-08-26.tar.gz`).
