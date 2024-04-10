# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['NormaScraper.py'],
    pathex=[],
    binaries=[],
    datas=[('atti_scaricati', 'atti_scaricati'), ('resources', 'resources'), ('usr', 'usr'), ('usr/cron', 'usr'), ('README.txt', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='NormaScraper-Betav0.3',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['resources/icon.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='NormaScraper-Betav0.3',
)
app = BUNDLE(
    coll,
    name='NormaScraper-Betav0.3.app',
    icon='resources/icon.icns',
    bundle_identifier=None,
)
