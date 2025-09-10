# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Collect dynamic imports and data required by xhtml2pdf/reportlab
hiddenimports_extra = (
    collect_submodules('xhtml2pdf') +
    collect_submodules('reportlab') +
    collect_submodules('reportlab.graphics.barcode') +
    collect_submodules('PIL') + [
        # Explicitly include common barcode modules (loaded via exec at runtime)
        'reportlab.graphics.barcode.code128',
        'reportlab.graphics.barcode.code39',
        'reportlab.graphics.barcode.code93',
        'reportlab.graphics.barcode.usps',
        'reportlab.graphics.barcode.eanbc',
        'reportlab.graphics.barcode.qr',
        # Local PDF generator module if imported dynamically
        'Pdf.pdf',
    ]
)
datas_extra = (
    collect_data_files('reportlab') +  # fonts, encodings, etc.
    collect_data_files('xhtml2pdf') +  # templates/resources
    [
        ('assets/logoUNEG.png', 'assets'),  # <-- add logo image
        ('assets/CL.png', 'assets'),  # <-- add CL.png image
        ('assets/Circular-CL.png', 'assets'), 
        ('assets/Login.png, 'assets'), 
        ('Pdf/modulo_estadistico.html', 'Pdf'),  # <-- add HTML template
        ('Pdf/consultar_asistencia.html', 'Pdf'),
        ('Pdf/consultar_falla_equipo.html', 'Pdf'),
        ('Pdf/estilos.css', 'Pdf'),  # <-- add estilos.css
    ]
)

block_cipher = None

a = Analysis(
    ['d:\\App_control_de_asistencias\\main.py'],
    pathex=['d:\\App_control_de_asistencias'],
    binaries=[],
    datas=datas_extra,  # was []
    hiddenimports=[
        'libsql',
        'dotenv',
        'tkinter',
        'Views.ventana_main',
        'Views.ventana_login',
        'Views.gestion_de_usuarios',
    ] + hiddenimports_extra,  # add collected dynamic imports
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Onefile build: include binaries/zipfiles/datas directly in EXE and do not use COLLECT.
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='App_control_de_asistencias',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True
)
