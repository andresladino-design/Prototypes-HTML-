# Copy Spec — DB-2026-05-25-001 · Refactor de Navegación Anomalías

> Agente: UX Writer | Fecha: 2026-05-25
> Entregable: copy de la nueva arquitectura recurso-céntrica (Patrón C) del Operation Center
> Tono principal: informar + guiar. Voz del Agente IA: business plain, sin jargon técnico.

---

## Glosario aplicado en este ciclo

Solo los términos que aparecen en este entregable.

| Término correcto | NO usar |
|---|---|
| Recurso | Asset, item, elemento, módulo |
| Espacio de trabajo | Workspace, área |
| Fuente | Origen, dataset (cuando se refiere a la fuente nativa) |
| Tablero | Dashboard, panel |
| Conciliación | Reconciliación |
| KPI | Métrica genérica |
| System KPI | KPI automático, KPI del sistema |
| Anomalía | Desviación |
| Señal de anomalía | Alerta atómica, alerta suelta |
| Incidente | Ticket, alerta agrupada |
| Agente IA | Bot, asistente, IA suelta |
| Configuración de monitoreo | Settings, ajustes |
| Umbral | Threshold, límite |
| Exportar | Export |
| Repositorio | Carpeta, contenedor |
| Período contable | Período fiscal |

---

## 1. Navegación

### 1.1 Top-nav del Operation Center · Item principal

**Surface**: Operation Center > nav primario > item del módulo

| Opción | Copy | Caracteres | Racional |
|---|---|---|---|
| Mantener actual | "Anomalías" | 9 | Familiar, sin costo de aprendizaje, pero estrecha el alcance del módulo refactorizado (que ahora cubre recursos, configuración, hipótesis IA, incidentes y señales). |
| Propuesta nueva | **"Monitoreo"** | 9 | Describe lo que el módulo hace (monitorear recursos del Op Center), no solo el subproducto que detecta. Alinea con `Monitor` del glosario clásico Simetrik y con `configuración de monitoreo` del Op Center. Acomoda futuras lentes (Recursos / Actividad). |

**Copy final**: "Monitoreo"

**Racional final**: el refactor desplaza el centro de gravedad del incidente al recurso. "Anomalías" describía la consecuencia visible. "Monitoreo" describe la práctica que el analista hace todos los días, y ya está acuñado dentro del producto (`configuración de monitoreo`, `monitor`). Reduce el malentendido de que el módulo es solo para ver problemas.

**Glosario verificado**: ✓ (Monitor existe; Monitoreo es la práctica asociada, sin colisión)

**Nota para LEAD**: si el cambio de label rompe deep links existentes o métricas de uso, podemos diferir el rename a una segunda iteración y conservar "Anomalías" en esta entrega.

---

### 1.2 Tabs/lentes dentro de la página · Modos del híbrido

**Surface**: Página del módulo > toolbar > tabs principales (2 modos)

#### Alternativa A

| Tab | Copy | Caracteres |
|---|---|---|
| Lente 1 | "Recursos" | 8 |
| Lente 2 | "Actividad" | 10 |

**Racional A**: pareja sustantivo + sustantivo, balanceada visualmente. "Recursos" usa el término del glosario y nombra la unidad central del refactor. "Actividad" cubre el feed de incidentes + señales sin comprometerse a un solo tipo.

#### Alternativa B (descartada)

| Tab | Copy | Caracteres |
|---|---|---|
| Lente 1 | "Inventario" | 10 |
| Lente 2 | "Incidentes" | 10 |

**Racional B (por qué se descarta)**: "Inventario" sugiere catálogo estático y no transmite que cada recurso es monitoreable. "Incidentes" limita la lente al subconjunto agrupado; deja afuera señales sueltas, hipótesis, hilo histórico.

**Copy final**: **"Recursos"** | **"Actividad"**

**Glosario verificado**: ✓ ("Recurso" oficial; "Actividad" se alinea con "Historial de actividad" del glosario clásico)

---

### 1.3 Breadcrumbs · Estructura jerárquica

**Surface**: Header de página > breadcrumb superior

```
N1: Espacio de trabajo > N2: Monitoreo > N3: {Nombre del recurso} > N4: {Lente actual}
```

**Ejemplos concretos**:

| Contexto | Breadcrumb |
|---|---|
| Lista de recursos | Espacio de trabajo / Monitoreo / Recursos |
| Detalle de recurso | Espacio de trabajo / Monitoreo / Reconciliación bancaria diaria |
| Tab de KPIs en un recurso | Espacio de trabajo / Monitoreo / Reconciliación bancaria diaria / KPIs |
| Incidente abierto desde Actividad | Espacio de trabajo / Monitoreo / Actividad / Incidente #INC-2026-04-018 |

**Variantes**:
- Si el nombre del recurso supera 40 caracteres, truncar con elipsis al final: "Reconciliación bancaria diaria de la cuent..."
- El N1 ("Espacio de trabajo") muestra el nombre del workspace activo cuando hay más de uno; si solo hay uno, se oculta.

**Racional**: profundidad mínima viable que permite saltar dos niveles arriba (a lista) y un nivel arriba (al recurso) sin perder contexto. Resuelve la fricción crítica 4 del Brief (sin breadcrumbs hoy).

**Glosario verificado**: ✓

---

## 2. Sidebar de recursos

### 2.1 Header del sidebar

| Surface | Copy | Caracteres | Racional |
|---|---|---|---|
| Título | "Recursos" | 8 | Sentence case, sustantivo del glosario. Sin verbo: el sidebar no es una acción. |
| Botón nuevo (icono + label en hover) | "Monitorear recurso" | 18 | Verbo en infinitivo. Describe la acción exacta (no "Agregar"). |

**Glosario verificado**: ✓

---

### 2.2 Categorías jerárquicas

**Surface**: Sidebar > grupos de la lista

| Categoría | Copy | Caracteres | Racional |
|---|---|---|---|
| Sección 1 | "Favoritos" | 9 | Convención universal, breve, traduce a EN/PT sin pérdida ("Favorites" / "Favoritos"). |
| Sección 2 | "Con monitoreo" | 13 | Describe la propiedad del recurso, no su estado de salud. Más claro que "Monitoreados" (que en español puede leerse pasivo o como categoría auditiva). |
| Sección 3 | "Sin monitoreo" | 13 | Pareja simétrica con la anterior. Lee como "todavía no configurado", invita a activar. |

**Alternativas descartadas**:
- "Monitoreados / No monitoreados" — funciona pero "no monitoreados" suena a juicio negativo. "Sin monitoreo" describe el hecho.
- "Activos / Inactivos" — colisiona con el estado del recurso en sí.
- "Vigilados / No vigilados" — connotación de control que no encaja con el tono Simetrik.

**Counters**: cada categoría muestra contador "(N)" al final del título cuando hay datos. Ej. "Con monitoreo (24)".

**Glosario verificado**: ✓

---

### 2.3 Dot indicator · Tooltips por estado

**Surface**: Sidebar > fila de recurso > dot izquierdo (4 px) > tooltip on hover

Reglas: tooltip de una sola oración, sin punto final `[7.3]`. Sin asumir color (light mode neutro). Voz del sistema, neutra.

| Estado | Tooltip | Caracteres | Racional |
|---|---|---|---|
| Saludable | "Dentro del rango habitual" | 26 | Plain language. Evita "todo bien", evita "OK". Conecta con el lenguaje del Agente IA que dirá "fuera del rango habitual" cuando haya anomalía. |
| Atención | "Variación leve respecto al patrón" | 33 | Severidad media sin alarmar. "Variación" en lugar de "desviación" para mantenerlo accesible. |
| Urgente | "Fuera del rango habitual" | 25 | Espejo del saludable. Describe el hecho, no el riesgo. La severidad la nombran las acciones, no el dot. |
| Sin monitoreo | "Este recurso aún no tiene monitoreo activo" | 43 | Describe el porqué del estado neutro. Invita implícitamente a activar. |

**Glosario verificado**: ✓ (sin usar `breach_pct` ni `severity` técnicos, traducidos a business plain)

**Nota para LEAD**: la severidad granular (Urgente / Alta / Media / Baja del glosario) se reserva para incidentes en Actividad. En el dot del sidebar, 4 estados visuales son suficientes y reducen ruido cognitivo.

---

### 2.4 Empty state · Sin recursos monitoreados

**Surface**: Sidebar > sección "Con monitoreo" cuando count = 0

| Elemento | Copy | Caracteres | Componente | Regla |
|---|---|---|---|---|
| Título | "Aún no monitoreas ningún recurso" | 33 | Typography/body-sm | `[7.1]` empty state |
| Descripción | "Activa el monitoreo en un recurso para detectar anomalías y recibir alertas." | 77 | Typography/caption | `[7.2]` `[3.5]` |
| CTA | "Activar monitoreo" | 17 | Button/outline-sm | — |

**Racional**: explica el porqué (título), el qué hacer (descripción), la acción concreta (CTA). Aplica regla empty state del rol UX Writer.

**Glosario verificado**: ✓

---

### 2.5 Search · Placeholder + atajo

**Surface**: Sidebar > header > campo de búsqueda con icono de lupa

| Elemento | Copy | Caracteres | Racional |
|---|---|---|---|
| Placeholder | "Buscar recurso" | 14 | Verbo en infinitivo + objeto del glosario. Sin "..." para no asumir nada. |
| Hint del atajo (kbd badge al lado derecho) | "Ctrl K" | 6 | Notación neutra, sin "Cmd" (asume macOS). El componente kbd muestra el modificador correcto según OS. |
| Tooltip del kbd | "Abrir búsqueda rápida" | 21 | `[7.3]` sin punto. Describe la acción, no el atajo. |

**Glosario verificado**: ✓

**Nota para Front Designer**: el badge `Ctrl K` cambia a `⌘ K` en macOS automáticamente vía detección de plataforma. El texto del tooltip es el mismo.

---

## 3. Vista de recurso · La home del refactor

### 3.1 Header del recurso

**Surface**: Página del recurso > zona superior

| Elemento | Copy | Caracteres | Componente | Regla |
|---|---|---|---|---|
| Nombre (h1) | "{Nombre del recurso}" | dinámico | Typography/h2 | `[7.1]` sin punto |
| Tipo + ID (subtítulo) | "{Tipo} · ID {recursoId}" | dinámico | Typography/caption | — |
| Badge de estado · saludable | "Sin anomalías" | 13 | Badge/success | `[7.1]` |
| Badge de estado · atención | "Variación detectada" | 19 | Badge/warning | `[7.1]` |
| Badge de estado · urgente | "Anomalía activa" | 15 | Badge/critical | `[7.1]` |
| Badge de estado · sin monitoreo | "Sin monitoreo" | 13 | Badge/neutral | `[7.1]` |
| Acción primaria (con monitoreo) | "Editar monitoreo" | 16 | Button/primary | — |
| Acción primaria (sin monitoreo) | "Activar monitoreo" | 17 | Button/primary | — |

**Tipos de recurso** (valores posibles del subtítulo):
- "Conciliación"
- "Fuente"
- "Unión de fuentes"
- "Tablero"
- "Dataset"

**Glosario verificado**: ✓

---

### 3.2 Card de hipótesis IA

**Surface**: Vista de recurso > zona superior, debajo del header > card destacada

Esta card es la materialización del "hilo IA" del patrón C. Reemplaza la pregunta natural del analista al abrir el recurso: "¿qué está pasando acá?"

#### Header de la card

| Opción | Copy | Caracteres | Racional |
|---|---|---|---|
| Conversacional | "¿Qué está pasando aquí?" | 23 | Empático, espeja la pregunta mental del analista, pero rompe el principio "profesionalismo sin solemnidad" y usa interrogación que cuesta traducir a EN/PT con la misma calidez. |
| Funcional (descartada) | "Análisis del agente" | 19 | Describe el componente, no el valor. Cae en la trampa category-reflex. |
| **Recomendada** | **"Resumen del Agente IA"** | 21 | Nombra el componente con el término oficial del glosario. Plain language. Traduce a "Summary from the AI Agent" sin pérdida. |

**Copy final del header**: "Resumen del Agente IA"

**Glosario verificado**: ✓ ("Agente IA" canónico, no "IA" suelto)

#### Estados de la card

| Estado | Elemento | Copy | Caracteres | Regla |
|---|---|---|---|---|
| Cargando | Loader inline | "Analizando datos del recurso..." | 31 | `[2.6]` |
| Generada · sin anomalía | Cuerpo (ejemplo) | "El recurso opera dentro de su patrón habitual. Último análisis hace {tiempo_relativo}." | dinámico | Voz neutra, tono informar |
| Generada · con anomalía | Cuerpo (ejemplo) | "Detecté una caída de {pct}% en {KPI} durante las últimas {ventana}. Suele ocurrir cuando {causa probable}." | dinámico | Voz del agente, plain language |
| Desactualizada | Banner sobre el cuerpo | "Este resumen es de hace {tiempo_relativo}. Los datos pueden haber cambiado." | dinámico | `[7.2]` con punto |
| Desactualizada | CTA del banner | "Regenerar resumen" | 17 | — |
| Sin datos suficientes | Cuerpo | "Aún no hay suficiente histórico para generar un resumen. Necesito al menos {días_min} días de datos." | dinámico | `[3.5]` causa + criterio |
| Sin datos · CTA | Botón | "Ver requisitos" | 14 | — |
| Error de generación | Cuerpo | "No se pudo generar el resumen en este momento. Vuelve a intentarlo en unos minutos." | 84 | `[3.5]` efecto + acción |
| Error de generación | CTA | "Reintentar" | 11 | — |

**Notas sobre voz del Agente IA**:
- Usa primera persona ("Detecté", "Necesito") con moderación; refuerza presencia sin antropomorfizar.
- No promete causa, propone hipótesis: "Suele ocurrir cuando…" en vez de "Esto se debe a…".
- Métricas en términos de negocio: "caída de 12%" en vez de `breach_pct: 0.12`.

**Glosario verificado**: ✓

**Nota para LEAD**: el patrón "Detecté…" es una decisión de tono que conviene validar con muestras reales. Alternativa más neutra: "El sistema detectó una caída…". Recomiendo primera persona del Agente IA como diferenciador de marca, pero requiere consistencia en otros agentes (Solutions, Executive Summary, Error Intelligence).

---

### 3.3 Tabs internas del recurso

**Surface**: Vista de recurso > tabs secundarias debajo del header + card de hipótesis

**Orden recomendado** (izquierda a derecha):

| Orden | Tab | Caracteres | Racional |
|---|---|---|---|
| 1 | "Estado" | 6 | Vista por defecto. Snapshot operativo: salud actual, KPIs visibles, últimas señales. Lo que el analista necesita ver primero. |
| 2 | "KPIs" | 4 | Detalle de los indicadores asociados al recurso. Incluye User KPI y System KPI. |
| 3 | "Histórico" | 9 | Línea de tiempo de anomalías, incidentes y cambios de configuración. Donde se va cuando "Estado" muestra algo raro y quiere contexto. |
| 4 | "Notificaciones" | 14 | Reglas de envío del recurso: canales, frecuencia, destinatarios. Configuración menos frecuente que KPIs. |
| 5 | "Configuración" | 14 | Umbrales, frecuencia de sondeo, ventanas de horario. El "modal monstruo" descompuesto. Última porque es la menos visitada en la operación diaria. |

**Racional del orden**:
1. **Estado primero** porque es el día a día (frecuencia: cada vez que entras).
2. **KPIs y Histórico** son las dos lentes de "qué pasó / qué está pasando" (alta frecuencia).
3. **Notificaciones y Configuración** son tareas de setup (baja frecuencia, alta importancia).

Mata la fricción del modal de 3566 LOC: cada concern vive en su tab, no en un Dialog acoplado.

**Glosario verificado**: ✓

---

### 3.4 Empty states de cada tab

**Surface**: Vista de recurso > tab interna sin datos

#### Tab Estado · recurso sin monitoreo

| Elemento | Copy | Caracteres | Regla |
|---|---|---|---|
| Título | "Activa el monitoreo para ver el estado" | 39 | `[7.1]` |
| Descripción | "Configura umbrales o detección con IA y empezarás a ver anomalías aquí." | 73 | `[7.2]` |
| CTA | "Activar monitoreo" | 17 | — |

#### Tab KPIs · sin KPIs definidos

| Elemento | Copy | Caracteres | Regla |
|---|---|---|---|
| Título | "Aún no hay KPIs asociados" | 26 | `[7.1]` |
| Descripción | "Agrega un KPI para medir el desempeño de este recurso." | 56 | `[7.2]` |
| CTA | "Agregar KPI" | 12 | — |

#### Tab Histórico · sin eventos

| Elemento | Copy | Caracteres | Regla |
|---|---|---|---|
| Título | "Sin actividad registrada" | 25 | `[7.1]` |
| Descripción | "Las anomalías, incidentes y cambios aparecerán aquí en orden cronológico." | 75 | `[7.2]` |

#### Tab Notificaciones · sin reglas configuradas

| Elemento | Copy | Caracteres | Regla |
|---|---|---|---|
| Título | "No hay notificaciones configuradas" | 35 | `[7.1]` |
| Descripción | "Define a quién avisar cuando este recurso presente anomalías." | 62 | `[7.2]` |
| CTA | "Agregar notificación" | 21 | — |

#### Tab Configuración · sin parámetros

| Elemento | Copy | Caracteres | Regla |
|---|---|---|---|
| Título | "Configura el monitoreo" | 22 | `[7.1]` |
| Descripción | "Define umbrales, frecuencia de sondeo y la ventana de horario en la que aplica." | 80 | `[7.2]` |
| CTA | "Configurar monitoreo" | 21 | — |

**Glosario verificado**: ✓

---

### 3.5 Activar monitoreo · CTA por contexto

**Surface**: Vista de recurso sin monitoreo > botón primario en el header

| Elemento | Copy | Caracteres |
|---|---|---|
| Botón | "Activar monitoreo" | 17 |
| Tooltip del botón (si recurso no apto) | "Este tipo de recurso aún no admite monitoreo automático" | 55 |
| Toast post-acción (éxito) | "Monitoreo activado" | 18 |
| Toast post-acción (descripción) | "Los umbrales por defecto ya están aplicados. Puedes ajustarlos en Configuración." | 81 |

**Glosario verificado**: ✓

---

### 3.6 Configuración inline · Edición sin modal

**Surface**: Tab "Configuración" > campos editables con autosave

Reemplaza el modal monstruo de 3566 LOC. La edición es inline, los cambios se guardan al perder foco o tras debounce.

| Elemento | Copy | Caracteres | Componente |
|---|---|---|---|
| Section header · umbrales | "Umbrales" | 9 | Typography/section-title |
| Subtítulo de sección | "Define cuándo una variación se considera anomalía." | 51 | Typography/caption |
| Botón inline | "Editar umbrales" | 15 | Button/ghost-sm |
| Estado guardado | "Cambios guardados" | 18 | Inline indicator |
| Estado guardando | "Guardando..." | 12 | Inline indicator |
| Estado error de guardado | "No se pudieron guardar los cambios. Reintenta." | 47 | Inline indicator/error |
| Botón en config existente | "Restablecer valores por defecto" | 31 | Button/text |
| Confirmación de reset · título | "¿Restablecer la configuración?" | 30 | Dialog |
| Confirmación de reset · descripción | "Los umbrales personalizados se reemplazarán por los valores por defecto." | 73 | Dialog `[7.2]` |
| Confirmación de reset · CTA primario | "Restablecer" | 11 | Button |
| Confirmación de reset · CTA secundario | "Cancelar" | 8 | Button |

**Racional**:
- "Editar umbrales" en lugar de "Editar configuración" porque la acción es específica a esa sección.
- "Cambios guardados" en presente porque el estado es persistente; se desvanece tras 2s.
- Confirmación de reset usa pregunta directa sin "¿Estás seguro?" `[3.5]`.

**Glosario verificado**: ✓

---

## 4. User KPI vs System KPI

### 4.1 Diferenciación visual con copy

**Surface**: Tab "KPIs" > listado de KPIs del recurso

Cada fila lleva un badge que distingue el tipo. El badge tiene tooltip explicando el origen.

| Elemento | Copy | Caracteres | Componente |
|---|---|---|---|
| Badge · User KPI | "KPI" | 3 | Badge/neutral |
| Tooltip del badge · User KPI | "Definido por el usuario sobre datos del tablero" | 47 | Tooltip `[7.3]` |
| Badge · System KPI | "Sistema" | 7 | Badge/info |
| Tooltip del badge · System KPI | "Generado automáticamente sobre fuentes de ingesta para complementar el monitoreo" | 80 | Tooltip `[7.3]` |
| Label de sección · User KPIs | "Tus KPIs" | 8 | Section-title |
| Label de sección · System KPIs | "KPIs del sistema" | 16 | Section-title |
| Subtítulo de sección · System KPIs | "Generados por Simetrik a partir de tus fuentes. Puedes activarlos o desactivarlos." | 84 | Caption `[7.2]` |

**Racional**:
- "Sistema" como label en lugar de "Automático" porque el origen es lo que importa al usuario, no el mecanismo.
- "Tus KPIs" en lugar de "KPIs de usuario" usa tuteo `[4.2]` y se siente más cercano.
- Aplica regla `[2.2]` con el término oficial "System KPI" del glosario Op Center, pero el label visible se traduce a "Sistema" porque es la práctica vigente del producto en español.

**Glosario verificado**: ✓

**Nota para LEAD**: el glosario tiene "System KPI" en inglés como término oficial. Decisión: el badge usa "Sistema" (español, breve), el tooltip y la documentación interna mantienen "System KPI". Si Producto prefiere "System" puro en la UI, ajustamos.

---

### 4.2 Tooltip explicando System KPI · "¿Por qué este KPI existe?"

**Surface**: Tab "KPIs" > fila de System KPI > icono de info al lado del nombre

| Elemento | Copy | Caracteres | Regla |
|---|---|---|---|
| Tooltip (estado activo) | "Este KPI complementa el monitoreo del recurso. Mide la salud de la fuente de ingesta {nombre_fuente}." | dinámico | `[7.3]` con punto (2 oraciones) |
| Tooltip (estado por cascada) | "Se activó automáticamente cuando habilitaste el monitoreo en {nombre_KPI_usuario}." | dinámico | `[7.3]` 1 oración, sin punto |

**Racional**: traduce el concepto de "cascada automática" del glosario a una explicación que el analista entienda: "se activó cuando hiciste X".

**Glosario verificado**: ✓

---

### 4.3 Toggle activar/desactivar System KPI

**Surface**: Tab "KPIs" > fila de System KPI > toggle a la derecha

| Elemento | Copy | Caracteres |
|---|---|---|
| Label del toggle | "Monitorear" | 10 |
| Estado activado · sublabel | "Activo · evaluado cada {frecuencia}" | dinámico |
| Estado desactivado · sublabel | "Desactivado" | 11 |
| Confirmación al desactivar · título | "¿Desactivar este KPI?" | 21 |
| Confirmación al desactivar · descripción | "Dejarás de recibir alertas relacionadas con esta fuente. Puedes reactivarlo cuando quieras." | 93 |
| Confirmación · CTA primario | "Desactivar" | 11 |
| Confirmación · CTA secundario | "Mantener activo" | 16 |
| Toast post-acción · activar | "KPI activado" | 13 |
| Toast post-acción · desactivar | "KPI desactivado" | 16 |
| Toast post-acción · descripción (desactivar) | "Ya no recibirás alertas de este KPI." | 37 |

**Glosario verificado**: ✓

---

## 5. Hilo IA inline en la vista de recurso

### 5.1 Frase tipo de la hipótesis

**Surface**: Card de hipótesis IA (sección 3.2) > cuerpo del resumen

Tres shapes por estado del recurso. Todos usan placeholders `{variable}` para que el Front Designer interpole.

#### Shape: recurso sin anomalía

```
El recurso opera dentro de su patrón habitual. Último análisis: {tiempo_relativo}.
```

Caracteres aproximados: 80. Tono neutro, informar.

#### Shape: recurso con anomalía activa, dato cuantificado

```
Detecté una {dirección} de {pct}% en {nombre_KPI} durante {ventana}. Está {comparación} del rango habitual de los últimos {período_baseline}.
```

Donde:
- `dirección` ∈ {"caída", "subida"}
- `pct` = número entero
- `nombre_KPI` = string
- `ventana` ∈ {"la última hora", "las últimas 24 horas", "los últimos {N} días"}
- `comparación` ∈ {"por debajo", "por encima"}
- `período_baseline` ∈ {"30 días", "90 días"}

**Ejemplo renderizado**: "Detecté una caída de 18% en `Volumen de transacciones` durante las últimas 24 horas. Está por debajo del rango habitual de los últimos 30 días."

Caracteres: ~150.

#### Shape: recurso con anomalía + recomendación

Agrega una segunda oración al shape anterior:

```
{primera oración del shape anterior} Suele ocurrir cuando {causa_probable}. Te recomiendo revisar {acción_sugerida}.
```

Donde:
- `causa_probable` viene del catálogo de Smart Rules / Categoría de problema (ej. "una fuente de ingesta deja de cargar archivos a tiempo", "se aplicó un cambio reciente al modelo contable").
- `acción_sugerida` mapea al recurso (ej. "el estado de la fuente {nombre}", "los últimos archivos del repositorio {nombre}").

**Ejemplo renderizado**: "Detecté una caída de 32% en `Tasa de match` durante las últimas 6 horas. Está por debajo del rango habitual de los últimos 30 días. Suele ocurrir cuando una fuente de ingesta deja de cargar archivos a tiempo. Te recomiendo revisar el estado de la fuente `bank_statements_daily`."

Caracteres: ~270.

**Glosario verificado**: ✓ (sin `breach_pct`, sin `severity`)

---

### 5.2 Acciones bajo la hipótesis

**Surface**: Card de hipótesis IA > acciones cuando hay incidente activo

Botones secundarios alineados al pie de la card. Verbo en infinitivo, máx. 25 caracteres `[regla CTA]`.

| Acción | Copy | Caracteres | Variante | Racional |
|---|---|---|---|---|
| Tomar el incidente | "Investigar incidente" | 20 | Button/primary | "Tomar" suena a apropiación; "Investigar" describe la acción mental del analista. Mapea al estado `En investigación` del ciclo de vida. |
| Ver detalle | "Ver detalle" | 11 | Button/outline | Acción genérica de profundizar sin tomar ownership. |
| Silenciar 1h | "Silenciar 1 hora" | 16 | Button/ghost | Específico sobre cuánto tiempo. Sin abreviar "h" porque rompe en otros idiomas. |
| Descartar | "Descartar" | 9 | Button/ghost-destructive | Término del glosario clásico (descartar ≠ eliminar). Sin "Ignorar" (anglicismo de tono). |

**Confirmaciones**:

| Acción | Título | Descripción | CTA primario | CTA secundario |
|---|---|---|---|---|
| Silenciar 1h | "¿Silenciar este incidente por 1 hora?" | "No recibirás nuevas alertas relacionadas durante este período. Al finalizar, el monitoreo vuelve a su comportamiento normal." | "Silenciar 1 hora" | "Cancelar" |
| Descartar | "¿Descartar este incidente?" | "Se marcará como falso positivo y se cerrará. Puedes reabrirlo desde Histórico si fue un error." | "Descartar" | "Cancelar" |

**Glosario verificado**: ✓

---

### 5.3 IA cuando no hay incidente

**Surface**: Card de hipótesis IA > recurso saludable

Decisión: **la IA sigue hablando**, no silencio total. El valor de la presencia del Agente IA es que el analista confía en que alguien está vigilando.

| Estado | Copy | Caracteres | Racional |
|---|---|---|---|
| Sin anomalía · primer mensaje | "El recurso opera dentro de su patrón habitual. Último análisis hace {tiempo_relativo}." | dinámico | Informar + tranquilizar sin felicitar. No "Todo bien", no "✓ Estable". |
| Sin anomalía · ventana extendida | "Sin anomalías detectadas en los últimos {N} días." | dinámico | Aparece tras 7+ días sin incidentes; refuerza la confianza por acumulación. |

**Glosario verificado**: ✓

**Nota para LEAD**: alternativa "silencio total" se descarta porque rompe la promesa del patrón C (hilo IA continuo). El presupuesto cognitivo es bajo: una sola oración neutra.

---

## 6. Lista de incidentes · Lente "Actividad"

### 6.1 Header de la lente

**Surface**: Tab "Actividad" > zona superior

| Elemento | Copy | Caracteres | Componente |
|---|---|---|---|
| Título de la lente | "Actividad" | 9 | Typography/h2 |
| Subtítulo | "Incidentes, señales y eventos de tus recursos monitoreados." | 60 | Typography/caption `[7.2]` |
| Botón secundario | "Exportar" | 9 | Button/outline |
| Botón primario (crear manual) | "Reportar incidente" | 18 | Button/primary |

**Glosario verificado**: ✓

---

### 6.2 Filtros chip

**Surface**: Tab "Actividad" > barra de filtros sobre la lista

Cada chip es un filtro con label corto. Cuando está activo, muestra el valor seleccionado.

| Filtro | Label inactivo | Label activo (ejemplo) | Caracteres |
|---|---|---|---|
| Estado | "Estado" | "Estado: Abierto, En investigación" | 6 / dinámico |
| Severidad | "Severidad" | "Severidad: Urgente, Alta" | 9 / dinámico |
| Recurso | "Recurso" | "Recurso: Reconciliación bancaria" | 7 / dinámico |
| Origen | "Origen" | "Origen: Sistema" | 6 / dinámico |
| Período | "Período" | "Últimos 7 días" | 7 / dinámico |
| Acción | "Limpiar filtros" | — | 15 |

**Valores del filtro Severidad**: Urgente · Alta · Media · Baja (en este orden).
**Valores del filtro Estado**: En observación · Abierto · En investigación · Confirmado · Resuelto · Cerrado.
**Valores del filtro Origen**: Sistema · Usuario.

**Glosario verificado**: ✓

---

### 6.3 Empty state de Actividad

**Surface**: Tab "Actividad" > lista vacía

| Estado | Título | Descripción | CTA |
|---|---|---|---|
| Sin actividad histórica | "Sin actividad por ahora" | "Las anomalías detectadas y los incidentes que reportes aparecerán aquí." | — |
| Sin resultados con filtros aplicados | "No encontramos incidentes con estos filtros" | "Ajusta o limpia los filtros para ver más resultados." | "Limpiar filtros" |

**Glosario verificado**: ✓

---

### 6.4 Card de incidente · Anatomía del copy

**Surface**: Tab "Actividad" > fila de incidente en la lista (formato card)

Cada card tiene cinco elementos de copy.

| Elemento | Copy / shape | Caracteres | Componente |
|---|---|---|---|
| Título (generado por IA) | shape: "{Categoría de problema} en {nombre_recurso}" | dinámico, ~60 | Typography/body-strong |
| Contexto (1 línea) | shape: "{Métrica} {comparación} en {pct}% durante {ventana}" | dinámico, ~70 | Typography/caption |
| Severidad (badge) | "Urgente" / "Alta" / "Media" / "Baja" | 4–7 | Badge |
| Recurso afectado (label + valor) | "Recurso: {nombre}" | dinámico | Typography/micro |
| Tiempo relativo | shape: "Hace {tiempo}" | dinámico | Typography/micro |
| Estado (badge) | "En observación" / "Abierto" / "En investigación" / "Confirmado" / "Resuelto" / "Cerrado" | 6–17 | Badge |

**Acciones rápidas en hover**:

| Acción | Copy | Caracteres |
|---|---|---|
| Abrir | "Abrir" | 5 |
| Asignar | "Asignar" | 7 |
| Posponer | "Posponer" | 8 |
| Descartar | "Descartar" | 9 |

**Ejemplo de card renderizada**:
- Título: "Archivo faltante en Reconciliación bancaria diaria"
- Contexto: "Volumen de transacciones por debajo en 24% durante las últimas 6 horas"
- Severidad: Alta
- Recurso: Recurso: Reconciliación bancaria diaria
- Tiempo: Hace 12 minutos
- Estado: Abierto

**Glosario verificado**: ✓ (usa "Categoría de problema" y "Anomalía" del glosario)

---

## 7. Estados de error y borde

### 7.1 Error de fetch del recurso

**Surface**: Vista de recurso > toda la página cuando el fetch falla

| Elemento | Copy | Caracteres | Componente | Regla |
|---|---|---|---|---|
| Título | "No se pudo cargar el recurso" | 28 | Alert/title | `[7.1]` `[3.5]` |
| Descripción | "Verifica tu conexión e intenta de nuevo. Si el problema persiste, contacta a soporte." | 88 | Alert/desc | `[7.2]` `[3.5]` |
| CTA primario | "Reintentar" | 11 | Button/primary | — |
| CTA secundario | "Volver a la lista" | 17 | Button/outline | — |

---

### 7.2 Permiso denegado · Read-only

**Surface**: Vista de recurso > usuario sin permiso de edición

| Elemento | Copy | Caracteres | Componente | Regla |
|---|---|---|---|---|
| Banner superior | "Tienes acceso de solo lectura a este recurso." | 46 | Alert/info | `[7.2]` |
| Banner descripción | "Solicita permiso a un administrador para editar la configuración." | 65 | Alert/desc | `[7.2]` |
| Botón del banner | "Solicitar acceso" | 16 | Button/text | — |
| Tooltip en botones deshabilitados | "Necesitas permiso de edición para esta acción" | 46 | Tooltip `[7.3]` |

---

### 7.3 Recurso archivado o eliminado

**Surface**: Vista de recurso > el recurso fue archivado o eliminado por otro usuario

| Caso | Título | Descripción | CTA |
|---|---|---|---|
| Archivado | "Este recurso está archivado" | "El monitoreo está pausado. Puedes restaurarlo desde la papelera del espacio de trabajo." | "Ir a papelera" |
| Eliminado | "Este recurso ya no existe" | "Fue eliminado del espacio de trabajo. Si crees que es un error, contacta a un administrador." | "Volver a la lista" |

**Glosario verificado**: ✓ ("papelera" del glosario clásico)

---

### 7.4 Configuración inválida

**Surface**: Tab "Configuración" > validación inline al guardar

| Caso | Mensaje | Caracteres | Componente | Regla |
|---|---|---|---|---|
| Umbral fuera de rango | "El valor debe estar entre {min} y {max}" | dinámico | Helper/error inline `[7.3]` |
| Umbral mayor que el superior | "El umbral inferior debe ser menor que el superior" | 48 | Helper/error inline `[7.3]` |
| Frecuencia inválida | "Selecciona una frecuencia de sondeo" | 36 | Helper/error inline `[7.3]` |
| Ventana de horario inválida | "La hora de inicio debe ser anterior a la hora de fin" | 53 | Helper/error inline `[7.3]` |
| Sin notificaciones configuradas + monitoreo activo | "Configura al menos una notificación para recibir alertas" | 56 | Alert inline `[3.5]` `[7.3]` |
| Error al guardar (genérico) | "No se pudieron guardar los cambios. Reintenta o recarga la página." | 65 | Toast/error `[3.5]` `[7.2]` |

**Glosario verificado**: ✓

---

## Tensiones documentadas

| Elemento | Tensión | Reglas | Decisión tomada |
|---|---|---|---|
| Top-nav "Anomalías" → "Monitoreo" | Familiaridad vs alineación con el refactor | `[2.1]` `[2.2]` | Recomendar el cambio. Si Producto prefiere conservar "Anomalías" para no romper expectativas, retroceder en esta iteración. Documentado en sección 1.1. |
| Header de la card de IA | Conversacional ("¿Qué está pasando aquí?") vs funcional ("Resumen del Agente IA") | `[1.3]` `[2.1]` `[4.4]` | Elegí "Resumen del Agente IA". Profesionalismo sin solemnidad gana sobre warmth conversacional. |
| Voz del Agente IA en primera persona ("Detecté", "Te recomiendo") | Diferenciación de marca vs riesgo de antropomorfizar | `[1.3]` `[4.4]` | Mantener primera persona moderada en la card de hipótesis. Necesita consistencia con Solutions Agent y Executive Summary; flag al LEAD. |
| Badge "Sistema" para System KPI | El glosario tiene "System KPI" en inglés como oficial, pero el badge necesita un label breve en español | `[2.2]` | Badge usa "Sistema" (label en español, breve). Tooltip y documentación interna mantienen "System KPI". Riesgo bajo: el badge no es el término oficial, solo su representación visual. |
| "Tus KPIs" como label de sección | Cercanía con tuteo vs neutralidad institucional | `[4.2]` | Aplicar tuteo `[4.2]`. "Tus KPIs" es consistente con la voz Simetrik. |
| Severidad "Urgente / Alta / Media / Baja" en badge del card de incidente | El glosario menciona estas categorías pero no las prioriza | `[2.2]` | Mantener las 4 severidades; alinearlas con la priorización jerárquica del Brief (Ingestion > Data Quality > Operational Results > Financial Results) se hace a nivel de scoring, no de label. |

---

## Textos fuera de scope

- Copy de los gráficos individuales dentro de KPIs (axis labels, tooltips de datapoints) — fuera del refactor de navegación.
- Copy del onboarding al Operation Center — fuera del scope, ya cubierto por otro flujo.
- Copy de notificaciones externas (cuerpo del Email, mensaje de Slack) — referenciado en SWAT-563 / DOE24, ciclo separado.
- Copy del modal `AnomalyMonitoringConfig` legacy — se elimina con el refactor, no se actualiza.
- Copy del componente AiChat / Sheet lateral del agente conversacional — fuera del scope de este refactor.

---

## Notas para Product Designer

- El header de la card de hipótesis IA ("Resumen del Agente IA") necesita 21 caracteres + ícono. Si el componente Card tiene padding ajustado, considerar typography/h4 en lugar de h3.
- El badge "Sin monitoreo" (13 caracteres) coexiste con badges de estado (≤19 caracteres). Validar que el componente Badge soporta ambos sin ruptura.
- El tooltip del System KPI por cascada usa 2 placeholders dinámicos; el componente debe soportar truncado del nombre del KPI si supera 30 caracteres.
- El subtítulo del recurso "{Tipo} · ID {recursoId}" usa el carácter `·` (middle dot, U+00B7) como separador. Verificar fuente.

---

## Notas para Front Designer

Placeholders dinámicos a interpolar:

- `{Nombre del recurso}` — string, máx. 80 caracteres, truncar con elipsis a 40 en breadcrumbs y a 30 en sidebar.
- `{Tipo}` — enum: "Conciliación", "Fuente", "Unión de fuentes", "Tablero", "Dataset".
- `{recursoId}` — string corto, formato `OC-{slug}-{n}`.
- `{nombre_KPI}` — string, máx. 60 caracteres.
- `{pct}` — número entero (sin decimales en el copy).
- `{dirección}` — enum: "caída" | "subida".
- `{ventana}` — enum: "la última hora", "las últimas 24 horas", "los últimos {N} días".
- `{tiempo_relativo}` — formato natural: "hace 5 minutos", "hace 2 horas", "hace 3 días". Usar utilidad de tiempo relativo existente.
- `{frecuencia}` — enum: "5 minutos", "15 minutos", "1 hora", "1 día".
- `{N}` — entero positivo.
- `{nombre_fuente}` — string del recurso fuente, máx. 60 caracteres.
- `{Categoría de problema}` — enum cerrado del glosario: "Archivo faltante", "Archivo fallido", "Variación de volumen", etc.

Toast duration: 4000 ms por defecto, 6000 ms en toasts con descripción larga (sección 4.3, 3.5).

Inline indicators de autosave (sección 3.6) se desvanecen tras 2000 ms.

---

## Contexto adicional solicitado

```yaml
contexto_adicional_solicitado:
  - fuente:     copy_previo
    motivo:     Confirmar si "System KPI" debe mantenerse en inglés en la UI o si "Sistema" como label en español ya está validado por Producto. Afecta sección 4.1.
    bloqueante: false
  - fuente:     locales
    motivo:     Voz de los otros Agentes IA (Solutions, Executive Summary, Error Intelligence). Decidí primera persona moderada en la card de hipótesis; necesito alinear con los demás para evitar inconsistencia.
    bloqueante: false
  - fuente:     producto
    motivo:     Si el cambio top-nav "Anomalías" → "Monitoreo" rompe deep links existentes, dashboards de métricas internas o entrenamientos del cliente. Si rompe, retroceder en esta iteración.
    bloqueante: false
```
