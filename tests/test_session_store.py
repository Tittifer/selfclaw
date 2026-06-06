from selfclaw import session_store


def use_temp_sessions(monkeypatch, tmp_path):
    session_dir = tmp_path / "sessions"

    monkeypatch.setattr(session_store, "SESSION_DIR", session_dir)


def test_load_missing_session_returns_empty_list(monkeypatch, tmp_path):
    use_temp_sessions(monkeypatch, tmp_path)

    messages = session_store.load_session("missing")

    assert messages == []


def test_save_and_load_session(monkeypatch, tmp_path):
    use_temp_sessions(monkeypatch, tmp_path)

    messages = [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "You said: hello"},
    ]

    session_store.save_session("test", messages)

    loaded = session_store.load_session("test")

    assert loaded == messages


def test_list_sessions(monkeypatch, tmp_path):
    use_temp_sessions(monkeypatch, tmp_path)

    session_store.save_session("study", [])
    session_store.save_session("work", [])

    sessions = session_store.list_sessions()

    assert sessions == ["study", "work"]


def test_clear_existing_session(monkeypatch, tmp_path):
    use_temp_sessions(monkeypatch, tmp_path)

    session_store.save_session("test", [])

    cleared = session_store.clear_session("test")

    assert cleared is True
    assert session_store.load_session("test") == []


def test_clear_missing_session(monkeypatch, tmp_path):
    use_temp_sessions(monkeypatch, tmp_path)

    cleared = session_store.clear_session("missing")

    assert cleared is False