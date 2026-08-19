# Registro de diseño — SWAT-577

**Esto no es handoff.** Acá vive el **porqué**: cómo se llegó a lo que hay que construir, qué se
evaluó y se descartó, y contra qué evidencia. Lo que hay que **construir** está en
[`../handoff/`](../handoff/00-spec.md).

La separación existe porque son dos audiencias distintas. Quien implementa necesita la spec y no
debería tener que leer 1.400 líneas de deliberación para encontrarla. Quien quiere **discutir una
decisión** necesita exactamente esas 1.400 líneas, porque si no la discusión se repite.

| Archivo | Qué contiene | Cuándo leerlo |
|---|---|---|
| [`01-decisiones.md`](01-decisiones.md) | **D1–D20** con razón, consecuencias y costo de revertir | Antes de proponer cambiar algo. Cada decisión dice qué se rompe si se revierte |
| [`02-benchmark.md`](02-benchmark.md) | **I1–I6**: qué hacen Grafana, Metabase, Almacenamiento y Finder, medido en el código | Cuando la pregunta es «¿cómo lo resuelven otros?» |
| [`03-exploracion-fe-be.md`](03-exploracion-fe-be.md) | El estado real de `fe-solutions-mf` y del BE **antes** de esta feature | Para ubicarte en el código existente |
| [`descartado/`](descartado/) | Dos documentos de un alcance que se revirtió | Solo si alguien vuelve a proponer carpetas transversales |

## Las decisiones que más caro sale revertir

| | | Costo |
|---|---|---|
| **D1** | Las carpetas son **por cuenta**, no por usuario | 🔴 modelo BE + migración |
| **D3** | Un tablero vive en **una sola** carpeta | 🔴 modelo BE + modelo mental |
| **D6** | Eliminar **disuelve un nivel**: el contenido sube a la madre | 🔴 es criterio del issue |
| **D15** | El agrupamiento se resuelve **server-side** | 🔴 condiciona todo el contrato de API |

## Sobre `descartado/`

El 2026-08-04 se amplió el alcance a las cuatro entidades del OC (Tableros, Datasets, Anomalías,
Pendientes) con una tabla `folders` compartida. El 2026-08-14 se revirtió a **solo Tableros**
(D10 revisada).

Los dos documentos se conservan **sin corregir**, a propósito. Describen un producto que no
existe, y sirven para una sola cosa: si alguien vuelve a proponer carpetas transversales, acá
está el análisis hecho — incluido lo que se descubrió que no cerraba.

## Convención

**Los documentos de este directorio no se reescriben cuando una decisión cambia.** Se agrega la
revisión conservando la anterior y su razón. Por eso D2, D6, D10 e I4 tienen el formato
«antes / ahora / por qué cambió»: el objetivo es que nadie tenga que adivinar si un número viejo
era un error o una decisión distinta.
