# Plan maestro — Centro de Disputas (Contracargos)

**Fecha:** 9 jul 2026 · **Con:** Andrea Giraldo (Product Engineering Manager) · **Proyecto Ohana:** Disputas

## Contexto (fuentes: Slack DM + Granola 7-jul y 9-jul)

Andrea está montando el **agente de disputas** y pidió apoyo de UX porque "la interfaz no está chevere" (Slack, 24-jun). Hoy 9-jul compartió por DM:

- `Centro disputas.html` — su prototipo actual del centro de disputas (insumo a auditar)
- Figma board **"Ideación 2.9 — DO"** — mapa del flujo/ideación
- **app.chargeflow.io/prevent** — competidor de referencia (tiene "ChargeScore")

**El problema:** los adquirentes/PSP (ej. PayU, cliente activo) pierden disputas por vencimiento de SLA cuando el volumen es alto, y los merchants no alcanzan a colectar evidencia. 5 actores: tarjetahabiente → emisor → marca (Visa/Mastercard vía Verify/Mastercom) → PSP adquirente → merchant. **Foco de Simetrik: PSP adquirente y merchant.**

**Las 3 capas del producto acordadas:**
1. **Observabilidad** — tablero: disputas activas, por vencer <3 días, win rate por disputa, ratio VAMP, tabla de reclamos + gráficos (CBK por franquicia/moneda/semana, picos, anomalía por reason code)
2. **Operatividad** — agente que cruza conciliaciones Simetrik vs. data de marca, calcula win probability con explicación, prioriza por SLA/aging (visión: 9 agentes, del análisis hasta postear en Mastercom/Verify)
3. **Remediación** — canal de salida adquirente→merchant: export dataset / API GET / sandbox / vinculación de cuentas Simetrik (ideal, efecto de red). Restricción PCI: nada de email/texto plano.

## Los 5 planes y su orden de ejecución

| # | Plan | Archivo |
|---|------|---------|
| 1 | Entender el problema | `01-entender-el-problema.md` |
| 2 | Investigar buenas prácticas y diversificar opciones | `02-investigacion-buenas-practicas.md` |
| 3 | Auditar el Operation Center actual (patrones reutilizables) | `03-auditoria-operation-center.md` |
| 4 | Prototipo de la experiencia | `04-plan-prototipo.md` |
| 5 | User flows y sitemaps en Ohana (antes del prototipo) | `05-user-flows-sitemaps-ohana.md` |
| 6 | Análisis del prototipo de Andrea (conservar/rehacer/conflictos) | `06-analisis-prototipo-andrea.md` |
| 7 | Glosario del dominio (referencia transversal) | `07-glosario-disputas.md` |

**Orden de ejecución:** **6 (✅ hecho, 9-jul)** → 1 → 2 y 3 (en paralelo) → **5 (flows/sitemaps primero, para validar la interacción con Andrea)** → 4 (prototipo).

> El prototipo de Andrea (`prototipos/Centro disputas.html`) ya resuelve mucho: modelo de 4 roles, pipeline de 5 fases, reason codes y umbrales VAMP/ECM reales, flujo agéntico de 8 pasos con gate humano, ChargeScore y detalle de caso con cruce por ARN. Se conserva como **spec de contenido y UX**; el código se rehace sobre desyk. Detalles y 5 conflictos a validar en el plan 6.

## Decisiones tomadas (9-jul — la reunión "Disputas - Entendimiento" es la fuente de verdad)

1. **Emisor fuera de alcance** — el switch de 4 roles del proto de Andrea queda como material de visión/demo; producción diseña para PSP adquirente + merchant.
2. **Rol primario del prototipo: PSP adquirente** — el merchant entra como receptor en la capa de remediación, no como vista propia.
3. **Sin win rate agregado** — win probability solo por disputa, con explicación.
4. **Sin "$ recuperado" agregado** — solo recuperación estimada por disputa dentro del ChargeScore, con disclaimer.
5. **ChargeScore resuelto** — es el win probability (anillo + recuperación estimada + disclaimer), ya adaptado por Andrea de Chargeflow.

Detalle y trazabilidad en `06-analisis-prototipo-andrea.md`.

## Preguntas abiertas que atraviesan todos los planes

- ¿Dónde vive el centro de disputas en la UI: tab del Operation Center, tablero aparte o vista propia? (la tabla de control tiene esquema distinto al OC) → lo decide el Plan 3
- ¿Umbral de automatización del agente? (ej. win probability >80% → corre solo) — pendiente con Sergio y equipo de anomalías
- Monitoreo de disputas vía modelo de paquetes de notif-resumen (propuesta nuestra, resolución 5 del plan 6) — **confirmar con Andrea**
- ¿Cómo se comunican hoy adquirente y merchant fuera de Simetrik? (lo investiga Andrea)
- ¿El canal de salida coincide con la estrategia de negocio de Alejo?
- Copy: en notif-resumen se evitó la palabra "agente" de cara al usuario; validar si aquí aplica la misma convención.
