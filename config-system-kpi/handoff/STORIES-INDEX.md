# Stories Index — Monitoreo de Ingesta

> Mapa de implementación, dependencias y convenciones para el agente Claude Code que tome estas historias desde Linear.

## Convenciones para el agente implementador

Antes de implementar cualquier historia:

1. **Leer `00-CONTEXT.md` primero**: glosario, tokens desyk, estados BADS, helpers Alpine ya existentes. Es el cimiento.
2. **Validar los `depends_on` del frontmatter**: las dependencias deben estar implementadas (o ir en la misma PR).
3. **Usar Acceptance criteria como source of truth**: si hay conflicto entre el copy del prototipo y los AC, ganan los AC.
4. **Respetar Out of scope**: no expandir el scope sin coordinar.
5. **Llenar gaps de Empty states marcados como ❌ pendiente** antes de mergear. Si encuentras un escenario que la tabla no menciona, agregalo al ticket antes de implementar.
6. **Reutilizar helpers Alpine existentes** (`dsActiveSimple`, `dsPromoteToFamily`, `selectConfigSource`, etc.) en lugar de reimplementar.
7. **Pixel-perfect con CSS existente**: usar clases ya definidas en el prototipo (`.ds-card`, `.tm-chart-card`, etc.).
8. **Español neutro**: sin slang regional, sin em-dashes (`—`), respetar glosario.

---

## Mapa de implementación (orden recomendado)

### Fase 1 — Shell y estados base
Estructura visual sobre la que todo lo demás se monta.

```
00-CONTEXT.md                          (referencia, no implementable)
├─ 02-vista-monitoreo                  (tabs y estructura, banner conceptos)
└─ 04-cards-monitores-ingesta          (cimiento visual del tab Ingesta)
```

### Fase 2 — Configuración uno-a-uno
El corazón del producto: modal de configuración y sus contenedores internos.

```
05-modal-configuracion                 (shell del modal completo)
├─ 07-contenedor-ventana-de-tiempo     (transversal a Low/Family/High)
├─ 08-contenedor-comportamiento-dia    (chasis Lu-Do + toggle)
│  ├─ 09-contenedor-volumen-archivos   (indicador)
│  ├─ 10-contenedor-cantidad-registros (indicador hermano)
│  ├─ 11-contenedor-notas-adicionales  (card colapsable opcional)
│  └─ 12-contenedor-grupos-high        (cards ds-group, modo High)
```

### Fase 3 — Activación masiva
Bulk modal y activation loader. Reutilizan el modal de configuración como destino.

```
06-activacion-masiva                   (bulk + activation loader)
```

### Fase 4 — Onboarding y educación
Banners promocionales y vista conceptual. Se pueden implementar en paralelo con la Fase 2-3.

```
01-banner-tablero                      (banner del dashboard)
03-banner-monitorear-tablero           (banner bulk del tab Ingesta)
13-journey-low-family-high             (documento conceptual, referencia)
```

---

## Tabla de dependencias

| Doc | Depende de | Bloquea a |
|---|---|---|
| `00-CONTEXT.md` | — | (referencia) |
| `01-banner-tablero` | — | `02-vista-monitoreo` |
| `02-vista-monitoreo` | — | `03-banner-monitorear-tablero`, `04-cards-monitores-ingesta` |
| `03-banner-monitorear-tablero` | `02-vista-monitoreo`, `04-cards-monitores-ingesta` | `06-activacion-masiva` |
| `04-cards-monitores-ingesta` | `02-vista-monitoreo` | `05-modal-configuracion`, `06-activacion-masiva` |
| `05-modal-configuracion` | `04-cards-monitores-ingesta` | `07`, `08`, `09`, `10`, `11`, `12` |
| `06-activacion-masiva` | `03-banner-monitorear-tablero`, `04-cards-monitores-ingesta` | `05-modal-configuracion` |
| `07-contenedor-ventana-de-tiempo` | `05-modal-configuracion` | — |
| `08-contenedor-comportamiento-dia` | `05-modal-configuracion` | `09`, `10`, `11`, `12` |
| `09-contenedor-volumen-archivos` | `08-contenedor-comportamiento-dia` | — |
| `10-contenedor-cantidad-registros` | `08-contenedor-comportamiento-dia` | — |
| `11-contenedor-notas-adicionales` | `08-contenedor-comportamiento-dia` | — |
| `12-contenedor-grupos-high` | `08`, `09`, `10`, `11` | — |
| `13-journey-low-family-high` | — (referencia conceptual) | — |

**Notas sobre dependencias**:
- `05` y `06` se "bloquean mutuamente" en cierto sentido: el activation loader (parte de `06`) precede al modal (`05`) en flujos individuales, pero el bulk modal (`06`) también lleva al modal individual para editar. En la práctica, implementar `05` primero y luego `06` aprovecha el modal ya construido.
- Los contenedores internos del modal (`07` a `12`) se pueden implementar en paralelo entre sí una vez que `05` y `08` están listos.

---

## Resumen por doc (qué entrega cada historia)

| ID | Título | Tipo | Prioridad | Estimación |
|---|---|---|---|---|
| `01-banner-tablero` | Banner promocional del tablero | Feature | P2 | S |
| `02-vista-monitoreo` | Vista de monitoreo del tablero (tabs) | Feature | P1 | M |
| `03-banner-monitorear-tablero` | Banner para activar bulk | Feature | P1 | S |
| `04-cards-monitores-ingesta` | Grid de cards de fuentes | Feature | P0 | M |
| `05-modal-configuracion` | Modal daysetup (creación + edición) | Feature | P0 | XL |
| `06-activacion-masiva` | Bulk modal + activation loader | Feature | P0 | XL |
| `07-contenedor-ventana-de-tiempo` | Card transversal de ventana | Feature | P1 | S |
| `08-contenedor-comportamiento-dia` | Chasis Lu-Do + toggle día | Feature | P0 | L |
| `09-contenedor-volumen-archivos` | Indicador de archivos | Feature | P0 | M |
| `10-contenedor-cantidad-registros` | Indicador de registros | Feature | P0 | M |
| `11-contenedor-notas-adicionales` | Card colapsable de notas | Feature | P2 | S |
| `12-contenedor-grupos-high` | Cards ds-group + peek (High) | Feature | P0 | L |
| `13-journey-low-family-high` | Documento conceptual | Spike | P3 | XS |

---

## Notas finales

- **Empty states**: muchos están marcados como ❌ pendiente. **No asumir copy**: si un empty state crítico no está descrito, agregar al ticket antes de implementar y validar con UX.
- **Endpoints BE**: los `GET /sources/{id}/monitoring`, `POST /sources/{id}/monitoring`, `POST /dashboards/{id}/monitoring/bulk-preview`, `POST /dashboards/{id}/monitoring/bulk-activate`, `GET /sources/{id}/analysis`, `GET /dashboards/{id}/monitoring-summary`, `GET /dashboards/{id}/monitoring-tabs` están **sugeridos** y deben coordinarse con el equipo de BE antes de implementar.
- **Figma**: links pendientes en todos los docs. Pedirlos al equipo de diseño antes de implementar.
- **Modo lectura vs edición**: el modal `05` cambia comportamiento según `daySetupReadonly`. Ver "Flujos específicos" en el doc 05 para diferencias detalladas.
- **Edición masiva NO está cubierta**: la edición sigue siendo uno-a-uno. Ver doc 06 "Edición masiva (NO cubierta)" para el razonamiento.
