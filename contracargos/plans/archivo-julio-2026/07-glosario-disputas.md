# Glosario — Centro de Disputas (contracargos)

Referencia de dominio para todo el proyecto (planes, flujos de Ohana, prototipo y copy). Fuentes: reuniones con Andrea (7 y 9 jul 2026), prototipo `Centro disputas.html` y estándares de las redes de pago.

## Actores del ecosistema

| Término | Definición |
|---------|------------|
| **Tarjetahabiente** | Dueño de la tarjeta. Inicia el reclamo ante su banco cuando desconoce o disputa un cobro. |
| **Banco emisor (Issuer)** | Banco que emitió la tarjeta. Recibe y valida el reclamo del tarjetahabiente y lo eleva a la red. **Fuera de alcance en esta fase.** |
| **Marca / Red (Franquicia)** | Visa, Mastercard, Amex. Clasifica la disputa con un reason code, mueve los fondos y arbitra. |
| **Adquirente** | Entidad que procesa pagos para el comercio ante la red (ej. dLocal, Cielo, Rede, Getnet). Recibe el contracargo de la marca, debita al merchant y le notifica. **Usuario primario de nuestro diseño.** |
| **PSP (Payment Service Provider)** | Proveedor de servicios de pago que agrega merchants (ej. PayU, Stripe, Adyen, EBANX). En este proyecto se usa junto con "adquirente" — es quien sufre el dolor de los SLA con volumen alto. |
| **Merchant (Comercio)** | Quien vendió (ej. Rappi, PedidosYa, Adidas). Decide si acepta el contracargo o lo disputa; es quien pierde o recupera el dinero. Receptor en la capa de remediación. |

## Ciclo de vida de la disputa

| Término | Definición |
|---------|------------|
| **Disputa** | Proceso formal en el que se cuestiona una transacción. Término paraguas de todo el flujo. |
| **Contracargo (CBK / Chargeback)** | Reverso del cobro: la marca debita al adquirente y este al merchant mientras se resuelve la disputa. |
| **Reason code** | Código con el que la marca clasifica el motivo de la disputa. Ejemplos reales: Visa **10.4** (fraude CNP), **13.1** (producto no recibido), **13.3** (no como se describe), **12.6** (pago duplicado), **11.3** (autorización tardía); Mastercard **4853** (defectuoso/no como se describe), **4837** (fraude), **4834** (procesamiento duplicado); Amex **C08**, **F24**. |
| **Representment (2ª presentación)** | Acción del merchant/adquirente de re-presentar la transacción con evidencia para revertir el contracargo. Es "disputar la disputa". |
| **Pre-arbitration (pre-arb)** | Fase previa al arbitraje: una parte rechaza el representment y la otra puede responder con más evidencia o aceptar antes de escalar. |
| **Arbitration (arbitraje)** | Última instancia: la marca decide quién gana. Tiene costos altos por caso. |
| **SLA** | Plazo máximo de cada etapa (responder, presentar evidencia). Si vence, se pierde la disputa por default — el dolor central del proyecto. |
| **Aging** | Días que lleva el contracargo en el flujo. Junto con el SLA restante define la prioridad de atención. |
| **Fases del pipeline (proto)** | Recepción → Investigación → Presentación → Revisión de red → Resuelto. |
| **Estados (proto)** | Vinculado · Requiere (acción) · Por presentar · Ganado · Perdido. |

## Identificadores y datos de la transacción

| Término | Definición |
|---------|------------|
| **ARN (Acquirer Reference Number)** | Identificador único de 23 dígitos que el adquirente asigna a la transacción al enviarla a la red. Viaja por todo el ciclo (compra, clearing, contracargo). Llave principal del cruce con conciliaciones. |
| **AUTH (código de autorización)** | Código corto (~6 caracteres) que genera el emisor al aprobar la compra. Segunda llave del cruce: **ARN + AUTH = match determinístico** (100% confianza en el proto). |
| **BIN** | Primeros 6-8 dígitos de la tarjeta; identifican al banco emisor. Llave secundaria de cruce. |
| **Token ID / Transaction ID** | Identificadores internos del procesador/pasarela para la transacción. Llaves secundarias cuando ARN o AUTH no llegan limpios. |
| **MCC** | Merchant Category Code: rubro del comercio (ej. 5942 librerías). Se usa en validaciones de cumplimiento. |
| **AVS** | Address Verification Service: verificación de dirección en la autorización ('Y' = coincide). Evidencia a favor del merchant. |
| **3DS (3-D Secure)** | Autenticación del tarjetahabiente en la compra. Si hubo 3DS 2.0, el fraude suele ser responsabilidad del emisor — evidencia fuerte. |
| **POS Entry Mode** | Cómo se capturó la tarjeta (ej. 81 = e-commerce). Contextualiza el tipo de transacción. |
| **ISO 8583 / mensaje 1442** | Estándar de mensajería financiera; el 1442 es el mensaje de presentación del contracargo/representment en la red. Lo arma el agente de filing. |
| **Clearing & settlement** | Compensación y liquidación: el movimiento real de fondos entre bancos. Contra esto se concilia. |

## Plataformas y programas de red

| Término | Definición |
|---------|------------|
| **Mastercom** | Plataforma de Mastercard donde se gestionan y presentan disputas. Destino del agente de filing. |
| **Verify (Visa Resolve Online)** | Equivalente de Visa para gestión de disputas. |
| **VAMP (Visa Acquirer Monitoring Program)** | Programa de Visa que monitorea el ratio de disputas/fraude del adquirente y sus merchants. Umbral 2.20% → baja a **1.50% desde abr-2026**; superarlo trae sanciones. KPI del tablero. |
| **ECM / HECM (Mastercard)** | Excessive Chargeback Merchant (1.50%) / High Excessive (3%): programas de Mastercard que sancionan merchants con exceso de contracargos. |
| **TC40 / SAFE** | Reportes de fraude que el emisor envía a la red (TC40 = Visa). Llegan **antes** que el contracargo (15-20 días de anticipación en el proto) — señal temprana. |
| **Verifi (Visa) / Ethoca (Mastercard)** | Servicios de alerta y resolución temprana de disputas (deflection) antes de que se vuelvan contracargo. |
| **Double-dip** | Cuando el merchant pierde dos veces el mismo monto (ej. reembolsó Y recibió el contracargo). El agente lo detecta en el cruce. |

## Métricas y elementos del producto

| Término | Definición |
|---------|------------|
| **Win probability** | Probabilidad de ganar una disputa específica, calculada por el agente (reglas mapeadas + inferencia) sobre data conciliada. Siempre con explicación del razonamiento. **Solo por disputa — el win rate agregado se descartó (9-jul).** |
| **ChargeScore** | Nombre del win probability en el proto de Andrea (adaptado de Chargeflow): anillo con el %, recuperación estimada, tiempo/OPEX ahorrado y disclaimer *"señal de priorización, no promesa"*. |
| **Ratio tipo VAMP** | KPI del tablero: qué tan cerca está el adquirente/merchant de romper los umbrales de las redes. |
| **Recuperación estimada** | Monto que el agente estima recuperar si se gana la disputa. Solo por disputa; el "$ recuperado" agregado se descartó como no calculable. |
| **Cola priorizada** | Tabla de reclamos ordenada por SLA restante + aging + win probability. Corazón de la capa de operatividad. |
| **La "carta"** | Detalle estructurado del caso: línea de vida, resumen (ARN, AUTH, BIN, reason), cruce con conciliación y análisis del agente. |
| **Gate humano** | Regla del flujo: nada se presenta a la red sin aprobación del analista (salvo automatización sobre umbral — pendiente con Sergio). |
| **Umbral de automatización** | Win probability a partir de la cual el agente corre solo (hipótesis ≥80%). Pendiente de validar con Sergio y equipo de anomalías. |
| **Canal de salida** | Cómo llega la solicitud de evidencia del adquirente al merchant: export de dataset, API GET o vinculación de cuentas Simetrik (ideal, efecto de red). |

## Términos Simetrik (glosario obligatorio del producto)

| Término | Uso en este proyecto |
|---------|----------------------|
| **Conciliación** | Cruce ya procesado de las transacciones del adquirente en Simetrik; insumo principal del agente. |
| **Fuente** | Origen de datos conectado (ej. archivo de Mastercard/Visa, procesador). |
| **Espacio de trabajo / Repositorio** | Contenedores estándar de la plataforma donde vive la configuración. |
| **Operation Center (OC)** | Módulo de tableros/operación donde (probablemente) vivirá el centro de disputas — veredicto pendiente del Plan 3. |
| ⚠️ **"Agente"** | Pendiente de validar: en notif-resumen el copy de cara al usuario evita "agente"/"Agente IA" (se usó "monitoreo"). Definir el término para disputas antes del handoff. |
