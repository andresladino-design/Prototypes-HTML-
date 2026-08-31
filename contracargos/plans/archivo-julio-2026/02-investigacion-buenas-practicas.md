# Plan 2 — Investigar buenas prácticas y diversificar opciones

## Objetivo
Levantar patrones de mercado para gestión de disputas y experiencias agénticas, y llegar a la sesión con Andrea con **alternativas A/B comparables** (forma de trabajo habitual: investigar → presentar opciones → decidir juntos).

## Referencias a estudiar
1. **Chargeflow** (`app.chargeflow.io/prevent`, enviado por Andrea) — prioridad:
   - Desarmar el **ChargeScore** (la barra de porcentaje): qué comunica, cómo gradúa la confianza — pregunta abierta desde el 7-jul.
   - Cómo muestra dónde se pierde la disputa y el dinero recuperado.
   - Su modelo de automatización: qué corre solo vs. qué pide confirmación.
2. **Otros players del espacio:** Stripe Disputes/Radar, Adyen Dispute Management, Justt, Sift/Chargeback App, Verifi (Visa) y Ethoca (Mastercard) — cómo presentan evidencia, SLA y priorización.
3. **Patrones transversales:**
   - Colas de trabajo priorizadas por urgencia (SLA countdown) — patrones de triage tipo bandeja.
   - Scores de probabilidad con explicación (explainable AI): cómo mostrar un 91% de win probability sin sobreprometer.
   - Human-in-the-loop: umbrales de automatización y estados "corrió solo / requiere revisión".
   - Tableros financieros: relación KPI ↔ tabla ↔ detalle (aplicar skill ux-data-viz: barras apiladas sobre pies, metadata auditable).

## Actividades
1. Recorrer Chargeflow Prevent con capturas anotadas (qué adoptar, qué evitar).
2. Benchmark rápido de 3–4 competidores en las dimensiones: tablero, detalle de disputa, score, evidencia, automatización, canal de salida.
3. Sintetizar en una matriz comparativa por dimensión.
4. **Diversificar:** para cada decisión clave de UX, formular 2–3 opciones con pros/contras:
   - a) Ubicación: tab en Operation Center vs. vista propia del módulo de disputas
   - b) Score: numérico vs. barra tipo ChargeScore vs. categorías (alta/media/baja)
   - c) Automatización: agente corre solo sobre umbral vs. siempre pide confirmación vs. configurable
   - d) Canal de salida: export vs. API vs. vinculación de cuentas

## Entregables
- `handoff/benchmark-disputas.md` — matriz comparativa + capturas
- Tabla de alternativas A/B por decisión, lista para revisar con Andrea

## Done cuando
Cada decisión clave tiene ≥2 opciones documentadas con recomendación argumentada.
