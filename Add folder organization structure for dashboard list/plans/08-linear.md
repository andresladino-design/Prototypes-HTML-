# Etapa 8 — Tickets en Linear

**Objetivo:** dejar SWAT-577 listo para entrar a un ciclo, con sub-issues por sistema y el handoff linkeado.
**Entregable:** SWAT-577 actualizado + sub-issues creados + doc ligera con links.
**Precondición:** Etapa 7 (el handoff es el insumo de los tickets).

---

## Convención del equipo

Las épicas se documentan **ligeras**: el issue padre describe el problema y **lista los sistemas involucrados**, con links al handoff;
el detalle vive en el handoff, no copiado en Linear. Los sub-issues se abren **por sistema**.

---

## 1. Actualizar SWAT-577 (el padre)

Agregar a la descripción, sin reescribir el reporte original:

- **Objetivo de UX** y las leyes que lo sustentan (Miller · reconocer > recordar).
- **Links:** prototipo en GitHub Pages · `handoff/07-handoff-fe.md` · `handoff/07-handoff-be.md` · `handoff/07-antes-despues.md` · flows de Moka.
- **Sistemas involucrados:**
  - `op-center-backend` — modelo, migración, CRUD de carpetas, filtro en `GET /dashboards`
  - `fe-solutions-mf` — panel de Tableros (carpetas, diálogos, servicios, i18n)
  - QA — plan de pruebas
  - Contenido/soporte — documentación de usuario final (C8)
- **Decisiones tomadas** (D1–D7) en una tabla de una línea cada una, con link al benchmark.
- **Fuera de alcance de la v1** (anidación, multi-selección, permisos por carpeta, colores) con su razón.

## 2. Sub-issues propuestos

| # | Título | Sistema | Depende de |
|---|--------|---------|-----------|
| S1 | BE — Modelo + migración de `dashboard_folders` y asignación de tableros | op-center-backend | — |
| S2 | BE — CRUD de carpetas (`GET`/`POST`/`PATCH`/`DELETE /dashboards/folders`) | op-center-backend | S1 |
| S3 | BE — Mover/quitar tablero (`PATCH /dashboards/{id}/folder`) + desagrupar al eliminar carpeta | op-center-backend | S1 |
| S4 | BE — `GET /dashboards`: filtro `folder_id`/`unfiled` + `folder` en la respuesta, sin romper `search` | op-center-backend | S1 |
| S5 | FE — Servicios y schemas de carpetas (`services/dashboards/folders/`) | fe-solutions-mf | S2, S4 |
| S6 | FE — `FolderSection`: render, colapsar/expandir, jerarquía visual, contador | fe-solutions-mf | S5 |
| S7 | FE — Crear / renombrar / eliminar carpeta (diálogos + validación + toasts) | fe-solutions-mf | S5 |
| S8 | FE — Mover a carpeta / quitar de la carpeta (menú + optimistic update) | fe-solutions-mf | S5, S6 |
| S9 | FE — Búsqueda cross-carpeta con la carpeta como metadato del resultado | fe-solutions-mf | S5, S6 |
| S10 | FE — Empty states, onboarding de la primera carpeta y telemetría | fe-solutions-mf | S6 |
| S11 | FE — i18n es/en/pt de las keys nuevas | fe-solutions-mf | S7, S8 |
| S12 | QA — Plan de pruebas del feature (incluye el caso "eliminar carpeta no borra tableros") | QA | S1–S11 |
| S13 | Doc — Ayuda para usuario final (C8) | Contenido | S6–S9 |

**Atajo válido si el ciclo aprieta:** S1+S2+S3 pueden ser un solo sub-issue de BE, y S6+S7 uno de FE. Lo que **no** se colapsa es S4 (el filtro sin romper búsqueda) ni S12 (QA), porque ahí están los dos riesgos del feature.

Cada sub-issue lleva: criterios de aceptación de su historia (Etapa 5), link al handoff correspondiente y link al prototipo.

## 3. Trazabilidad historia ↔ ticket

Tabla en el handoff: HU-01…HU-08 → sub-issues que la implementan → criterio C1…C8 que cierra.
Sirve para verificar que ningún criterio del issue quedó sin ticket.

## 4. Definition of done

- [ ] SWAT-577 actualizado con objetivo de UX, sistemas, decisiones, links y fuera de alcance.
- [ ] Sub-issues creados con label por sistema y estimación pedida a cada dev.
- [ ] Cada sub-issue linkea handoff + prototipo; ninguno repite el detalle del handoff.
- [ ] Matriz de trazabilidad HU ↔ ticket ↔ criterio, sin huecos.
- [ ] Dependencias declaradas en Linear (blocked by / blocks).
- [ ] El prototipo publicado y accesible desde el issue.

## 5. Riesgos

- **Copiar el handoff dentro de Linear:** se desincroniza al primer cambio. Linear linkea; el handoff es la fuente.
- **Sub-issues por pantalla en vez de por sistema:** rompe la convención y complica la asignación.
- **Abrir tickets antes de cerrar D1** — si el scope de las carpetas (usuario vs. cuenta) cambia después, S1 se rehace y arrastra a todos.
