# Resumen diario consolidado — Slack (Block Kit)

Spec del mensaje de Slack del resumen diario de anomalías. Es el equivalente del template de Email (`templates.html`), pero en formato nativo de Slack.

## Cómo probar el render

1. Abrir el **Block Kit Builder**: https://app.slack.com/block-kit-builder
2. Pegar el contenido de `slack-blockkit.json`.
3. Se ve el render real de Slack y se puede ajustar en vivo.

## Qué reemplazar antes de producción

- **`image_url`** de cada bloque `image`: hoy apunta a `https://REEMPLAZAR.simetrik.com/...`. Va el PNG del gráfico renderizado server-side (ver nota "Cómo se muestra el gráfico" en `templates.html`). En Slack la imagen se sirve por URL hospedada (firmada, con expiración), no por adjunto.
- **`url`** de los botones: deep links reales al tablero y a la configuración del resumen.
- Las **fechas, conteos, títulos y narrativas** son data dinámica que arma el backend por cada envío.

## Decisiones de contenido (según reunión 2026-06-22)

- Foco en **incidentes abiertos** (cada uno es un `section` + `image`).
- Los **resueltos** no llevan tarjeta: van como una **línea sutil** (`context`) al final ("1 incidente notificado ayer ya se resolvió").
- El resumen refleja el **estado actual** al momento del envío, no el de la notificación original.
- Disclaimer: "lo que sigue abierto del día anterior".
- Config a nivel de cuenta; un resumen por canal/receptor que recibió notificaciones (no se duplica al mismo canal).

## Mapa de bloques

| Bloque | Contenido |
|---|---|
| `header` | 📊 Resumen diario · fecha |
| `context` | Tablero + nº de incidentes abiertos |
| `divider` | — |
| `section` + `image` | Incidente abierto 1 (estado, fuente, narrativa, gráfico) |
| `section` + `image` | Incidente abierto 2 |
| `divider` | — |
| `context` | Línea sutil de resueltos |
| `actions` | Botones: Ver en Simetrik (primary) · Configurar resumen |
| `context` | Disclaimer |
