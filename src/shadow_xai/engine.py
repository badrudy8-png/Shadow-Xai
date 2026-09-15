"""Core conversation interfaces for Shadow-Xai."""

from dataclasses import dataclass
from typing import TextIO


@dataclass(frozen=True)
class ChatMessage:
    """One message stored in the local conversation history."""

    role: str
    text: str


@dataclass(frozen=True)
class ChatResponse:
    """A response returned by the conversation engine."""

    text: str
    provider: str = "placeholder"


class ChatEngine:
    """Local conversation engine boundary for future model adapters.

    The default provider is deterministic and requires no network or API key.
    A future adapter can replace ``_generate`` while keeping the public API.
    """

    def __init__(self, provider: str = "placeholder") -> None:
        self.provider = provider
        self._history: list[ChatMessage] = []

    @property
    def history(self) -> tuple[ChatMessage, ...]:
        """Return an immutable snapshot of the current conversation history."""
        return tuple(self._history)

    def clear_history(self) -> None:
        """Remove all messages from the local conversation."""
        self._history.clear()

    def respond(self, message: str) -> ChatResponse:
        """Generate a response and append the exchange to local history."""
        cleaned = message.strip()
        if not cleaned:
            raise ValueError("message must not be empty")

        self._history.append(ChatMessage(role="user", text=cleaned))
        response = ChatResponse(text=self._generate(cleaned), provider=self.provider)
        self._history.append(ChatMessage(role="assistant", text=response.text))
        return response

    def _generate(self, message: str) -> str:
        """Generate a safe local response until a model adapter is configured."""
        return f"Shadow-Xai masih dalam tahap fondasi. Pesan diterima: {message}"

    def run_interactive(
        self,
        input_stream: TextIO,
        output_stream: TextIO,
        prompt: str = "Anda> ",
    ) -> None:
        """Run a simple stdin/stdout chat loop.

        Type ``/help`` for commands and ``/exit`` or press Ctrl-D to stop.
        """
        output_stream.write("Shadow-Xai interactive mode. Ketik /help untuk bantuan.\n")
        while True:
            output_stream.write(prompt)
            output_stream.flush()
            line = input_stream.readline()
            if line == "":
                output_stream.write("\nSampai jumpa.\n")
                return
            command = line.strip()
            if not command:
                continue
            if command in {"/exit", "/quit"}:
                output_stream.write("Sampai jumpa.\n")
                return
            if command == "/help":
                output_stream.write("Perintah: /help, /clear, /exit\n")
                continue
            if command == "/clear":
                self.clear_history()
                output_stream.write("Riwayat percakapan dihapus.\n")
                continue
            try:
                output_stream.write(f"Shadow-Xai> {self.respond(command).text}\n")
            except ValueError as error:
                output_stream.write(f"Error: {error}\n")
