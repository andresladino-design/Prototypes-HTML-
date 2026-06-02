---
epic: MONITOR_INGESTA
issue_type: Feature
priority: P2
estimate: S
labels: [ux, frontend, monitoring, onboarding, dashboard]
depends_on: []
blocks: [02-vista-monitoreo]
component_areas: [shell, dashboard]
---

# 01 · Entrada al monitoreo desde el tablero (banner + botón de modo)

> Cómo se entra al monitoreo de un tablero. El monitoreo es un **modo** del mismo tablero (ver `02-vista-monitoreo`), no una página aparte. Hay **3 entradas** desde la vista `currentView === 'dashboard'`. La principal pedagógica es el banner promocional encima del grid; las otras dos son persistentes (botón en el header y item en el menú contextual del tablero).

## Resumen

- **Quién lo ve**: usuarios que abren un tablero donde el monitoreo todavía no está activo (`!monitoringActive`). El banner se puede descartar (`dashBannerDismissed`); las otras dos entradas (botón header + menú ⋮) son siempre visibles.
- **Cuándo**: al abrir el tablero. El banner es un push pedagógico de activación; las otras dos entradas están siempre disponibles para entrar/salir del modo.
- **Qué decisión habilita**: empezar a configurar el monitoreo de la ingesta y las métricas del tablero, o posponerlo si el tablero fue modificado recientemente.
- **Por qué existe**: el monitoreo necesita ver datos estables para aprender qué es lo normal. El banner cambia su tono según si el tablero está estable o fue modificado hace poco. El **estado del monitoreo** ("Sin configurar" / "Monitoreando") vive como badge en el **botón "Monitoreo" del header** (ver Entradas, abajo).

> **Nota de implementación**: el banner verde de confirmación `tm-dash-secured` (estado "Monitoreado") está **diseñado en CSS pero NO implementado en el HTML** (no se renderiza ningún elemento con esa clase). El estado se comunica hoy vía el badge del botón "Monitoreo". Mantener `tm-dash-secured` como propuesta pendiente, no como algo presente en el prototipo.

## Entradas al monitoreo (3)

Las tres llevan a `currentView = 'tablero-monitoreo'` con `tmTab = 'metricas'`. El tab global "Tableros" del header superior queda activo; no hay breadcrumb.

| Entrada | Dónde | Selector / trigger | Notas |
|---|---|---|---|
| **Botón de modo** (principal, persistente) | Cluster de acciones del header del tablero, anclado al **borde derecho** | `.secondary-btn` con `@click="currentView = 'tablero-monitoreo'; tmTab = tmTab \|\| 'metricas'"`; label "Monitoreo" + badge de estado `.tm-card-badge` ("Sin configurar" / "Monitoreando") | Es el mismo botón que en modo monitoreo se transforma en "Volver al tablero" (ver `02`). Lleva el estado del monitoreo. Es el último elemento del cluster para quedar fijo cuando las demás acciones se ocultan |
| **Banner promocional** (pedagógico, descartable) | Encima del grid de gráficos | `.tm-banner.col-span-3`, `x-show="!monitoringActive && !dashBannerDismissed"` | Push de activación. 2 variantes (estable / recién modificado). Detalle abajo |
| **Menú contextual del tablero** (⋮) | Item del menú del tablero en el panel izquierdo | `.dashboard-menu-item` con `@click="currentView = 'tablero-monitoreo'; tmTab = 'metricas'; closeDashboardMenu()"` | Atajo desde la lista de tableros |

## Anatomía

> Esta sección detalla el **banner promocional**. El botón de modo del header se documenta arriba (Entradas) y su contraparte "Volver al tablero" en `02-vista-monitoreo`.

| Componente | Clase / selector | Función |
|---|---|---|
| Contenedor banner | `.tm-banner.col-span-3` | Bloque ancho tres columnas en el grid del tablero |
| Cerrar | `.tm-banner-close` | Descarta el banner (set `dashBannerDismissed = true`) |
| Stack de iconos | `.tm-banner-icon-stack` (back + front + dot) | Composición visual con sombra y punto AI |
| Texto | `.tm-banner-text` con `.tm-banner-title` y `.tm-banner-subtitle` | Título y subtítulo educativo |
| CTA | `.tm-banner-cta` con `.tm-banner-cta-icon` | Botón primario que lleva al monitoreo |
| Banner de éxito ⚠️ **NO implementado** | `.tm-dash-secured` + `.tm-dash-secured-icon` + `.tm-dash-secured-link` | Reemplazo propuesto cuando `monitoringActive === true`. Solo existe el CSS; no hay markup que lo renderice. Hoy el estado se ve en el badge del botón "Monitoreo" |

## Estados

| Estado | Condición | Visual |
|---|---|---|
| **Estable** | `!monitoringActive && !dashboardRecentlyModified` | Icono de gráfico de líneas. Title "Buen momento para empezar a monitorear". CTA "Empezar a monitorear". |
| **Recién modificado** | `!monitoringActive && dashboardRecentlyModified` | Icono de reloj. Title "Dale unos días antes de monitorear este tablero". CTA "Configurar de todos modos". |
| **Descartado** | `dashBannerDismissed === true` | Banner oculto. Las otras 2 entradas (botón header, menú ⋮) siguen visibles. |
| **Monitoreado** | `monitoringActive === true` | El banner promocional no se muestra. El estado "Monitoreando" se ve en el badge del botón "Monitoreo" del header. *(El banner verde `tm-dash-secured` está propuesto pero NO implementado.)* |

Máquina de estados:

```
ESTABLE ────────────► (click CTA / botón header / menú ⋮) ──► modo monitoreo
RECIEN_MODIFICADO ──► (click CTA / botón header / menú ⋮) ──► modo monitoreo
ESTABLE / MOD ──────► (close X)                            ──► DESCARTADO (botón header y ⋮ siguen)
MONITOREADO ────────► estado en el badge del botón "Monitoreo"
```

## Flujos de usuario (Experience-Driven User Story)

**Flujo A · Activar monitoreo desde tablero estable**
- **Como** usuario del tablero
- **Quiero** entender que es un buen momento para monitorear y entrar al flujo de configuración
- **Para** asegurarme de que cualquier desvío futuro me sea notificado
- **Camino**:
  1. Abro el tablero. Veo el banner con icono de gráfico, title "Buen momento para empezar a monitorear" y CTA "Empezar a monitorear".
  2. Hago click en el CTA. La app navega a `tablero-monitoreo` con `tmTab = 'metricas'`.

**Flujo B · Pospuesta por cambios recientes**
- **Como** usuario que acaba de editar el tablero
- **Quiero** saber por qué no es ideal empezar a monitorear ahora
- **Para** decidir si igual configuro o si espero
- **Camino**:
  1. Abro el tablero. Veo el banner con icono de reloj y texto "Cambiaste sus gráficos o los datos que lo alimentan hace pocos días".
  2. Si decido continuar, hago click en "Configurar de todos modos" y entro al monitoreo. Si no, cierro con la X.

## Interacciones

| Trigger | Resultado | Side effects |
|---|---|---|
| Click en botón "Monitoreo" del header (`.secondary-btn`) | Entra al modo: `currentView = 'tablero-monitoreo'`, `tmTab = tmTab \|\| 'metricas'` | Aparece glow azul, se ocultan acciones de tablero, el botón pasa a "Volver al tablero" |
| Click en item "Monitoreo" del menú ⋮ (`.dashboard-menu-item`) | Igual que arriba + `closeDashboardMenu()` | — |
| Click en `.tm-banner-cta` | Navega a `tablero-monitoreo` y selecciona `tmTab = 'metricas'` | Cambia `currentView` y `tmTab` |
| Click en `.tm-banner-close` | Oculta el banner | `dashBannerDismissed = true` |
| Click en `.tm-dash-secured-link` ⚠️ **no implementado** | (propuesto) navegaría a `tablero-monitoreo` | El elemento no existe en el HTML |
| Cambio en `monitoringActive` | Cambia el badge del botón "Monitoreo" (Sin configurar ↔ Monitoreando) | Re-render por Alpine |

## Data contracts

Necesario para renderizar:

- `monitoringActive: boolean` (cliente o BE) indica si al menos una fuente o métrica del tablero está siendo monitoreada.
- `dashboardRecentlyModified: boolean` derivado de la fecha del último cambio en gráficos o datasets (umbral sugerido: 7 días).
- `dashBannerDismissed: boolean` (puede persistirse por usuario o por sesión).

Endpoint sugerido: `GET /dashboards/{id}/monitoring-summary` que devuelva `{ monitoring_active, recently_modified, last_modified_at }`.

## Edge cases

- **Sin datos**: si no se conoce `dashboardRecentlyModified`, default a `false` (estable).
- **Cargando**: ocultar el banner hasta resolver `monitoringActive` para evitar parpadeo.
- **Tablero recién creado sin gráficos**: si el grid está vacío, no mostrar banner.
- **Usuario sin permisos para activar monitoreo**: el CTA debería estar deshabilitado o redirigir a una vista de solicitud (no resuelto en el prototipo).

## Empty states (importante)

El prototipo HTML actual solo tiene algunos empty states. Esta historia debe enumerarlos para que el implementador los considere.

| Escenario | Condición | Copy propuesto | CTA | Implementado en HTML? |
|---|---|---|---|---|
| Loading inicial | `monitoringActive === undefined` mientras resuelve fetch | No renderizar banner (evita parpadeo) | (ninguno) | ❌ pendiente |
| Tablero sin gráficos | Grid vacío | No mostrar banner | (ninguno) | ❌ pendiente |
| Sin permisos para activar | `user.canActivateMonitoring === false` | "No tienes permiso para activar el monitoreo de este tablero." | Link "Solicitar acceso" | ❌ pendiente |
| Error de red al cargar `monitoring-summary` | Fetch falló | "No pudimos verificar el estado del monitoreo." con icono `alert-triangle` ámbar | Botón "Reintentar" | ❌ pendiente |
| Tablero recién creado | `created_at < 24h` | Variante del estado "Recién modificado" con copy "Dale unos días para acumular datos." | "Configurar de todos modos" | ❌ pendiente |
| Estado descartado en sesión anterior | `dashBannerDismissed === true` persistido | Banner oculto. No mostrar siquiera el verde de éxito (decisión del producto) | (ninguno) | ❌ pendiente |

**Nota para el implementador**: si encuentras un escenario que esta tabla no menciona, agregalo al ticket antes de implementar.

## Edge cases (validación)

- Sin datos de `dashboardRecentlyModified`: default a `false` (estable).
- Loading: ocultar el banner hasta resolver `monitoringActive` para evitar parpadeo.
- Tablero recién creado sin gráficos: no mostrar banner.
- Cambio de `monitoringActive` en runtime: el banner promocional debe reemplazarse por el verde sin recargar.
- Texto del CTA en idioma diferente: verificar que no rompa el layout `.tm-banner-cta`.

## Componentes desyk a usar

> Mapeo del prototipo HTML a los componentes oficiales del design system desyk
> (basado en shadcn/ui). El implementador debe reusar estos componentes en lugar
> de replicar las clases CSS custom del prototipo.

| Elemento del prototipo | Componente desyk | Variants / props | Notas de uso |
|---|---|---|---|
| `.tm-banner` (contenedor banner promocional) | `Alert` + `AlertTitle` + `AlertDescription` | `variant="default"` con override para fondo violeta tenue | Bloque ancho `col-span-3` en el grid del dashboard |
| `.tm-banner-close` (X de descarte) | `Button` | `variant="ghost" size="icon"` con ícono `X` de Lucide | Acción de cerrar el banner |
| `.tm-banner-cta` (CTA "Empezar a monitorear" / "Configurar de todos modos") | `Button` | `variant="default" size="default"` con ícono trailing | Acción primaria que navega al monitoreo |
| `.tm-banner-icon-stack` (stack visual con sombra y dot AI) | Componente custom (compuesto) | — | Composición decorativa con SVGs apilados |
| `.tm-dash-secured` (banner verde de éxito) | `Alert` | `variant="default"` con override para fondo `success` | Reemplaza el banner promocional cuando hay monitoreo activo |
| `.tm-dash-secured-icon` (escudo verde) | Ícono `ShieldCheck` de Lucide | — | Identidad visual del estado monitoreado |
| `.tm-dash-secured-link` ("Ver monitoreo") | `Button` | `variant="link"` | Navega a la vista de monitoreo |

**Componentes compuestos (no existen en desyk, hay que componerlos):**
- `DashboardMonitoringBanner` — wrapper que decide entre el banner promocional y el banner de éxito según `monitoringActive`. Combina `Alert` + stack de íconos custom + `Button` (CTA o link).
- `BannerIconStack` — composición visual con tres capas SVG (back + front + dot violeta AI). No corresponde a un componente desyk; construirlo en el feature.

**Referencias:**
- Repo desyk: `~/Simetrik/desyk-components` (read-only).
- Lista oficial de componentes shadcn/ui que desyk extiende.

## Implementation notes

- **Helpers Alpine ya existentes** a reusar: `currentView`, `tmTab`, `dashBannerDismissed`.
- **CSS/clases**: `.tm-banner`, `.tm-banner-cta`, `.tm-banner-icon-stack`, `.tm-dash-secured` (ya existen).
- **Endpoints BE** que esta historia necesita: `GET /dashboards/{id}/monitoring-summary` devolviendo `{ monitoring_active, recently_modified, last_modified_at }`.
- **Tokens desyk**: `hsl(var(--primary))` para CTA y stack icons, `hsl(var(--success))` para banner monitoreado, `hsl(var(--ai-purple))` para dot del icon stack.
- **Animation / motion**: transición opacity + transform 200ms ease-out al aparecer y al descartar.

## Out of scope

- Persistencia server-side de `dashBannerDismissed` (queda en cliente por ahora).
- Variante para multi-tablero (banner global de workspace).
- Vista de error 403 con detalle por permiso.
- A/B testing de copy.

## Criterios de aceptación

1. **Given** un tablero sin monitoreo activo y estable, **When** el usuario lo abre, **Then** se muestra el banner con title "Buen momento para empezar a monitorear".
2. **Given** el mismo tablero con `dashboardRecentlyModified = true`, **When** el usuario lo abre, **Then** el title es "Dale unos días antes de monitorear este tablero" y el CTA dice "Configurar de todos modos".
3. **Given** el banner visible, **When** el usuario hace click en la X, **Then** el banner se oculta y `dashBannerDismissed` queda en `true`.
4. **Given** el banner visible, **When** el usuario hace click en el CTA, **Then** la vista cambia a `tablero-monitoreo` con `tmTab = 'metricas'`.
5. **Given** `monitoringActive === true`, **When** se renderiza el dashboard, **Then** el badge del botón "Monitoreo" del header dice "Monitoreando" y el banner promocional no se muestra. *(El banner verde `tm-dash-secured` queda como propuesta, no implementado.)*
6. El banner ocupa tres columnas del grid (`col-span-3`).
7. **Given** el dashboard, **Then** existen 3 entradas al monitoreo: botón "Monitoreo" (header, con badge de estado), banner promocional (descartable) e item "Monitoreo" del menú ⋮. Descartar el banner no oculta las otras dos.
8. Los textos no deben usar em-dashes ni slang regional (verificar copy contra glosario).

## Dependencies

- **Depende de**: ninguna (es la puerta de entrada).
- **Bloquea a**: `02-vista-monitoreo` (el CTA lleva ahí).
- **Relacionado con**: `00-CONTEXT.md` (glosario).

## Verification (cómo probarlo)

1. Abrir `index.html` y navegar al tablero (`currentView = 'dashboard'`).
2. Forzar `monitoringActive = false` y `dashboardRecentlyModified = false` en Alpine devtools. Verificar copy "Buen momento para empezar a monitorear".
3. Forzar `dashboardRecentlyModified = true`. Verificar copy "Dale unos días antes de monitorear este tablero" y CTA "Configurar de todos modos".
4. Hacer click en el CTA. Verificar navegación a `tablero-monitoreo` con `tmTab === 'metricas'`.
5. Hacer click en la X. Verificar `dashBannerDismissed = true` y banner oculto.
6. Forzar `monitoringActive = true`. Verificar que el badge del botón "Monitoreo" del header pasa a "Monitoreando" y el banner promocional desaparece. *(El banner verde `tm-dash-secured` no se renderiza: no está implementado.)*
7. Probar el banner en viewport angosto (< 1024px) para verificar `col-span-3` no rompa layout.

## References

- **HTML** (ubicar por selector): banner `<div class="tm-banner col-span-3" x-show="!monitoringActive && !dashBannerDismissed">`; botón de modo del header `<button class="secondary-btn" @click="currentView = 'tablero-monitoreo'; tmTab = tmTab || 'metricas'">` (con `.tm-card-badge`); item del menú `<div class="dashboard-menu-item" @click="currentView = 'tablero-monitoreo'; ...">`.
- **CSS** (por selector): `.tm-banner`, `.tm-banner-icon-stack`, `.tm-banner-cta`, `.tm-card-badge`. `.tm-dash-secured` existe en CSS pero sin markup (no implementado).
- **Figma**: (pendiente de link)
- **Docs hermanos**: `[00-CONTEXT.md](./00-CONTEXT.md)`, `[02-vista-monitoreo.md](./02-vista-monitoreo.md)`.
- **Backend**:
  - Op-center: `~/Simetrik/op-center-backend/apps/anomaly_configs/` (config wrapper).
