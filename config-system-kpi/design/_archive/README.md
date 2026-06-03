# Archivo — diseño previo (modelo Health Banner / landing / sidebar)

> ⚠️ **Estos documentos están OBSOLETOS.** Describen una versión anterior del prototipo de monitoreo de tableros que fue **reemplazada por completo**. Se conservan solo como referencia histórica de las decisiones de esa fase.

## Qué describen (y ya no existe en el prototipo)

Estos 6 docs corresponden a un pase de diseño anterior (`craft` sobre `index 2.html`) que apostaba por:

- Un **Health Banner** del tablero (`.tb-health-*`) con pipeline horizontal Ingesta → Calidad → Conciliación → KPIs.
- Una **landing dedicada** "Estado del monitoreo" (`anomaliesNav === 'monitoring.landing'`).
- Un **sidebar de monitoreo** con secciones Operación (Estado / Incidentes / Historial) y Configuración (KPIs / Dependencias / Notificaciones / Overrides).
- Un **wizard de 5 pasos** (Activar KPIs → Dependencias/lineage → Tipos de alerta → Notificaciones → Disclaimer de madurez).
- Un **pipeline visual** reutilizable (`.tm-pipeline-*`).

Nada de eso está en el `index.html` actual (`anomaliesNav`, `monitoring.landing`, `tb-health`, `tm-pipeline`, el sidebar de monitoreo y el wizard de 5 pasos no existen).

## Qué reemplazó a este modelo

El prototipo actual modela el monitoreo como un **modo del tablero** (`currentView: 'dashboard' | 'tablero-monitoreo'`) con una **barra de tabs** por etapa (Ingesta · Calidad · Conciliación · Métricas) y un modal de configuración Low/Family/High.

- La documentación de diseño **vigente** vive en `design/` (un nivel arriba de esta carpeta).
- La especificación **implementable** vive en `../../handoff/`.

## Qué se rescató

El **glosario** de `04-copy-recomendaciones.md` (sección 1) sigue siendo válido y ya está consolidado en `../../handoff/00-CONTEXT.md` (fuente canónica). El resto del copy de ese doc (banner por estados, pipeline, wizard, overrides) refiere a componentes que no existen.
