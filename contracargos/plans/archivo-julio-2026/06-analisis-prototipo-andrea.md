# Plan 6 — Análisis del prototipo de Andrea (`Centro disputas.html`)

**Insumo:** `prototipos/Centro disputas.html` (compartido por Slack el 9-jul, 2.025 líneas, autocontenido, vanilla JS sin Tailwind ni frameworks). Este documento registra QUÉ ya resolvió Andrea, qué conservamos, qué rehacemos y qué contradice lo acordado en las reuniones.

## Qué contiene (inventario)

**Vistas:** shell de Simetrik (sidebar + tabs de producto) → tab **Tableros** (dashboard editable) y tab **Disputas** (pipeline + tabla) → **detalle de caso** (3 sub-tabs: Línea de vida · Análisis del agente · Desglose/cruce) → **flujo agéntico animado** de 8 pasos → **modal de Monitoreo inteligente** (wizard 3 pasos con umbrales VAMP/ECM) → panel "Agregar gráfico" (catálogo de 24 widgets).

**Datos:** 4 roles conmutables (Issuer / Merchant / PSP / Adquirente), cada uno con 5 KPIs + gráficos propios; 10 disputas mock ricas (reason codes reales de Visa/MC/Amex, ARN, AUTH, BIN, SLA, ChargeScore); 6 agentes nombrados (Reconciliation, Intake, Validation, Representment Analysis, Pre-Arbitration con gate humano, Filing → postea en Mastercom); estados Vinculado/Requiere/Ganado/Perdido/Por presentar; 5 fases de pipeline.

## ✅ Conservar (es la spec de contenido y UX, no de código)

| Qué | Por qué |
|-----|---------|
| **Modelo conceptual completo**: roles, 5 fases del pipeline, estados, reason codes reales, umbrales VAMP 2.20%→1.50% (1-abr-2026) y ECM/HECM | Es el activo más valioso; conocimiento de dominio ya validado por Andrea |
| **Flujo agéntico de 8 pasos** con gate humano ("nothing is filed without your approval"), memo legal y win probability progresiva (45→91%) | Define la narrativa del agente y el human-in-the-loop; base directa para el Flujo 2 de Ohana |
| **Detalle de caso**: línea de vida del contracargo (PAYIN→TC40→Notificado→Debitado→2ª Presentación), análisis por agente con % de confianza y chip AI/determinístico, tabla de cruce (ARN+AUTH) | Coincide con la "carta" estructurada acordada el 9-jul y con el principio "explicable, no caja negra" |
| **ChargeScore resuelto**: anillo con score + recuperación estimada + tiempo/OPEX ahorrado + disclaimer "señal de priorización, no promesa" | Responde la pregunta abierta del 7-jul: Andrea ya adaptó el patrón de Chargeflow |
| **Wizard de monitoreo** con cálculo de "distancia para romper el umbral" de red | Lógica valiosa; conecta con el trabajo de anomalías/notif-resumen |
| **Copy y glosario**: representment, pre-arbitration, double-dip, TC40, Verifi/Ethoca, ISO 8583/mensaje 1442, Mastercom | Alimenta directamente el glosario del Plan 1 y el design.md |
| **Estética**: claro, tipo Linear/Notion, índigo ≈ desyk, Inter, tabular-nums | Ya alineada con nuestra identidad; validar detalles contra tokens desyk |

## 🔄 Rehacer (el código es spec visual, no base)

| Qué | Cómo |
|-----|------|
| Todo el render (vanilla JS + innerHTML, SVG artesanal) | Reconstruir con nuestra convención: Tailwind CDN + Alpine + tokens desyk |
| Idioma mixto (dashboard en español, flujo agéntico 100% en inglés) | Unificar en español con el glosario del design.md |
| Dos modelos de datos duplicados para tablas (`DATA[role].rows` vs `DISPUTES`) con esquemas distintos | Un solo modelo de disputa canónico |
| Azul de gráficos `#3b63e6` ≠ primary desyk | Paleta ux-data-viz sobre tokens desyk |
| Gráficos SVG a mano | Patrones de chart de desyk/OC |
| Sidebar, lista de 155 tableros y tabs decorativos | Depende del veredicto de ubicación (Plan 3): solo se recrea el shell necesario |

## ✅ Conflictos RESUELTOS — la reunión del 9-jul ("Disputas - Entendimiento") es la fuente de verdad

El prototipo de Andrea es anterior al entendimiento de hoy; donde chocan, **mandan los acuerdos de la reunión**:

1. **Rol Emisor → FUERA de alcance.** El 9-jul se acordó explícitamente dejar al emisor fuera por complejidad; foco = PSP adquirente + merchant. El switch de 4 roles y la narrativa del flujo agéntico desde el emisor ("intelligence layer on both sides") quedan como **material de visión/demo comercial**, no entran al diseño de producción. Nuestro prototipo no incluye vista de emisor.
2. **Win rate agregado → SE ELIMINA.** Descartado el 9-jul. El win rate solo existe **por disputa individual** (win probability con explicación). Los KPIs "Win rate 58%" y la proyección "+26 pts con Simetrik" del proto no pasan al tablero.
3. **"Recuperado $214K" → SE ELIMINA del tablero.** La plata recuperada se descartó como no calculable a nivel agregado. La **recuperación estimada por disputa** (dentro del ChargeScore, es una predicción del agente, no un dato contable) sí se conserva, con su disclaimer.
4. **Rol primario → PSP adquirente.** Es quien vive el dolor central (pierde disputas por SLA con volumen alto) y para quien se definieron los KPIs del tablero. El **merchant** aparece como receptor en la capa 3 (canal de salida/remediación), no como vista propia en esta fase.
5. **Monitoreo inteligente → reutiliza el modelo de notif-resumen.** No se diseña un sistema de monitoreo paralelo: las alertas de disputas (SLA por vencer, distancia al umbral VAMP/ECM) se modelan como **paquetes/reglas por usuario** del sistema de notificaciones ya diseñado. La lógica de "distancia para romper el umbral" del wizard de Andrea se conserva como tipo de regla. *(Propuesta derivada de convenciones existentes, no discutida explícitamente el 9-jul — confirmar con Andrea en la próxima sesión.)*

### KPIs del tablero que SÍ van (acuerdo 9-jul)
Disputas activas · Por vencer <3 días · Win probability por disputa (en tabla, no como KPI agregado) · Ratio tipo VAMP · Tabla de reclamos + gráficos CBK (franquicia/moneda/semana, picos, anomalía por reason code).

## Impacto en los otros planes

- **Plan 1:** el glosario y el mapa de flujo parten del modelo del proto (ya hay mucho resuelto); en la sesión de validación solo queda confirmar la resolución 5 (monitoreo) y comunicar las 1–4.
- **Plan 2:** ChargeScore deja de ser incógnita; el benchmark se enfoca en lo que el proto NO cubre (canal de salida merchant, colas de triage por SLA).
- **Plan 3:** la auditoría del OC debe confirmar si el "dashboard editable con catálogo de widgets" del proto mapea al tablero real del OC.
- **Plan 5:** los Flujos 1–3 de Ohana se modelan tomando el pipeline y el flujo agéntico del proto como primera hipótesis.
- **Plan 4:** el prototipo nuestro rehace este contenido sobre desyk, en español, con un solo modelo de datos y el rol primario que se decida.

## Done cuando
~~Las 5 preguntas de conflicto están respondidas~~ ✅ Resueltas el 9-jul con los acuerdos de la reunión (arriba). Queda: confirmar con Andrea la resolución 5 (monitoreo vía notif-resumen) y que cada elemento del inventario tiene destino conservar / rehacer / descartar — ya asignado en las tablas de este documento.
