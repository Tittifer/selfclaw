from selfclaw.agent import Agent


class SessionManager:
    def __init__(self, llm, memory_limit=5):
        self.llm = llm
        self.memory_limit = memory_limit
        self.agents = {}

    def get_agent(self, session_id):
        if session_id not in self.agents:
            self.agents[session_id] = Agent(
                self.llm,
                session_id=session_id,
                memory_limit=self.memory_limit,
            )

        return self.agents[session_id]

    def chat(self, session_id, user_text):
        agent = self.get_agent(session_id)
        return agent.chat(user_text)