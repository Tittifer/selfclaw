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
        json.dump(messages, file, indent=2, ensure_ascii=False)


def list_sessions():
    if not SESSION_DIR.exists():
        return []

    sessions = []

    for path in SESSION_DIR.glob("*.json"):
        sessions.append(path.stem)

    return sorted(sessions)


def clear_session(session_id):
    path = get_session_path(session_id)

    if path.exists():
        path.unlink()
        return True

    return False