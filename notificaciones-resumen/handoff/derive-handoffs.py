#!/usr/bin/env python3
"""Deriva los 3 HTML de handoff desde index.html por rangos de líneas verificados.

Cada variante = keep-list de rangos (1-indexed, inclusivos) + reemplazos exactos.
Aborta si una aserción de frontera o un reemplazo no calza (protege contra drift
de index.html).
"""
import sys, pathlib

SRC = pathlib.Path(__file__).resolve().parent.parent / 'index.html'
OUT = pathlib.Path(__file__).resolve().parent

lines = SRC.read_text(encoding='utf-8').splitlines(keepends=True)

def L(n):  # 1-indexed
    return lines[n-1]

# ---- Aserciones de frontera: si index.html cambió, fallar fuerte ----
ASSERTS = {
    1909: '<body',
    1912: '<!-- ============ PRIMARY SIDEBAR',
    1995: '<!-- ============ SECONDARY PANEL',
    2073: '<!-- ============ MAIN',
    2087: '<!-- Dashboard header -->',
    2116: '<!-- ============ VISTA TABLERO',
    2295: '<!-- ============ VISTA MONITOREO',
    2353: '<!-- ============ VISTA ANOMALÍAS',
    2367: '<div id="anLeftGestion"',
    2489: '</div>',
    2491: '<div id="anLeftConfig"',
    2534: '<div id="anLeftHistorial"',
    2543: '</aside>',
    2546: '<section id="anRightGestion"',
    2608: '</section>',
    2611: '<section id="anRightConfig"',
    2612: '<div id="anCfgIngesta"',
    2621: '</div>',
    2624: '<div id="anCfgNotif"',
    2831: '<section id="anRightHistorial"',
    2860: '</section>',
    2862: '</div>',
    2863: '</main>',
    2867: '<!-- ============ DIALOG: Detalle de fuente',
    3127: '<!-- ============ DIALOG: Monitoreo inteligente',
    3884: '<script>',
    3885: '// ---- Pending dashboards',
    4010: '// ---- View toggle',
    4020: '// ---- Tabs superiores',
    4031: '// Selección de una incidencia',
    4038: '// Sub-tabs de Anomalías',
    4051: '// Tabla de Historial',
    4080: '// ---- Filtros de la vista de incidentes',
    4087: 'function esc(s)',
    4166: '// ---- Filtros guardados',
    4198: 'function goGestionFilter()',
    4202: '// ======== Paquetes de notificación',
    4546: 'function anConfNav',
    4555: '// Grilla de fuentes',
    4568: ']',
    4569: 'let anIngRendered',
    4575: '// ---- Detalle de fuente',
    4608: '// ---- Sub-tabs dentro del panel',
    4634: '// ¿Dónde? — enciende/apaga',
    4643: '// Agrega un chip',
    4664: '}',
    4665: '// ¿Cuándo notificar?',
    4754: '// ---- Monitor dialog',
    4822: '// ---- Gráfica "Vista previa',
    4876: '/* ===== Detección de anomalías por serie',
    5150: 'nsInit();',
    5152: 'lucide.createIcons();',
    5153: '</script>',
    5154: '</body>',
}
for n, frag in ASSERTS.items():
    if frag not in L(n):
        sys.exit(f'ASSERT FAIL línea {n}: esperaba {frag!r}, hay: {L(n)[:90]!r}')

BANNER_CSS = '''  <style>
    .hoff-badge{position:fixed;right:14px;bottom:14px;z-index:400;background:#1c1c22;color:#fff;border-radius:10px;padding:9px 14px;font:500 12px/1.45 Inter,system-ui,sans-serif;box-shadow:0 6px 24px rgba(10,10,20,.28);max-width:330px;}
    .hoff-badge b{display:block;font-weight:600;font-size:12.5px;}
    .hoff-badge span{display:block;color:#b9b9c4;margin-top:2px;font-weight:400;}
    .oos{opacity:.4;pointer-events:none;cursor:default;}
  </style>
</head>'''

def build(name, keep_ranges, replacements, title, banner_b, banner_span, header_comment):
    text = ''.join(''.join(L(i) for i in range(a, min(b, len(lines)) + 1)) for a, b in keep_ranges)
    # título + banner
    replacements = [
        ('<title>Simetrik · Centro de Operaciones · Tableros</title>', f'<title>{title}</title>'),
        ('</head>', BANNER_CSS),
        ('<!DOCTYPE html>', f'<!DOCTYPE html>\n<!-- {header_comment} -->'),
    ] + replacements
    for old, new in replacements:
        if text.count(old) != 1:
            sys.exit(f'{name}: reemplazo no único ({text.count(old)}x): {old[:80]!r}')
        text = text.replace(old, new)
    banner = f'  <div class="hoff-badge"><b>{banner_b}</b><span>{banner_span}</span></div>\n'
    # insertar banner justo después de la línea <body ...>
    idx = text.index('<body')
    eol = text.index('\n', idx) + 1
    text = text[:eol] + banner + text[eol:]
    (OUT / name).write_text(text, encoding='utf-8')
    print(f'{name}: {len(text.splitlines())} líneas')

TAB_TABLEROS = '''<div class="top-tab active" data-top="tableros" onclick="switchTop('tableros',this)"><i data-lucide="layout-grid"></i> Tableros</div>'''
TAB_ANOM = '''<div class="top-tab" data-top="anomalias" onclick="switchTop('anomalias',this)"><i data-lucide="circle-dot"></i> Anomalías</div>'''
TAB_PEND = '''<div class="top-tab" data-top="pendientes" onclick="switchTop('pendientes',this)"><i data-lucide="circle-dashed"></i> Pendientes</div>'''
TAB_ALM = '''<div class="top-tab" data-top="almacenamiento" onclick="switchTop('almacenamiento',this)"><i data-lucide="archive"></i> Almacenamiento</div>'''
TAB_ASI = '''<div class="top-tab" data-top="asientos" onclick="switchTop('asientos',this)"><i data-lucide="book-open"></i> Asientos contables</div>'''

# tabs estáticos comunes (sin switchTop): activo en Anomalías (H1/H3) o Tableros (H2)
def tabs_static(active):
    reps = []
    reps.append((TAB_TABLEROS, '<div class="top-tab%s" data-top="tableros"><i data-lucide="layout-grid"></i> Tableros</div>'
                 % (' active' if active == 'tableros' else ' oos" title="Fuera de alcance de esta épica')))
    reps.append((TAB_ANOM, '<div class="top-tab%s" data-top="anomalias"><i data-lucide="circle-dot"></i> Anomalías</div>'
                 % (' active' if active == 'anomalias' else ' oos" title="Fuera de alcance de esta épica')))
    for tab, key, icon, label in ((TAB_PEND, 'pendientes', 'circle-dashed', 'Pendientes'),
                                  (TAB_ALM, 'almacenamiento', 'archive', 'Almacenamiento'),
                                  (TAB_ASI, 'asientos', 'book-open', 'Asientos contables')):
        reps.append((tab, f'<div class="top-tab oos" data-top="{key}" title="Fuera de alcance de esta épica"><i data-lucide="{icon}"></i> {label}</div>'))
    return reps

SEG_GESTION = '''<button class="an-seg-tab active" data-sub="gestion" onclick="anSubtab('gestion',this)" title="Gestión">'''
SEG_HIST = '''<button class="an-seg-tab" data-sub="historial" onclick="anSubtab('historial',this)" title="Alertas">'''
SEG_CONFIG = '''<button class="an-seg-tab" data-sub="config" onclick="anSubtab('config',this)" title="Configuración">'''
VIEW_ANOM_HIDDEN = '<div id="viewAnomalias" class="flex-1 flex min-h-0 hidden">'

# ============ HANDOFF 1 ============
build(
    'handoff-1-filtros-incidentes.html',
    keep_ranges=[
        (1, 1993),            # head + styles + sidebar
        (2073, 2085),         # main + top bar
        (2353, 2489),         # vista Anomalías: aside con Gestión (lista + filtros)
        (2543, 2608),         # cierre aside + detalle Gestión
        (2862, 2864),         # cierres viewAnomalias/main/flex
        (3884, 3884),         # <script>
        (4031, 4037),         # anSelect
        (4080, 4197),         # filtros + guardados (sin goGestionFilter)
        (4199, 4200),         # init preview + listener global
        (4555, 4568),         # AN_SOURCES (lista de recursos del menú Filtrar)
        (5152, 5157),         # lucide + cierres
    ],
    replacements=tabs_static('anomalias') + [
        (VIEW_ANOM_HIDDEN, '<div id="viewAnomalias" class="flex-1 flex min-h-0">'),
        (SEG_GESTION, '<button class="an-seg-tab active" data-sub="gestion" title="Gestión">'),
        (SEG_HIST, '<button class="an-seg-tab oos" data-sub="historial" title="Alertas · fuera de alcance (handoff 3)">'),
        (SEG_CONFIG, '<button class="an-seg-tab oos" data-sub="config" title="Configuración · fuera de alcance (handoff 3)">'),
    ],
    title='Handoff 1 · Filtros en la vista de incidentes',
    banner_b='Handoff 1 · Filtros en la vista de incidentes',
    banner_span='Prototipo acotado a esta épica. Lo atenuado no hace parte de la entrega.',
    header_comment='Derivado de ../index.html — alcance: handoff-1-filtros-incidentes.md. No editar a mano: los cambios de producto van en index.html y se re-derivan.',
)

# ============ HANDOFF 2 ============
build(
    'handoff-2-config-anomalias-tableros.html',
    keep_ranges=[
        (1, 2351),            # head + sidebar + panel tableros + topbar + header + vista Tablero + vista Monitoreo
        (2863, 2864),         # cierres main/flex
        (2866, 3882),         # dialogs: fuente + monitoreo inteligente
        (3884, 4019),         # <script> + pendientes + charts + monitor cards + view toggle
        (4087, 4087),         # esc()
        (4555, 4568),         # AN_SOURCES
        (4575, 4606),         # detalle de fuente
        (4608, 4752),         # sub-tabs + renderSourceGrid + canales + cuándo notificar
        (4754, 5157),         # monitor dialog + gráfica preview + detección por serie + init
    ],
    replacements=tabs_static('tableros'),
    title='Handoff 2 · Configuración de detección de anomalías',
    banner_b='Handoff 2 · Configuración de detección de anomalías',
    banner_span='Prototipo acotado a esta épica. Lo atenuado no hace parte de la entrega.',
    header_comment='Derivado de ../index.html — alcance: handoff-2-config-anomalias-tableros.md. No editar a mano: los cambios de producto van en index.html y se re-derivan.',
)

# ============ HANDOFF 3 ============
build(
    'handoff-3-notificaciones-y-vista-anomalias.html',
    keep_ranges=[
        (1, 1993),            # head + styles + sidebar
        (2073, 2085),         # main + top bar
        (2353, 2611),         # vista Anomalías completa hasta anRightConfig
        (2622, 2860),         # config (sin página Ingesta) + historial
        (2862, 2864),         # cierres
        (3884, 3884),         # <script>
        (4031, 4078),         # anSelect + anSubtab + renderHist
        (4080, 4200),         # filtros + guardados (los reutiliza el editor)
        (4202, 4568),         # paquetes de notificación + anConfNav + AN_SOURCES
        (4643, 4664),         # addChip (chips de correo/canal del editor)
        (5152, 5157),         # lucide + cierres
    ],
    replacements=tabs_static('anomalias') + [
        (VIEW_ANOM_HIDDEN, '<div id="viewAnomalias" class="flex-1 flex min-h-0">'),
        # entrar a Configuración aterriza en Notificaciones (la página Ingesta es del handoff 2)
        ("if (which === 'config') renderIngesta();", "if (which === 'config') renderPkgList();"),
        ("      if (cfg === 'ingesta') { renderIngesta(); closeSource(); }\n", ''),
        ('''<button class="an-confitem is-sel" onclick="anConfNav(this,'ingesta')">''',
         '<button class="an-confitem oos" title="Fuera de alcance (handoff 2)">'),
        ('''<button class="an-confitem" onclick="anConfNav(this,'notif')">''',
         '''<button class="an-confitem is-sel" onclick="anConfNav(this,'notif')">'''),
        ('<div id="anCfgNotif" class="an-ingesta hidden">', '<div id="anCfgNotif" class="an-ingesta">'),
    ],
    title='Handoff 3 · Notificaciones de incidentes y vista de Anomalías',
    banner_b='Handoff 3 · Notificaciones de incidentes y vista de Anomalías',
    banner_span='Prototipo acotado a esta épica. Lo atenuado no hace parte de la entrega; los filtros de Gestión se especifican en el handoff 1.',
    header_comment='Derivado de ../index.html — alcance: handoff-3-notificaciones-y-vista-anomalias.md. No editar a mano: los cambios de producto van en index.html y se re-derivan.',
)

print('OK')
