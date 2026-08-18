> # ⛔ DOCUMENTO DESCARTADO
>
> **D10 se revirtió el 2026-08-14: las carpetas son solo de Tableros.** Este benchmark
> (T1–T6) comparaba los cuatro paneles del OC para diseñar el sistema transversal.
>
> Se conserva como registro. **Lo único que sobrevive y sigue siendo útil es el patrón de
> panel (D11, los 9 slots)**: describe la anatomía real del panel de Tableros y dónde entra
> el slot 7, que es lo que agrega este feature.
>
> **No usar como fuente para implementar.** Ver [`01-decisiones.md`](01-decisiones.md) § D10.

# Benchmark — organización transversal a varias entidades

**Fecha:** 2026-08-04
**Pregunta de fondo:** cuando un producto tiene que organizar **varios tipos de contenido** (tableros, datasets, alertas, eventos), ¿usa un solo namespace de carpetas o uno por tipo? ¿Y qué hace con las cosas que **llegan solas**?
**Complementa:** [`01-benchmark.md`](01-benchmark.md) (interacción, I1–I6) · [`06-organizacion-transversal.md`](06-organizacion-transversal.md) (el modelo elegido)

---

## Resumen: el modelo elegido tiene precedente directo

| # | Pregunta | Respuesta del benchmark |
|---|----------|------------------------|
| **T1** | ¿Un namespace de carpetas para todos los tipos, o uno por tipo? | **Uno solo.** Grafana, Metabase y Power BI usan un contenedor único que aloja varios tipos. Nadie mantiene namespaces paralelos por tipo. |
| **T2** | ¿Cómo se muestra una carpeta con tipos distintos? | **Tabs por tipo** dentro de la carpeta (Grafana: *Dashboards / Panels / Alert rules*) o **lista mixta con icono por tipo** (Metabase). |
| **T3** | ¿Y las cosas que llegan solas (alertas, eventos)? | Tres respuestas distintas — **es la pregunta interesante**. Ver §3. |
| **T4** | ¿Cómo se llama el concepto? | Folder (Grafana) · Collection (Metabase) · Workspace (Power BI) · Tag (Datadog). |
| **T5** | ¿Membresía exclusiva o múltiple? | **Exclusiva** donde hay carpetas (Metabase: *"only in one collection at a time"*); múltiple solo donde el mecanismo es tags (Datadog). |
| **T6** | ¿Los permisos viven en la carpeta? | Sí en Grafana y Metabase, y **heredan hacia abajo** a todos los tipos por igual. |

**Conclusión:** la decisión de D10 —una tabla `folders` compartida, cada vista mostrando lo suyo— **es el patrón dominante**, no una invención. Y Grafana es el precedente más cercano porque resuelve exactamente el caso que abrió el feedback: **carpetas que contienen tableros y reglas de alerta**.

---

## 1. Grafana — el precedente más cercano

Grafana mete en la misma carpeta **dashboards y reglas de alerta**, y la carpeta se navega **con tabs por tipo**:

> *"When you assign permissions to a folder, those permissions apply to all resources within that folder, including dashboards, alert rules, SLOs, and more."*
>
> *"It doesn't matter which tab you're on (**Dashboards, Panels, or Alert rules**); the folder permission you set applies to all."*
> — [Grafana docs · Manage access using folders](https://grafana.com/docs/grafana/latest/alerting/set-up/configure-rbac/access-folders/)

**Lo que valida:**

1. **Un solo namespace de carpetas** para tipos distintos (T1).
2. **Tabs por tipo dentro de la carpeta** (T2) — que en nuestro caso ya existen: el panel del OC tiene tabs Tableros | Datasets, y las vistas de Anomalías y Pendientes son secciones propias. **La estructura de navegación ya está.**
3. Los permisos se administran en la carpeta y bajan a todo (T6).

**El matiz importante:** en Grafana **la regla de alerta se declara en la carpeta** — se crea *dentro* de ella. La regla es **configuración**; lo que la regla dispara (el firing) es un **evento** y no se archiva en ningún lado.

→ Traducido a Simetrik: el equivalente de la "alert rule" no es el incidente, es la **configuración de monitoreo** del gráfico o del dataset. Y esa configuración **ya cuelga** de un gráfico → tablero → carpeta. Así que la cadena de herencia que propone D10 **ya está completa** y no hace falta declarar nada nuevo.

---

## 2. Metabase — inherencia por co-locación, casi idéntica a la nuestra

Las colecciones contienen *"questions, dashboards, models, **timelines**, and other collections"*, y los eventos de una timeline **aparecen solos** en los gráficos de la misma colección:

> *"Timelines are groups of events associated with a collection… **events you've added to a timeline will show up on time series questions stored in the same collection as that timeline**."*
> — [Metabase docs · Events and timelines](https://www.metabase.com/docs/latest/exploration-and-organization/events-and-timelines)

Es exactamente el mecanismo de **membresía heredada** de D10: el evento no se archiva, **se resuelve por el contenedor del recurso al que pertenece**.

También confirma la exclusividad (D3): *"a single item, like a question or dashboard, can only be in one collection at a time"* — [Collections](https://www.metabase.com/docs/latest/exploration-and-organization/collections).

---

## 3. El contrafactual: Datadog no usa carpetas

Datadog organiza monitores y dashboards **con tags**, no con carpetas: *"you can create fewer dashboards and utilize tag filters to see more information in one place"* — [Best practices for tagging your monitors](https://www.datadoghq.com/blog/tagging-best-practices-monitors/).

**Qué enseña:** para entidades que **llegan en volumen y son efímeras** (monitores disparando, señales), el mecanismo que gana es **filtrar por atributo**, no clasificar en contenedores. Datadog además pone el costo explícito: los tags exigen **gobierno** — *"a quarterly review process… remove unused tags"* — porque sin convención se degradan.

**Cómo se resuelve la tensión en nuestro diseño:** no hay que elegir. En D10 la carpeta es un **atributo derivado** del recurso, así que en la vista de Anomalías **la carpeta se comporta como un tag** (filtrás por ella) mientras en Tableros y Datasets se comporta como una carpeta (metés cosas adentro). Un solo concepto, dos comportamientos según la naturaleza de la entidad — y sin pedirle al usuario que mantenga taxonomías paralelas, que es el costo que Datadog paga.

---

## 4. Las tres respuestas a "¿qué hago con lo que llega solo?"

| Producto | Mecanismo | Qué se declara | Qué se deriva |
|----------|-----------|----------------|---------------|
| **Grafana** | La **regla** vive en la carpeta | La configuración de la alerta | El disparo (no se archiva) |
| **Metabase** | Co-locación | La timeline en la colección | El evento aparece en los gráficos de esa colección |
| **Datadog** | Tags + filtros | Los tags del monitor | Todo se consulta por filtro |
| **Simetrik (D10)** | **Herencia del recurso** | Tablero / dataset en la carpeta | La anomalía y el pendiente heredan del recurso al que apuntan |

Los cuatro comparten el principio: **nadie le pide al usuario clasificar eventos a mano.** Nuestro diseño es el de Metabase con el anclaje explícito de Grafana.

---

## 5. Respuestas a las sub-decisiones abiertas

| # | Pregunta | Respuesta del benchmark |
|---|----------|------------------------|
| **SD-1** | ¿Archivar un incidente puntual a mano? | **No.** Ninguno de los tres lo permite: Grafana archiva la regla, Metabase la timeline, Datadog nada. Confirma la recomendación de dejarlo fuera de la v1. |
| **SD-2** | ¿Carpeta en Anomalías como filtro, agrupación o ambas? | **Filtro** primero (es lo que hace Datadog y es lo que la vista ya sabe hacer con `AnomaliesFilterPanel`). La agrupación puede venir después; el filtro es lo que resuelve la tarea. |
| **SD-3** | ¿Un filtro guardado puede tener "carpeta" como criterio? | **Sí, y es el puente entre los dos sistemas.** `IncidentSavedFilter.filters` es un JSONB opaco, así que sumar `folder_id` **no requiere migración**. |
| **SD-5** | ¿"Carpeta" sigue sirviendo siendo transversal? | **Sí.** Grafana usa "Folder" para exactamente esta mezcla (dashboards + alert rules). "Colección" sería más preciso pero rompe con Almacenamiento, que ya dice "carpeta" en el producto. **Se mantiene "carpeta".** |
| **SD-6** | ¿Nombre único por cuenta a secas? | **Sí.** Un solo namespace: es lo que hace que "Adquirencia" sea un concepto del negocio y no dos listas paralelas. |

**SD-4** (Pendientes: tabla puente vs. herencia indirecta) el benchmark no la responde — es una restricción de nuestra arquitectura, no una decisión de diseño. Sigue abierta y requiere hablar con el equipo del datahub.

---

## 6. Lo que nadie hace (y por qué no lo vamos a hacer)

1. **Namespaces de carpetas paralelos por tipo.** Ningún producto revisado mantiene "carpetas de dashboards" separadas de "carpetas de datasets". Refuerza la decisión de D10 contra la alternativa que se descartó.
2. **Obligar a archivar eventos.** Nadie. Es la razón por la que la membresía de anomalías es heredada.
3. **Mezclar tipos en una lista sin distinción visual.** Metabase mezcla, pero **con icono por tipo**. Si alguna vista nuestra llegara a mostrar tipos juntos, necesita el icono.

---

## 7. Anti-patrón a evitar, con nombre propio

**La deuda de gobierno de los tags** (Datadog): sin convención, la taxonomía se degrada y hay que hacer limpieza periódica. Aplica a nuestras carpetas: por eso **I5** definió objetivo de 7 ± 2 y aviso suave sobre 15, y por eso la métrica que se vigila es el **% de ítems dentro de una carpeta**, no la cantidad de carpetas.

---

## Fuentes

- [Manage access using folders or data sources · Grafana Alerting](https://grafana.com/docs/grafana/latest/alerting/set-up/configure-rbac/access-folders/)
- [Folder access control · Grafana](https://grafana.com/docs/grafana/latest/administration/roles-and-permissions/folder-access-control/)
- [Events and timelines · Metabase](https://www.metabase.com/docs/latest/exploration-and-organization/events-and-timelines)
- [Collections · Metabase](https://www.metabase.com/docs/latest/exploration-and-organization/collections)
- [Best practices for tagging your monitors · Datadog](https://www.datadoghq.com/blog/tagging-best-practices-monitors/)
- [Getting Started with Tags · Datadog](https://docs.datadoghq.com/getting_started/tagging/)
- Código: `op-center-backend` (`incident_saved_filters`, `anomaly_signals`, `anomaly_incident_entities`, `datasets`) · `fe-solutions-mf` (`DatasetList`, `AnomaliesFilterPanel`, `services/pending`)
