# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_all

# Collect all Matplotlib dynamic backends, drivers, and font assets
datas, binaries, hiddenimports = collect_all('matplotlib')

project_root = os.path.abspath(os.path.join(SPECPATH, '..'))
src_dir = os.path.abspath(os.path.join(SPECPATH, '../src'))

hiddenimports += [
    'PIL._tkinter_finder',
    'matplotlib.backends.backend_pdf',
    'matplotlib.backends.backend_svg',
    'matplotlib.backends.backend_agg',
]

a = Analysis(
    ['../src/main.py'],
    pathex=[project_root, src_dir],
    binaries=[],
    datas=[('../src/images', 'src/images'), ('../src/fonts', 'src/fonts')],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='LLMScoreVisualizer',
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='LLMScoreVisualizer',
)
app = BUNDLE(
    exe,
    name='LLMScoreVisualizer.app',
    icon=None,
    bundle_identifier='com.sergiu.llmscorevisualizer',
)
