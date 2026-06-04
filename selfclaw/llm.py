from abc import ABC, abstractmethod


class LLMClient(ABC):
    @abstractmethod
    def generate(self, messages):
        pass


class MockLLMClient(LLMClient):
    def generate(self, messages):
        last_message = messages[-1]["content"]

        if messages and messages[0]["role"] == "system":
            memory = messages[0]["content"]
            return f"I found this memory:\n{memory}\n\nYou said: {last_message}"

        return f"You said: {last_message}"


def create_llm_client(config):
    provider = config["provider"]

    if provider == "mock":
        return MockLLMClient()

    raise ValueError(f"Unsupported provider: {provider}")