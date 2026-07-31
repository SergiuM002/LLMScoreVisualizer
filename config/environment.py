import platform
import os

OPERATING_SYSTEM = platform.system()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SESSIONS_DIR = os.path.join(os.path.join(BASE_DIR, "data"), "sessions.json")
LASTLOGIN_DIR = os.path.join(os.path.join(BASE_DIR, "data"), "lastlogin.json")