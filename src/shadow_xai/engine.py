"""Core conversation engine with provider, memory, security, and RAG hooks."""

from dataclasses import dataclass
import logging
from typing import TextIO

from .config import Settings
from .llm import LLMAdapter, LLMMessage, build_adapter
from .memory import MemoryStore
from .rag import KnowledgeBase
from .security import SecurityPolicy
from .observability import event


@dataclass(frozen=True)
class ChatMessage:
    role: str
    text: str


@dataclass(frozen=True)
class ChatResponse:
    text: str
    provider: str = "placeholder"


class ChatEngine:
    def __init__(self, provider: str = "placeholder", *, settings: Settings | None = None, memory: MemoryStore | None = None, adapter: LLMAdapter | None = None, user_id: str = "default") -> None:
        self.settings = settings or Settings()
        self.provider = provider
        self.user_id = user_id
        self.memory = memory
        adapter_provider = self.settings.model_provider if provider == "placeholder" else provider
        self.adapter = adapter or build_adapter(adapter_provider, base_url=self.settings.model_base_url, api_key=self.settings.model_api_key, model=self.settings.model_name, timeout=self.settings.model_timeout)
        self.security = SecurityPolicy()
        self.knowledge = KnowledgeBase()
        self._history: list[ChatMessage] = []
        self.logger = logging.getLogger("shadow_xai.engine")

    @property
    def history(self) -> tuple[ChatMessage, ...]:
        return tuple(self._history)

    def clear_history(self) -> None:
        self._history.clear()
        if self.memory:
            self.memory.delete_user(self.user_id)

    def add_knowledge(self, text: str, source: str = "inline") -> int:
        return self.knowledge.ingest(text, source)

    def respond(self, message: str) -> ChatResponse:
        cleaned = self.security.validate_input(message)
        self._history.append(ChatMessage("user", cleaned))
        if self.memory:
            self.memory.add(self.user_id, "user", cleaned)
        messages = [LLMMessage("system", self.settings.system_prompt)]
        messages += [LLMMessage(item.role, item.text) for item in self._history[-10:]]
        context = self.knowledge.context(cleaned)
        if context:
            messages.insert(1, LLMMessage("system", f"Knowledge context with sources:\n{context}"))
        text = self.security.validate_output(self.adapter.complete(messages))
        event(self.logger, "chat.response", provider=self.provider, input_chars=len(cleaned), output_chars=len(text))
        response = ChatResponse(text=text, provider=self.provider)
        self._history.append(ChatMessage("assistant", text))
        if self.memory:
            self.memory.add(self.user_id, "assistant", text)
        return response

    def run_interactive(self, input_stream: TextIO, output_stream: TextIO, prompt: str = "Anda> ") -> None:
        output_stream.write("Shadow-Xai interactive mode. Ketik /help untuk bantuan.\n")
        while True:
            output_stream.write(prompt); output_stream.flush(); line = input_stream.readline()
            if line == "": output_stream.write("\nSampai jumpa.\n"); return
            command = line.strip()
            if not command: continue
            if command in {"/exit", "/quit"}: output_stream.write("Sampai jumpa.\n"); return
            if command == "/help": output_stream.write("Perintah: /help, /clear, /exit\n"); continue
            if command == "/clear": self.clear_history(); output_stream.write("Riwayat percakapan dihapus.\n"); continue
            try: output_stream.write(f"Shadow-Xai> {self.respond(command).text}\n")
            except ValueError as error: output_stream.write(f"Error: {error}\n")
