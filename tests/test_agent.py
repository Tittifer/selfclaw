from selfclaw.agent import Agent
from selfclaw import session_store


class RecordingLLM:
    def __init__(self):
        self.messages = None

    def generate(self, messages):
        self.messages = messages
        return "mock reply"


def use_temp_sessions(monkeypatch, tmp_path):
    session_dir = tmp_path / "sessions"

    monkeypatch.setattr(session_store, "SESSION_DIR", session_dir)


def test_agent_chat_saves_messages(monkeypatch, tmp_path):
    use_temp_sessions(monkeypatch, tmp_path)

    llm = RecordingLLM()
    agent = Agent(llm, session_id="test")

    reply = agent.chat("hello")

    assert reply == "mock reply"

    saved = session_store.load_session("test")

    assert saved == [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "mock reply"},
    ]


def test_agent_uses_skill_before_llm(monkeypatch, tmp_path):
    use_temp_sessions(monkeypatch, tmp_path)

    llm = RecordingLLM()
    agent = Agent(llm, session_id="test")

    reply = agent.chat("time")

    assert reply.startswith("当前时间是 ")
    assert llm.messages is None


def test_agent_includes_persona_in_llm_messages(monkeypatch, tmp_path):
    use_temp_sessions(monkeypatch, tmp_path)

    llm = RecordingLLM()
    agent = Agent(llm, session_id="test")

    agent.chat("hello")

    assert llm.messages[0]["role"] == "system"
    assert "SelfClaw" in llm.messages[0]["content"]


def test_agent_includes_memory_in_llm_messages(monkeypatch, tmp_path):
    use_temp_sessions(monkeypatch, tmp_path)

    monkeypatch.setattr(
        "selfclaw.agent.search_memory",
        lambda query, limit=5: ["- [now] 我喜欢 Python"],
    )

    llm = RecordingLLM()
    agent = Agent(llm, session_id="test")

    agent.chat("Python")

    system_messages = [
        message["content"]
        for message in llm.messages
        if message["role"] == "system"
    ]

    assert any("Relevant memories" in message for message in system_messages)
    assert any("我喜欢 Python" in message for message in system_messages)