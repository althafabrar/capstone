# logic/config.py
import json
import os
from datetime import time

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "notif_enabled": True,
    "notif_method": "Email",
    "notif_priority": "Normal",
    "schedule_on": False,
    "schedule_type": "Harian",
    "schedule_time": "08:00",
    "fav_products": [],
    "theme_choice": "Dark Grey (Default)"
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)

    return data

def save_config(config: dict):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
