# 04 · Copy y recomendaciones

> Copy real del prototipo (modelo modo + tabs) y reglas de redacción. El **glosario canónico** vive en [`../handoff/00-CONTEXT.md`](../handoff/00-CONTEXT.md) (consolidado desde el companion skill `ux-writer`). Este doc no lo duplica: lo aplica.

## 1 · Reglas de voz (recordatorio)

- **Español neutro**, sin slang regional. Sin em-dashes (—) ni `--`; usar comas, dos puntos, paréntesis, puntos.
- **Glosario obligatorio** (Op Center v2.8): Fuente/Dataset, Monitoreo, Anomalía, Señal de anomalía, Incidente, Tablero, KPI, Agente IA, BADS. No traducir ni sinonimizar.
- **Sin "Powered by AI" / sparkles**: la IA es core, no feature opcional.

## 2 · Copy del modo (navegación)

| Elemento | Copy | Notas |
|---|---|---|
| Botón de modo (en Tablero) | **Monitoreo** + badge "Sin configurar" / "Monitoreando" | El badge refleja `monitoringActive` |
| Botón de modo (en Monitoreo) | **Volver al tablero** | Mismo botón, reetiquetado; es la salida |
| Tabs de etapa | **Ingesta de datos** · **Calidad de datos** · **Salud de conciliaciones** · **Métricas de gráficos** | Calidad y Conciliación con badge **Pronto** |

## 3 · Banner zero-state del tablero (entrada pedagógica)

Dos variantes según `dashboardRecentlyModified`:

| Variante | Título | Subtítulo (resumen) | CTA |
|---|---|---|---|
| Estable | **Buen momento para empezar a monitorear** | "Este tablero no ha tenido cambios en los últimos días... el monitoreo puede aprender qué es lo normal y avisarte si algo se desvía." | **Empezar a monitorear** |
| Recién modificado | **Dale unos días antes de monitorear este tablero** | "Cambiaste sus gráficos o los datos que lo alimentan hace pocos días. El monitoreo necesita ver cómo se comporta cuando ya no cambia..." | **Configurar de todos modos** |

## 4 · Banner "Conceptos clave" (onboarding del modo monitoreo)

- Eyebrow: **Monitorea tu tablero**
- Título: **Asegura que todo el proceso esté monitoreado**
- Texto: "Tus gráficos se alimentan de fuentes usadas en los dataset. Monitorea todo el proceso desde ingesta de datos hasta el resultado para confiar en lo que ves en tu tablero."
- Cards: **Ingesta de datos** · **Métricas de gráficos** · **Gestión de anomalías** (showcase con pill "Anomalía detectada").
- Cerrable (✕). Es onboarding; al cerrarlo el contexto del modo se mantiene por el botón y el glow.

## 5 · Acciones de etapa (barra de tabs)

| Etapa | Buscador (placeholder) | Acción |
|---|---|---|
| Ingesta | "Buscar fuente…" | **Activar 1 a la vez** / **Activar las N a la vez** (singular/plural por cantidad de fuentes sin configurar) |
| Métricas | "Buscar gráfico…" | (sin acción bulk) |

## 6 · Estados de una fuente (cards de Ingesta)

| Estado | Label del badge | Color |
|---|---|---|
| Sin configurar | **Sin configurar** | gris |
| Aprendiendo | **Aprendiendo** | azul (info) |
| Monitoreado | **Monitoreado** | verde (success) |

## 7 · Modal de configuración (Low/Family/High)

Copy clave (ver `../handoff/05` y contenedores `07`-`12` para el detalle): loader "Simetrik está analizando tu fuente…", feedback "Cambiaste a configuración por día de la semana", chip IA "Autocompletado por el agente" / "Sugerencia: …". El switch de día cambia su label según estado (afirma la acción): "este día espero que lleguen archivos" / "este día no espero que lleguen archivos".

## 8 · Pendientes de copy

- **Banner verde de "monitoreado"** (`tm-dash-secured`, "Ver monitoreo"): copy propuesto pero **no implementado** (ver `../handoff/01`). Si se implementa, alinear con el glosario.
- **Empty states** sin copy definitivo (tablero sin fuentes, errores de carga, sin permisos): listados en los handoff `01`/`02`/`03`/`04` como pendientes.
