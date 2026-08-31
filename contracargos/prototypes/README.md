# Prototipos — Contracargos

| Archivo | Qué es | Estado |
|---|---|---|
| `acceso-marketplace.html` | **⭐ El que se presenta.** El camino del merchant desde el Marketplace hasta el tablero operando | Al día con la sesión del 28-ago |
| `contracargos-merchant.html` | El tablero al que llega. Tokens desyk reales | Iterable, 28-ago-2026 |
| `../plans/archivo-agosto-2026/presentacion-ab-2026-08-27.html` | La presentación A/B sobre el proto de Andrea. **Archivada:** la opción B se descartó el 28-ago | Archivo |
| `../plans/archivo-julio-2026/proto-andrea-original-2026-06-30.html` | El proto de Andrea **sin tocar** | Respaldo del original |

---

## Qué cambió el 28-ago

La sesión con Andrea cerró el A/B y reacotó el prototipo. Las decisiones y su rastro están en `../plans/05-cambios-post-sesion-28-ago.md`; acá queda lo que se ve en pantalla:

- **Gana el Marketplace.** La opción B (sugerencia proactiva en el Centro de operaciones) se descartó y salió del prototipo. Le quitaba visibilidad al usuario —si el motor no podía armar el tablero, el merchant nunca se enteraba de que podía— y una sugerencia que se cierra obliga a inventar cómo devolverla
- **Una tarjeta por tipo de actor** en el catálogo: merchant, adquirente, PSP y emisor. Se descartó que el backend infiriera el actor por la industria del cliente, porque hay clientes que son dos cosas a la vez: Melin tiene Mercado Pago (PSP) y marketplace, y dLocal opera cuatro industrias. Solo merchant navega; adquirente ya existe en dev y hay que refinarlo, PSP está por definir y emisor queda fuera de alcance
- **Sin selector de rol dentro del tablero.** El actor lo define el template que se instaló, no un switch en la vista
- **Sin pestaña de Disputas.** Baja a ser un gráfico más del tablero, para que el usuario no tenga que irse a otro lado
- **Sin flujo del emisor.** Los 8 pasos tipo Mastercard son de otro actor que todavía no se toca

---

## acceso-marketplace.html

Siete pasos, recorribles con el rail de arriba o con Atrás / Siguiente. Alpine + Tailwind sobre los tokens de `design.md`.

| # | Paso | Qué muestra |
|---|---|---|
| 1 | Catálogo | Las cuatro tarjetas por actor dentro de la categoría *contracargos*, que ya existe en dev |
| 2 | Detalle | Vista previa con datos de ejemplo, el **árbol de dependencias** de todo lo que se va a crear y qué hereda del Centro de operaciones |
| 3 | Espacio de trabajo | Dónde se instala. La pantalla ya existe en el Marketplace |
| 4 | Instalación | Asíncrona: tablero, conjuntos de datos, conciliaciones y anomalías |
| 5 | Aterrizaje | El tablero creado **aunque falte una fuente**. No bloquea: solo espera lo que depende de ella |
| 6 | Conectar la fuente | Vincular recursos existentes en vez de cargar archivos, con la confianza del motor y las dos salidas para corregir |
| 7 | Tablero listo | Operando, con el monitoreo vigilando el ratio y las fuentes |

### El argumento, en una línea

**Economía de lógica.** El Marketplace ya resuelve separar casos de uso, elegir espacio, mostrar el árbol de dependencias, manejar la fuente faltante y crear el conjunto de datos. Y como lo instalado es un conjunto de datos normal, el tablero hereda gratis las anomalías, las alertas por incidente y los resúmenes del Operation Center.

### Lo que hay que resolver, y no es de diseño

- **¿Todos los clientes ven el Marketplace?** Es el bloqueante real. Si el acceso está restringido por permisos, el camino de entrada se replantea entero
- El catálogo es **global, cross-account**: publicar Contracargos significa que lo ven todas las cuentas habilitadas, no solo los marketplaces
- **No hay actualización en sitio:** quien ya instaló se queda con la versión vieja del template
- Alinear con **Pedro Marota**, que va a montar controles de contracargos desde el Simetrik Agent

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
- El ciclo de vida del contracargo está bloqueado hasta que Santi confirme las llaves de cruce
- **Averiguar los permisos de acceso al Marketplace por tipo de cliente.** Bloqueante: si no todos lo ven, el camino de entrada se replantea
- Refinar los templates de contracargos que ya están en dev (categoría y template de adquirencia, de Daiver Doria)
- Definir qué métricas cambian para PSP y para adquirente respecto al merchant
