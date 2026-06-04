import json
from pathlib import Path

SESSION_DIR = Path("data/sessions")


def get_session_path(session_id):
    return SESSION_DIR / f"{session_id}.json"


def load_session(session_id):
    path = get_session_path(session_id)

    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_session(session_id, messages):
    SESSION_DIR.mkdir(parents=True, exist_ok=True)

    path = get_session_path(session_id)

    with path.open("w", encoding="utf-8") as file:
        json.dump(messages, file, indent=2)