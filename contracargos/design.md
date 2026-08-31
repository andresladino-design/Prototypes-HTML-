# Design — Contracargos (merchant)

Fuente de verdad de diseño del prototipo. Basado en **desyk** `@simetrikinc/desyk-components@1.30.0-0`, tokens extraídos de `dist/styles.css` y `dist/tailwind-preset.cjs` del paquete instalado en `fe-solutions-mf`. Nada de valores inventados: lo que está acá mapea 1:1 con producción.

Los prototipos usan Tailwind CDN + Alpine + Lucide, con estas variables declaradas en `:root`.

## Principios

1. **El merchant no viene a explorar, viene a frenar la sangría.** La pantalla abre con lo debitado y lo que hay que bloquear hoy. Explorar el histórico es secundario.
2. **Notificado y debitado no son el mismo dolor.** Notificado es prevención (todavía puedo hacer algo), debitado es pérdida consumada (esta es la plata que ya perdí). El diseño no los mezcla en un solo número.
3. **La tasa contra el umbral de red es un semáforo, no un KPI más.** Pasarse de VAMP o ECM trae sanción de la marca. Se muestra siempre la distancia al umbral, no solo el valor actual.
4. **Explicable, no caja negra.** Todo lo que infiere el motor (qué recurso es un chargeback, la severidad de una anomalía) va con su nivel de confianza y su razonamiento visible.
5. **Plataforma agentizada, no Excel.** El tablero llega armado; el usuario ajusta, no construye desde cero. Si una vista se siente "acá tienes 24 widgets, arma lo tuyo", hay que refactorizar.
6. **Auditable siempre.** Moneda explícita junto al valor, `tabular-nums`, fecha del corte visible. PCI: tarjetas enmascaradas a últimos 4, nunca PAN completo.
7. **Denso pero calmado.** Barra de calidad: Linear, Notion, Arc. Bordes antes que sombras, una sola acción primaria por vista.

## Tokens

### Color base (tema claro, desyk 1.30.0-0)

| Token | Hex | CSS var (HSL) | Uso |
|-------|-----|---------------|-----|
| background | `#FFFFFF` | `0 0% 100%` | Fondo de página |
| foreground | `#18181B` | `240 6% 10%` | Texto principal |
| card | `#FFFFFF` | `0 0% 100%` | Cards y widgets |
| card-foreground | `#09090B` | `240 10% 4%` | Texto en card |
| popover | `#FFFFFF` | `0 0% 100%` | Popovers y dropdowns |
| primary | `#3939F9` | `240 94% 60%` | Acción primaria, nav activa, links |
| primary-foreground | `#FAFAFA` | `0 0% 98%` | Texto sobre primary |
| secondary | `#F4F4F5` | `240 5% 96%` | Botón secundario, chips |
| muted | `#F4F4F5` | `240 5% 96%` | Fondos suaves, hover, zebra |
| muted-foreground | `#8C8C8C` | `0 0% 55%` | Texto secundario, labels, captions |
| accent | `#F4F4F5` | `240 5% 96%` | Hover de items de lista |
| border | `#D9D9D9` | `0 0% 85%` | Bordes y divisores |
| input | `#D9D9D9` | `0 0% 85%` | Borde de campos |
| ring | `#5285EF` | `221 83% 63%` | Focus ring |
| scroll | `#D3D6DA` | `216 8% 84%` | Scrollbar |

### Color de sidebar

| Token | Hex | CSS var | Uso |
|-------|-----|---------|-----|
| sidebar-background | `#FAFAFA` | `0 0% 98%` | Fondo del sidebar (light, nunca dark) |
| sidebar-foreground | `#3F3F46` | `240 5% 26%` | Texto de nav |
| sidebar-accent | `#F4F4F5` | `240 6% 96%` | Item hover / activo |
| sidebar-border | `#E4E4E7` | `240 6% 90%` | Divisores del sidebar |

### Color semántico

| Token | Hex | CSS var | Uso en contracargos |
|-------|-----|---------|---------------------|
| success | `#16A34A` | `138 76% 36%` | Reversión ganada, tasa bajo umbral, tarjeta bloqueada |
| warning | `#C68A04` | `41 96% 40%` | Cerca del umbral de red, notificado sin gestionar |
| destructive | `#DC2626` | `360 72% 51%` | Debitado, umbral roto, doble débito detectado |
| info | `#2563EB` | `221 83% 53%` | Estado informativo, en proceso |

### Color AI (bloques generados por el agente)

| Token | Valor | Uso |
|-------|-------|-----|
| ai-purple | `#BD38FF` · `280 100% 61%` | Inicio del gradiente |
| ai-blue | `#5487FC` · `222 97% 66%` | Fin del gradiente |
| ai-gray-primary | `#F0F2F9` · `228 33% 96%` | Fondo suave de bloque AI |
| ai-gray-secondary | `#DDE1EF` · `224 33% 91%` | Borde suave de bloque AI |
| ai-gradient-primary | `linear-gradient(90deg, ai-purple, ai-blue)` | Acento de bloque inferido / narrativa |
| ai-gradient-primary-border | mismo gradiente al 20% de opacidad | Borde de bloque AI |

Regla: el gradiente AI marca **lo que infirió el sistema** (clasificación de chargeback, causa de anomalía, confianza), nunca lo que el usuario configuró.

### Paleta de gráficos (chart-1 … chart-8, desyk)

| Token | Hex | CSS var |
|-------|-----|---------|
| chart-1 | `#6B9BF0` | `222 83% 69%` |
| chart-2 | `#A177F5` | `264 92% 70%` |
| chart-3 | `#7FE3C4` | `161 70% 67%` |
| chart-4 | `#7BD186` | `127 52% 62%` |
| chart-5 | `#89CDF0` | `201 82% 74%` |
| chart-6 | `#F5B96B` | `34 90% 69%` |
| chart-7 | `#F3C0A6` | `21 81% 82%` |
| chart-8 | `#E48793` | `354 71% 74%` |

Orden de uso: chart-1 en adelante. Categóricas cualitativas (franquicia, adquirente, reason code) usan esta paleta; los estados de negocio (notificado / debitado / revertido) usan **semánticos**, no la paleta de charts, porque significan algo.

### Tipografía

- **Familia:** `Inter` (preset desyk: `['Inter', 'ui-sans-serif', 'system-ui', ...]`). En prototipos, cargar por Google Fonts: `Inter:wght@100..900`.
- **Escala:** título de página 20/semibold · título de sección 16/semibold · título de card 14/semibold · body 14/regular · tabla y metadata 13 · label y caption 12 · KPI grande 28–32/semibold.
- **Números:** `font-variant-numeric: tabular-nums` en todo lo financiero (montos, conteos, porcentajes, SLA). Moneda siempre visible junto al valor, en `muted-foreground`.
- **Única excepción a la escala:** el hero del **Marketplace** (`Marketplace de templates`) usa un título de 32px. Es una superficie de catálogo, no de operación, y en producción se ve así. Ninguna otra pantalla pasa de 20px.
- ⚠️ **Los tamaños salen de esta escala, no de medir capturas de pantalla.** Una captura en retina duplica los píxeles y lleva a poner 34px donde van 20. Si hay que verificar contra producción, se lee el CSS del repo (`fe-solutions-mf`), no la imagen.

### Spacing y radius

- **Radius:** `--radius: 0.5rem` (8px). Cards, inputs y modales 8px; badges y chips full; el sidebar no lleva radius.
- **Spacing:** escala Tailwind de 4px. Padding de card 16–24px, gap de grid del tablero 16px, alto de fila de tabla 44px.
- **Sombras:** mínimas. Preferir `border` sobre `shadow`, como el Operation Center. Sombra solo en overlays (popover, sheet, dialog).
- **Botones:** altura ~30px (`h-[30px]` en producción), texto 12.5px, padding 8–9px × 13px. Un botón a ancho completo sigue teniendo esa altura: **nunca se convierte en un bloque de 50px+**.

## Voz y tono

Español, directo, sin alarmismo. La urgencia la comunica el color y la posición, nunca las mayúsculas ni los signos de admiración.

**Glosario Simetrik obligatorio** (no se traduce ni se sinonimiza): Conciliación, Fuente, Asiento contable, Período contable, Espacio de trabajo, Repositorio, Dataset, Tablero, Anomalía, Incidente, KPI.

**Glosario del dominio (merchant):**

| Término | Qué es |
|---|---|
| Contracargo (CBK) | El reverso que el adquirente le hace al marketplace |
| Notificado | El adquirente avisa que va a debitar. Todavía se puede gestionar |
| Debitado | El adquirente ya descontó la plata. Pérdida consumada |
| Reversión | El contracargo se revierte a favor del merchant |
| Doble débito | El mismo contracargo descontado dos veces (liquidación + refund) |
| Reason code | Código de la marca que explica el motivo (10.4, 13.1, 4837, C08) |
| Tasa de contracargos | CBK / transacciones del período, medida por red |
| VAMP / ECM | Programas de umbral de Visa y Mastercard. Romperlos trae sanción |
| Adquirente | Quien procesa y emite los archivos de contracargo |
| Franquicia | Visa, Mastercard, Amex |

**Términos prohibidos en la UI:** "dashboard" (es Tablero), "reconciliación" (es Conciliación), "workspace" (es Espacio de trabajo), "chargeback" en labels de cara al usuario (es Contracargo; se admite "CBK" en columnas estrechas).

⚠️ **Pendiente de definición:** en el trabajo de notificaciones se acordó que el copy de cara al usuario **no dice "agente" ni "Agente IA"**, usa "monitoreo". Confirmar con Andrea si acá aplica lo mismo antes del handoff. Mientras tanto el prototipo dice "monitoreo".

## Patrones de componentes

- **Encabezado de tablero:** título + "N conjuntos de datos usados" + acciones a la derecha. El botón de Monitoreo muestra su estado como pill dentro del propio botón (`Monitoreo · Activado`), patrón ya existente en el Operation Center.
- **KPI card:** valor grande tabular + label + contexto auditable (contra qué se compara, de qué corte es). Prohibido el patrón SaaS "número grande + flecha verde + sparkline" sin contexto.
- **Semáforo de umbral de red:** por franquicia, una fila con `nombre · programa (VAMP/ECM) · operador ≤ · valor actual · umbral`, y debajo la distancia en puntos. Verde bajo umbral, warning cerca, destructive roto.
- **Tabla de contracargos:** DataTable desyk. Sort, filtros multiselect, paginación. Columna de estado con Badge semántico, columna de monto tabular con moneda, reason code como chip.
- **Badge de estado:** Notificado (warning suave), Debitado (destructive suave), Revertido (success suave), Doble débito (destructive sólido, es un hallazgo).
- **Bloque AI:** borde `ai-gradient-primary-border`, fondo `ai-gray-primary`, contiene la narrativa, la confianza y las acciones recomendadas como botones. Es el mismo patrón de las anomalías de BADS, no se inventa uno nuevo.
- **Chat:** botón persistente en SidebarFooter que abre Sheet lateral. Nunca burbuja flotante, nunca modal centrado.
- **Detalle de caso:** Sheet lateral por defecto. Dialog solo si la tarea exige atención modal.
- **Empty state con forma:** mostrar la forma del dato esperado (las columnas que va a traer el archivo de notificados) más la acción propuesta, no un ícono gris con "no hay datos".
- **Línea de vida del contracargo:** timeline horizontal con nodos fechados (PAYIN → Notificado → Debitado → Reversión) y el movimiento de fondos en cada uno. Solo se dibuja si las llaves de cruce permiten encadenar; si no, se degrada a los estados que sí existen.

## Bans (además de los de desyk y simetrik-ui)

- Side-stripe de color en cards. Usar fondo tintado o ícono leading.
- Gradient text.
- Sidebar dark con main light. Todo el shell es light.
- Sparkle ✨ y badges "Powered by AI".
- Hex sueltos fuera de estos tokens.
- Em-dash (—) en copy de UI. En documentos internos sí se usa.
- Doble scroll vertical anidado.
- Pie charts para composición de montos. Barras apiladas.

## Decisiones

- 2026-08-26 — `design.md` inicializado desde los tokens reales de `desyk-components@1.30.0-0` (`fe-solutions-mf/node_modules`), incluyendo la paleta `chart-1..8` que faltaba en la versión de julio de `plans/archivo-julio-2026/design-julio-2026.md`.
- 2026-08-26 — Rol primario del prototipo pasa de PSP adquirente (acuerdo 9-jul) a **merchant / marketplace**, por el reacote de la sesión del 26-ago. **Decidido por Andres**, se le comunica a Andrea.
- 2026-08-26 — Notificado y debitado se tratan como dos lecturas separadas, no como un total agregado. Es la distinción que Andrea marcó como la más álgida para el marketplace.
- 2026-08-26 — Los estados de negocio usan color semántico, no la paleta de charts, para que el color signifique lo mismo en el tablero y en la tabla.
- 2026-08-26 — Umbrales de red corregidos: Visa VAMP ya no es 2.20%, bajó a **1.50%** el 1-abr-2026. VAMP y ECM comparten el 1.5% pero con fórmulas distintas (VAMP incluye fraude TC40), así que se modelan por separado.
- 2026-08-28 — Corregido el detalle del template: estaba construido midiendo píxeles de una captura en retina (título 34px, botón de 56px de alto, body 16.5px). Se rebajó todo a la escala de este documento. **La escala manda sobre la medición.**
- 2026-08-26 — Primer prototipo sobre estos tokens en `prototypes/contracargos-merchant.html` (Tailwind CDN + Alpine + Lucide). El proto de Andrea queda como insumo de contenido, no se edita.
- 2026-08-26 — El top nav usa los **5 tabs reales de producción** (Tableros, Anomalías, Pendientes, Almacenamiento, Asientos contables), verificados en `fe-solutions-mf/.../mainLayout/constants.ts`. **No existe un tab "Disputas"**; crearlo sería una decisión de producto, no de diseño.
- 2026-08-26 — Los tabs del top nav son **píldoras circulares** (`TabsList shape="circle"`), no subrayados. Los botones del header del tablero son de `h-[30px]`.
- 2026-08-28 — **El tablero no tiene estado de configuración pendiente.** Instalado el template, queda usable: las fuentes de los marketplaces ya están integradas (caso de fuentes preintegradas). Se descarta el patrón de mock data + banner "Pending Setup" + widgets `Locked` que se había adoptado el 26-ago; sigue siendo válido para templates que piden archivos, pero no para este.
