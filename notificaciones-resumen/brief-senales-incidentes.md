# Design Brief — Configuración de notificaciones: señales e incidentes (P0)

> Producido con `/simetrik-ui shape` · discovery socrático del 2026-06-26
> Fuente de feedback: sesión 26-jun "Notificaciones y monitoreo — señales, incidentes y sensibilidad"
> Ancla de producto: Brain v2.8 · `operation-center/funcionalidades/anomalias`

## Registro y usuario
- **Registro:** Producto (appv2) — analista / contador / ops del cliente.
- **Uso:** ocasional, bajo carga; el usuario revisa tarde y no quiere ruido.
- **Dato clave a 2s:** "¿tengo algo que atender hoy?"
- **Modo de interacción:** configurar una vez, confiar después.

## Modelo canónico (del Brain, no inventado)
- **Señal de anomalía** (`AnomalySignal`): atómica, ruidosa. Estados `ACTIVE → RESOLVED`. Categorías `TRIGGER`, `TRAJECTORY`, `NEW_SERIES`.
- **Incidente** (`Incident`): agrupa señales + problem category + recommended actions. 9 estados: `WATCHING → OPEN → CONFIRMED` + terminales (`AUTO_CLOSED`, `USER_CLOSED`, `RESOLVED`, `CLOSED`, `MERGED`).
- Backend ya separa ambos (topics Pulsar `oc-bads-anomaly` / `oc-bads-incident`). **La separación existe; falta exponerla en UI.**
- **Glosario:** "Señal de anomalía" e "Incidente". Nunca "alerta" / "ticket". Sin "agente/IA" en copy de usuario.

## Decisiones del discovery

| # | Decisión | Detalle |
|---|----------|---------|
| Q1 | **Confirmación = "al cierre de ventana"** | Copy simplificado. ⚠️ **A validar con Iván/BADS**: el backend confirma cuando responde el workflow runner (`OPEN`), no estrictamente al cerrar la ventana. Si no calza, ajustar copy. |
| Q2 | **Un solo eje "nivel de ruido"** | 3 escalones: *Solo lo confirmado (incidentes)* → *+ alertas tempranas (señales)* → *Todo, en tiempo real*. **Reemplaza** el actual `¿Cuándo notificar?` (Nunca/Solo al cierre/Todo el tiempo), colapsando "qué" + "cuándo" en una escalera. "Nunca" pasa a ser el estado apagado (sin canales). |
| Q3 | **Severidad sí, antigüedad no** | Bajo "Solo lo confirmado" se revela filtro opcional: *solo severidad alta*. La antigüedad (>1 día) queda fuera del prototipo por ahora. |
| Q4 | **El cierre siempre cierra el loop** | Si hubo apertura notificada, el cierre/resolución se notifica siempre (cualquier escalón). Es el desenlace de algo conocido, no ruido nuevo. |
| Q5 | **Preview en vivo de lo que recibirás** | Cada escalón muestra un mini-timeline con ejemplos concretos de las notificaciones que llegarían. Enseña el modelo mostrando el resultado, no la teoría. |

## Comportamiento por escalón (resumen)

| Escalón | Apertura | Updates intermedios | Cierre/resuelto | Filtro |
|---|---|---|---|---|
| **Solo lo confirmado** | ✓ incidente | — | ✓ siempre | severidad (opc.) |
| **+ alertas tempranas** | ✓ incidente + señales | parcial | ✓ siempre | — |
| **Todo, en tiempo real** | ✓ todo | ✓ stream completo | ✓ siempre | — |

## Patrón de layout elegido
**Escalones apilados con preview inline** (progressive disclosure). Radios apilados en una columna; el escalón seleccionado se expande y revela su mini-timeline de "Recibirás algo así" y, en "Solo lo confirmado", el filtro `☐ Solo severidad alta`. Cabe en el modal angosto actual; migra limpio a página completa (P2) sin rediseño.

```
¿Cuánto quieres que te avise?

◉ Solo lo confirmado (incidentes)
  ┌ Recibirás algo así ───────────┐
  │ 🔴 Incidente abierto            │
  │ 🟢 Resuelto · 8:00am            │
  └─────────────────────────────────┘
  ☐ Solo severidad alta

○ + alertas tempranas (señales)
○ Todo, en tiempo real
```

- Reemplaza el `¿Cuándo notificar?` actual (dropdown Nunca/close/during).
- "Nunca" = estado apagado: sin canales activos → no hay notificaciones (se conserva el aviso "configura al menos un canal").
- Motion: expansión 200ms ease-out (canon Simetrik); el preview no es decorativo, es pedagógico.

## Fuera de alcance de este P0
- Criterio de antigüedad (>1 día).
- Destinatarios internos vs externos + duplicados (P1, requiere verificación de Ing).
- Migración modal → página completa (P2).
- Wording "Resumen diario", feedback visual de sensibilidad (P1, otras tandas).

## Riesgo abierto
- **Timing de confirmación** (Q1): bloquea el copy final. Validar con Iván antes de handoff.
