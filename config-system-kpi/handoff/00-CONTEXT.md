# 00 · Contexto compartido — Monitoreo de Ingesta

## Glosario

| Correcto | Banned | Notas |
|---|---|---|
| Fuente | dataset (en conciliación), origen | Entidad principal monitoreada |
| Anomalía | desviación genérica | Detección que el sistema dispara |
| Señal de anomalía | alerta, alerta atómica | Atómico, evento de detección |
| Incidente | ticket, alerta agrupada | Agrupador de señales |
| Tablero | dashboard | Vista de KPIs del cliente |
| Espacio de trabajo | workspace | Contenedor multi-tenant |
| Conciliación | reconciliación | Proceso de cruce de datos |
| Dataset | tabla de datos, set de datos | **Solo en Op Center** sí es oficial |
| KPI | métrica genérica | Indicador monitoreado |
| Monitoreo | monitor (verbo en inglés), monitorear excesivo | Sustantivo o verbo según contexto |

Idioma: **español neutro**. No usar slang regional. No usar em-dashes (`—`), usar
comas, dos puntos, paréntesis o puntos. No usar tildes incorrectamente.

## Estados del monitoreo (BADS lifecycle)

El monitoreo de una fuente se deriva de la agregación de KPIs de BADS. En el UI
se exponen **3 estados** (de los 6 internos del BE):

| Estado UI          | Origen BADS                                                 | Cuándo aplica                          | Visual                                             |
| ------------------ | ----------------------------------------------------------- | -------------------------------------- | -------------------------------------------------- |
| **Sin configurar** | No hay KPIs registrados (`resources[i].status === 'empty'`) | Fuente nueva, sin monitor activado     | Badge gris, dot muted                              |
| **Aprendiendo**    | KPIs en `COLLECTING` (baseline no listo)                    | Activado pero sin historial suficiente | Badge **info azul**, dot `hsl(var(--info))`        |
| **Monitoreado**    | Todos los KPIs en `READY` (baseline completo)               | Healthy, scoring activo                | Badge **success verde**, dot `hsl(var(--success))` |

**Estados internos BADS (referencia)** — `src/bads/models/kpi.py:28`:
- `REGISTERED` → `COLLECTING` → `READY`
- Branches: `ERROR`, `RECOMPUTING`, `DEREGISTERED` (no expuestos en UI por ahora)

**Wrapper op-center**: `AnomalyMonitoringConfig.is_active` + `deactivation_reason`
(`dataset_query_changed`, `chart_config_changed`, `bads_sync_failed`, `manual`).

## Modelo de configuración del monitor (3 perfiles)

| Perfil | `monitorMode` | `useGroupsAll` | Descripción |
|---|---|---|---|
| **Low** | `'igual'` | `false` | Configuración única aplicada a todos los días. Candado cerrado en el tab switcher. |
| **Family** | `'por-dia'` | `false` | Cada día tiene su propia configuración. Candado abierto. |
| **High** | `'por-dia'` | `true` | Monitoreo por grupos de archivos (patrón detectado por BADS). |

**Transiciones**:
- Low → Family: cambiar dropdown `Monitorear`, o editar un input, o apagar el toggle del día → dispara `dsPromoteToFamily(reason)` con banner de retroalimentación.
- Family → High: click `Monitorear grupos` en el banner del día → `dsActivateGroups()` (loader 1.4s, se siembran grupos en todos los días).

## Tipos de ingesta (de la fuente)

8 valores oficiales:
- `Manual`, `Simetrik`, `SFTP Push`, `SFTP Pull`, `S3 Pull`, `Distribución`, `Parseo`, `JAAS`

Helper UI: `ingestionTypeFor(r)` devuelve uno determinístico por id.

## Convenciones visuales

### Contenedores
- Cards (`ds-card`, `ds-indicator`, `ds-notes`, `ds-day-toggle`): **padding 16, radius 12, gap 24** column.
- Sub-cards (`tm-chart-card` para fuentes): padding 14, radius 12, gap 12.

### Modales
- Daysetup, bulk-activate, AI analysis, activation loader: **768 × 740**, max-width 96vw, max-height 94vh.
- Border-radius 12-16 según contexto. Padding 24.

### Badges
- Convención fija: `display: flex, height 24, padding 2×10, gap 4, flex-shrink 0, border-radius 9999px`.
- Color del fondo según semantic: muted (gris), success (verde), info (azul), warning (ámbar), destructive (rojo), AI purple para chips de agente.

### Tipografía
- Title 16/600/24 — secciones principales (Ventana de tiempo, Comportamiento de la fuente).
- Sub 12/400/16 — descripciones, muted-foreground.
- Body 14/400/20 — inputs, labels.
- Label 14/500 line-height 1 — labels de campos.

### Tokens de color (desyk)
- `hsl(var(--foreground))` = `#18181b`
- `hsl(var(--muted-foreground))` = `#71717a`
- `hsl(var(--border))` = `#e4e4e7`
- `hsl(var(--muted))` = `#f4f4f5`
- `hsl(var(--primary))` violeta Simetrik
- `hsl(var(--ai-purple))` = `#b638ff` (acento AI)
- `hsl(var(--info))` = `#2563eb`
- `hsl(var(--success))` verde
- `hsl(var(--warning))` ámbar
- `hsl(var(--destructive))` rojo

### Motion
- 120ms / 200ms / 320ms ease-out.
- Microinteracciones **pedagógicas** (especialmente cuando opera la IA): explican qué pasa.
- Pulse rings y dot pulses para AI thinking.

## Estado global Alpine relevante

| Variable | Tipo | Notas |
|---|---|---|
| `selectedConfigSource` | Object | Fuente activa en el modal. `null` = modal cerrado. |
| `daySetup` | Object | Estado del modal de configuración (ver doc 05). |
| `daySetupReadonly` | Boolean | `true` cuando vemos detalle de un monitor configurado (no editable). |
| `bulkActivateOpen` | Boolean | Modal bulk visible. |
| `bulkActivateStage` | 1\|2\|3 | Etapa actual del bulk. |
| `activationLoaderOpen` | Boolean | Loader pre-daysetup. |
| `aiAnalysisOpen` | Boolean | Modal "Resultados de análisis". |
| `tmTab` | String | Tab activo: `'ingesta'`, `'calidad'`, `'conciliacion'`, `'metricas'`. |

## Helpers JS clave

| Helper | Devuelve |
|---|---|
| `monitoringStateFor(r)` | `'unconfigured' \| 'learning' \| 'monitored'` |
| `monitoringStateLabel(state)` | Label en español |
| `ingestionTypeFor(r)` | Uno de los 8 tipos de ingesta |
| `workspaceFor(r)` | Workspace sin sufijo de país (`· BO` etc.) |
| `daySetupHasConfig` (getter) | `true` si la fuente ya tiene `dayConfig` |
| `dsActiveSimple()` | Devuelve `daySetup.shared` (Low) o `day.simple` (Family) |
| `dsActiveDay()` | Día activo del switcher |

## Referencias backend
- BADS: `~/Simetrik/bads/src/bads/models/`
- Op-center: `~/Simetrik/op-center-backend/apps/anomaly_configs/`
- Lifecycle KPI: `src/bads/models/kpi.py:28`
- Estados de incidente: `src/bads/models/workflows.py:127`
