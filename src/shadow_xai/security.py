"""Security primitives for prompt and tool boundaries."""

import re


class SecurityPolicy:
    def __init__(self, max_input_chars: int = 12000, max_output_chars: int = 24000) -> None:
        self.max_input_chars, self.max_output_chars = max_input_chars, max_output_chars
        self.audit: list[dict[str, str]] = []

    def validate_input(self, text: str) -> str:
        value = text.strip()
        if not value:
            raise ValueError("message must not be empty")
        if len(value) > self.max_input_chars:
            raise ValueError("input is empty or exceeds the configured limit")
        self.audit.append({"event": "input_validated", "length": str(len(value))})
        return value

    def validate_output(self, text: str) -> str:
        if len(text) > self.max_output_chars:
            raise ValueError("output exceeds the configured limit")
        return text

    @staticmethod
    def redact_secrets(text: str) -> str:
        patterns = [r"(?i)(api[_-]?key|token|password)\s*[:=]\s*[^\s,;]+"]
        for pattern in patterns:
            text = re.sub(pattern, lambda m: m.group(1) + "=[REDACTED]", text)
        return text
