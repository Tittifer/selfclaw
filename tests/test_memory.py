from selfclaw import memory


def use_temp_memory(monkeypatch, tmp_path):
    memory_dir = tmp_path / "memory"
    memory_path = memory_dir / "notes.md"

    monkeypatch.setattr(memory, "MEMORY_DIR", memory_dir)
    monkeypatch.setattr(memory, "MEMORY_PATH", memory_path)


def test_add_and_load_memory(monkeypatch, tmp_path):
    use_temp_memory(monkeypatch, tmp_path)

    added = memory.add_memory("我喜欢 Python")

    assert added is True

    memories = memory.load_memories()

    assert len(memories) == 1
    assert "我喜欢 Python" in memories[0]


def test_add_memory_skips_duplicate(monkeypatch, tmp_path):
    use_temp_memory(monkeypatch, tmp_path)

    first = memory.add_memory("我喜欢 Python")
    second = memory.add_memory("我喜欢 Python")

    assert first is True
    assert second is False

    memories = memory.load_memories()

    assert len(memories) == 1


def test_search_memory(monkeypatch, tmp_path):
    use_temp_memory(monkeypatch, tmp_path)

    memory.add_memory("我喜欢 Python")
    memory.add_memory("我喜欢 JavaScript")

    results = memory.search_memory("Python")

    assert len(results) == 1
    assert "Python" in results[0]


def test_search_memory_limit(monkeypatch, tmp_path):
    use_temp_memory(monkeypatch, tmp_path)

    memory.add_memory("Python memory 1")
    memory.add_memory("Python memory 2")
    memory.add_memory("Python memory 3")

    results = memory.search_memory("Python", limit=2)

    assert len(results) == 2


def test_clear_memories(monkeypatch, tmp_path):
    use_temp_memory(monkeypatch, tmp_path)

    memory.add_memory("我喜欢 Python")
    memory.clear_memories()

    assert memory.load_memories() == []