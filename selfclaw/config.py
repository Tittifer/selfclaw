import json
from pathlib import Path

CONFIG_PATH = Path("selfclaw.json")

DEFAULT_CONFIG = {
    "provider": "mock",
    "model": "mock-model",
    "api_key": "",
    "base_url": "",
}


def load_config():
    if not CONFIG_PATH.exists():
        return DEFAULT_CONFIG.copy()

    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_config(config):
    with CONFIG_PATH.open("w", encoding="utf-8") as file:
        json.dump(config, file, indent=2)