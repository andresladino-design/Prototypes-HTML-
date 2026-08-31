# Plan 1 — Entender el problema

## Objetivo
Consolidar un entendimiento compartido y documentado del dominio de disputas/contracargos: actores, flujo, dolores por actor y alcance de Simetrik, para que todas las decisiones de diseño se anclen ahí.

## Insumos
- Transcript Granola: "Disputas - Entendimiento" (9-jul) y "Contracargos — flujo, operación y tablero" (7-jul)
- Figma board "Ideación 2.9 — DO" de Andrea (mapa del flujo)
- `Centro disputas.html` compartido por Andrea (refleja su modelo mental actual)
- Datos de la POC de volumen de contracargos (Andrea quedó de compartirlos)
- Caso PayU como cliente ancla

## Actividades
1. **Mapear el flujo end-to-end** con los 5 actores (tarjetahabiente, emisor, marca, PSP adquirente, merchant) y las fases: reclamo → clasificación por la marca → notificación al PSP → débito al merchant → decisión → pre-arbitration → arbitration. Contrastar contra el board de Figma de Andrea.
2. **Documentar dolores por actor** (foco PSP y merchant):
   - PSP: pierde disputas por vencimiento de SLA con volumen alto; debe clasificar y notificar al merchant a tiempo.
   - Merchant: no le queda tiempo para colectar evidencia; es quien pierde el dinero.
3. **Delimitar alcance:** emisor queda fuera (complejidad). Anotar explícitamente qué NO se diseña.
4. **Glosario del dominio:** ✅ hecho — ver `07-glosario-disputas.md` (actores, ciclo de vida, identificadores ARN/AUTH/BIN, programas de red, métricas y términos Simetrik). Queda validarlo con Andrea y pasar el copy por /ux-writer.
5. **Listar los datos disponibles:** conciliaciones Simetrik del adquirente + archivos de marca (Mastercard/Visa) con estados y códigos. Identificar el gap: comunicación adquirente↔merchant fuera de la plataforma.
6. **Sesión de validación con Andrea** (30 min): revisar el mapa y cerrar dudas del flujo.

## Entregables
- `handoff/entendimiento-problema.md` — flujo, actores, dolores, alcance, glosario
- Lista de preguntas cerradas vs. abiertas (alimenta el plan maestro)

## Done cuando
Andrea confirma que el mapa refleja el flujo real y no quedan ambigüedades sobre actores ni alcance.
