import platform
import sys
import os
from pathlib import Path

OPERATING_SYSTEM = platform.system()

try:
    BASE_DIR = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent.parent))
except AttributeError:
    BASE_DIR = Path(__file__).resolve().parent.parent

IMAGES_DIR = BASE_DIR / "images"
FONT_DIR = BASE_DIR / "fonts"

