import platform
import sys
import os
from pathlib import Path

OPERATING_SYSTEM = platform.system()

try:
    BASE_DIR = Path(getattr(sys, '_MEIPASS', os.path.abspath(".")))
except AttributeError:
    BASE_DIR = Path(__file__).resolve().parent.parent

IMAGES_DIR = BASE_DIR / "src" / "images"