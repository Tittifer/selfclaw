from selfclaw.session_store import load_session, save_session
from selfclaw.skills import run_skill
from selfclaw.memory import search_memory
from selfclaw.persona import load_persona


class Agent:
    def __init__(self, llm, session_id="default", memory_limit=5):
        self.llm = llm
        self.session_id = session_id
        self.memory_limit = memory_limit
        self.messages = load_session(session_id)

    def chat(self, user_text):
        self.messages.append({
            "role": "user",
            "content": user_text,
        })

        skill_reply = run_skill(user_text)

        if skill_reply is not None:
            reply = skill_reply
        else:
            memory_results = search_memory(user_text, limit=self.memory_limit)
            llm_messages = [
                {
                    "role": "system",
                    "content": load_persona(),
                },
            ]

            llm_messages.extend(self.messages)

            if memory_results:
                memory_text = "\n".join(memory_results)
                llm_messages.insert(1, {
                    "role": "system",
                    "content": f"Relevant memories:\n{memory_text}",
                })

            reply = self.llm.generate(llm_messages)

        self.messages.append({
            "role": "assistant",
            "content": reply,
        })

        save_session(self.session_id, self.messages)

        return reply