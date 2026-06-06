from pathlib import Path

PERSONA_PATH = Path("data/persona.md")

DEFAULT_PERSONA = """You are SelfClaw, a helpful Python learning agent.
You explain things clearly and keep answers concise.
"""


def load_persona():
    if not PERSONA_PATH.exists():
        return DEFAULT_PERSONA

    with PERSONA_PATH.open("r", encoding="utf-8") as file:
        return file.read()
    

def save_persona(text):
    PERSONA_PATH.parent.mkdir(parents=True, exist_ok=True)

    with PERSONA_PATH.open("w", encoding="utf-8") as file:
        file.write(text)


def reset_persona():
    save_persona(DEFAULT_PERSONA)