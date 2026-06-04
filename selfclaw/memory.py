from datetime import datetime
from pathlib import Path

MEMORY_DIR = Path("data/memory")
MEMORY_PATH = MEMORY_DIR / "notes.md"


def add_memory(text):
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"- [{now}] {text}\n"

    with MEMORY_PATH.open("a", encoding="utf-8") as file:
        file.write(line)


def load_memories():
    if not MEMORY_PATH.exists():
        return []

    with MEMORY_PATH.open("r", encoding="utf-8") as file:
        return file.readlines()


def search_memory(query):
    memories = load_memories()
    results = []

    for memory in memories:
        if query in memory:
            results.append(memory.strip())

    return results