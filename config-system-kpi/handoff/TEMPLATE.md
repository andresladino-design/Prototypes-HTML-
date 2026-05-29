# Template — Historia de usuario Linear-ready

> Cada documento de `handoff/` cumple esta estructura. Está pensado para que un
> agente de Claude Code pueda tomar la historia desde Linear y empezar a
> implementarla sin contexto adicional fuera del repo.

---

```yaml
---
epic: MONITOR_INGESTA
issue_type: Feature | Bug | Refactor | Spike
priority: P0 | P1 | P2 | P3
estimate: XS | S | M | L | XL
labels: [ux, frontend, monitoring, ...]
depends_on: [STORY_ID_1, STORY_ID_2]   # IDs internos del handoff (file slugs)
blocks: [STORY_ID_3]
component_areas: [shell, dashboard, modal-config, bulk-modal, ...]
---
```

# NN · Título de la historia

> Una línea: qué entrega esta historia, dónde vive, para quién.

## Resumen
Un párrafo (3-5 oraciones) con: el problema, la decisión / acción que habilita,
qué cambia en la experiencia, por qué importa ahora.

## User story
> **Como** [tipo de usuario]
> **Quiero** [acción concreta]
> **Para** [outcome de negocio o personal]

Si hay variantes (creación vs edición, uno-a-uno vs masivo), listar cada una con
su propia frase Como / Quiero / Para.

## Anatomía (UI)
| Componente | Selector / clase | Responsabilidad | Origen |
|---|---|---|---|
| Header | `.ds-card-title` | Título de la sección | desyk + custom |
| ... | ... | ... | ... |

## Estados
Tabla:
| Estado | Condición / trigger | Visual | Editable |
|---|---|---|---|

Si aplica, máquina de estados textual:
```
INITIAL → ACTIVE → COMPLETED
   ↓
  ERROR (recuperable a ACTIVE)
```

## Comportamiento contextual
Cómo cambia según contexto (modo, flag, rol). Tabla:
| Condición | Visible | Editable | Datos | Side effects |
|---|---|---|---|---|

## Interacciones
Tabla:
| Trigger | Acción del sistema | Próximo estado | Feedback al usuario |
|---|---|---|---|

## Data binding
Variables del state Alpine que la historia lee/escribe. Path completo.
| Variable | Tipo | Lectura | Escritura |
|---|---|---|---|
| `daySetup.monitorMode` | `'igual' \| 'por-dia'` | render condicional | `dsPromoteToFamily()` |

## Acceptance criteria
Numerados. Formato Gherkin donde aplica.
1. **Dado** [contexto], **cuando** [acción], **entonces** [resultado verificable].
2. ...

## Implementation notes
- **Helpers Alpine ya existentes** a reusar: `monitoringStateFor(r)`, `ingestionTypeFor(r)`, `dsActiveSimple()`, etc.
- **CSS/clases** a usar (preferir reusar lo del prototipo en lugar de crear nuevas).
- **Endpoints BE** que esta historia consume (o que necesita aún): `GET /anomaly_configs/:id`, etc.
- **Tokens desyk** a respetar.
- **Animation / motion**: duraciones canónicas, qué transiciones aplicar.

## Out of scope
Lista explícita de lo que **NO** se hace en esta historia (para evitar scope creep
del implementador).

## Empty states (importante)
**Identificar todos los escenarios donde el contenedor podría no tener datos.**
El prototipo HTML actual solo tiene algunos empty states (loaders, casos puntuales).
Aunque no estén pintados todavía, esta historia debe enumerarlos y describir copy,
visual y CTA esperados. Tabla:

| Escenario | Condición | Copy propuesto | CTA | Implementado en HTML? |
|---|---|---|---|---|
| Sin datos del BE | API devuelve `[]` | "Aún no hay X..." | botón "Agregar X" o link | ❌ pendiente |
| Sin permisos | Rol del usuario no tiene acceso | "No tenés permiso para ver X" | enlace a soporte | ❌ pendiente |
| Error de red | Fetch falló | "No pudimos cargar X. Reintentar." | botón "Reintentar" | ❌ pendiente |
| Loading | Mientras carga | spinner / skeleton | (ninguno) | ✅ / ❌ |
| Búsqueda sin resultados | `filter().length === 0` | "Sin resultados para X" | clear filter | ✅ / ❌ |
| ... | | | | |

**Nota para el agente implementador**: si encontrás un escenario que esta tabla
no menciona, agregalo al ticket antes de implementar — no asumas el copy.

## Edge cases (validación)
- Valor extremo (cero, máximo, negativo).
- Texto demasiado largo (truncado / wrap).
- Múltiples elementos a la vez.
- Conflictos de estado (ej. dos toggles excluyentes).
- Etc.

## Dependencies
- **Depende de**: `STORY_ID_X` (qué bloquea esto).
- **Bloquea a**: `STORY_ID_Y`.
- **Relacionado con**: otros docs del handoff.

## Verification (cómo probarlo)
Pasos manuales para QA:
1. Abrir el prototipo en `index.html`.
2. Navegar a [...].
3. Verificar que [...].
4. Probar edge case [...].

## References
- **HTML**: `../index.html` líneas X-Y.
- **Figma**: (pendiente de link)
- **Docs hermanos**: `[05-modal-configuracion.md](./05-modal-configuracion.md)`, `[00-CONTEXT.md](./00-CONTEXT.md)`.
- **Backend**:
  - BADS: `~/Simetrik/bads/src/bads/models/...`
  - Op-center: `~/Simetrik/op-center-backend/apps/anomaly_configs/...`

---

## Notas para el agente implementador

Cuando un agente de Claude Code lea esta historia desde Linear:
1. Leer **00-CONTEXT.md** primero (glosario, tokens, estados BADS).
2. Leer **STORIES-INDEX.md** para entender el orden de implementación.
3. Verificar que los `depends_on` ya están implementados (o están en la misma PR).
4. Implementar siguiendo Acceptance criteria como source of truth.
5. No salirse del Out of scope.
6. Mantener consistencia con los helpers Alpine ya existentes (no reinventar).
