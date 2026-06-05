import json
from pathlib import Path

CONFIG_PATH = Path("selfclaw.json")

DEFAULT_CONFIG = {
    "provider": "mock",
    "model": "mock-model",
    "api_key": "",
    "base_url": "",
}

ALLOWED_CONFIG_KEYS = set(DEFAULT_CONFIG.keys())


def load_config():
    config = DEFAULT_CONFIG.copy()

    if not CONFIG_PATH.exists():
        return config

    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        user_config = json.load(file)

    config.update(user_config)
    return config


def save_config(config):
    with CONFIG_PATH.open("w", encoding="utf-8") as file:
        json.dump(config, file, indent=2, ensure_ascii=False)