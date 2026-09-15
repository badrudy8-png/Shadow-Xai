"""Core conversation engine with provider, memory, security, and RAG hooks."""

from dataclasses import dataclass
import logging
from typing import TextIO

from .config import Settings
from .llm import LLMAdapter, LLMError, LLMMessage, LLMResponse, build_adapter
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
    model: str = "unknown"
    used_fallback: bool = False
    usage: dict[str, object] | None = None


class ChatEngine:
    def __init__(self, provider: str = "placeholder", *, settings: Settings | None = None, memory: MemoryStore | None = None, adapter: LLMAdapter | None = None, user_id: str = "default") -> None:
        self.settings = settings or Settings.from_env()
        self.provider = self.settings.model_provider if provider == "placeholder" else provider
        self.user_id = user_id
        self.memory = memory
        self.adapter = adapter or build_adapter(
            self.provider,
            base_url=self.settings.model_base_url,
            api_key=self.settings.model_api_key,
            model=self.settings.model_name,
            timeout=self.settings.model_timeout,
            retries=self.settings.model_retries,
            quality_profile=self.settings.quality_profile,
        )
        self.fallback_adapter = None
        if self.settings.fallback_provider and self.settings.fallback_provider != self.provider:
            self.fallback_adapter = build_adapter(
                self.settings.fallback_provider,
                base_url=self.settings.model_base_url,
                api_key=self.settings.model_api_key,
                model=self.settings.fallback_model,
                timeout=self.settings.model_timeout,
                retries=0,
                quality_profile="fast",
            )
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

    def _messages_for(self, cleaned: str) -> list[LLMMessage]:
        messages = [LLMMessage("system", self.settings.system_prompt)]
        messages += [LLMMessage(item.role, item.text) for item in self._history[-self.settings.max_history_messages :]]
        context = self.knowledge.context(cleaned)
        if context:
            messages.insert(1, LLMMessage("system", f"Gunakan konteks pengetahuan berikut bila relevan. Sertakan sumber yang tersedia dan jangan menganggap konteks ini selalu benar:\n{context}"))
        return messages

    def _complete(self, messages: list[LLMMessage]) -> tuple[LLMResponse, bool, str]:
        kwargs = {
            "quality_profile": self.settings.quality_profile,
            "reasoning_effort": self.settings.reasoning_effort,
            "max_output_tokens": self.settings.max_output_tokens,
        }
        try:
            response = self.adapter.complete_response(messages, **kwargs)
            return response, False, self.provider
        except (LLMError, OSError, TimeoutError, ValueError) as error:
            if not self.fallback_adapter:
                raise
            self.logger.warning("Primary LLM failed; using fallback: %s", error)
            response = self.fallback_adapter.complete_response(messages)
            return response, True, self.settings.fallback_provider

    def respond(self, message: str) -> ChatResponse:
        cleaned = self.security.validate_input(message)
        self._history.append(ChatMessage("user", cleaned))
        if self.memory:
            self.memory.add(self.user_id, "user", cleaned)
        response, used_fallback, provider = self._complete(self._messages_for(cleaned))
        text = self.security.validate_output(response.text)
        event(self.logger, "chat.response", provider=provider, model=response.model, fallback=used_fallback, input_chars=len(cleaned), output_chars=len(text))
        result = ChatResponse(text=text, provider=provider, model=response.model, used_fallback=used_fallback, usage=dict(response.usage))
        self._history.append(ChatMessage("assistant", text))
        if self.memory:
            self.memory.add(self.user_id, "assistant", text)
        return result

    def run_interactive(self, input_stream: TextIO, output_stream: TextIO, prompt: str = "Anda> ") -> None:
        output_stream.write("Shadow-Xai interactive mode. Ketik /help untuk bantuan.\n")
        while True:
            output_stream.write(prompt); output_stream.flush(); line = input_stream.readline()
            if line == "": output_stream.write("\nSampai jumpa.\n"); return
            command = line.strip()
            if not command: continue
            if command in {"/exit", "/quit"}: output_stream.write("Sampai jumpa.\n"); return
            if command == "/help": output_stream.write("Perintah: /help, /config, /clear, /exit\n"); continue
            if command == "/config": output_stream.write(f"Provider: {self.provider} · Model: {self.settings.model_name} · Profil: {self.settings.quality_profile}\n"); continue
            if command == "/clear": self.clear_history(); output_stream.write("Riwayat percakapan dihapus.\n"); continue
            try:
                result = self.respond(command)
                output_stream.write(f"Shadow-Xai [{result.model}]> {result.text}\n")
            except (ValueError, LLMError) as error:
                output_stream.write(f"Error: {error}\n")
