# Design Brief — Refactor de Navegación Anomalías

```yaml
[META]
  brief_id:            DB-2026-05-25-001
  fecha:               2026-05-25
  feature:             operation-center
  registro:            producto
  bootstrap:           full
  epic_ref:            (no hay épica Linear todavía — este Brief la origina)
  agentes_requeridos:
    ux_research:       false   # decisión LEAD: usuario eligió tempo rápido, no investigación primero
    ux_writer:         true
  orden_de_spawn:      [product-designer, ux-writer]   # PD y Writer en paralelo (PD lidera estructura, Writer copia)
```

## [CONTEXTO PROVISTO] — empacado por LEAD

### brain
ProductEngineeringBrain v2.8 `operation-center/funcionalidades/anomalias/`:
- `Definicion - Anomalias.md` — 21 casos de uso
- `Arquitectura - Anomalias.md` — 5 servicios: AMS, KPISs, BADS, Brain, AVA
- Estados del ciclo: Open → Resolved (manual/auto) | Dismissed | Postponed
- Priorización jerárquica: Ingestion > Data Quality > Operational Results > Financial Results
- Épicas relevantes:
  - **DOE16** Detección IA + parametrización (RFC Complete)
  - **DOE17** Configuración de alertas por usuario en KPIs/datasets/widgets (RFC Complete)
  - **DOE18** Centro de anomalías (RFC Complete)
  - **DOE24** Notificaciones externas Slack/Email/Webhooks (RFC Complete)

### linear
- **SWAT-1433** [FE] Smart Monitoring UI para charts `pending_kpi` (In Progress, Camila) — síntoma del monolito
- **SWAT-535/536/537/538** [E2.2] Parametrización System KPIs (In Progress, Andres) — milestone M3 Production Readiness I
- **SWAT-693** Rediseño panel izquierdo anomalías (Done, Andres) — refactor reciente del sidebar
- **SWAT-563** [Épica 8.2] Reglas de envío (Backlog, M8) — paraguas de reglas de notificación
- **SWAT-705** SignalGroupingStrategy pluggable (Todo) — agrupación con LLM
- **SWAT-791** [BADS] Incident timeline endpoint (Backlog) — referencia Traversal
- **SWAT-912** Refactor sidebars OC (Done) — alineación con Storage pattern

### codigo
Repo `/Users/andres94ladino/Simetrik/fe-solutions-mf` (mapeo del agente Explore — completo):

- **`src/oc/features/anomalies/`** (raíz del módulo)
- **`pages/AnomaliesPage.tsx`** (990 LOC) — única página, 3 modos vía toolbar tabs: `INCIDENTS | CONFIG | HISTORY`
- **`framework/routes/anomalies.tsx`** — 5 rutas, todas renderizan la misma página
  - `/operation-center/anomalies` (base)
  - `/operation-center/anomalies/incidents/:incidentId`
  - `/operation-center/anomalies/resources`
  - `/operation-center/anomalies/resources/:resourceId`
  - `/operation-center/anomalies/signals` (histórico)

**El monolito**:
- **`components/AnomalyMonitoringConfig/AnomalyMonitoringConfig.tsx`** (3566 LOC) — Dialog modal con `SolutionsDialogNavigation` + sidebar stepper
- Sub-componentes co-ubicados (174KB total):
  - `SystemKpiDetailView.tsx` (2416 LOC) — el segundo monolito; tabs Metadata | Sample Data | (Config TBD)
  - `AiCollectingLoader.tsx`, `SlackChannelCard.tsx`, etc.
- Sections: Schedule (frequency, timezone, time window) + Notifications (Email + Slack) + Series N (thresholds + narrative preview)
- 40+ useState, lógica mezclada
- `activeSection` usa strings como `"series-${metricKey}"` → quebradizo si key tiene guiones (line 1725, 800, 1136, 1949)

**Sidebar de la lista**:
- `AnomaliesPage` con `AnomaliesToolbar` (3 mode tabs) + `AnomaliesSidebar` (collapsible, 96w/14w) + Detail panel (60% width)
- `AnomalyCard.tsx` (155 LOC), `AnomaliesActiveFiltersBar`, `AnomaliesHistoryTable`
- State: URL params + Zustand (`oc_anomalies_sidebar_collapsed_v2`) + localStorage (sort pref)

**System KPI**:
- `components/SystemKpiTab/SystemKpiTab.tsx` (101 LOC) — searchable list, infinite scroll, search debounced 400ms
- `SystemKpiSourceList.tsx`, `SystemKpiSourceDetail.tsx`
- **No integrado a `AnomalyMonitoringConfig`** — son hermanos en el sidebar, no padre-hijo

**User KPI**:
- **No existe componente separado**. Flujo de creación implícito: usuario abre modal `AnomalyMonitoringConfig` desde un chart (chart_id en URL).

**Patrones de navegación detectados**:
- Tabs (3 modes) en toolbar
- Sidebar collapse persistente
- ❌ NO breadcrumbs
- ❌ NO Cmd+K / Command palette
- ✅ URL persistence buena (`?chart_id=`, `:incidentId`, `:resourceId`)
- Modal dialog para config = escalón extra
- Nested tabs en detail panel (Evidence | Consequences | Timeline)

**Fricciones críticas (del Explore)**:
1. **Monolito 3566 LOC** — refactor de un tab toca toda la máquina de estado
2. **Duplicación** — `SystemKpiDetailView` y `AnomalyMonitoringConfig` ambos editan thresholds
3. **`activeSection` quebradizo** — string-based con concat
4. **Sin breadcrumbs** — usuario se pierde en modal profundo
5. **3 superficies de config** confusas (System KPI tab + Source Detail + Modal monstruo)

### locales
- `ops-roadmap/02-kpis-pendientes-avanzados/README.md` (este repo) — caso pending_kpi
- `ops-roadmap/04-refactor-navegacion/README.md` (este repo) — research note original
- `ops-roadmap/05-reglas-notificacion-mvp/` — sub-temas de notificación
- `ops-roadmap/10-notifications-system-kpis/README.md` — milestone M2.5

### copy_previo
Glosario Op Center v2.8 vigente:
- Dataset ✓ (en Op Center "dataset" SÍ es término oficial)
- Anomalía (no "desviación")
- **Señal de anomalía** (no "alerta atómica" ni "alerta" suelta)
- **Incidente** (no "ticket" ni "alerta agrupada")
- Tablero (no "dashboard")
- KPI (no "métrica genérica")
- Agente IA (no "bot" ni "asistente")
- BADS (sistema de detección genérico — interno)
- Espacio de trabajo (no "workspace")
- Fuente (no "origen" en este dominio)

### figma
no_consultado

### granola
no_consultado

---

## Decisiones del LEAD durante discovery socrático

Respuestas del humano:
1. **Dolor central**: los 4 entrelazados (descubrimiento + complejidad + jerarquía + flujo) → no es fix puntual, es refactor de arquitectura de información
2. **Usuario**: Analista financiero/contador del cliente, Producto, diario, power user de dominio, casual de UI
3. **Día 1**: configura primero, recibe alertas después
4. **Entidad raíz**: híbrido — dos navegaciones complementarias, con preferencia por C
5. **IA**: explica incidente (sugiere durante) — reforzar `SynthesizeInitialHypothesis` ya en prod

**Patrón arquitectónico elegido**: **C. Recurso-céntrico con hilo IA**
- La unidad central es el **Recurso** (chart o fuente)
- Una sola vista por recurso muestra TODO: config + activity + histórico
- IA sintetiza estado al abrir cada recurso
- Mata el modal monstruo → config inline en tabs del recurso
- Sidebar = lista completa de recursos (monitoreados + no monitoreados) con dot indicator de salud

**Tempo**: Rápido — `shape → prototype` mismo día. UX Research skip esta vez.

---

## [CONTEXTO]

```yaml
problema: >
  El módulo de Anomalías del Op Center sufre 4 fricciones encadenadas:
  (1) descubrimiento ambiguo — el usuario no sabe dónde empezar (¿lista de
  incidentes? ¿catálogo de KPIs? ¿chart?); (2) un monolito de configuración
  de 3566 LOC (AnomalyMonitoringConfig) que mete sidebar stepper, schedule,
  notificaciones y N series en un solo modal; (3) jerarquía rota — System
  KPI Tab, Source Detail y Modal monstruo editan los mismos thresholds en
  tres superficies distintas; (4) flujo quebrado — config sin breadcrumbs,
  sin Cmd+K, con tabs anidados en tabs anidados. El analista pierde el
  hilo de qué recurso está monitoreando y por qué.

usuario: >
  Analista financiero / contador del cliente. Power user del dominio (sabe
  qué es un asiento, una conciliación, un período contable). Casual de la
  UI — entra a configurar el Día 1, recibe alertas en su día a día. Trabaja
  en un Espacio de trabajo del cliente, con acceso a Fuentes y Tableros que
  ya conoce. No es ingeniero de datos.

outcome: >
  El analista llega a Anomalías y en menos de 3 clicks puede: (a) ver qué
  Recursos están con salud roja hoy, (b) abrir uno y entender el incidente
  activo sin leer el modal monstruo, (c) ajustar la config del Recurso
  (umbrales, ventana, notificaciones) sin perder el contexto del incidente
  que está viendo, (d) activar/desactivar monitoreo de un System KPI o
  crear un User KPI desde un chart, todo en la misma vista de Recurso.

donde_aporta_la_IA: sugiere_durante
  # Al abrir cualquier Recurso, el Agente IA sintetiza la hipótesis inicial
  # del estado actual (SynthesizeInitialHypothesis ya en prod). No reemplaza
  # al analista: le ahorra el primer minuto de "qué pasó aquí" con copy en
  # lenguaje del operador, no del scoring engine.

ubicacion_navegacional: N2 Op Center → Anomalías (N3 = vista de Recurso, N4 = tabs internas del Recurso)
```

---

## [ALCANCE]

```yaml
in_scope:
  - Sustitución del modelo "3 tabs (Incidents | Config | History)" por "Recurso-céntrico con hilo IA"
  - Nueva vista de Recurso (N3) con tabs internas: Resumen | Configuración | Incidentes | Histórico
  - Sidebar de Recursos como home del módulo (lista jerárquica: Favoritos / Monitoreados / No monitoreados)
  - Dot indicator de salud por Recurso (verde / amber / rojo / off)
  - Búsqueda Cmd+K friendly sobre la lista de Recursos, debounced
  - Reemplazo del modal AnomalyMonitoringConfig (3566 LOC) por tabs inline con autosave por sección
  - Toggle "Monitorear con System KPI" en la vista de Recurso (chart o fuente)
  - Flujo "+ Monitorear este chart" desde el chart detail → crea User KPI y aterriza en vista de Recurso
  - Hipótesis sintética del Agente IA en el header de la vista de Recurso (cuando hay incidente activo)
  - Lista de Incidentes como vista secundaria accesible en 1 click (sub-route /anomalies/incidents)
  - Breadcrumbs canónicos N2→N3→N4
  - Migración gradual con feature flag, paridad temporal entre vista vieja y nueva
  - Patrón AiChat canónico (botón → Sheet lateral) accesible desde la vista de Recurso

out_of_scope:
  - Cambios en el motor BADS / AMS / KPISs / Brain / AVA (backend intocable)
  - Nuevos tipos de detección (lo que detecta el sistema no cambia)
  - Nuevos canales de notificación más allá de Email + Slack ya soportados
  - Reglas de envío avanzadas (SWAT-563, va en otro epic)
  - SignalGroupingStrategy con LLM (SWAT-705, va en otro epic)
  - Notificaciones externas Slack/Email/Webhooks rediseñadas (DOE24 ya RFC Complete, no se toca acá)
  - Rediseño visual del chart de evidencia dentro del incidente (se reutiliza el actual)
  - Mobile breakpoint exhaustivo (out — Op Center se usa en desktop)

intocable:
  - URL params actuales (?chart_id=, :incidentId, :resourceId) — deben seguir funcionando
  - Contratos API existentes con AMS, KPISs, BADS
  - Zustand store oc_anomalies_sidebar_collapsed_v2 (la migración no rompe estado guardado)
  - Glosario Op Center v2.8 (Anomalía, Señal de anomalía, Incidente, Tablero, KPI, Agente IA, Fuente, Espacio de trabajo, Dataset, BADS)
  - Componentes desyk (no se inventa nada nuevo, se compone)

estados_requeridos:
  # Sidebar de Recursos
  - empty: el espacio de trabajo no tiene Recursos creados todavía (onboarding inline)
  - loading: primer fetch del catálogo de Recursos (skeleton, no spinner full screen)
  - con_datos: lista poblada con Favoritos + Monitoreados + No monitoreados
  - filtrando: usuario escribiendo en Cmd+K (debounced 400ms, mismo patrón que SystemKpiTab)
  - sin_resultados_busqueda: query no matchea ningún Recurso (mensaje + sugerencia)
  - sin_permisos: usuario read-only ve la lista pero no puede activar monitoreo (tooltip)
  - error_fetch: catálogo no carga (mensaje + acción de reintento)

  # Vista de Recurso
  - sin_seleccion: ningún Recurso abierto — estado inicial del módulo (CTA "elegí un Recurso")
  - cargando_recurso: skeleton de header + tabs
  - recurso_off: Recurso no monitoreado todavía (CTA "Activar monitoreo" como primary action)
  - recurso_monitoreado_sin_incidentes: tab Resumen con hipótesis IA "todo en orden" + actividad reciente
  - recurso_con_incidente_activo: tab Resumen con hipótesis IA del incidente + acceso directo a tab Incidentes
  - recurso_con_onboarding: primera vez activando monitoreo (tab Configuración guiada, no wizard modal)
  - recurso_read_only: usuario no puede editar config (tabs visibles, inputs disabled, badge "Solo lectura")
  - recurso_error_fetch: error cargando datos del Recurso (mensaje + reintento)

  # Configuración inline
  - autosave_idle: nada cambió, sin indicador
  - autosave_pending: usuario tipeando, indicador discreto "Guardando…"
  - autosave_success: cambio guardado, check fugaz al lado del campo
  - autosave_error: no se pudo guardar, badge inline + acción reintentar
  - validacion_local: campo inválido (umbral negativo, ventana 0), error inline
  - cambios_no_guardados_en_navegacion: usuario sale con cambios pending → confirm dialog

  # Hipótesis IA
  - generando: skeleton "El Agente IA está revisando este Recurso…"
  - lista: tarjeta de hipótesis con copy + acciones (Ver evidencia, Marcar como ruido)
  - sin_hipotesis: Recurso muy nuevo o sin señal, mensaje neutro
  - error: la hipótesis no pudo generarse (fallback: mostrar última señal sin síntesis)

  # Lista de Incidentes (vista secundaria)
  - tabla_con_datos | empty | filtrando | sin_resultados | error_fetch
```

---

## [SEÑALES DE CALIDAD]

```yaml
# Cada criterio responde sí/no binario. Si el QA Design no puede responder
# con sí/no, el criterio está mal escrito y debe reformularse.

navegacion:
  - El usuario llega a /operation-center/anomalies y ve la lista de Recursos como vista raíz (no la lista de Incidentes)
  - El breadcrumb muestra "Op Center › Anomalías › <Nombre del Recurso> › <Tab>" en N3 y N4
  - Cmd+K filtra la lista de Recursos por nombre, fuente y tablero asociado
  - Cada Recurso en la lista tiene un dot indicator de salud visible sin hover
  - La lista de Incidentes está accesible en máximo 1 click desde la vista raíz

arquitectura:
  - El modal AnomalyMonitoringConfig NO se abre en ningún flujo del nuevo diseño
  - Toda la configuración de un Recurso se edita inline en su tab Configuración
  - Cada sección de configuración (Schedule, Notifications, Thresholds) tiene autosave independiente
  - No hay nested tabs > 2 niveles (vista de Recurso → tab interna, pero NO tab dentro de tab)
  - El usuario nunca ve "system-${metricKey}" o strings concatenados como activeSection en URL

ia:
  - Al abrir un Recurso con incidente activo, la hipótesis del Agente IA está visible above-the-fold
  - El copy de la hipótesis usa términos del glosario (Anomalía, Señal, Incidente), no jerga del scoring engine
  - El usuario puede aceptar/rechazar la hipótesis en 1 click
  - El AiChat se abre desde botón en SidebarFooter como Sheet lateral, NO como burbuja flotante

system_kpi_vs_user_kpi:
  - Desde un chart, el botón "+ Monitorear este chart" crea un User KPI y aterriza al usuario en la vista de Recurso
  - El toggle "Activar System KPI" está visible en la vista de Recurso (tipo Fuente) cuando aplica
  - Visualmente se distingue Recurso tipo System KPI vs User KPI (badge + icono)

paridad_y_migracion:
  - Detrás de feature flag, el usuario puede alternar entre la vista vieja y la nueva
  - Ningún URL viejo rompe — todos los URLs existentes redirigen al equivalente nuevo
  - El estado guardado en Zustand (sidebar collapsed) se respeta en la vista nueva

estados:
  - Cada estado listado en [ALCANCE].estados_requeridos está diseñado e implementado
  - El estado read_only se distingue del estado normal por badge visible
  - El estado error_fetch siempre incluye acción de reintento

prohibiciones (bans absolutos):
  - No hay modal centrado en ningún flujo del módulo (excepto confirm dialogs de destrucción)
  - No hay AiChat flotante esquina inferior
  - No hay copy con em-dashes
  - No hay sparkle emoji en botones de IA
  - No hay "Powered by AI" badges
  - No hay gradient text
  - No hay doble scroll vertical anidado
```

---

## [REFERENCIA VISUAL]

```yaml
referencias:
  - https://linear.app             # patrón de Sidebar lista + Detail panel, dot indicators de salud, Cmd+K nativo
  - https://www.notion.so          # sidebar jerárquico con secciones colapsables (Favoritos / Espacios)
  - https://arc.net                # densidad cómoda, tipografía clara, sin decoración
  - https://claude.ai              # vista de "thread" como contenedor de actividad + agente IA inline
  - https://docs.datadoghq.com/monitors/  # Datadog monitor detail: header con estado + tabs (Settings / Events / Logs)
  - https://sentry.io              # Sentry issue detail: timeline + acciones rápidas + assignee, sin modal

tokens_a_usar:
  # Light mode consistente — no dark mode en este refactor
  colores:
    salud:
      verde:   --color-success-500    # Recurso saludable
      amber:   --color-warning-500    # Recurso con alerta menor / Recurso con configuración pendiente
      rojo:    --color-danger-500     # Recurso con incidente activo
      off:     --color-neutral-300    # Recurso no monitoreado (dot vacío)
    acento:
      primary: --color-primary-600    # única acción primaria por vista (CTA principal)
    superficie:
      page:    --color-neutral-50
      card:    --color-white
      hover:   --color-neutral-100
  tipografia:
    heading:   --font-display-md      # nombre del Recurso en header
    body:      --font-body-md
    mono:      --font-mono-sm         # IDs, umbrales numéricos
  spacing:
    section:   --space-6              # entre secciones de Configuración
    inline:    --space-2              # entre label e input
  radius:
    card:      --radius-md
    pill:      --radius-full          # badges de estado

componentes_desyk_a_usar:
  layout:
    - Sidebar          # lista de Recursos (N2 → N3)
    - SidebarFooter    # botón Agente IA (abre Sheet)
    - Breadcrumb       # N2 → N3 → N4
  contenedores:
    - Card             # tarjeta de hipótesis IA, agrupación de config
    - Sheet            # AiChat lateral, panel de detalle de Incidente desde lista
    - Tabs             # tabs internas de la vista de Recurso (Resumen | Config | Incidentes | Histórico)
  contenido:
    - Badge            # estado del Recurso, tipo (System/User), Solo lectura
    - Avatar           # owner del Recurso, agente IA
    - EmptyState       # sin_seleccion, sin_resultados_busqueda, recurso_off
    - Skeleton         # loading states
    - Toast            # autosave_success / autosave_error
  formulario:
    - Input            # umbrales, ventana
    - Select           # frequency, timezone
    - Switch           # activar/desactivar monitoreo, activar/desactivar System KPI
    - Button           # CTA primary (uno por vista)
  feedback:
    - InlineAlert      # validación local, cambios_no_guardados
    - AiChat           # patrón canónico Simetrik (botón → Sheet)

notas_visuales:
  - Densidad organizada estilo Linear: lista de Recursos con info-density alta pero respiración
  - Una sola acción primaria por vista (ej: en recurso_off, primary = "Activar monitoreo"; en recurso_con_incidente_activo, primary = "Resolver incidente")
  - Dot indicator de salud es el único elemento de color en la lista — el resto neutro
  - Header de la vista de Recurso es sticky con: breadcrumb + nombre + badges + acción primaria
  - Tarjeta de hipótesis IA tiene un acento sutil (border-left o icon, NO gradient text NO sparkle)
  - Autosave indicator es minúsculo, esquina del campo, nunca un toast grande
  - Tabs internas estilo "underline tabs" no "pill tabs" (jerarquía: pill = N2, underline = N3/N4)
```

---

## [STACK TÉCNICO]

```yaml
microfrontend: fe-solutions-mf

archivos_de_referencia:
  # Lo que existe y debe coexistir durante la migración:
  - src/oc/features/anomalies/pages/AnomaliesPage.tsx                          # 990 LOC — entry point, debe sobrevivir refactorizado
  - src/oc/features/anomalies/framework/routes/anomalies.tsx                   # 5 rutas — ampliar, no romper
  - src/oc/features/anomalies/components/AnomaliesToolbar/                     # los 3 mode tabs deben morir
  - src/oc/features/anomalies/components/AnomaliesSidebar/                     # ya refactorizado (SWAT-693, SWAT-912) — base del nuevo sidebar de Recursos
  - src/oc/features/anomalies/components/AnomalyCard.tsx                       # 155 LOC — adaptar como ResourceCard
  - src/oc/features/anomalies/components/SystemKpiTab/SystemKpiTab.tsx         # 101 LOC — patrón de búsqueda debounced 400ms, reusar
  - src/oc/features/anomalies/components/SystemKpiTab/SystemKpiSourceDetail.tsx # base de la vista de Recurso tipo Fuente

  # Lo que debe morir (gradualmente):
  - src/oc/features/anomalies/components/AnomalyMonitoringConfig/AnomalyMonitoringConfig.tsx   # 3566 LOC — el modal monstruo
  - src/oc/features/anomalies/components/AnomalyMonitoringConfig/SystemKpiDetailView.tsx       # 2416 LOC — duplicación de thresholds
  - src/oc/features/anomalies/components/AnomalyMonitoringConfig/AiCollectingLoader.tsx        # se reemplaza por Skeleton + patrón "hipótesis IA"
  - SolutionsDialogNavigation pattern dentro del módulo                                         # mata el sidebar stepper modal

notas_de_integracion:
  feature_flag:
    nombre_tentativo: oc_anomalies_resource_centric_v1
    estrategia: >
      Flag por usuario/workspace. Con flag OFF se ve la vista actual (3 mode tabs).
      Con flag ON se ve la nueva vista de Recurso. Durante la migración ambas
      coexisten en el mismo build.

  paridad_temporal:
    - Ambas vistas escriben/leen el mismo backend (AMS, KPISs, BADS) — no hay
      migración de datos
    - Los URLs viejos siguen funcionando: el handler de rutas detecta flag ON
      y redirige a la estructura nueva preservando params
    - El sidebar collapsed state (Zustand oc_anomalies_sidebar_collapsed_v2) se
      respeta en ambas vistas

  rutas_nuevas:
    - /operation-center/anomalies                       # raíz = lista de Recursos (vista nueva) | lista de Incidentes (vista vieja)
    - /operation-center/anomalies/resources             # mismo destino que raíz (alias)
    - /operation-center/anomalies/resources/:resourceId           # vista de Recurso, tab default "resumen"
    - /operation-center/anomalies/resources/:resourceId/config    # tab Configuración
    - /operation-center/anomalies/resources/:resourceId/incidents # tab Incidentes (lista filtrada por Recurso)
    - /operation-center/anomalies/resources/:resourceId/history   # tab Histórico
    - /operation-center/anomalies/incidents             # lista de Incidentes global (vista secundaria)
    - /operation-center/anomalies/incidents/:incidentId           # incidente específico (abre como Sheet sobre lista, NO modal)

  restricciones:
    - NO se inventa componente desyk nuevo — todo se compone con los existentes
    - Backend NO cambia (DOE16/17/18/24 mantienen sus contratos)
    - El monolito AnomalyMonitoringConfig debe morir por sustitución gradual, no eliminación abrupta
    - Durante la coexistencia, el código nuevo vive en src/oc/features/anomalies/v2/ (sub-carpeta) hasta cleanup final
```

---

## [SLICING]

```yaml
# Cada slice = entregable shippable en producción detrás de feature flag.
# Mantiene paridad funcional con la vista actual. Linear sub-issues sugeridos.

slice_1_foundation:
  titulo: "Foundation — feature flag + ruteo + sidebar de Recursos"
  scope:
    - Crear feature flag oc_anomalies_resource_centric_v1
    - Estructura de carpeta src/oc/features/anomalies/v2/
    - Sidebar de Recursos (lista jerárquica: Favoritos / Monitoreados / No monitoreados)
    - Dot indicator de salud por Recurso
    - Búsqueda Cmd+K debounced 400ms
    - Rutas nuevas con redirect-preservando-params desde URLs viejos
    - Estado sin_seleccion (vista raíz cuando no hay :resourceId)
  shippable: >
    Con flag ON, el usuario ve la nueva home pero al elegir un Recurso aterriza
    todavía en el modal viejo. Útil para validar IA de descubrimiento sin tocar config.
  sub_issues_estimados: 2

slice_2_resource_view_readonly:
  titulo: "Vista de Recurso read-only — tabs internas + hipótesis IA"
  scope:
    - Layout de N3 (header sticky + Breadcrumb + Tabs internas)
    - Tab Resumen con tarjeta de hipótesis IA (consume SynthesizeInitialHypothesis)
    - Tab Incidentes (lista filtrada por Recurso)
    - Tab Histórico (read-only)
    - Estados recurso_monitoreado_sin_incidentes / recurso_con_incidente_activo / recurso_read_only
    - Sheet de Incidente al abrir desde lista (NO modal)
  shippable: >
    Con flag ON, el usuario puede navegar y entender el estado de un Recurso
    sin tocar config. La config sigue abriendo el modal viejo desde tab "Configuración".
  sub_issues_estimados: 3

slice_3_inline_config_schedule_notifications:
  titulo: "Configuración inline — Schedule + Notifications con autosave"
  scope:
    - Tab Configuración con secciones (Schedule, Notifications)
    - Autosave por sección (idle / pending / success / error)
    - Validación local inline
    - Confirm dialog de cambios_no_guardados al navegar fuera
  shippable: >
    Con flag ON, dos secciones de la config (Schedule + Notifications) viven
    inline. Thresholds sigue abriendo el modal viejo embebido. Coexistencia.
  sub_issues_estimados: 2

slice_4_inline_config_thresholds:
  titulo: "Configuración inline — Thresholds (Series N) + onboarding del Recurso"
  scope:
    - Sección Thresholds inline (reemplazo final de AnomalyMonitoringConfig)
    - Estado recurso_off → CTA "Activar monitoreo" (primary action)
    - Estado recurso_con_onboarding (primera vez activando)
    - Eliminación del último entry point al modal AnomalyMonitoringConfig
  shippable: >
    El modal AnomalyMonitoringConfig deja de abrirse en cualquier flujo con
    flag ON. Slice más sensible — review extra de paridad funcional.
  sub_issues_estimados: 3

slice_5_user_kpi_creation_flow:
  titulo: "Flujo + Monitorear este chart → User KPI en vista de Recurso"
  scope:
    - Botón "+ Monitorear este chart" en chart detail (fuera del módulo Anomalías)
    - Crea User KPI y redirige a /anomalies/resources/:resourceId con onboarding
    - Toggle "Activar System KPI" en vista de Recurso tipo Fuente
    - Badges visuales User vs System
  shippable: >
    Cierra el loop de creación. El usuario tiene un flujo end-to-end de
    descubrimiento → configuración → monitoreo sin tocar el modal viejo.
  sub_issues_estimados: 2

slice_6_cleanup_y_default_on:
  titulo: "Cleanup — flag default ON + eliminación de código legacy"
  scope:
    - Feature flag default ON para todos los usuarios
    - Eliminación de AnomalyMonitoringConfig.tsx (3566 LOC) y co-ubicados
    - Eliminación de AnomaliesToolbar (los 3 mode tabs)
    - Eliminación de la carpeta src/oc/features/anomalies/v2/ (promoción a raíz)
    - QA de regresión completo
  shippable: >
    El módulo viejo deja de existir. -6KLOC en el repo. Telemetría de adopción
    confirma que nadie depende ya del flag OFF.
  sub_issues_estimados: 2

dependencias:
  - slice_2 depende de slice_1 (necesita rutas y sidebar)
  - slice_3 depende de slice_2 (necesita el contenedor de tabs)
  - slice_4 depende de slice_3 (autosave pattern compartido)
  - slice_5 puede hacerse en paralelo a slice_3/4 (toca otra superficie)
  - slice_6 depende de TODOS los anteriores

estimacion_total: 6 slices, ~14 sub-issues, 4-6 semanas con un FE + UX Designer
```

---

## [INFORMACION_FALTANTE]

```yaml
# Gaps detectados que el LEAD debería resolver antes (o durante) el prototype.

bloqueantes:
  - id: gap-01
    tema: contrato_hipotesis_IA
    descripcion: >
      No tengo el schema exacto de respuesta de SynthesizeInitialHypothesis.
      ¿Devuelve título + texto + acciones? ¿Devuelve confidence score? ¿Lista
      de evidencias citadas? Necesario para diseñar la tarjeta con precisión.
    fuente_sugerida: codigo (buscar SynthesizeInitialHypothesis en repo BE) o brain (DOE16)
    bloqueante: true

  - id: gap-02
    tema: definicion_de_Recurso
    descripcion: >
      ¿Un Recurso es siempre chart-o-fuente? ¿Un Tablero puede ser Recurso?
      ¿Un Dataset es Recurso o solo se monitorean sus charts? Esto define
      la jerarquía del sidebar y el badge de tipo.
    fuente_sugerida: brain (Definicion - Anomalias.md, casos de uso 1-21)
    bloqueante: true

no_bloqueantes:
  - id: gap-03
    tema: feature_flag_existente
    descripcion: >
      ¿Existe ya el sistema de feature flags en fe-solutions-mf o hay que
      crearlo? El nombre tentativo es propuesta — confirmar convención.
    fuente_sugerida: codigo (buscar useFeatureFlag, LaunchDarkly, etc.)
    bloqueante: false

  - id: gap-04
    tema: telemetria_de_adopcion
    descripcion: >
      Para slice_6 (default ON), necesitamos definir qué evento de telemetría
      mide adopción de la vista nueva. ¿Existe ya pipeline de eventos?
    fuente_sugerida: brain (operation-center/telemetria) o codigo
    bloqueante: false

  - id: gap-05
    tema: comportamiento_de_Favoritos
    descripcion: >
      La sección "Favoritos" del sidebar — ¿es manual (estrella por usuario)
      o algorítmica (más visitados)? ¿Existe ya el concepto en el producto?
    fuente_sugerida: brain o granola (entrevistas con analistas)
    bloqueante: false

  - id: gap-06
    tema: read_only_permisos
    descripcion: >
      ¿Existe rol "viewer" en el Op Center hoy o este refactor lo introduce?
      Afecta diseño del badge "Solo lectura" y comportamiento de inputs.
    fuente_sugerida: brain (RBAC en operation-center)
    bloqueante: false

  - id: gap-07
    tema: mobile_breakpoint
    descripcion: >
      Confirmado out-of-scope, pero validar con humano que ningún usuario
      analista opera Op Center desde tablet. Si sí, repensar slice 6.
    fuente_sugerida: granola o humano directo
    bloqueante: false
```

---

> Hasta acá el Brief canónico. El bloque `[COPY Y TONO]` lo llena el UX Writer en paralelo.

---

## Estructura detallada — Patrón C Recurso-céntrico

> Esta sección no es parte del Brief canónico, es el "shape" del prototype que el LEAD pidió. Sirve como spec accionable para el Front Designer (o quien maquetee el HTML prototype).

### 1. Anatomía de la vista de Recurso

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│ [Sidebar Recursos]   │ [Header Recurso — sticky]                                  │
│  ─ Búsqueda Cmd+K    │  Breadcrumb: Op Center › Anomalías › <Recurso> › <Tab>     │
│  ─ Favoritos (3)     │  ─────────────────────────────────────────────────────     │
│    ● Cobros Diarios  │  ●  Nombre del Recurso              [Badge: User KPI]      │
│    ● Conciliación P  │      <subtitle: Fuente · Tablero asociado>                 │
│    ○ Asientos Q4     │                              [Primary Action según estado] │
│  ─ Monitoreados (12) │                                                            │
│    ● Recurso A       │  ┌─ Tabs underline ──────────────────────────────────┐    │
│    ● Recurso B  ⚠    │  │ Resumen │ Configuración │ Incidentes │ Histórico  │    │
│    ● Recurso C  ●    │  └────────────────────────────────────────────────────┘   │
│  ─ No monitoreados   │                                                            │
│    ○ Recurso D       │  [Content Area — tab activo]                              │
│    ○ Recurso E       │                                                            │
│                      │  (Resumen) → Card hipótesis IA + actividad reciente       │
│                      │  (Configuración) → Secciones con autosave inline          │
│                      │  (Incidentes) → Lista filtrada por este Recurso           │
│                      │  (Histórico) → Read-only, eventos pasados                 │
│                      │                                                            │
│ [SidebarFooter]      │                                                            │
│  ▸ Agente IA  [→]    │                                                            │
└───────────────────────────────────────────────────────────────────────────────────┘
```

**Zonas y componentes desyk:**

| Zona | Componente desyk | Notas |
|---|---|---|
| Sidebar de Recursos (N2→N3) | `Sidebar` + secciones colapsables | Patrón canónico Simetrik N2/N3. Sticky a la izquierda, ancho fijo (256px expandido, 56px colapsado). |
| Búsqueda Cmd+K | `Input` con icono + atajo de teclado | Debounced 400ms (reutilizar patrón de `SystemKpiTab`). |
| Footer del sidebar | `SidebarFooter` con botón Agente IA | Click → abre `Sheet` lateral con el AiChat. NUNCA flotante. |
| Header del Recurso | Composición (`Breadcrumb` + heading + `Badge` + `Button`) | Sticky top. Una sola acción primaria visible según estado. |
| Tabs internas | `Tabs` estilo underline | 4 tabs fijas. NO sub-tabs. Si una tab necesita sub-navegación, se resuelve con secciones scrolleables. |
| Content area | Composición (`Card`, `EmptyState`, `Skeleton`, formularios) | Scroll vertical único. NO doble scroll. |
| Detalle de Incidente | `Sheet` lateral sobre la tab Incidentes | Click en fila de la lista → Sheet desde la derecha (no modal centrado). |
| Confirm dialogs | `Dialog` (única excepción al ban modal) | Solo para confirmaciones destructivas (descartar cambios). |

**Leyes desyk aplicadas:**
- Light mode consistente, sin dark mode opcional.
- Una acción primaria por vista (en header, según estado del Recurso).
- Color principal = atención dirigida (dot indicators y CTA primary, nada más).
- Densidad organizada — referente Linear, Notion.

---

### 2. Hilo IA — la hipótesis sintética al abrir un Recurso

**Comportamiento:**
- Al abrir cualquier Recurso, el tab Resumen muestra arriba una `Card` con la hipótesis del Agente IA.
- Consume el endpoint que hoy alimenta `SynthesizeInitialHypothesis` (DOE16, ya en prod).
- La hipótesis es proactiva: el agente "sugiere durante" el flujo natural del operador, no espera a que el usuario pregunte.

**Anatomía de la tarjeta de hipótesis (ASCII):**

```
┌────────────────────────────────────────────────────────────────────┐
│ ◐ Agente IA · hace 2 min                                  [···]    │
│                                                                    │
│  Se detectaron 3 Señales de anomalía en Cobros Diarios entre el    │
│  20 y el 23 de mayo. El patrón sugiere un atraso en la ingestión   │
│  de la Fuente "Banco XYZ", no una caída real de cobros.            │
│                                                                    │
│  Evidencia:                                                         │
│  · Señal #1284 — gap de 6h en la Fuente Banco XYZ                  │
│  · Señal #1285 — recuperación parcial al día siguiente             │
│  · Señal #1286 — patrón se repite en períodos anteriores           │
│                                                                    │
│  [ Ver Incidente completo ]   [ Marcar como ruido ]                │
└────────────────────────────────────────────────────────────────────┘
```

**Reglas de copy (input para el UX Writer):**
- Lenguaje del operador: "Señales", "Fuente", "Cobros", "ingestión". NO "scoring", "anomaly score", "z-score", "outlier detection".
- Sin sparkles, sin "Powered by AI", sin gradient text.
- Sin em-dashes en el copy. Usar comas, dos puntos, paréntesis.
- Tono: informar + sugerir. NO afirma ("hay un problema") — hipotetiza ("el patrón sugiere").
- Marcador visual de IA: icono `◐` o avatar pequeño + label "Agente IA · hace N min". Eso es todo. No badge "AI", no halo de color.

**Estados de la tarjeta:**
- `generando` → Skeleton + texto "El Agente IA está revisando este Recurso…"
- `lista` → Hipótesis completa con acciones
- `sin_hipotesis` → Card neutra "Sin hallazgos relevantes. Última revisión hace N min."
- `error` → Fallback: mostrar última Señal sin síntesis, con mensaje "El Agente IA no pudo generar una hipótesis. Mostramos los datos directos."

**Acciones disponibles:**
- `Ver Incidente completo` → navega a tab Incidentes con incidente seleccionado.
- `Marcar como ruido` → feedback al modelo (alimenta DOE16 v2). Hace que la hipótesis colapse a un mensaje neutro.
- `[···]` overflow → "Regenerar hipótesis", "Reportar problema con esta hipótesis".

---

### 3. Flujo de configuración inline — la muerte del modal monstruo

**Antes** (lo que se reemplaza):
- `AnomalyMonitoringConfig.tsx` (3566 LOC) abre Dialog modal con `SolutionsDialogNavigation` (sidebar stepper) + secciones Schedule, Notifications, Series N.
- Submit gigante al final, riesgo de perder cambios al cerrar.

**Después** (tab Configuración del Recurso):

```
┌─ Tab Configuración (scroll vertical) ─────────────────────────────┐
│                                                                    │
│ ── Schedule ──────────────────────────── [Guardando…]              │
│   Frecuencia:  [Diario ▾]                                          │
│   Horario:     [09:00 ▾]   Zona: [America/Bogota ▾]                │
│   Ventana:     [Últimos 7 días ▾]                                  │
│                                                                    │
│ ── Notificaciones ────────────────────────── [✓ Guardado]          │
│   Email:       [✓] alertas@empresa.com  [+ Agregar]                │
│   Slack:       [✓] #ops-anomalias       [Configurar canal]         │
│                                                                    │
│ ── Umbrales (Series) ──────────────────────                        │
│   Serie 1 (Cobros COP):                                            │
│     Mín: [10.000]   Máx: [50.000]                                  │
│     Acción al violar: [Crear Incidente ▾]                          │
│                                                                    │
│   [+ Agregar otra serie]                                           │
│                                                                    │
│ ── Zona peligrosa ────────────────────────                         │
│   [ Desactivar monitoreo de este Recurso ]                         │
└────────────────────────────────────────────────────────────────────┘
```

**Comportamiento de autosave:**
- Cada sección tiene su propio ciclo de autosave (debounced 800ms desde último cambio).
- Indicador inline al lado del título de la sección: `Guardando…` → `✓ Guardado` (check fugaz, 2s).
- Error de guardado → `InlineAlert` con acción "Reintentar".
- NUNCA un botón "Guardar todo" al final. NUNCA un submit gigante.
- Si el usuario navega fuera con cambios pending → `Dialog` de confirmación "Tienes cambios sin guardar. ¿Salir igualmente?".

**Validación local:**
- Umbral negativo, ventana 0, frecuencia inválida → error inline debajo del campo.
- No bloquea el resto de la sección, solo invalida ese campo.

**Onboarding (primera vez activando monitoreo en un Recurso):**
- Estado `recurso_off` muestra `EmptyState` con CTA primary "Activar monitoreo".
- Al activar → `recurso_con_onboarding`: la tab Configuración muestra valores sugeridos por el Agente IA con copy guía ("Sugerencias basadas en datos históricos. Podés ajustar después.").
- NO wizard modal. Es la misma vista, con valores pre-llenados y un tooltip discreto.

---

### 4. User KPI vs System KPI — diferenciación visual y flujos

**Diferenciación visual:**

| Elemento | Recurso tipo System KPI | Recurso tipo User KPI |
|---|---|---|
| Badge en header | `Badge` outline "System KPI" | `Badge` solid "User KPI" |
| Icono en sidebar | `◇` (diamond outline) | `●` (filled dot) |
| Origen visible en subtitle | "Detectado por BADS" | "Creado por <Usuario> · <fecha>" |
| Toggle "Activar System KPI" | Visible y editable | No aplica (oculto) |
| Sección "Crear desde…" | No aplica | Visible (chart de origen linkeado) |

**Toggle "Activar/Desactivar System KPI"** (item 1 del roadmap):
- Ubicación: tab Configuración → sección Schedule → primera fila.
- Componente: `Switch` con label "System KPI activo".
- Estado ON: BADS evalúa este Recurso según sus reglas estándar.
- Estado OFF: BADS deja de generar Señales para este Recurso. Las existentes quedan en histórico.

**Flujo "+ Monitorear este chart" (creación de User KPI):**
1. Usuario está en un chart detail (fuera del módulo Anomalías, en Tableros u Op Center).
2. Ve un botón "+ Monitorear este chart" (primary, una sola vez).
3. Click → backend crea Recurso tipo User KPI con defaults sugeridos por IA.
4. Redirect a `/operation-center/anomalies/resources/:resourceId` con estado `recurso_con_onboarding`.
5. Tab Configuración pre-llena con valores sugeridos. Usuario ajusta y los autosave guarda.
6. Usuario sale → el Recurso queda monitoreado, aparece en sidebar bajo "Monitoreados".

---

### 5. Sidebar de Recursos — estructura jerárquica

```
┌─ Sidebar Recursos ─────────────────────────┐
│                                            │
│ 🔍 Buscar Recursos…       [⌘K]             │
│                                            │
│ ▾ Favoritos (3)                            │
│   ● Cobros Diarios            [User]       │
│   ● Conciliación Período Q2   [System]     │
│   ⚠ Asientos Cierre Mes       [User]       │
│                                            │
│ ▾ Monitoreados (12)                        │
│   ● Recurso A                              │
│   ● Recurso B            ⚠ 2 incidentes    │
│   ● Recurso C            ● 1 incidente     │
│   ● Recurso D                              │
│   …                                        │
│                                            │
│ ▾ No monitoreados (47)                     │
│   ○ Fuente Banco XYZ                       │
│   ○ Fuente Pasarela ABC                    │
│   ○ Tablero Cobros Mensual                 │
│   …                                        │
│                                            │
├────────────────────────────────────────────┤
│ ▸ Agente IA                          [→]   │
└────────────────────────────────────────────┘
```

**Reglas:**
- 3 secciones colapsables: Favoritos · Monitoreados · No monitoreados (en ese orden).
- Cada Recurso = una fila con: dot indicator (color de salud) + nombre + meta opcional (badge tipo, contador de incidentes).
- Dot indicator colors:
  - **Verde** (`--color-success-500`): saludable, sin Señales abiertas.
  - **Amber** (`--color-warning-500`): config pendiente o Señal menor.
  - **Rojo** (`--color-danger-500`): Incidente activo.
  - **Off** (`--color-neutral-300`, vacío): no monitoreado.
- Búsqueda Cmd+K filtra en tiempo real con debounce 400ms. Match en nombre, fuente asociada, tablero asociado.
- Sin resultados → `EmptyState` corto con sugerencia.
- Sidebar collapsible (Zustand `oc_anomalies_sidebar_collapsed_v2` ya existente, respetar).

---

### 6. Lista de Incidentes — vista secundaria, 1 click

**Acceso:**
- Botón secundario en el header del módulo (al lado del título "Anomalías"): "Ver todos los Incidentes" → ruta `/anomalies/incidents`.
- Atajo en el `EmptyState` de `sin_seleccion`: "¿Buscás un Incidente específico? Ver lista de Incidentes".

**Vista:**
- Tabla con columnas: Estado · Recurso afectado · Fecha apertura · Severidad · Asignado · Acciones.
- Filtros canónicos: estado (Open / Resolved / Dismissed / Postponed), severidad, fecha, Recurso.
- Click en fila → abre `Sheet` lateral con detalle del Incidente. NUNCA modal centrado.
- Desde el Sheet, el botón "Abrir Recurso" navega a la vista de Recurso correspondiente (cierra el Sheet).

**Por qué vista secundaria y no home:**
- La home es "qué Recursos están en problemas hoy" (Recurso-céntrica).
- La lista de Incidentes es la "lente Actividad" del híbrido — útil cuando el usuario sabe que algo pasó pero no recuerda el Recurso.

---

### 7. Anti-patrones a evitar — bans absolutos en este refactor

Prohibido explícitamente:

- **Modal monstruo** — la config NUNCA se abre en Dialog. Vive inline en el tab Configuración.
- **Doble scroll** — un solo scroll vertical en el content area. Si una sección necesita más espacio, se rediseña, no se anida un scroll.
- **Breadcrumbs ausentes** — TODA vista N3 y N4 muestra breadcrumb.
- **Sub-tabs dentro de tabs** — máximo 1 nivel de tabs internas. Si hace falta más, se usa scroll + anchor links.
- **AiChat flotante esquina inferior** — patrón canónico Simetrik: botón en SidebarFooter → Sheet lateral.
- **Sparkles ✨ en botones de IA** — el agente se identifica con avatar o icono geométrico, no con emoji decorativo.
- **"Powered by AI" badges** — la IA es invisible cuando funciona, identificable cuando habla, nunca un sticker de marketing.
- **Gradient text** (`background-clip: text` + gradient) — copy en color sólido del token correspondiente.
- **Em-dashes** (`—`) en copy — usar comas, dos puntos, paréntesis.
- **Submit gigante** — autosave por sección, sin botón "Guardar todo".
- **Spinner full-screen** — usar `Skeleton` por componente.
- **Toast para autosave** — indicador inline al lado del título de la sección, no toast bottom-right.
- **Colores fuera de tokens desyk** — todos los colores vienen de los tokens, sin hex hardcoded.
- **Dark mode opcional** — light mode consistente en todo el refactor.
- **Hero metric template SaaS** — la home es lista de Recursos, no un dashboard de KPIs grandotes.
- **Grids idénticos de cards** (icon + heading + descripción repetidos) — la jerarquía visual se construye con el dot indicator y la tipografía, no con cards-templates.

---

_Fin del Brief + estructura. Listo para feedback del LEAD o spawn del Front Designer / UX Writer._
