# Plan 4 — Prototipo de la experiencia

## Objetivo
Construir un prototipo HTML navegable del Centro de Disputas que materialice las 3 capas (observabilidad, operatividad, remediación) para validar con Andrea, Iván y el caso PayU.

## Prerrequisitos
- Plan 1 validado (entendimiento), Plan 2 (alternativas decididas), Plan 3 (patrones OC elegidos)
- **Plan 5 ejecutado primero:** user flows y sitemap aprobados en Ohana — el prototipo implementa esa interacción, no la define
- ✅ `Centro disputas.html` de Andrea auditado (ver `06-analisis-prototipo-andrea.md`): se conserva el modelo conceptual, el flujo agéntico de 8 pasos, el detalle de caso y el ChargeScore; se rehace todo el código sobre desyk, en español, con un solo modelo de datos.
- ✅ Conflictos resueltos con los acuerdos del 9-jul: **rol primario PSP adquirente, sin vista de emisor, sin win rate agregado ni "$ recuperado"**; monitoreo vía modelo notif-resumen (confirmar con Andrea).

## Stack y convenciones
- HTML autocontenido en `prototipos/` (Tailwind CDN + Alpine.js + Lucide), tokens de desyk (`tokens.css`)
- Datos mock realistas: disputas con reason codes reales de Visa/Mastercard, monedas, SLA variados, caso tipo PayU
- Enlazar cada prototipo a su flujo con `ohana_flow_set_proto`

## Alcance por capa

### Capa 1 — Observabilidad (tablero) — perspectiva del PSP adquirente
- KPIs: disputas activas · por vencer <3 días · ratio VAMP (la win probability vive en la tabla y el detalle, por disputa — no como KPI agregado)
- Tabla de reclamos: nº reclamo, franquicia, país, adquirente, merchant, valor, moneda, SLA (countdown visual), win probability, estado
- Gráficos (dataset preseleccionado, skill ux-data-viz): CBK por franquicia, por moneda, por semana; picos; anomalía por reason code
- Excluido (acuerdos 9-jul): plata recuperada agregada, win rate agregado, vista de emisor, switch de roles

### Capa 2 — Operatividad (detalle + agente)
- Detalle de disputa: la "carta" estructurada (nº autorización, ABS, data de la marca, match con conciliación interna)
- Win probability con **explicación del razonamiento** (patrón narrativa BADS de anomalías; explainable, sin caja negra)
- Priorización por SLA/aging; acciones recomendadas → botones
- Estados de automatización: «corrió automáticamente (sobre umbral)» vs. «requiere tu revisión» — umbral pendiente con Sergio, dejarlo parametrizado en el mock

### Capa 3 — Remediación (canal de salida)
- Prototipar la(s) opción(es) elegida(s) en Plan 2 (export / API / vinculación de cuentas)
- Estados de permisos/seguridad PCI (enmascarar tarjetas, validación de receptor)
- Si no hay decisión aún: demo A/B con switch (forma de trabajo habitual) para recoger feedback

## Fases de construcción
1. **F1:** tablero de observabilidad (mayor certeza, ya acordado)
2. **F2:** detalle de disputa + experiencia del agente
3. **F3:** canal de salida (mayor incertidumbre; puede ser A/B)
4. **QA:** ux-heuristics + revisión de copy con ux-writer (glosario Simetrik; validar convención sobre la palabra "agente")

## Entregables
- `prototipos/centro-disputas.html` (+ variantes A/B si aplica)
- Sesión de feedback con Andrea por fase; comentarios en Ohana (`ohana_create_comment`)

## Done cuando
Andrea valida las 3 capas y el prototipo queda listo para preparar handoff a las épicas correspondientes.
