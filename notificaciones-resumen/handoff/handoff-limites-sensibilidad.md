# Handoff — Sensibilidad y Límites del gráfico (hard limits por bound)

Fecha: 2026-06-24
Origen: `notificaciones-resumen/index.html` → `.sens-row` (Sensibilidad) + `.tm-limits-block` (límites por bound) del diálogo de monitoreo (prototipo validado)
Registro: **Interno (Operation Center)** — operador Simetrik ajustando cómo el Agente IA evalúa un gráfico (K Cast)
Patrón de presentación: **Fila de control (sens-row)** + **grid de bounds con override sobre el valor sugerido por el Agente IA**

---

## 1. Contexto y objetivo

Define **cómo de exigente** es el Agente IA al evaluar un gráfico y **qué límites duros** disparan un incidente.

- **Sensibilidad** (Nula / Media / Alta): regula cuándo el agente considera que algo es desviación, antes de tocar el límite duro.
- **Límites por bound** (inferior / superior): valores duros activables; el Agente IA propone un **valor sugerido** y el operador puede sobreescribirlo (modo manual), con opción de revertir al sugerido.

Objetivo: que el operador calibre el monitoreo con dos perillas claras (sensibilidad relativa + límites absolutos) entendiendo siempre cuál es la propuesta del agente y cuándo se apartó de ella.

## 2. Usuario y registro

- **Registro:** Interno / Op Center. Power user recurrente.
- **Modo de uso:** ajuste fino, comparación contra el valor sugerido. Quiere ver de inmediato si está en automático (sugerido) o manual (override).
- **Dato clave al primer vistazo:** ¿qué tan sensible está y qué límites están activos vs. sugeridos?

## 3. Historias de usuario

**HU-1 — Ajustar sensibilidad**
> Como operador, quiero elegir entre sensibilidad Nula, Media o Alta, para balancear entre perderme desviaciones y recibir ruido, entendiendo qué implica cada nivel.
- Segmented de 3 opciones; al cambiar, título y subtítulo se actualizan describiendo el comportamiento.

**HU-2 — Activar/desactivar un límite duro**
> Como operador, quiero encender o apagar el límite inferior y el superior de forma independiente, para monitorear solo los bounds que importan en este gráfico.
- Checkbox por bound; al apagar, el input se atenúa pero **conserva su valor**.

**HU-3 — Sobreescribir el valor sugerido del Agente IA**
> Como operador, quiero cambiar el valor propuesto por el agente y poder volver al sugerido con un clic, para tener control manual sin perder la referencia del agente.
- Al diferir del sugerido aparece un chip "Valor sugerido: N"; al hacer clic, revierte.

## 4. Arquitectura de componentes desyk

| Mock (prototipo) | Componente desyk | Notas |
|---|---|---|
| `.sens-row` | `Card` / row de control (composición) | ícono `gauge` + título/sub dinámico + control a la derecha |
| `.bgroup` (Nula/Media/Alta) | `SegmentedControl` | 3 opciones, valor controlado; cambia copy asociado |
| `.tm-limits-header` | label de sección | uppercase, `muted-foreground`; ícono `box`/`layers` |
| `.tm-limit-field` + `.tm-limit-check` | `Checkbox` + grupo de campo | estado `is-off` atenúa el input |
| `.tm-limit-input` | `Input` (numérico, `tabular-nums`) | `data-suggested` = valor del agente |
| `.tm-limit-chip` (revert) | `Badge` clickeable / `Button` ghost xs | visible solo si `value !== suggested`; ícono `rotate-ccw` |

**Estructura sugerida (React):**

```
<SensitivityRow value={sens} onChange={setSens} />   // Nula | Media | Alta

<LimitsBlock title="Todas las categorías">
  <LimitField bound="min" label="Límite inferior" enabled value suggested onChange onToggle onRevert />
  <LimitField bound="max" label="Límite superior" enabled value suggested onChange onToggle onRevert />
</LimitsBlock>
```

Lógica clave (del prototipo):
- `chip.hidden = value.trim() === suggested` → el chip "Valor sugerido" aparece solo en override.
- `revert` → `value = suggested`, oculta chip.
- `toggle` → `field.is-off`, input `disabled`; el chip sigue su propia regla.

## 5. Estados

- **Loading:** skeleton del row de sensibilidad y de los dos inputs.
- **Inicial (automático):** ambos bounds activos con el **valor sugerido por el Agente IA**; sin chip de override.
- **Override (manual):** valor distinto al sugerido → chip "Valor sugerido: N" visible.
- **Bound apagado:** input atenuado e inerte, conserva valor.
- **Error de validación:** valor no numérico / inferior ≥ superior → borde `destructive` + microcopy.
- **Sin límites activos:** ambos apagados → meta "Sin monitoreo" (de `updateLimitsMeta()`).

## 6. Copy completo (glosario aplicado)

> Glosario Op Center: **Agente IA**, **incidente**, **gráfico/KPI**. "Valor sugerido" = propuesta del Agente IA.

**Sensibilidad** (títulos/subtítulos dinámicos, de `SENS_COPY`)
- Nula → `Sensibilidad · nula` · `Solo avisa cuando el valor supera el límite fijo que definiste.`
- Media → `Sensibilidad · media` · `Avisa al acercarse al límite, pasado un umbral intermedio.`
- Alta → `Sensibilidad · alta` · `Avisa ante cualquier desviación inusual, sin esperar al límite fijo.`
- Opciones segmented: `Nula` / `Media` / `Alta`

**Límites**
- Header: `Todas las categorías`
- Labels: `Límite inferior` · `Límite superior`
- Chip revert: `Valor sugerido: <N>` (ícono `rotate-ccw`)
- Meta (estado): `Sin monitoreo` / `Monitoreando 1 límite` / `Monitoreando 2 límites`

## 7. Microinteracciones

| Interacción | Detalle |
|---|---|
| Cambio de sensibilidad | título/sub hacen cross-fade `200ms ease-out`; opción segmented activa con `box-shadow` ring |
| Apagar bound | input → `opacity .45` + inerte, transición `120ms` |
| Aparición chip revert | fade-in sutil al diferir del sugerido (`120ms`) |
| Revert | input vuelve al sugerido; chip desaparece |
| Focus input | borde `primary` `120ms` |

Durations canónicas: 120 / 200 / 320 ms ease-out.

## 8. AI integration

- El **valor sugerido** lo calcula el **Agente IA / BADS**. La UI debe dejar claro que el default proviene del agente y que el override es manual (el chip de revert es la pista pedagógica: "puedes volver a lo que propuso el agente").
- La **sensibilidad** modula la confianza del agente para llamar desviación antes del límite duro. No badges "AI", no sparkles.

## 9. Endpoints esperados

`GET /monitoring/{chartId}/thresholds` →
```json
{
  "sensitivity": "media",
  "limits": {
    "min": { "enabled": true, "value": 120, "suggested": 120 },
    "max": { "enabled": true, "value": 480, "suggested": 480 }
  }
}
```
`PUT /monitoring/{chartId}/thresholds` con el mismo shape. `suggested` es read-only (lo provee el agente).

## 10. Edge cases y validaciones

- Valor no numérico o vacío con bound activo → error, bloquea guardar.
- `min >= max` (ambos activos) → error de coherencia entre bounds.
- Valores negativos / decimales según el tipo de KPI (definir por categoría).
- Ambos bounds apagados → permitido (solo sensibilidad), meta "Sin monitoreo".
- Recalcular `suggested` (nuevo aprendizaje del agente) mientras hay override → mantener el override; actualizar el target del chip al nuevo sugerido.
- Sensibilidad "Nula" con ambos límites apagados → estado sin monitoreo efectivo: advertir al guardar.

## 11. Test cases sugeridos

1. Cambiar sensibilidad actualiza título y subtítulo correctos por nivel.
2. Editar un input a un valor distinto del sugerido muestra el chip "Valor sugerido".
3. Clic en el chip revierte al sugerido y oculta el chip.
4. Apagar un bound atenúa el input, lo vuelve inerte y conserva su valor.
5. `min >= max` con ambos activos dispara error de coherencia.
6. Meta refleja 0 / 1 / 2 límites activos.

## 12. Tokens utilizados

`--primary #3D3BF5` (foco input, accent checkbox, opción segmented activa) · `bg-segment` (fondo del segmented) · `--border` (bordes inputs) · `muted-foreground` (header, meta) · `text-primary #1F1B2E` · `info #2563EB` (chip revert) · `warning` (sensibilidad media) · `destructive` (errores de validación). Radius: `10px` inputs, `7px` chip revert, `8px` segmented.

## 13. Checklist pre-PR

- [ ] Sensibilidad resuelta con `SegmentedControl` desyk (no botones custom)
- [ ] Inputs con `Input` desyk numérico, `tabular-nums`
- [ ] Chip "Valor sugerido" visible solo en override; revert funcional
- [ ] Bound off → input atenuado e inerte, conserva valor
- [ ] Glosario: "Agente IA", "incidente", "valor sugerido"
- [ ] Validaciones: numérico, `min<max`, sin-monitoreo
- [ ] Microinteracciones 120/200/320 ms ease-out
- [ ] Light mode consistente
- [ ] A11y: labels asociados a checkbox/input, foco visible, contraste AA
- [ ] Tests: cambio de sensibilidad + override/revert + coherencia min/max
