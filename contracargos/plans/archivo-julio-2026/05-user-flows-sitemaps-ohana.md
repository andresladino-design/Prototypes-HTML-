# Plan 5 — User flows y sitemaps en Ohana (antes del prototipo)

## Objetivo
Definir y validar la **interacción** en boards de Ohana (Moka) antes de escribir una línea del prototipo: qué ve cada actor, en qué momento y por qué camino — resolviendo la duda de navegación que quedó abierta el 9-jul («qué ve el usuario y en qué momento»).

## Estado actual en Ohana (9-jul, tarde)
✅ Los tres user flows están construidos en Moka:
- **«Flujo principal»** (`smrduvh8ua5j`, 11 nodos) — Flujo B: triage del analista del PSP, con decisión ¿disputar?, gate humano y envío a Mastercom/Verify.
- **«Agente de disputas — automatización»** (`smrdv4xkiqlq`, 11 nodos) — Flujo C: ingesta de marca → cruce → win probability → decisión por umbral (Sí: corre solo y notifica · No: subflow al triage del Flujo principal).
- **«Remediación — canal adquirente a merchant»** (`smrdv7lsgjoq`, 10 nodos) — Flujo D: gap de evidencia → validación PCI → ¿cuenta Simetrik? (Sí: vinculación · No: dataset o API) → merchant responde → vuelve al triage.

Pendiente: sitemap (espera veredicto del Plan 3), anatomía de pantallas clave (E), sesión de validación con Andrea sobre los boards. Nota: quedó un board duplicado vacío «Agente de disputas — automatización» (`smrdv203aso6`) por un conflicto de sync con el app — borrarlo desde la UI de Ohana.

## Método (memoria ohana-moka-workflow)
- Iniciar sesión con `ohana_status` y leer `ohana_flow_guide` antes de construir
- Usar solo tools de intención (`ohana_flow_add_step`, `add_branch`, `ohana_sitemap_add_page`) — nunca coordenadas; layout automático
- User flows: nodo `start` → pasos → decisiones (`kind:"decision"` + branches: verde=éxito, rojo=error/rechazo, azul=normal) → `end` en cada camino
- Pantallas reales como `kind:"page"/"modal"/"dialog"`; subflujos con `flowRef`
- Al existir el prototipo: `ohana_flow_set_proto` para el botón «Ver prototipo»

## Artefactos a construir

### A. Sitemap del Centro de Disputas
Jerarquía según el veredicto del Plan 3 (tab del OC vs. vista propia):
- Centro de disputas → Tablero (KPIs + gráficos) → Tabla de reclamos → Detalle de disputa → Panel del agente → Configuración (umbral de automatización, notificaciones) → Canal de salida

**Decisiones que acotan los flujos (9-jul, ver plan 6):** rol primario = analista del PSP adquirente; sin caminos del emisor; el flujo agéntico de 8 pasos del proto de Andrea es la primera hipótesis del Flujo 2, re-narrado desde el adquirente y en español.

### B. Flujo 1 — Triage del analista del PSP (flujo principal)
Entra al tablero → detecta disputas por vencer (<3 días) → abre la cola priorizada → revisa detalle con win probability y explicación → decisión: ¿disputar? → Sí: prepara evidencia/carta → envía (Mastercom/Verify vía agente) · No: acepta el contracargo → fin.

### C. Flujo 2 — El agente automatizado
Llega data de la marca → agente cruza contra conciliaciones → calcula win probability → decisión por umbral: sobre umbral → corre solo y notifica · bajo umbral → encola para revisión humana. Modela el human-in-the-loop que se validará con Sergio.

### D. Flujo 3 — Remediación adquirente → merchant
Disputa lista → decisión de canal (export / API / vinculación Simetrik) → validación de permisos PCI → merchant recibe/consulta → responde con evidencia → vuelve al flujo del PSP. (Ramas por escenario: merchant con cuenta Simetrik vs. sin cuenta.)

### E. (Opcional) Anatomía de pantallas clave
Para tablero y detalle de disputa: Página → Regiones → Secciones → Componentes (`ohana_flow_set_layout` + `ohana_flow_add_section`/`add_component`), conectando componentes accionables a sus destinos.

## Validación
1. Construir borradores de sitemap + flujos B y C
2. Sesión con Andrea sobre el board (comentarios vía Ohana) — contrastar contra su Figma «Ideación 2.9 — DO»
3. Iterar; el flujo D se detalla cuando haya decisión de canal de salida
4. Congelar flows → arranca el Plan 4 (prototipo)

## Done cuando
Andrea aprueba sitemap y flujos principales; cada camino tiene inicio y fin claros y las decisiones (umbral, canal) están modeladas aunque sus valores sigan abiertos.
