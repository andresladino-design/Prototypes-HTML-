# Design — Centro de Disputas

Basado en **desyk** (`@simetrikinc/desyk-components`), extraído de `dist/styles.css` y `tailwind-preset.cjs` del paquete real. Los prototipos usan Tailwind CDN + estas variables para fidelidad visual con producción.

## Principios

1. **Simetrik es una plataforma agentizada, no un Excel** — el análisis del agente (win probability, narrativa) es protagonista, no un adorno.
2. **Reutilizar patrones del Operation Center** antes de inventar UI nueva (tabs, tablas, badges, tableros).
3. **El SLA manda** — la urgencia (vence en <3 días) debe leerse de un vistazo: color + countdown, nunca solo texto.
4. **Explicable, no caja negra** — todo score (win probability) va acompañado de su razonamiento y metadata auditable.
5. **Datos financieros auditables** — valores con moneda explícita, PCI: tarjetas siempre enmascaradas (últimos 4).
6. **Barra de calidad**: Linear / Notion / Arc — denso pero calmado, sin ruido visual.

## Tokens

### Color (tema claro — valores desyk)

| Token | Valor | CSS var (HSL) | Uso |
|-------|-------|---------------|-----|
| background | #FFFFFF | `0 0% 100%` | Fondo de página |
| foreground | #18181B | `240 6% 10%` | Texto principal |
| primary | #3939F9 | `240 94% 60%` | Acciones principales, links, focus |
| primary-foreground | #FAFAFA | `0 0% 98%` | Texto sobre primary |
| secondary / muted | #F4F4F5 | `240 5% 96%` | Fondos suaves, hover, chips |
| muted-foreground | #8C8C8C | `0 0% 55%` | Texto secundario, labels |
| border / input | #D9D9D9 | `0 0% 85%` | Bordes, divisores |
| ring | #5285EF | `221 83% 63%` | Focus ring |
| card | #FFFFFF | `0 0% 100%` | Cards y widgets |

### Color semántico (estados de disputa y SLA)

| Token | Valor | CSS var | Uso en Disputas |
|-------|-------|---------|-----------------|
| success | #16A240 | `138 76% 36%` | Disputa ganada, win probability alta |
| warning | #C88A04 | `41 96% 40%` | SLA por vencer (<3 días), revisión pendiente |
| destructive | #DC2828 | `360 72% 51%` | SLA vencido, disputa perdida, errores |
| info | #2563EB | `221 83% 53%` | Estados informativos, en proceso |

### Color AI (narrativa del agente)

| Token | Valor | Uso |
|-------|-------|-----|
| ai-purple | #BD38FF | `280 100% 61%` — inicio del gradiente |
| ai-blue | #5487FC | `222 97% 66%` — fin del gradiente |
| ai-gradient-primary | `linear-gradient(90deg, ai-purple, ai-blue)` | Bordes/acentos de bloques generados por IA (win probability, narrativa, acciones recomendadas) |
| ai-gray-primary | #F0F2F9 | `228 33% 96%` — fondo suave de bloques AI |

### Tipografía

- **Familia:** `Inter, Roboto, sans-serif` (preset desyk); cargar Inter por CDN en prototipos.
- **Escala:** títulos de página 18–20/semibold · títulos de card 14/semibold · body 14/regular · tabla y metadata 13 · labels/captions 12 · KPIs grandes 28–32/semibold tabular-nums.
- **Números financieros:** siempre `tabular-nums`, moneda visible junto al valor.

### Spacing & radius

- **Radius base:** `0.5rem` (8px, `--radius` desyk). Cards y modales 8px; badges/chips full.
- **Spacing:** escala Tailwind de 4px. Padding de card 16–24px; gap entre widgets del tablero 16px.
- **Sombras:** mínimas; preferir bordes (`border`) sobre sombras, como el OC.

## Voz y tono

- Español, directo, sin alarmismo; la urgencia la comunica el diseño, no las mayúsculas.
- **Glosario Simetrik obligatorio:** Conciliación, Fuente, Espacio de trabajo, Repositorio.
- **Glosario del dominio:** disputa, contracargo (CBK), reason code, aging, SLA, win probability, ratio VAMP, pre-arbitration, arbitration, franquicia (Visa/Mastercard), adquirente, merchant.
- ⚠️ Pendiente validar: en notif-resumen el copy evita "agente"/"Agente IA" de cara al usuario. Definir con Andrea el término aquí (¿"análisis de disputas"?) antes del handoff.

## Patrones de componentes

- **KPI cards** (tablero): valor grande + label + delta; sin pie charts — barras apiladas para montos (regla ux-data-viz).
- **DataTable desyk** para la tabla de reclamos: sort, filtros multiselect, paginación; columna SLA con countdown y color semántico; columna win probability con barra de progreso.
- **Badge** para estados de disputa (nueva / en análisis / enviada / pre-arbitration / ganada / perdida) y para franquicia.
- **Tabs** (patrón OC) si el centro vive como tab del Operation Center; **underline-tabs** para sub-vistas.
- **Progress** para win probability: barra + porcentaje + link "ver razonamiento".
- **Bloque AI**: borde con `ai-gradient-primary`, fondo `ai-gray-primary`; contiene narrativa, razonamiento del score y acciones recomendadas como botones (patrón BADS de anomalías).
- **Empty states con forma**: mostrar la forma de los datos esperados + acción propuesta (skill ux-onboarding).
- **Dialog/Sheet** para el detalle de disputa ("carta": nº autorización, ABS, data de la marca, match con conciliación).

## Decisiones

- 2026-07-09 — design.md inicializado desde los tokens reales de desyk (`fe-solutions-mf/node_modules/@simetrikinc/desyk-components`), no valores inventados, para que el handoff mapee 1:1 con producción.
- 2026-07-09 — Los bloques generados por el agente usan el sistema AI de desyk (ai-purple→ai-blue) para distinguir contenido IA de datos duros, consistente con la estrategia agentizada del producto.
- 2026-07-09 — Semántica de SLA: warning = por vencer <3 días, destructive = vencido; alineada con las severidades del OC.
- 2026-07-09 — **Rol primario: PSP adquirente.** El emisor queda fuera de alcance (acuerdo reunión "Disputas - Entendimiento"); el switch de 4 roles del proto de Andrea es material de visión, no de producción. El merchant entra solo como receptor en la capa de remediación.
- 2026-07-09 — **Sin métricas agregadas descartadas:** ni win rate general ni "$ recuperado" en el tablero. La win probability y la recuperación estimada existen solo por disputa (ChargeScore), siempre con disclaimer "señal de priorización, no promesa".
- 2026-07-09 — El flujo agéntico de nuestro prototipo se narra desde el adquirente y en español (el de Andrea estaba en inglés y desde el emisor).
- 2026-07-09 — Monitoreo/alertas de disputas (SLA, distancia a umbral VAMP/ECM) se modelan como reglas del sistema de notificaciones de notif-resumen, no como sistema paralelo — pendiente confirmar con Andrea.
