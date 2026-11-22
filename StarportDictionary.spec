# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['run_starport.py'],
    pathex=['src'],
    binaries=[],
    datas=[('knowledge-packs', 'knowledge-packs'), ('src/starport_dictionary/ui/resources', 'starport_dictionary/ui/resources')],
    hiddenimports=['PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PySide6.QtWebEngineCore', 'PySide6.Qt3DCore', 'PySide6.QtMultimedia', 'PySide6.QtQuick', 'tkinter', 'pytest'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='StarportDictionary',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
