from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
ASSETS_DIR = ROOT_DIR / "assets"
MODELS_DIR = ROOT_DIR / "models"
MENU_PATH = DATA_DIR / "menu.json"
HAND_MODEL_PATH = MODELS_DIR / "hand_landmarker.task"
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
HOLD_DURATION = 1.0
IDLE_TIMEOUT = 45
