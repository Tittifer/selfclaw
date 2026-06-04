from selfclaw.session_store import load_session, save_session
from selfclaw.skills import run_skill
from selfclaw.memory import search_memory


class Agent:
    def __init__(self, llm, session_id="default"):
        self.llm = llm
        self.session_id = session_id
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
            memory_results = search_memory(user_text)
            llm_messages = self.messages.copy()

            if memory_results:
                memory_text = "\n".join(memory_results)
                llm_messages.insert(0, {
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