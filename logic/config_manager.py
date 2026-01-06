import json
import os
from .config import DEFAULT_CONFIG

CONFIG_FILE = "config.json"


def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)

    # ====== FIX TYPE ======
    if not isinstance(data.get("schedule_time"), str):
        data["schedule_time"] = DEFAULT_CONFIG["schedule_time"]

    if not isinstance(data.get("fav_products"), list):
        data["fav_products"] = []

    return {**DEFAULT_CONFIG, **data}