# Etapa 3 — Vista espejo en HTML del panel de tableros (baseline "antes")

**Objetivo:** replicar en HTML el panel de Tableros **tal como está hoy en producción**, sin carpetas.
**Entregable:** `prototypes/00-baseline-tableros.html`
**Precondición:** Etapa 2 (`design/tokens.css`). Puede adelantarse en paralelo a la Etapa 1: no depende de D1–D7.

---

## Por qué esta etapa existe

1. Es el **"antes"** del handoff. La convención del equipo es enumerar los cambios contra el estado real de producción, y para eso hace falta un antes fiel, no una captura.
2. Es el **andamio** del prototipo final: la Etapa 6 solo inyecta carpetas dentro de este baseline, así que todo lo que quede fiel acá se hereda gratis.
3. Fuerza a descubrir detalles que el diseño suele olvidar: el botón pin que aparece en hover, el badge ámbar de instalación pendiente, el contador que resta pendientes, el sentinel de scroll infinito.

---

## 1. Qué se replica, componente por componente

Fuente: `fe-solutions-mf/src/oc/features/dashboards/` (rutas exactas en `design-record/03-exploracion-fe-be.md` §2).

```
Panel (ancho ~280 px, borde derecho, fondo --sidebar-background)
├── Header: "Tableros" + botón colapsar (chevron izquierda)
├── Tabs segmentadas: [ Tableros | Datasets ]
├── Botón "＋ Nuevo tablero"  (Button variant=outline, w-full, gap-1.5)
├── Input de búsqueda "Buscar tablero" (icono Search)
└── ScrollArea
    ├── "Configuraciones pendientes (12)"   filas con badge Info ámbar
    ├── "Favoritos (5/15)"                  grip + fila + pin, contenedor punteado
    └── "Tableros (155)"  + toggle A→Z      filas normales, scroll infinito
```

### Detalles de fidelidad obligatorios (los que se suelen perder)

| Detalle | Comportamiento real |
|---------|--------------------|
| Iconos de privacidad | `Globe` en `text-info` (público) · `Lock` en `text-muted-foreground` (privado) · `h-3.5 w-3.5` |
| Instalación pendiente | Reemplaza el icono de privacidad por un círculo `bg-warning/15` con `Info` dentro |
| Botón pin | `text-muted-foreground/0` → visible en `group-hover`; `Pin` si no es favorito, `PinOff` si lo es |
| Botón `⋮` | Misma mecánica de aparición en hover; abre el menú de 5 acciones |
| Click derecho | Abre un `ContextMenu` con **los mismos** ítems del `⋮` |
| Fila activa | `bg-accent` + `font-medium` |
| Grip `⠿` | Solo en filas de Favoritos, `text-muted-foreground/40` → `group-hover:text-foreground`, `cursor-grab` |
| Truncado | El nombre trunca con `title` = nombre completo (los tableros se llaman `Adquirencia_2026_06_04...`) |
| Contador de Tableros | Total del server **menos** los pendientes |
| Toggle de orden | `ArrowDownAZ` / `ArrowUpZA`, solo visible si hay > 0 tableros, con tooltip |
| Sin acceso | Fila con `opacity-60`, botón deshabilitado, `title` = "Acceso restringido" |

## 2. Estados a incluir (para que el baseline sirva de referencia completa)

Un panel de control oculto (o query param `?state=`) que permita mostrar:

1. `ready` — 155 tableros, 12 pendientes, 5 favoritos (el caso de la captura).
2. `loading` — skeletons: 3 filas en las secciones, 5 en Tableros.
3. `error` — icono `AlertCircle`, mensaje "No se pudieron cargar los tableros", botón "Reintentar".
4. `empty` — "Sin tableros" + "Aquí verás los tableros creados." + CTA "＋ Nuevo tablero".
5. `no-results` — 'No se encontraron tableros para "xyz"'.
6. `search` — búsqueda activa con el filtro aplicado y el debounce simulado (300 ms).

## 3. Datos mock

Derivarlos de la captura para que el problema se vea de verdad:

- 155 tableros, la mayoría con el patrón `Adquirencia_2026_06_04_...` (nombres largos, casi indistinguibles → **esta es la evidencia visual del problema**).
- 12 en "Configuraciones pendientes", 5 favoritos (uno de ellos privado, con `Lock`).
- Mezcla de público/privado y 1–2 sin acceso.
- Mock en un `<script>` con un array plano; el mismo array lo consume la Etapa 6.

## 4. Cómo se construye

- Tailwind CDN + `design/tokens.css` con los nombres de variable de desyk → clases arbitrarias tipo `bg-[hsl(var(--sidebar-background))]` o un `tailwind.config` inline que mapee los tokens.
- Alpine.js para hover/menús/estados; Lucide vía CDN.
- Autocontenido, sin build. Scroll infinito simulado (cargar 20 más al llegar al final).

## 5. Definition of done

- [ ] `prototypes/00-baseline-tableros.html` abre sin build y se ve **indistinguible** de la captura al comparar lado a lado.
- [ ] Los 6 estados alcanzables desde el panel de control.
- [ ] Los menús `⋮` y de click derecho tienen los 5 ítems reales, con el mismo copy de `dashboards.main.json`.
- [ ] Hover revela pin y `⋮`; la fila activa se ve como en producción.
- [ ] Documentado en el README del proyecto como **"estado actual (antes)"**.

## 6. Riesgos

- **Sobre-construir:** es un baseline, no el prototipo final. Interacciones que no sean visibles en la captura o necesarias para el "antes" no van.
- **Perder densidad:** si el panel se ve más "aireado" que el real, el prototipo de carpetas va a mentir sobre cuánto cabe en pantalla — y la Ley de Miller es justamente el argumento del issue.
