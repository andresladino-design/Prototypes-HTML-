---
epic: MONITOR_INGESTA
issue_type: Spike
priority: P3
estimate: XS
labels: [ux, documentation, monitoring, reference, journey]
depends_on: []
blocks: []
component_areas: [documentation]
---

# 13 · Journey Low / Family / High — Síntesis del modelo

> Documento conceptual. Para la implementación detallada de cada paso ver docs 05-12.

## El problema

Una fuente de datos en Simetrik no es homogénea. Algunas son simples (un archivo diario, mismo formato, mismo volumen). Otras llegan en patrones diferenciados por día (lunes pesado por el corte semanal, martes liviano). Otras encierran subconjuntos con patrones propios (Visa, Mastercard y Acquirer llegando juntas en un mismo SFTP).

Si forzamos al usuario a configurar todo desde el primer modal con un nivel de detalle máximo, se rinde antes de empezar. Si simplificamos demasiado, perdemos precisión y el monitor empieza a disparar falsos positivos. La solución es un modelo que **escala con la complejidad real de la fuente**, no con la complejidad del UI.

Por eso definimos 3 perfiles internos. El usuario nunca los nombra. El UI los expone gradualmente y le permite subir un escalón solo cuando lo necesita.

## Los 3 perfiles (internos)

| Perfil | `monitorMode` | `useGroupsAll` | Cuándo aplica | Qué espera el usuario |
|---|---|---|---|---|
| **Low** | `'igual'` | `false` | Default al entrar al modal. Fuente con comportamiento uniforme. | Una sola config. Se aplica a todos los días sin discriminar. Candado cerrado. |
| **Family** | `'por-dia'` | `false` | El usuario detectó que los días se comportan distinto. | Cada día con su propio Volumen + Cantidad + Notas. Tabs muestran dot azul en días monitoreados. |
| **High** | `'por-dia'` | `true` | El agente detectó grupos con patrones diferenciados (ej. `Visa_*`, `Mastercard_*`) y el usuario los activa. | Cada día tiene grupos. Cada grupo se configura por separado. |

## Diagrama del journey

```
Low (default al abrir el modal)
  · Candado cerrado en el tab switcher
  · Badge "Igual todos los días" visible
  · dsActiveSimple() devuelve daySetup.shared

   |
   |  Tres caminos de promoción a Family:
   |    1. Dropdown "Monitorear" → "Por día de la semana"
   |        (transición silenciosa, el usuario lo pidió)
   |    2. Editar input de Volumen/Cantidad o togglear el switch del indicador
   |        (dsPromoteToFamily('edit') + banner de feedback 6s)
   |    3. Apagar el toggle "Monitorear fuente los [día]"
   |        (dsPromoteToFamily('toggle') + banner)
   ↓

Family (config por día)
  · Candado abierto
  · Dots azules en tabs de días con monitorEnabled
  · dsActiveSimple() devuelve day.simple del día activo

   |
   |  Promoción a High:
   |    Click en banner "Monitorear grupos" (CTA del slot Low/Family)
   |    → dsActivateGroups()
   |    → loader pedagógico ~1.4s "Detectando los grupos de archivos"
   |    → siembra grupos en todos los días (dsSeedGroupsFor)
   ↓

High (config por grupo, por día)
  · Mismo candado abierto que Family
  · Cards ds-group reemplazan los indicadores planos
  · Primer grupo del día arranca expandido (Figma)
```

## Empty states (importante)

El prototipo HTML actual solo tiene algunos empty states (loaders, casos puntuales). Aunque no estén pintados, esta historia debe enumerarlos para que el implementador los considere a nivel de journey, no solo de contenedor.

| Escenario | Condición | Copy propuesto | CTA | Implementado en HTML? |
|---|---|---|---|---|
| Fuente sin patrones (Low forzado) | Agente no detectó grupos en ningún día | Banner "Monitorear grupos" oculto. El usuario solo puede usar Low o Family. | (ninguno) | ❌ (banner siempre visible si `!daySetupHasConfig`) |
| Fuente sin sugerencias del agente | BE devolvió `_sArrivesAt/_sMin/_sMax === null` para toda la fuente | Chip "Sin sugerencias disponibles" en todos los inputs. Usuario configura desde cero. | (ninguno, configura manual) | ❌ |
| Loading inicial del modal | Fetch de seed + sugerencias en curso | Skeleton en todo el modal (Ventana de tiempo + indicadores) durante <1s. | (ninguno) | ❌ |
| Error al cargar config existente | Fetch del `dayConfig` falló | Estado vacío central "No pudimos cargar la configuración. Cierra y vuelve a intentar." | Botón "Reintentar" + botón "Cerrar". | ❌ |
| Todos los días apagados | `daySetup.days.every(d => !d.monitorEnabled)` | Banner sobre el footer "Esta fuente quedará sin monitoreo. Activa al menos un día para guardar." | (ninguno, bloquea Guardar) | ❌ |
| Transición Low → Family fallida | `dsPromoteToFamily()` lanzó excepción | Toast destructive "No pudimos cambiar a configuración por día." | "Reintentar" en el toast. | ❌ |
| Transición Family → High fallida | `dsActivateGroups()` no devolvió grupos | Banner ámbar "No encontramos grupos diferenciados. Quédate en Family." | Botón "Entendido" cierra el banner. | ❌ |
| Detalle (readonly) sin config completa (legacy) | Fuente migrada con config parcial | Card por sección con "Sin configurar" y CTA "Configurar ahora". | Botón "Configurar ahora" pasa a edición. | ❌ |
| Búsqueda sin resultados (futuro, si se agrega filtro por fuente en el modal) | `filteredSources.length === 0` | "No encontramos fuentes que coincidan." | Botón "Limpiar filtro". | ❌ |

## Escenarios poco probables

- **Fuente sin patrones detectables**: el agente no encuentra grupos diferenciados. El usuario nunca ve el banner "Monitorear grupos" o, si lo ve, al activarlo el día muestra el estado vacío `ds-day-off`. Se queda cómodo en Low.
- **Usuario que ignora los grupos**: el agente detecta grupos pero el usuario decide no activarlos. Se queda en Family con la misma config simple aplicada por día. No es un error: hay fuentes donde el costo de configurar por grupo no compensa.
- **Días apagados**: en Family o High, el usuario apaga el toggle de un día (ej. domingo). Ese día queda con `monitorEnabled: false`, sin dot azul en el tab, sin indicadores ni banner. Si la fuente nunca llega ese día, es el comportamiento correcto.
- **Mezcla Family + High parcial**: el modelo no soporta esto. `useGroupsAll` es global: o todos los días usan grupos o ninguno. Es una decisión de modelo para evitar cuadrículas 7 días × N grupos vacías.
- **Detalle (readonly)**: el modal puede abrirse en modo lectura. Toggle del día y switches de indicadores se ocultan. Notas se muestran solo si tienen contenido. Útil para revisar configs sin tocar nada.

## Cómo el UI sintetiza este modelo

1. **Default es Low**. Al abrir el modal por primera vez, el usuario siempre arranca simple. La complejidad se gana, no se impone.
2. **Candado en el tab switcher**. Es la metáfora visual del modo. Cerrado: tus 7 días comparten configuración. Abierto: cada día tiene la suya. Sin texto, una sola seña visual que el usuario entiende intuitivamente.
3. **Banner pedagógico "Monitorear grupos"**. Es la palanca para subir a High. Vive en el slot Low/Family con ilustración SVG que muestra 3 archivos convergiendo a un hub. Solo aparece cuando hay grupos detectados y la config no existe (`!daySetupHasConfig`).
4. **Promoción con feedback**. Cuando el usuario edita un input en Low, no le preguntamos "querés cambiar a config por día?" — lo promovemos silenciosamente y le mostramos un banner azul de 6s explicando qué pasó (`changeFeedback`). La promoción nunca es destructiva: el `shared` se clona a cada día.
5. **Loader pedagógico de 1.4s**. La transición Family → High muestra un spinner con copy "Simetrik está identificando los archivos que comparten patrón". No es espera real (los datos ya están sembrados); es para enseñar que algo no trivial está pasando.
6. **Chips violetas de agente**. En todo el modal sin config, los inputs muestran "Autocompletado por el agente" o "Sugerencia: N". Le recuerdan al usuario que partió de una propuesta, y le permiten volver a ella con un click.

## Por qué importa para implementación

- **Nunca exponer las etiquetas Low/Family/High en el UI**. Son nomenclatura interna para devs y diseñadores. El usuario ve "Igual todos los días" o "Por día de la semana".
- **Defaults**. Al abrir el modal, `monitorMode: 'igual'` y `useGroupsAll: false`. Siempre.
- **Side effects pedagógicos**. Toda transición automática (edit input → Family) debe ir acompañada de feedback visual claro (`changeFeedback` banner). Sin esto, el usuario se desorienta.
- **Promoción no destructiva**. `dsPromoteToFamily` clona `shared` a cada día. El usuario no pierde lo que escribió en Low.
- **Activación global de grupos**. `dsActivateGroups` siembra grupos en los 7 días de una sola pasada. No hay opción de activarlos día por día (decisión de modelo).

## Empty states (importante)

Este documento es **conceptual / referencia**. Los empty states reales viven en los docs 05-12 (cada contenedor enumera los suyos). Aquí solo resumimos los **estados macro** del journey:

| Escenario macro | Condición | Manejo | Implementado en HTML? |
|---|---|---|---|
| Fuente sin patrones detectables | El agente no encuentra grupos en histórico | Usuario nunca ve banner "Monitorear grupos". Si lo activa por error, día muestra `ds-day-off` | ✅ implementado |
| Usuario ignora los grupos | Banner visible pero usuario no activa | Se queda en Family con config simple | ✅ comportamiento por default |
| Días apagados (Family/High) | Toggle día OFF | Día queda con `monitorEnabled: false`, sin dot azul ni indicadores | ✅ implementado |
| Mezcla Family + High parcial | No soportado por el modelo | `useGroupsAll` es global. Decisión consciente del modelo | N/A |
| Modal en readonly | Fuente ya configurada | Toggle día oculto, switches con opacity 0.6, notas solo si tienen contenido | ✅ implementado |
| Promoción Low→Family fallida | `dsPromoteToFamily()` lanzó excepción | (no manejado) Toast destructive con retry | ❌ pendiente (ver doc 08) |
| Activación de grupos fallida | `dsActivateGroups()` lanzó excepción | (no manejado) Toast destructive, volver a Family | ❌ pendiente (ver doc 12) |

## Componentes desyk a usar

> Este documento es conceptual y de referencia: no se implementa directamente.
> Esta sección sintetiza los componentes desyk que aparecen a lo largo del
> journey Low / Family / High. El detalle por contenedor vive en los docs 07-12.

| Elemento del journey | Componente desyk | Variants / props | Notas de uso |
|---|---|---|---|
| `.ds-lock` (candado del tab switcher) | Ícono `Lock` / `LockOpen` de Lucide | — | Metáfora visual del modo Low vs Family/High |
| `.ds-low-chip` ("Igual todos los días") | `Badge` | `variant="default"` con override warning + ícono `Lock` | Indica modo Low |
| `.ds-tab-dot` (dot primary en días monitoreados) | `<span>` decorativo con `bg-primary` | — | Visual interno del `TabsTrigger` |
| `.ds-feedback` (banner transitorio Low→Family) | `Alert` + `AlertDescription` | `variant="default"` con override azul info; auto-dismissed | Banner pedagógico de 6s tras promoción automática |
| `.calc-loader` (loader pedagógico Family→High) | Componente custom (compuesto) | — | Spinner 1.4s con copy "Detectando los grupos de archivos" |
| `.ds-groups-banner` (banner pedagógico "Monitorear grupos") | `Card` con ilustración SVG + `Badge` pill + `Button` CTA | `variant="default"` para CTA, override violeta AI | Banner que promueve a High desde el slot Low/Family |
| `.ds-ai-chip` (chips violetas de sugerencia AI) | `Badge` | `variant="secondary"` con override violeta AI | "Autocompletado por el agente" o "Sugerencia: N" |
| Toast de error en promociones (futuro) | `Toast` + `useToast` | `variant="destructive"` | Para empty states de promoción fallida |

**Componentes compuestos (no existen en desyk, hay que componerlos):**
- `MonitorModeChip` — chip warning "Igual todos los días" (ver doc 08).
- `PedagogicalLoader` — loader 1.4s (ver doc 05).
- `MonitorGroupsBanner` — banner pedagógico con ilustración SVG (3 archivos convergiendo a hub) + pill + CTA "Monitorear grupos". Compuesto sobre `Card` + `Badge` + `Button` + ilustración custom.
- `ChangeFeedbackBanner` — banner azul transitorio auto-dismissed por timer. Wrapper sobre `Alert` con lógica de timeout.
- `AiSuggestionChip` — chip violeta clickable (ver doc 07).

**Referencias:**
- Repo desyk: `~/Simetrik/desyk-components` (read-only).
- Lista oficial de componentes shadcn/ui que desyk extiende.
- Para el detalle por contenedor del journey, ver docs 05-12.

## Implementation notes

- **Helpers Alpine clave** referenciados a lo largo del journey: `dsPromoteToFamily(reason)`, `dsActivateGroups()`, `dsToggleDayMonitor()`, `dsSeedGroupsFor()`, `dsActiveSimple()`, `dsActiveDay()`, `daySetupHasConfig`, `daySetupReadonly`.
- **CSS/clases** macro: `.ds-lock`, `.ds-low-chip`, `.ds-tab-dot`, `.ds-feedback`, `.calc-loader`, `.ds-groups-banner`.
- **Tokens desyk**: el journey usa el sistema completo (primary, ai-purple, warning, info, success).
- **Animation / motion**: 6s timer del banner `changeFeedback`, 1.4s loader pedagógico de grupos, 200ms transición de candado.

## Out of scope (a nivel modelo)

- **Downgrade automático**: no hay forma de pasar de High a Family o de Family a Low desde el UI (decisión de modelo).
- **Mezcla parcial Family + High**: no soportado. `useGroupsAll` aplica a todos los días o a ninguno.
- **Exposición de las etiquetas Low/Family/High al usuario**: son nomenclatura interna. El usuario ve "Igual todos los días" o "Por día de la semana", nunca los nombres internos.
- **Configuración por día de la ventana de tiempo**: marcada como `Próx.` en el footer del card de ventana.
- **Templates de configuración reutilizables**: no es parte del MVP.

## Criterios de aceptación

Este documento es de referencia conceptual. No hay AC implementables directos. Los AC viven en los docs 05-12.

Para el agente implementador, considerar estas **reglas de oro** como AC implícitos:
1. Default es Low siempre que se abre el modal por primera vez.
2. Promoción no destructiva: `dsPromoteToFamily` clona `shared` a cada día sin perder valores.
3. Activación de grupos siembra los 7 días en una sola pasada.
4. Toda transición automática (edit input → Family) debe ir acompañada de feedback visual (`changeFeedback` banner).
5. Nunca exponer "Low / Family / High" en copy de usuario.

## Dependencies

- **Depende de**: ninguna (documento de referencia).
- **Bloquea a**: ninguna.
- **Relacionado con**: TODOS los docs del handoff (es la síntesis).

## Verification (cómo probarlo)

Este doc no se implementa. Verifica que los docs 05-12 respeten las reglas macro descritas aquí:

1. Validar que el modal nunca exponga "Low / Family / High" en copy de usuario (solo en código y devtools).
2. Validar que el default al abrir es Low (`monitorMode === 'igual'`, `useGroupsAll === false`).
3. Validar que las 3 promociones a Family disparan banner feedback.
4. Validar que activar grupos siembra los 7 días.
5. Validar que `useGroupsAll` es global (no se puede activar día por día).

## References

- **Docs hermanos**:
  - `[00-CONTEXT.md](./00-CONTEXT.md)`: glosario, tokens, estados BADS.
  - `[05-modal-configuracion.md](./05-modal-configuracion.md)`: estructura completa del modal daysetup.
  - `[07-contenedor-ventana-de-tiempo.md](./07-contenedor-ventana-de-tiempo.md)`: el único card transversal a los 3 perfiles.
  - `[08-contenedor-comportamiento-dia.md](./08-contenedor-comportamiento-dia.md)`: el chasis donde se materializa el modelo.
  - `[09-contenedor-volumen-archivos.md](./09-contenedor-volumen-archivos.md)`, `[10-contenedor-cantidad-registros.md](./10-contenedor-cantidad-registros.md)`: indicadores planos y por grupo.
  - `[11-contenedor-notas-adicionales.md](./11-contenedor-notas-adicionales.md)`: card colapsable opcional.
  - `[12-contenedor-grupos-high.md](./12-contenedor-grupos-high.md)`: cards `ds-group` exclusivas de High.
- **Figma**: (pendiente de link)
- **Backend**:
  - BADS: `~/Simetrik/bads/src/bads/models/kpi.py:28` (lifecycle).
  - Op-center: `~/Simetrik/op-center-backend/apps/anomaly_configs/` (`AnomalyMonitoringConfig.is_active`).
