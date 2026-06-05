import json
import urllib.error
import urllib.request
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
    

class OpenAICompatibleClient(LLMClient):
    def __init__(self, model, api_key, base_url):
        if not model:
            raise ValueError("openai-compatible provider requires model")

        if not api_key:
            raise ValueError("openai-compatible provider requires api_key")

        if not base_url or base_url == "none":
            raise ValueError("openai-compatible provider requires base_url")

        self.model = model
        self.api_key = api_key
        self.base_url = base_url

    def generate(self, messages):
        endpoint = self.base_url.rstrip("/") + "/chat/completions"

        payload = {
            "model": self.model,
            "messages": messages,
        }

        data = json.dumps(payload).encode("utf-8")

        request = urllib.request.Request(
            endpoint,
            data=data,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
        )

        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                response_data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"LLM API error {error.code}: {body}") from error
        except urllib.error.URLError as error:
            raise RuntimeError(f"LLM network error: {error}") from error

        return response_data["choices"][0]["message"]["content"]


def create_llm_client(config):
    provider = config["provider"]

    if provider == "mock":
        return MockLLMClient()

    if provider == "openai-compatible":
        return OpenAICompatibleClient(
            model=config["model"],
            api_key=config["api_key"],
            base_url=config["base_url"],
        )

    raise ValueError(f"Unsupported provider: {provider}")