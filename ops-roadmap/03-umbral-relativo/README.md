# 3. Soportar umbral relativo (%)

**Prioridad**: 🟣 P3 (morado)
**Impacto**: 3 · **Esfuerzo**: 2 · **Neto**: 10
**Nota original**: *"start research, user prod data to land better feedback"*

## Qué se necesita

Permitir definir umbrales en **porcentaje relativo** (vs absoluto) — ej. "alerta si baja >20% vs ayer" en lugar de "alerta si valor < 1000".

## Estado en Linear

### Antecedentes (umbrales hoy son absolutos)

| Issue | Título | Status | Nota |
|---|---|---|---|
| SWAT-519 | [E1.1] Definir reglas/umbrales por serie y por métrica | Done | Hard limits min/max actuales |
| SWAT-256 | Declaración explícita de series y umbrales por serie al registrar KPI | Done | `hard_l_min`/`hard_l_max` por serie |
| SWAT-223 | [BE-1] Migración aditiva: anomaly_kpi_configs + kpi_config_id | Done | Schema base |
| SWAT-522 | [E1.3] Generación de signals por umbral y por detección adaptativa | Done | Trigger / Trajectory hard / Trajectory adaptativo |
| SWAT-787 | Configurar colores por umbrales en monitores de pendientes | Canceled | Idea similar, abandonada |

### No hay issue específico para umbral relativo (%)

Detección adaptativa (`Trajectory adaptativo`) usa percentiles internos, pero el **usuario no puede declarar "%-delta"** como threshold.

## Research necesario

> *"start research, user prod data to land better feedback"*

- ¿Qué casos de uso en prod muestran que el % es más natural que el absoluto?
- ¿Vs período anterior (ayer, mismo día semana pasada)?
- ¿Vs baseline aprendido?
- Interacción con el detector adaptativo existente (¿reemplaza, suma, override?)

## Contexto Brain

- Épica DOE16 (Detección IA y parametrización, thresholds, exclusión de fuentes) — aquí encaja
- `Definicion - Anomalias.md` lista los 21 casos de uso → revisar cuáles piden % delta
