# Prototipos — Contracargos

| Archivo | Qué es | Estado |
|---|---|---|
| `../Simetrik · Centro de Disputas — Operations Center.html` | **⭐ El archivo de la presentación.** El proto de Andrea, con las dos experiencias de acceso integradas encima | Listo para presentar, 27-ago-2026 |
| `acceso-al-tablero-ab.html` | Las mismas dos experiencias, versión limpia sobre tokens desyk | Alterno, 26-ago-2026 |
| `contracargos-merchant.html` | El tablero al que llegan las dos. Tokens desyk reales | Iterable, 26-ago-2026 |
| `plans/archivo-julio-2026/proto-andrea-original-2026-06-30.html` | El proto de Andrea **sin tocar** | Respaldo del original |

---

## El archivo de la presentación

Los dos caminos viven **dentro del prototipo de Andrea**, que es el que se presenta. Se añadieron como una capa: todo lleva prefijo `pz-` y se inyecta por JavaScript, así que **el markup y el JS originales no se modificaron**. El respaldo del original está en `plans/archivo-julio-2026/`.

**Cómo se maneja en vivo**

| Gesto | Qué hace |
|---|---|
| Botones **Opción A / Opción B** | Cambia de camino y vuelve al paso 1 |
| Rail de pasos | Salta a cualquier paso |
| **← →** | Paso anterior y siguiente |
| **A** / **B** | Salta de camino sin usar el mouse |

Cada paso trae abajo el título de lo que se ve y por qué, para no tener que recordar el guion. Cuando el paso depende de algo que no existe todavía, sale una etiqueta amarilla a la derecha.

Los caminos usan el shell real del prototipo: el sidebar marca Marketplace o Centro de operaciones según dónde esté el usuario, y el tablero final es el mismo de Andrea. El tab **Tableros** del header devuelve siempre al tablero ya montado.

---

## acceso-al-tablero-ab.html

Responde la pregunta que dejó Andrea: *"no sé dónde meterle el cómo llegar a esa mierda del tablero"*. Dos experiencias completas, recorribles paso a paso, con switch arriba.

### Opción A · Template en el Marketplace — 4 pasos

1. **Catálogo** con Contracargos
2. **Detalle**: vista previa del tablero, categorías, publicador, beneficios
3. **Instalación** asíncrona
4. **Tablero operando**, usable de una

> Las fuentes de notificados y debitados de los marketplaces ya están integradas en Simetrik, así que el template se instala con fuentes preintegradas: **no hay pantalla de configuración, ni carga de archivos, ni widgets bloqueados**.

### Opción B · Sugerencia en el Centro de operaciones — 3 pasos

1. **Lo ve sugerido** en su lista de tableros, sin buscarlo
2. **Revisa qué se detectó**, con la confianza por recurso y la opción de corregir
3. **Tablero operando**

### El argumento

Las dos terminan en el **mismo tablero**. La puerta se decide después; el contenido no cambia. Por eso no son dos construcciones, son la misma con dos entradas: cuando A existe, la sugerencia de B simplemente instala el template ya publicado.

Recomendación: **A primero, B después.** A no inventa interfaz: el template, el preview, la instalación y el destacado del catálogo ya están construidos y verificados en `fe-solutions-mf` y en el Brain. Y con las fuentes preintegradas queda en 3 clics, contra 2 de B, así que **el argumento de "menos pasos" que sostenía a B se desinfló**. Lo que le queda a B es que el merchant no tiene que saber que el template existe; es real, pero ya no compensa inventar un patrón de "sugerido" en esta iteración.

### Lo que hay que decidir el viernes, y no es de diseño

- El catálogo del Marketplace es **global, cross-account**. No hay segmentación por cuenta: publicar Contracargos significa que lo ven todas las cuentas habilitadas, no solo los 11 marketplaces
- **No hay actualización en sitio.** Si mejoramos el template, quien ya lo instaló se queda con la versión vieja
- Los nombres de los recursos instalados se sufijan con timestamp

### Hallazgo que vale la pena resaltar en la presentación

**Instalar y ya.** Para los marketplaces el template se arma con fuentes preintegradas, así que entre abrir el catálogo y tener el control operando hay tres clics. Ese es el argumento más fuerte de la opción A y conviene decirlo con esas palabras.

---

## contracargos-merchant.html

Tailwind CDN + Alpine + Lucide, tokens de `design.md`. Un solo archivo, sin dependencias de build.

**Selector de estado** arriba a la derecha, para recoger feedback:

| Estado | Qué muestra |
|---|---|
| Operación normal | El día a día. Visa a 0,08 puntos de romper VAMP |
| Umbral roto | Visa en 1,68%, por encima de VAMP. El semáforo gana jerarquía |
| Detección parcial | El motor clasificó 3 de 9 recursos, confianza 31%. Bloque AI con las salidas para corregir |

## Qué se corrigió respecto al proto de Andrea

**Estructura**
- El switch de 4 roles (Issuer / Merchant / PSP / Adquirente) **colapsa a merchant**. Los otros tres eran material de demo comercial
- Fuera el flujo agéntico de 8 pasos y el ChargeScore: son del mundo del emisor, no del merchant que recibe el débito
- Subtabs reacotados a **Resumen · Notificados · Debitados · Controles**
- **El tab "Disputas" no existe en producción.** El OC real tiene 5: Tableros, Anomalías, Pendientes, Almacenamiento, Asientos contables. El prototipo ahora usa esos cinco

**Fidelidad con el frontend real** (verificado en `fe-solutions-mf`)
- Header de `h-14`, `px-7`, con ícono Radar + título + badge Beta
- Tabs del top nav en píldora circular, no subrayados (`TabsList size="lg" shape="circle"`)
- Header del tablero con padding `pl-4 pr-5 pt-5 pb-3` y botones de `h-[30px]`
- Botón de Monitoreo como botón normal con badge `success`, no como botón verde
- Sidebar en light con los tokens `--sidebar-*`. Nunca dark
- Chat como botón en el pie del sidebar que abre panel lateral

**Diseño**
- Tokens reales de `desyk-components@1.30.0-0`: `--primary` es `#3939F9`, no el `#3b63e6` del proto original. Paleta `chart-1..8` de desyk para las categóricas
- Los **estados de negocio usan color semántico**, no la paleta de charts, para que el color signifique lo mismo en todas partes
- El gradiente AI marca **solo lo inferido** por el sistema, nunca lo que configuró el usuario
- Inter, `tabular-nums` en todo lo financiero, moneda visible
- Todo en español. El proto original mezclaba dashboard en español con el flujo agéntico en inglés

**Contenido**
- **Notificado y debitado no se suman.** Son dos KPIs separados, porque son dos dolores distintos
- El tercer KPI no es un número, es un **semáforo con la distancia al umbral**
- **Umbral corregido: VAMP ya no es 2,20%.** Bajó a 1,50% el 1-abr-2026. Y se explica en el panel por qué el umbral va por red y no agregado: VAMP suma fraude TC40, ECM cuenta solo contracargos
- Los tres controles operativos (tarjetas por bloquear, doble débito, cruce con venta interna) tienen su propia pestaña, cada uno como lista accionable
- El panel de monitoreo hace visible que **se vigilan dos cosas**: la columna del dato de negocio y las fuentes que la alimentan

## Pendiente

- Las pestañas Notificados y Debitados son placeholder, falta definir columnas con Andrea
- Falta el prototipo A/B/C de las rutas de acceso (`plans/01`), que es el otro entregable del viernes
- El ciclo de vida del contracargo está bloqueado hasta que Santi confirme las llaves de cruce
