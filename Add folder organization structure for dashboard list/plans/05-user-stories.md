# Etapa 5 — User stories UX

**Objetivo:** convertir los 7 flujos en historias con criterios de aceptación verificables, listas para que FE/BE estimen y para que QA pruebe.
**Entregable:** `handoff/05-user-stories.md`
**Precondición:** Etapa 4 (los flujos definen el alcance de cada historia).
**Herramienta:** skill `ux-user-stories` (audiencia: diseño + FE + BE + QA), y `ux-heuristics` como paso de revisión.

---

## 1. Mapa de historias ↔ flujos ↔ criterios del issue

| Historia | Flujo | Criterio |
|----------|-------|----------|
| HU-01 · Ver mis tableros agrupados en carpetas | F7 | C4 |
| HU-02 · Crear una carpeta | F1 | C1 |
| HU-03 · Mover un tablero a una carpeta | F2 | C2 |
| HU-04 · Quitar un tablero de una carpeta sin eliminarlo | F3 | C3 |
| HU-05 · Renombrar una carpeta | F4 | C1 |
| HU-06 · Eliminar una carpeta sin perder los tableros | F5 | C1, D6 |
| HU-07 · Buscar un tablero esté donde esté | F6 | C5 |
| HU-08 · Entender qué son las carpetas la primera vez (empty state / onboarding) | F1 | C8 |

## 2. Formato de cada historia

```
### HU-0X · <título en lenguaje de usuario>

**Como** <rol OC: analista de conciliación / lead de FinOps / admin de cuenta>
**quiero** <capacidad>
**para** <resultado medible>

**Contexto UX:** momento en el journey · qué sabe el usuario al llegar · qué carga cognitiva trae.

**Criterios de aceptación** (Given / When / Then, verificables)
- [ ] ...

**Estados de interfaz:** default · hover · focus · loading · success · error · vacío · sin permisos
**Componentes desyk:** <lista, con link al design.md>
**Copy:** labels, placeholders, mensajes de error, toasts (en español, glosario Simetrik)
**Accesibilidad:** foco, orden de tabulación, roles/aria, contraste, alternativa al drag & drop
**Métrica de éxito:** cómo sabremos que funcionó
**Fuera de alcance:** lo que esta historia NO hace
```

## 3. Criterios de aceptación que no se pueden olvidar

Vienen del código real (exploración §2.4) y del brief:

- **Búsqueda:** cruza todas las carpetas · sigue siendo server-side con debounce de 300 ms · cada resultado indica su carpeta · al limpiar, el panel recupera el estado de expansión anterior.
- **Paginación:** el scroll infinito (20 por página) sigue funcionando con carpetas presentes; una carpeta con 60 tableros no rompe la carga.
- **Orden:** el toggle A→Z existente sigue disponible y su alcance está definido (D5).
- **Coexistencia:** "Configuraciones pendientes" y "Favoritos" **no cambian** de comportamiento. Un tablero puede estar en una carpeta **y** ser favorito.
- **No destructivo:** eliminar carpeta **jamás** elimina tableros; quitar de carpeta tampoco. El copy lo dice explícito.
- **Permisos:** un tablero sin acceso (`has_access: false`) dentro de una carpeta se sigue viendo atenuado y no navegable, como hoy.
- **Límites:** definir máximo de carpetas y máximo de largo del nombre (Almacenamiento y tableros ya tienen validación de nombre; alinear).
- **Errores:** nombre duplicado (409) se muestra inline en el diálogo, no como toast solo; fallos de red muestran `Alert` inline en diálogos destructivos y toast en acciones de fila.
- **Teclado:** todo el flujo se completa sin mouse. Si el drag & drop entra (D7), el menú `⋮` es su equivalente accesible obligatorio.

## 4. Métricas de éxito del feature (para la historia raíz)

Del objetivo de UX: *bajar el tiempo de encontrar un tablero*.

- % de cuentas con ≥1 carpeta creada a los 30 días.
- % de tableros dentro de una carpeta vs. sueltos, por cuenta.
- Nº de búsquedas por sesión **antes vs. después** (la hipótesis es que baja: si navegar funciona, se busca menos).
- Tiempo hasta abrir el primer tablero de la sesión.
- Tasa de error en el diálogo de eliminar carpeta (abandonos → señal de copy confuso).

→ Estas métricas requieren eventos de telemetría; se listan en el handoff FE (Etapa 7) para que se instrumenten con el feature, no después.

## 5. Revisión heurística antes de cerrar

Pasar las 8 historias por `ux-heuristics`:

- **Visibilidad del estado:** ¿se ve en qué carpeta está un tablero, siempre?
- **Control y libertad:** ¿hay "Deshacer" en quitar/mover?
- **Reconocer > recordar:** ¿el selector de carpetas muestra las carpetas, o exige escribir el nombre?
- **Prevención de error:** ¿el diálogo destructivo dice qué pasa con los N tableros?
- **Flexibilidad:** ¿hay atajo (drag) sin sacrificar el camino accesible?
- **Miller:** ¿cuántas carpetas caben antes de que el panel vuelva a ser una lista larga? ¿hay que sugerir un máximo razonable?
- **Hick:** el menú `⋮` pasa de 5 a 6–7 ítems. ¿Sigue siendo legible o hay que agrupar con separadores?

## 6. Definition of done

- [ ] 8 historias en `handoff/05-user-stories.md` con el formato completo.
- [ ] Cada criterio del issue (C1–C8) trazado a al menos una historia.
- [ ] Copy definitivo en español para cada mensaje, listo para volverse keys de i18n.
- [ ] A11y explícita por historia (no un párrafo genérico al final).
- [ ] Revisión heurística aplicada y los hallazgos incorporados.
- [ ] Métricas de éxito con los eventos de telemetría que las alimentan.

## 7. Riesgos

- **Historias que describen la UI en vez de la necesidad** — el criterio de aceptación debe ser verificable sin asumir un layout concreto.
- **Inflar el alcance** con multi-selección, carpetas compartidas con permisos propios o anidación: van a "Fuera de alcance" con su razón, no a las historias.
- Criterios no verificables ("debe ser intuitivo"). Si QA no puede probarlo, no es criterio.
