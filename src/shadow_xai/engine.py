"""Core conversation interfaces for Shadow-Xai."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ChatResponse:
    """A model response returned by the conversation engine."""

    text: str
    provider: str = "placeholder"


class ChatEngine:
    """Minimal engine boundary for future model-provider adapters."""

    def __init__(self, provider: str = "placeholder") -> None:
        self.provider = provider

    def respond(self, message: str) -> ChatResponse:
        """Return a deterministic response until a model adapter is configured."""
        cleaned = message.strip()
        if not cleaned:
            raise ValueError("message must not be empty")
        return ChatResponse(
            text=(
                "Shadow-Xai masih dalam tahap fondasi. "
                f"Pesan diterima: {cleaned}"
            ),
            provider=self.provider,
        )
