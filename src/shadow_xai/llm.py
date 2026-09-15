"""Provider-neutral LLM adapters with quality-aware OpenAI-compatible transport.

The adapter deliberately uses the standard library so the local-first package has
no mandatory runtime dependency. External providers are opt-in through environment
variables and must expose an OpenAI-compatible ``/chat/completions`` endpoint.
"""

from dataclasses import dataclass, field
import json
import subprocess
import time
from typing import Any, Iterator, Mapping
from urllib import error, request


@dataclass(frozen=True)
class LLMMessage:
    role: str
    content: str


@dataclass(frozen=True)
class LLMResponse:
    text: str
    model: str = "unknown"
    usage: Mapping[str, Any] = field(default_factory=dict)
    finish_reason: str | None = None
    raw: Mapping[str, Any] = field(default_factory=dict)


class LLMError(RuntimeError):
    """Raised when a provider cannot produce a valid response."""


class LLMAdapter:
    name = "base"

    def complete_response(self, messages: list[LLMMessage], **kwargs: object) -> LLMResponse:
        return LLMResponse(text=self.complete(messages, **kwargs), model=self.name)

    def complete(self, messages: list[LLMMessage], **kwargs: object) -> str:
        raise NotImplementedError

    def stream(self, messages: list[LLMMessage], **kwargs: object) -> Iterator[str]:
        yield self.complete(messages, **kwargs)


class EchoAdapter(LLMAdapter):
    """Deterministic offline adapter used for development and safe fallback."""

    name = "echo"

    def complete(self, messages: list[LLMMessage], **kwargs: object) -> str:
        user = next((m.content for m in reversed(messages) if m.role == "user"), "")
        return (
            "Saya menerima pesan Anda. Shadow-Xai sedang berjalan dalam mode lokal "
            "tanpa provider eksternal. Untuk jawaban berbasis model bahasa, setel "
            "SHADOW_MODEL_PROVIDER=openai-compatible dan konfigurasi endpoint-nya.\n\n"
            f"Pesan: {user}"
        )

    def stream(self, messages: list[LLMMessage], **kwargs: object) -> Iterator[str]:
        yield from self.complete(messages, **kwargs).split(" ")


class OpenAICompatibleAdapter(LLMAdapter):
    """Transport for OpenAI, compatible gateways, and self-hosted model servers."""

    name = "openai-compatible"

    def __init__(self, base_url: str, api_key: str, model: str, timeout: float = 60.0, retries: int = 2) -> None:
        if not base_url or not api_key:
            raise ValueError("base_url and api_key are required")
        if not model or model == "auto":
            raise ValueError("a concrete model is required for OpenAI-compatible adapter")
        self.base_url = base_url.rstrip("/")
        self.endpoint = self.base_url + "/chat/completions"
        self.api_key, self.model = api_key, model
        self.timeout, self.retries = timeout, max(0, retries)

    @staticmethod
    def resolve_model(model: str, quality_profile: str = "balanced") -> str:
        """Resolve a portable quality profile to a model ID."""
        if model and model != "auto":
            return model
        return {
            "fast": "gpt-5-mini",
            "balanced": "gpt-5",
            "quality": "gpt-5.5",
            "reasoning": "claude-opus-4-7",
        }.get(quality_profile, "gpt-5")

    @staticmethod
    def build_payload(
        messages: list[LLMMessage],
        *,
        model: str,
        quality_profile: str = "balanced",
        reasoning_effort: str = "medium",
        max_output_tokens: int = 1800,
        **kwargs: object,
    ) -> dict[str, Any]:
        selected = OpenAICompatibleAdapter.resolve_model(model, quality_profile)
        payload: dict[str, Any] = {
            "model": selected,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "stream": False,
        }
        if selected.startswith("gpt-"):
            payload["max_completion_tokens"] = max_output_tokens
            payload["reasoning"] = {"effort": reasoning_effort}
        elif selected.startswith("claude-"):
            budget = min(max(256, max_output_tokens // 2), 4096)
            payload["max_tokens"] = max(max_output_tokens, budget + 1)
            payload["thinking"] = {"type": "enabled", "budget_tokens": budget}
        elif selected.startswith("gemini-"):
            payload["max_tokens"] = max_output_tokens
            payload["thinking"] = {"budget_tokens": min(1024, max_output_tokens // 2)}
        else:
            payload["max_tokens"] = max_output_tokens
        payload.update(kwargs)
        return payload

    def _request(self, payload: dict[str, Any]) -> Mapping[str, Any]:
        body = json.dumps(payload).encode("utf-8")
        req = request.Request(
            self.endpoint,
            data=body,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
        )
        last_error: Exception | None = None
        for attempt in range(self.retries + 1):
            try:
                with request.urlopen(req, timeout=self.timeout) as response:
                    data = json.load(response)
                if not isinstance(data, dict):
                    raise LLMError("provider returned a non-object response")
                return data
            except (error.HTTPError, error.URLError, TimeoutError, json.JSONDecodeError, LLMError) as exc:
                last_error = exc
                if attempt >= self.retries:
                    break
                time.sleep(min(2 ** attempt, 8))
        raise LLMError(f"LLM request failed after {self.retries + 1} attempt(s): {last_error}") from last_error

    @staticmethod
    def _extract_text(data: Mapping[str, Any]) -> str:
        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMError("provider response has no choices[0].message.content") from exc
        if isinstance(content, str):
            return content.strip()
        if isinstance(content, list):
            return "\n".join(str(part.get("text", "")) for part in content if isinstance(part, dict)).strip()
        raise LLMError("provider returned unsupported message content")

    def complete_response(self, messages: list[LLMMessage], **kwargs: object) -> LLMResponse:
        data = self._request(self.build_payload(messages, model=self.model, **kwargs))
        choice = data.get("choices", [{}])[0]
        return LLMResponse(
            text=self._extract_text(data),
            model=str(data.get("model", self.model)),
            usage=data.get("usage", {}) if isinstance(data.get("usage", {}), dict) else {},
            finish_reason=choice.get("finish_reason") if isinstance(choice, dict) else None,
            raw=data,
        )

    def complete(self, messages: list[LLMMessage], **kwargs: object) -> str:
        return self.complete_response(messages, **kwargs).text


class LocalCommandAdapter(LLMAdapter):
    name = "local-command"

    def __init__(self, command: str, timeout: float = 60.0) -> None:
        if not command:
            raise ValueError("command is required")
        self.command, self.timeout = command, timeout

    def complete(self, messages: list[LLMMessage], **kwargs: object) -> str:
        prompt = "\n".join(f"{m.role}: {m.content}" for m in messages)
        result = subprocess.run(self.command, input=prompt, text=True, shell=True, capture_output=True, timeout=self.timeout, check=True)
        return result.stdout.strip()


def build_adapter(
    provider: str,
    *,
    base_url: str = "",
    api_key: str = "",
    model: str = "",
    timeout: float = 60.0,
    retries: int = 2,
    quality_profile: str = "balanced",
    command: str = "",
) -> LLMAdapter:
    normalized = provider.lower().replace("_", "-")
    if normalized in {"openai", "openai-compatible", "compatible", "anthropic", "gemini", "custom"}:
        concrete_model = OpenAICompatibleAdapter.resolve_model(model, quality_profile)
        return OpenAICompatibleAdapter(base_url, api_key, concrete_model, timeout, retries)
    if normalized == "local-command":
        return LocalCommandAdapter(command or base_url or model, timeout)
    return EchoAdapter()
