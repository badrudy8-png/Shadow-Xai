"""Provider-neutral LLM adapters. External providers are optional."""

from dataclasses import dataclass
import json
import subprocess
from typing import Iterator
from urllib import request


@dataclass(frozen=True)
class LLMMessage:
    role: str
    content: str


class LLMAdapter:
    name = "base"

    def complete(self, messages: list[LLMMessage], **kwargs: object) -> str:
        raise NotImplementedError

    def stream(self, messages: list[LLMMessage], **kwargs: object) -> Iterator[str]:
        yield self.complete(messages, **kwargs)


class EchoAdapter(LLMAdapter):
    name = "echo"

    def complete(self, messages: list[LLMMessage], **kwargs: object) -> str:
        user = next((m.content for m in reversed(messages) if m.role == "user"), "")
        return f"Shadow-Xai masih dalam tahap fondasi. Pesan diterima: {user}"

    def stream(self, messages: list[LLMMessage], **kwargs: object) -> Iterator[str]:
        yield from self.complete(messages, **kwargs).split()


class OpenAICompatibleAdapter(LLMAdapter):
    name = "openai-compatible"

    def __init__(self, base_url: str, api_key: str, model: str, timeout: float = 30.0) -> None:
        if not base_url or not api_key:
            raise ValueError("base_url and api_key are required")
        self.endpoint = base_url.rstrip("/") + "/chat/completions"
        self.api_key, self.model, self.timeout = api_key, model, timeout

    def complete(self, messages: list[LLMMessage], **kwargs: object) -> str:
        payload = {"model": self.model, "messages": [m.__dict__ for m in messages], "stream": False, **kwargs}
        req = request.Request(self.endpoint, data=json.dumps(payload).encode(), headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"})
        with request.urlopen(req, timeout=self.timeout) as response:
            data = json.load(response)
        return str(data["choices"][0]["message"]["content"])


class LocalCommandAdapter(LLMAdapter):
    name = "local-command"

    def __init__(self, command: str, timeout: float = 60.0) -> None:
        self.command, self.timeout = command, timeout

    def complete(self, messages: list[LLMMessage], **kwargs: object) -> str:
        prompt = "\n".join(f"{m.role}: {m.content}" for m in messages)
        result = subprocess.run(self.command, input=prompt, text=True, shell=True, capture_output=True, timeout=self.timeout, check=True)
        return result.stdout.strip()


def build_adapter(provider: str, *, base_url: str = "", api_key: str = "", model: str = "", timeout: float = 30.0, command: str = "") -> LLMAdapter:
    if provider == "openai-compatible":
        return OpenAICompatibleAdapter(base_url, api_key, model, timeout)
    if provider == "local-command":
        return LocalCommandAdapter(command, timeout)
    return EchoAdapter()
