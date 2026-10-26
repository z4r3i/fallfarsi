"""
Settings persistence.
"""
import json
import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".fal4mir"
CONFIG_FILE = CONFIG_DIR / "settings.json"

DEFAULT_CONFIG = {
    "window_x": 100,
    "window_y": 100,
    "language": "fa",
    "always_on_top": True,
    "dark_mode": False,
    "refresh_seconds": 3600,
    "favorites": [],
}


def _ensure_dir():
    CONFIG_DIR.mkdir(exist_ok=True)


def load():
    _ensure_dir()
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE) as f:
                return json.load(f)
        except Exception:
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()


def save(config: dict):
    _ensure_dir()
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
