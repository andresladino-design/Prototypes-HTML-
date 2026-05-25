# Prototypes HTML — UX Team Simetrik

Repositorio de prototipos HTML del equipo de UX. Cada carpeta es un prototipo independiente con su propio `README.md` y changelog.

🔗 **Ver prototipos online:** https://andresladino-design.github.io/Prototypes-HTML-/

---

## Prototipos disponibles

| Prototipo | Descripción | Última actualización | Link |
|-----------|-------------|----------------------|------|
| [Monitor Anomaly Recon](./monitor-anomaly-recon/) | Monitor de anomalías de conciliación para Operation Center | 2026-05-25 | [Ver](https://andresladino-design.github.io/Prototypes-HTML-/monitor-anomaly-recon/) |
| [Config System KPI](./config-system-kpi/) | Configuración de KPIs del sistema en Operation Center | 2026-05-25 | [Ver](https://andresladino-design.github.io/Prototypes-HTML-/config-system-kpi/) |

---

## Cómo agregar un nuevo prototipo

1. Crear carpeta en kebab-case: `nuevo-prototipo/`
2. Agregar `index.html` con el prototipo (Tailwind CDN + Alpine.js + Lucide Icons)
3. Crear `README.md` dentro de la carpeta usando el [template](#template-de-readme-por-prototipo)
4. Agregar entrada en la tabla de arriba
5. Agregar enlace en `index.html` raíz (landing page)
6. Commit + push

```bash
git add .
git commit -m "feat: agregar prototipo <nombre>"
git push
```

GitHub Pages se actualiza automático en ~1 min.

---

## Template de README por prototipo

```markdown
# <Nombre del prototipo>

Breve descripción de qué resuelve este prototipo y para qué audiencia.

**Última actualización:** YYYY-MM-DD
**Estado:** 🟢 Activo | 🟡 En revisión | 🔴 Deprecado

## Cómo verlo

- Online: https://andresladino-design.github.io/Prototypes-HTML-/<carpeta>/
- Local: abrir `index.html` en el navegador

## Stack

- Tailwind CSS (CDN)
- Alpine.js
- Lucide Icons
- desyk tokens (si aplica)

## Changelog

### YYYY-MM-DD
- Cambio 1
- Cambio 2
```

---

## Stack común

- **Tailwind CSS** vía CDN
- **Alpine.js** para interactividad
- **Lucide Icons** vía CDN
- **desyk tokens** (`tokens.css`) para fidelidad visual con Simetrik

## Convenciones

- Carpetas en `kebab-case`
- Cada prototipo es autocontenido (un `index.html` + assets propios)
- Sin build steps — todo abre directo en el navegador
- README actualizado con cada cambio significativo
