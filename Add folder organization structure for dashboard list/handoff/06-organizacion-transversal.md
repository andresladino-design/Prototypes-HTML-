# Organización transversal — carpetas para las cuatro entidades del OC

**Fecha:** 2026-08-04
**Origen:** feedback al prototipo. El alcance pasa de "carpetas para tableros" a **un sistema de organización transversal**.
**Decisiones tomadas:** carpeta **compartida entre entidades** · alcance v1 = **las cuatro** (Tableros, Datasets, Anomalías, Pendientes) · las cuatro con **carpetas**.

---

## 1. El precedente de la casa (y qué confirma)

El feedback apunta a lo que ya existe para anomalías. Lo que hay en el código:

| Precedente | Qué es | Scope |
|-----------|--------|-------|
| `IncidentSavedFilter` | *"A named, account-shared preset of incident list filters"* | **Por cuenta**; `created_by_user_id` solo auditoría |
| `NotificationPackage` | Regla de notificación a nivel de cuenta | **Por cuenta** |
| `DashboardFavorite` | Atajo personal con orden | Por usuario |

**Confirma D1:** los contenedores con nombre creados por el usuario en el OC son **por cuenta**, y el autor se guarda solo para trazabilidad. La carpeta hereda esa convención.

---

## 2. El problema que abre "carpetas para las cuatro" — y cómo se resuelve

Tableros y datasets **existen y persisten**: el usuario los mete en una carpeta. Anomalías y pendientes **llegan solos y no dejan de llegar**: nadie puede archivar a mano un incidente que todavía no ocurrió, y si lo archivara, el siguiente incidente del mismo gráfico volvería a quedar sin clasificar.

**La solución no es dejar anomalías afuera: es que la membresía sea heredada.**

> **La carpeta se declara sobre los recursos estables. Las anomalías y los pendientes heredan la carpeta del recurso al que apuntan.**

Esto funciona porque el modelo **ya guarda ese vínculo**:

| Entidad | Cómo entra a la carpeta | Anclaje real en el código |
|---------|------------------------|---------------------------|
| **Tableros** | Declarada — el usuario lo mueve | `dashboards.folder_id` (nuevo) |
| **Datasets** | Declarada — el usuario lo mueve | `datasets.folder_id` (nuevo) |
| **Anomalías** | **Heredada** del gráfico / recurso | `anomaly_signals.chart_id` → chart → dashboard · `anomaly_incident_entities.resource_id + resource_type` (`source='scope'` \| `'blast_radius'`) |
| **Pendientes** | **Heredada** de la conciliación | `resource_id` + `resource_type` (`reconciliations` \| `advanced_reconciliation`) — ⚠️ ver §5 |

**Consecuencia para el usuario:** organiza **una vez**, sobre tableros y datasets, y automáticamente obtiene "las anomalías de Adquirencia" y "los pendientes de Adquirencia" — **incluidas las que aún no existen**. Es más potente que archivar a mano, y es cero trabajo extra.

### Sub-decisión abierta (SD-1)

¿Además de la herencia, el usuario debería poder **archivar un incidente puntual** en una carpeta a mano (por ejemplo, un incidente de Adquirencia que quiere revisar junto al cierre contable)? Se puede sumar como excepción sobre la herencia, pero abre la pregunta de qué pasa con los incidentes futuros del mismo recurso. **Recomiendo no incluirlo en la v1** y ver si aparece la necesidad.

---

## 3. Modelo de datos

Una sola tabla de carpetas por cuenta, **sin `entity_type`**: "Adquirencia" es UNA carpeta; cada vista muestra lo suyo.

```python
class Folder(Base):
    __tablename__ = "folders"                      # ← genérica, no "dashboard_folders"
    id: UUID (pk)
    name: str(255)
    account_id: str(255), index                    # D1
    created_by: str(255) | None                    # trazabilidad, como IncidentSavedFilter
    order: int                                     # reservado; el orden de la v1 es A→Z (D5)
    created_at / updated_at
    __table_args__ = (UniqueConstraint("account_id", "name"),)
```

Membresía **declarada** — una columna por entidad, no una tabla puente:

```python
# dashboards.py  y  datasets.py  (misma forma en ambas)
folder_id: Mapped[uuid.UUID | None] = mapped_column(
    UUID(as_uuid=True),
    ForeignKey("folders.id", ondelete="SET NULL"),
    nullable=True, index=True,
)
```

Por qué columna y no puente:

- **D3 (exclusividad)** la garantiza el esquema, ahora **por entidad**: un tablero en una carpeta, un dataset en una carpeta. Nada impide que la misma carpeta tenga 24 tableros y 8 datasets — eso es justo lo que se busca.
- **D6 (eliminar carpeta desagrupa)** lo hace `ON DELETE SET NULL` en el motor, para las dos entidades a la vez.
- Sumar una tercera entidad declarada más adelante (gráficos, repositorios) es **una columna**, no una migración de modelo.

Membresía **heredada** — no se persiste: se **resuelve en la query** siguiendo el anclaje de la tabla de §2. Guardar `folder_id` en un incidente lo dejaría desincronizado en cuanto el tablero cambie de carpeta.

---

## 4. Qué cambia en cada vista

| Vista | Cambio | Costo |
|-------|--------|-------|
| **Panel de Tableros** | Carpetas en la sección "Tableros" (lo ya diseñado y prototipado) | Hecho |
| **Panel de Datasets** | El **mismo** componente en el tab Datasets. Ya comparte `SidebarList`, búsqueda con debounce y scroll infinito; `DatasetList` (447 líneas) tiene la misma anatomía que `DashboardList` (520) | **Bajo** |
| **Anomalías** | Filtro y agrupación **por carpeta** en la lista de incidentes. Se suma al `AnomaliesFilterPanel` y convive con `incident_saved_filters` (un filtro guardado puede incluir una carpeta) | Medio |
| **Pendientes** | Filtro por carpeta, resolviendo la carpeta de la conciliación | **Alto** — ver §5 |

**El componente nace compartido:** `shared/components/FolderSection/` + `services/folders/`, no dentro de `features/dashboards/`. Es lo que hace que datasets salga casi gratis y que anomalías reuse el selector de carpeta.

---

## 5. ⚠️ Pendientes es distinto, y ya sé por qué

El feedback lo intuía (*"ahí creo que se iba a tocar hacer alguna diferencia en cómo implementarlo"*). La razón es concreta:

**Los pendientes cuelgan de una conciliación que vive en otro servicio.** En `services/pending/queriesFn.ts` la resolución es:

```
resource_id + resource_type ('reconciliations' | 'advanced_reconciliation')
  → GET /api/v1/reconciliations/{id}/  con baseURL: datahub  y header x-skt-workspace
```

Es decir: el recurso ancla **no está en la base de datos de `op-center-backend`**, así que no se le puede poner una columna `folder_id` como a `dashboards` y `datasets`.

Dos caminos:

| | Cómo | Costo / riesgo |
|---|------|----------------|
| **(a) Tabla puente para recursos externos** | `folder_external_items(folder_id, resource_type, resource_id)` en OC. La conciliación entra a la carpeta sin tocar el datahub. | Medio. Rompe la simetría "una columna por entidad", pero **solo** para lo que vive afuera. Recomendado. |
| **(b) Herencia indirecta** | Los pendientes heredan la carpeta de los tableros/datasets que consumen esa conciliación | Bajo costo, pero la relación es difusa: un dataset puede tocar varias conciliaciones y el resultado sería impredecible. |

**Recomiendo (a)**, y que Pendientes sea el **último** entregable: es el único que necesita un modelo extra y coordinación con otro equipo.

---

## 6. Qué sobrevive de lo ya hecho

**Sin cambios:** D1 (por cuenta, ahora con respaldo del precedente) · D2 (un nivel) · D5 (orden A→Z) · D6 (eliminar desagrupa) · D7 (menú + drag) · D8 (wizard de 2 pasos) · D9 (Agregar tableros) · I1–I6 · `design.md` completo · el baseline · el prototipo.

**Se ajusta:**

| Qué | Antes | Ahora |
|-----|-------|-------|
| Tabla BE | `dashboard_folders` | **`folders`** (genérica) |
| Componente FE | `features/dashboards/components/FolderSection/` | **`shared/components/FolderSection/`** |
| Servicio FE | `services/dashboards/folders/` | **`services/folders/`** |
| D3 exclusividad | "un tablero, una carpeta" | "un **ítem** de cada entidad, una carpeta" — la carpeta sí mezcla entidades |
| Copy del wizard | "Elige los tableros" | Parametrizado por entidad: "Elige los tableros" / "Elige los datasets" |
| Copy destructivo | "Los 24 tableros volverán a la lista" | Debe contar **por entidad**: "24 tableros y 8 datasets volverán a sus listas" |
| Contadores | Uno | **Por vista** — el tab Tableros muestra 24, el tab Datasets muestra 8 |

---

## 7. Orden de entrega propuesto

1. **Tableros** — ya diseñado y prototipado. Valida el sistema con datos reales.
2. **Datasets** — el mismo componente en el tab de al lado. Confirma que lo transversal funciona.
3. **Anomalías** — filtro/agrupación por carpeta, integrado con los filtros guardados que ya existen.
4. **Pendientes** — al final: necesita la tabla puente de §5 y coordinación con el servicio del datahub.

Los cuatro comparten **una** tabla, **un** componente y **un** lenguaje. Lo que cambia por entidad es cómo se resuelve la membresía, no el concepto.

---

## 8. Preguntas abiertas

| # | Pregunta |
|---|----------|
| **SD-1** | ¿Se puede archivar un incidente puntual a mano, además de la herencia? (Recomiendo no en la v1) |
| **SD-2** | ¿La carpeta se muestra en la vista de Anomalías como filtro, como agrupación de la lista, o las dos? |
| **SD-3** | ¿Un filtro guardado de incidentes puede tener "carpeta" como criterio? (Debería: es lo que une los dos sistemas) |
| **SD-4** | Pendientes: ¿tabla puente (a) o herencia indirecta (b)? Requiere hablar con el equipo del datahub |
| **SD-5** | ¿"Carpeta" sigue siendo el nombre correcto ahora que es transversal, o conviene "Colección"/"Grupo"? Para tableros y datasets "carpeta" funciona; para un stream de anomalías es menos natural |
| **SD-6** | ¿El nombre de carpeta es único por cuenta a secas, o único por cuenta considerando que agrupa varias entidades? (Recomiendo: único por cuenta, es una sola lista de nombres) |
