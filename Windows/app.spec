# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from pathlib import Path

# Get the path to the virtual environment's site-packages
if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    # We're in a virtual environment
    site_packages = Path(sys.executable).parent.parent / 'Lib' / 'site-packages'
else:
    # We're using the system Python
    site_packages = Path(sys.executable).parent / 'Lib' / 'site-packages'

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Include Streamlit's static files (Windows paths)
        (str(site_packages / 'streamlit' / 'static'), 'streamlit/static'),
        (str(site_packages / 'streamlit' / 'runtime'), 'streamlit/runtime'),
        # Include altair for Streamlit charts
        (str(site_packages / 'altair'), 'altair'),
        # Include any other necessary data files
        (str(site_packages / 'streamlit' / 'components'), 'streamlit/components'),
    ],
    hiddenimports=[
        'streamlit',
        'streamlit.web.cli',
        'streamlit.web.bootstrap',
        'streamlit.runtime.scriptrunner.magic_funcs',
        'streamlit.runtime.caching',
        'streamlit.runtime.caching.cache_data_api',
        'streamlit.runtime.caching.cache_resource_api',
        'streamlit.runtime.caching.storage',
        'streamlit.runtime.caching.storage.dummy_cache_storage',
        'streamlit.runtime.caching.storage.in_memory_cache_storage',
        'streamlit.runtime.uploaded_file_manager',
        'streamlit.components.v1',
        'streamlit.components.v1.components',
        'streamlit.logger',
        'streamlit.config',
        'requests',
        'PIL',
        'PIL.Image',
        'io',
        'time',
        'altair',
        'altair.vegalite',
        'altair.vegalite.v4',
        'altair.vegalite.v4.schema',
        'validators',
        'watchdog',
        'watchdog.observers',
        'watchdog.events',
        'tornado',
        'tornado.web',
        'tornado.websocket',
        'tornado.httpserver',
        'tornado.ioloop',
        'click',
        'toml',
        'typing_extensions',
        'pympler',
        'pympler.tracker',
        'blinker',
        'cachetools',
        'gitpython',
        'protobuf',
        'pyarrow',
        'pandas',
        'numpy',
        'certifi',
        'urllib3',
        'idna',
        'charset_normalizer',
        'packaging',
        'tenacity',
        'jsonschema',
        'rich',
        'pydeck',
        'tzlocal',
        'python_dateutil',
        'pytz',
        'six',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AI_Image_Generator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None  # Optional: add an icon file (use .ico format for Windows)
)