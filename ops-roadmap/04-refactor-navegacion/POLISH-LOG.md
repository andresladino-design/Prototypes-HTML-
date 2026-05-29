# Polish Log · Refactor Navegación Anomalías

Bitácora de iteraciones del mock `mock.html`. Cada iteración representa un ciclo `critique → layout → polish`.

---

## Iteración 1 · Critique inicial (31/60 → 48/60)

| ID | Issue | Fix |
|---|---|---|
| F-001 | Sparkles en botones IA | Reemplazado por `bot` |
| F-002 | Gradient surface decorativo | Eliminado, surface neutra + border-left violet |
| F-003 | AiChat sin Sheet canónico | Stub funcional añadido (botón footer → Sheet lateral) |
| F-005 | Dos acciones primarias compiten | "Notificaciones" overflow [···] |
| F-007 | Breadcrumb sin N4 | Añadido tab actual |
| F-008 | P0/P1/P2 jerga | Reemplazado por checkboxes neutros |
| em-dashes | 4 ocurrencias `—` | Sustituidos por `:` o `·` |
| F-10 | Voseo argentino | Tuteo neutro |
| F-12 | Formato ID | "Fuente · ID xxx" |
| F-13 | "Block Kit" jerga | "Incidentes consolidados con acciones inline" |
| F-14 | Badge "NUEVO" marketing | "Beta" |
| F-15 | Iconos sin aria-label | 9 aria-labels añadidos |
| F-16 | Dot 7px → 6px | OK |
| F-11 | Histórico placeholder | Empty state real |
| F-17 | Hero metric cards | Fila densa |

---

## Iteración 2 · Refactor estructural (feedback humano)

Tras feedback "el sidepanel del Centro de Operaciones lo trae el provider":

- **Top-nav horizontal eliminado**. Shell ahora respeta arquitectura real provider-app + fe-solutions-mf:
  - Provider sidebar global (240px, light): Logo + Workspace selector + 9 items (Overview, Simetrik Agent, **Operation Center**, Marketplace, Automate, Operate, Audit, Tools, Payments) + Footer
  - OC top sub-nav: 4 módulos (Tableros / Pendientes / **Monitoreo** / Storage)
  - Module sidebar: lentes contextuales
- Workspace selector con `chevrons-up-down`, avatar RM, sub-label cliente
- Footer del provider sidebar: avatar usuario + bell con dot rojo + help + collapse

---

## Iteración 3 · Reorganización por concerns

Feedback humano: "el monitor es config, la actividad es el hallazgo. Estamos cruzando datos."

| Cambio | Antes | Después |
|---|---|---|
| Lente "Recursos" | Solo Fuentes | Renombrada a **"Monitores"**, agrupa Fuentes + Tableros |
| Categorías sidebar | Favoritos / Con monitoreo / Sin monitoreo | Favoritos / **Sobre fuentes** / **Sobre tableros** / Sin monitoreo |
| Sidebar icon | Dot indicator de salud | Icono que distingue origen (`hard-drive` vs `layout-dashboard`) |
| Header del monitor | Con badge "Anomalía activa" | **Sin badge** (lo pediste explícitamente) |
| Tab "Estado" | Card de hipótesis IA + KPIs | Renombrado a **"Resumen"** = vista de **configuración visible** |
| Lente Actividad | Cards full-page | **Master-detail**: lista en sidebar, detalle full en main |
| Hipótesis IA + acciones | En tab Resumen del monitor | Movido a **panel derecho de Actividad** |

---

## Iteración 4 · Eliminación de lista duplicada

Feedback humano: "aquí estamos repitiendo el panel".

- Eliminado el LEFT panel master del área principal de Actividad
- La lista vive **solo en el sidebar del módulo** (master)
- El área principal queda solo con el detail panel del hallazgo seleccionado

---

## Iteración 5 · Feedback general · 7 puntos estructurales

| Punto | Cambio |
|---|---|
| **2** Reorden lentes | Actividad primero (default landing), Monitores segundo |
| **3** Buscador contextual | Placeholder dinámico según `lens` |
| **5** CTAs dentro del Agente IA | Investigar/Asignar movidos del header sup-derecho a la card IA |
| **1+4** Detalle por kind | Source: días de evaluación + ventana + file patterns con entidades Date/Sequence. Dashboard: tabla multi-serie por métrica (País × Min × Max + métrica global). Datos validados contra `monitoringConfig/schemas.ts` y `SystemKpiTab/PrepEditMode.tsx` |
| **6+7** Consistencia contenedores | Patrón canónico aplicado a TODAS las sections: `<section><header><h2>title</h2><p>subtitle</p></header><div>content</div></section>` |

---

## Iteración 6 · Combo critique → layout → polish para acciones

Critique de acciones produjo 12 inconsistencias y matriz canónica. Cambios aplicados:

### Layout

| ID | Fix |
|---|---|
| L-01 | "Investigar" (primary) **devuelto al header del incidente**, junto a "Marcar como Resuelto" (outline + dropdown stub) y overflow [···]. El primary ya no queda enterrado en la card IA. |
| L-02 | Card IA footer simplificado: queda solo Asignar (outline) + Silenciar 1 hora (ghost) + grupo cierre (`ml-auto`): Marcar falso positivo · Descartar |
| L-03 | "Descartar" ahora es **ghost destructive** (`text-red-600 hover:bg-red-50`), separado de "Marcar falso positivo" con divider sutil (`w-px h-4 bg-zinc-200`) |
| L-04 | Text-links de cards unificados: `Editar configuración →`, `Ver todos los KPIs →`, `Ver historial →` (eran "Editar →", "Ver todos →", "Ver histórico →" — tres patrones distintos para el mismo rol) |
| L-05 | **Zona peligrosa** al final del tab Configuración: contenedor con border-red-200 + bg-red-50/30, agrupa Restablecer + Pausar + Eliminar con tratamiento destructive |

### Findings críticos del critique aplicados

1. ✅ Primary del incidente NO enterrado — está en header con outline "Marcar como Resuelto"
2. ✅ "Editar →" doble significado resuelto → "Editar monitoreo" en header (primary), "Editar configuración →" en cards (link)
3. ✅ "Descartar" destructive + separador
4. ✅ Restablecer suelto → Zona peligrosa
5. ⚠️ Estado "monitor pausado" / "monitor off" → reservado en Zona peligrosa pero no como vista completa (out of scope esta iteración)

### Polish

- 1 em-dash residual en comentario HTML → `·`
- Verificación: cero `—`, cero `✨`, cero `breach_pct`, cero "Powered by"

---

## Pendientes para iteración futura

- Vista del **monitor pausado / off** completa (con CTA "Activar monitoreo")
- Estado **sin permisos / read-only** (banner + buttons disabled)
- Estados de **error de fetch**, **archivado**, **carga**
- Telemetría para medir adopción (gap-04)
- Confirm dialogs para Restablecer / Eliminar (la Zona peligrosa solo expone los buttons)
- Diferenciación de tab **Configuración** entre Source y Dashboard (hoy comparte UI; el Dashboard necesita editor de series inline)
