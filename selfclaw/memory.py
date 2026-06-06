from datetime import datetime
from pathlib import Path

MEMORY_DIR = Path("data/memory")
MEMORY_PATH = MEMORY_DIR / "notes.md"


def add_memory(text):
    if memory_exists(text):
        return False

    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"- [{now}] {text}\n"

    with MEMORY_PATH.open("a", encoding="utf-8") as file:
        file.write(line)

    return True


def load_memories():
    if not MEMORY_PATH.exists():
        return []

    with MEMORY_PATH.open("r", encoding="utf-8") as file:
        return file.readlines()


def search_memory(query, limit=5):
    memories = load_memories()
    results = []

    for memory in memories:
        if query in memory:
            results.append(memory.strip())

    return results[:limit]


def memory_exists(text):
    memories = load_memories()

    for memory in memories:
        if memory.endswith(f"{text}\n") or memory.endswith(text):
            return True

    return False


def clear_memories():
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    with MEMORY_PATH.open("w", encoding="utf-8") as file:
        file.write("")