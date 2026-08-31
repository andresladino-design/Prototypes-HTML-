# 04 — Respuestas a las preguntas abiertas

**Fecha:** 26-ago-2026 · **Método:** Brain v2.8, código de producción en `fe-solutions-mf`, reglas públicas de red
**Estado:** 5 resueltas con evidencia · 2 decididas por Andres · 4 siguen necesitando a un humano

---

## ✅ P8 — ¿Un control de contracargos cabe en el Marketplace?

**Respuesta: sí, y es exactamente el artefacto para el que se construyó.**

Fuente: `Brain/versions/v2.8/operation-center/funcionalidades/templates-y-marketplace/Definicion - Templates y Marketplace.md` (commit `ae66cd5`, 30-jun-2026).

Un **Template** empaqueta *"un dashboard completo del OC junto con todas sus dependencias (datasets, recursos, reconciliaciones, agrupaciones/uniones, fuentes/super-fuentes) y el contexto documentado"*. El modelo formal (UC-25) es: Dashboard (1, obligatorio) + Datasets (1+, obligatorio) + Pendientes / **Anomalías** / Archivos / Recursos / Contexto AI (0+, opcional).

Es decir, **el "control" de contracargos ES un template**, no algo que haya que forzar dentro de uno. La duda de la sesión estaba mal planteada: no es "un control metido en un marketplace de otra cosa", el marketplace es literalmente un catálogo de controles empaquetados.

**Lo que esto desbloquea, y que no habíamos considerado:**

| Capacidad ya construida | Qué significa para contracargos |
|---|---|
| Las **anomalías viajan dentro del template** y se provisionan en la instalación (UC-12, Paso 2) | El monitoreo de umbral de red puede venir **pre-configurado**. El merchant no lo arma |
| **Contexto AI** estructurado por dashboard, gráfico, fuente y anomalía (UC-28) | Las definiciones del dominio (qué es notificado, qué es debitado, por qué importa el umbral) viajan con el template y el Solutions Agent las puede explicar |
| **Fuentes preintegradas** (UC-16, Paso 6.3) | ⭐ **El caso de contracargos.** Los marketplaces ya tienen notificados y debitados en Simetrik, así que el template se arma con fuentes preintegradas y **la instalación se completa sola: el tablero aterriza usable, sin configurar nada** (confirmado por Andres, 28-ago) |
| Swap de fuentes existentes (Paso 6.2) | Camino alterno si alguna fuente no viene preintegrada: se reemplaza la del template por una del workspace, preservando el mapeo |
| Mock data + banner "Pending Setup" (Paso 4) | Flujo general para templates que sí piden archivos. **No aplica a contracargos** |
| **Redirect automático al OC** con el filtro global ya puesto en el tablero instalado (Paso 3) | La instalación no deja al usuario buscando dónde quedó su tablero |
| **Fuentes preintegradas** (Paso 6.3) | Si todas las fuentes son preintegradas, la instalación es 100% automática y aterriza con datos reales |
| **Box / URL de partner** (Paso 12) | El mismo flujo embebido en la URL del cliente. Relevante para marketplaces grandes |

**Restricciones que hay que llevar a la reunión, no son menores:**

1. **El catálogo es cross-account global.** Un template publicado *"queda disponible para todas las cuentas habilitadas"*, gated solo por el sub-flag `OperationCenter.modules.marketplace`. **No existe segmentación por cuenta.** No se puede ofrecer el template solo a los 11 marketplaces: o lo ve todo el mundo, o no se publica. Esto responde de una la pregunta 2 del viernes.
2. **No hay desinstalación ni rollback** en esta fase.
3. **No hay update-in-place.** Cómo se le comunica al usuario que hay una versión nueva de un template instalado es un **gap abierto** documentado en el propio Brain.
4. Cada instalación **sufija los nombres con timestamp** para no colisionar. Van a aparecer tableros llamados `Contracargos_1756...`. Hay que ver cómo se lee eso.
5. Publicar requiere permiso `MarketplaceAdmin`; instalar solo `oc:view` + el sub-flag.

---

## ✅ P9 — ¿El Operation Center puede tener un patrón de "sugerido"?

**Respuesta: en el OC no existe y habría que inventarlo. Pero en el Marketplace ya existe y está construido.**

Busqué el patrón en el Brain (`Definicion - Navegacion y Home.md`) y en el código. En el OC, la navegación solo garantiza persistencia de contexto y el Home account-level es un lanzador hacia OC, Marketplace y Workspaces legacy. **No hay ninguna noción de contenido sugerido.** El grep de `suggest|sugerid|recomend` sobre `features/dashboards`, `features/datasets` y `features/anomalies` solo devuelve autocompletado de SQL y parseo de errores.

En cambio, el **Marketplace Manager** (UC-01) ya permite curar el layout del catálogo: *"cuántos templates destacados (featured) se muestran y cuáles"*, *"cuántos recomendados (recommended)"*, banners y beneficios. Y está construido: en `fe-solutions-mf/src/oc/features/marketplace/components` existen `MarketplaceFeaturedSection`, `MarketplaceFeaturedCard`, `MarketplaceHeroCarousel`, `BenefitsCarousel`, `CategoryGrid`, más el módulo `marketplace-admin` completo.

**Consecuencia para la spec 01:** la ruta 3 no es "sugerencia en el Operation Center" contra "template en Marketplace". **La sugerencia ya existe, solo que vive en el Marketplace.** Destacar Contracargos como *featured* es configuración en un panel que ya está construido, cero UI nueva. Lo que no existe es la sugerencia **proactiva dentro del OC**, del tipo "detectamos contracargos en tus fuentes", y eso sí es patrón nuevo.

Esto parte la ruta 3 en dos cosas distintas que estaba mezclando:
- **3a · Destacado en el Marketplace** — ya existe, costo cero, descubribilidad media
- **3b · Detección proactiva en el OC** — no existe, costo alto, descubribilidad máxima

---

## ✅ P7 — ¿Cómo se expone la columna normalizada que el monitoreo necesita?

**Respuesta: ya hay un contrato en producción, y encaja.**

Fuente: `fe-solutions-mf/src/oc/features/anomalies/components/AnomalyMonitoringConfig/types.ts`.

Una regla de monitoreo (`LocalKpiRule`) se ata a:

```ts
{
  metric_field_id: string;
  metric_reference: string;      // "actual column name sent to BE"
  metric_aggregation?: string;
  thresholds: [{ operator, value, series_value }];
}
```

y el snapshot de configuración incluye `dateColumnId`, `categoryColumnNames[]`, `granularity`, `timezone`, `frequency`.

Tres cosas se confirman:

1. **El monitoreo se ata a una columna concreta del dataset por nombre** (`metric_reference`). Lo que dije en la sesión no era una hipótesis de diseño: es el contrato real. Sin esa columna normalizada no hay nada que monitorear.
2. **`categoryColumnNames` + `series_value` dan la segmentación.** El umbral "por red" que Andrea prototipó no es una feature nueva: es `categoryColumnNames: ["franquicia"]` con un `threshold.series_value` por cada red. Ya se puede.
3. **`thresholds[]` es una lista con operador y valor**, así que el `≤ 2.20%` de Visa y el `≤ 1.50%` de Mastercard son dos filas de la misma regla.

**Y el segundo monitoreo, el de la fuente, también existe.** El Paso 9.3 del flujo documenta las *"anomalías de ingesta"*, con *"acceso directo a la sección de Fuentes"* para recargar, reemplazar o corregir el mapeo. El loop que planteé en la sesión (no poder distinguir una anomalía real de un archivo que no llegó) ya está resuelto en producto.

**Sigue abierto para Santi:** quién calcula y materializa esa columna normalizada del dato de negocio, y en qué punto de la cadena.

---

## ✅ Umbrales VAMP / ECM — los del prototipo están vencidos

El prototipo de Andrea pre-carga **Visa VAMP 2.20%** con la nota "→ 1.50% el 1-abr-2026". **Esa fecha ya pasó.** Desde el 1 de abril de 2026 el umbral de VAMP para merchant es **1.5%**, aplicado en US, Canadá, UE y Asia-Pacífico. Mastercard ECM sigue en **1.5% con más de 100 contracargos al mes**.

Hay un detalle que **no es cosmético y el prototipo no refleja**: los dos programas llegan al mismo 1.5% por fórmulas distintas.

| Programa | Fórmula |
|---|---|
| **Visa VAMP** | (Fraude TC40 + Disputas TC15) / Transacciones liquidadas TC05 |
| **Mastercard ECM** | Conteo puro de contracargos sobre transacciones, con el mes anterior en el denominador |

O sea que VAMP **incluye reportes de fraude**, no solo contracargos. El toggle "Cálculo del ratio: Por red / Agregado" del wizard de Andrea es más importante de lo que parece: un agregado entre redes es un número que no significa nada para ninguna de las dos.

**Acción:** corregir el 2.20% a 1.50% en el prototipo, y modelar las dos fórmulas por separado.

Fuentes: [MRC — Stricter VAMP Ratio Thresholds Are Now in Effect](https://merchantriskcouncil.org/learning/resource-center/member-news/blog/2026/stricter-vamp-ratio-thresholds-are-now-in-effect-heres-how-to-stay-compliant) · [Visa VAMP Threshold April 2026](https://justt.ai/blog/visa-vamp-threshold-changes-april-2026/) · [Chargeback Threshold Limits: Every Network, 2026](https://www.chargeflow.io/blog/chargeback-threshold-limits) · [Mastercard ECM Program: Thresholds & Tiers](https://chargebacks911.com/mastercard-chargebacks/mastercard-excessive-fraud-chargeback-monitoring-programs/mastercard-ecm-program-thresholds-tiers/)

---

## ⏳ Siguen necesitando a un humano

| # | Pregunta | Para | Por qué no se puede resolver leyendo |
|---|---|---|---|
| 1 | ~~¿El merchant reemplaza al PSP?~~ | Andrea | ✅ **Resuelta 26-ago por Andres: el merchant reemplaza al PSP.** Queda confirmarlo con Andrea, pero el diseño ya no lo trata como supuesto |
| 2 | ¿Usuario diario: el operativo que bloquea tarjetas, o el manager? | Andrea | Requiere conocer a los usuarios reales de los 11 marketplaces |
| 3 | ¿Qué debe absorber en los primeros 2 segundos? | Andrea | Hipótesis actual: cuánto se debitó y cuántas tarjetas faltan por bloquear |
| 4 | ¿"Monitoreo" o "agente" en el copy? | Andrea | Hay conflicto entre la corrección de Andres y el glosario de `simetrik-ui` |
| 5 | ¿La data permite encadenar notificado → debitado → reversión? | Santi | Depende del contenido real de los archivos de cada adquirente |
| 6 | ¿Qué llaves de cruce sobreviven al diccionario canónico? | Santi | Ídem |
| 7b | ¿Quién materializa la columna normalizada y en qué punto de la cadena? | Santi | El contrato del front ya se conoce; falta el lado del backend |
| — | ~~¿Consolidamos `Disputas/` y `contracargos/`?~~ | Andres | ✅ **Resuelta 26-ago: consolidado en `contracargos/`.** Planes de julio en `plans/archivo-julio-2026/`, board de Moka migrado |

---

## Qué cambia en las specs

1. **`01-spec-acceso-al-tablero.md`** — la ruta 3 se parte en 3a (destacado en Marketplace, ya existe) y 3b (detección proactiva en el OC, no existe). La ruta 4 deja de ser "a validar" y pasa a "confirmada, con cinco restricciones". La pregunta de "¿se ofrece a los 11 o se publica?" ya tiene respuesta: **hoy solo se puede publicar al catálogo global**.
2. **`02-spec-tablero-merchant.md`** — el tablero **no tiene estado de configuración**: instalado el template, queda usable (fuentes preintegradas, confirmado por Andres el 28-ago). Se caen el empty state, el mock data con "Pending Setup" y la vinculación de fuentes. Se corrigen los umbrales. El monitoreo se documenta contra el contrato real de `AnomalyMonitoringConfig`.
