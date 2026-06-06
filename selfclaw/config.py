import json
import os
from pathlib import Path

CONFIG_PATH = Path("selfclaw.json")

DEFAULT_CONFIG = {
    "provider": "mock",
    "model": "mock-model",
    "api_key": "",
    "base_url": "",
    "memory_limit": 5,
}

ENV_CONFIG_KEYS = {
    "provider": "SELFCLAW_PROVIDER",
    "model": "SELFCLAW_MODEL",
    "api_key": "SELFCLAW_API_KEY",
    "base_url": "SELFCLAW_BASE_URL",
    "memory_limit": "SELFCLAW_MEMORY_LIMIT",
}

ALLOWED_CONFIG_KEYS = set(DEFAULT_CONFIG.keys())

CONFIG_VALUE_TYPES = {
    "memory_limit": int,
}


def parse_config_value(key, value):
    value_type = CONFIG_VALUE_TYPES.get(key)

    if value_type is None:
        return value

    try:
        return value_type(value)
    except ValueError as error:
        raise ValueError(f"{key} must be {value_type.__name__}") from error


def load_config():
    load_env_file()

    config = DEFAULT_CONFIG.copy()

    if CONFIG_PATH.exists():
        with CONFIG_PATH.open("r", encoding="utf-8") as file:
            user_config = json.load(file)

        config.update(user_config)

    for config_key, env_key in ENV_CONFIG_KEYS.items():
        env_value = os.environ.get(env_key)

        if env_value:
            config[config_key] = parse_config_value(config_key, env_value)

    return config


def save_config(config):
    with CONFIG_PATH.open("w", encoding="utf-8") as file:
        json.dump(config, file, indent=2, ensure_ascii=False)
    

def load_env_file():
    env_path = Path(".env")

    if not env_path.exists():
        return

    with env_path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                continue

            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())