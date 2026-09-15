"""Environment-backed configuration with safe defaults."""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    model_provider: str = "echo"
    model_name: str = "shadow-local"
    model_base_url: str = ""
    model_api_key: str = ""
    model_timeout: float = 30.0
    memory_path: str = "shadow_xai.db"
    system_prompt: str = "Anda adalah Shadow-Xai, asisten yang jujur, aman, dan ringkas."
    personality: str = "helpful"
    max_agent_steps: int = 5

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            model_provider=os.getenv("SHADOW_MODEL_PROVIDER", "echo"),
            model_name=os.getenv("SHADOW_MODEL_NAME", "shadow-local"),
            model_base_url=os.getenv("SHADOW_MODEL_BASE_URL", ""),
            model_api_key=os.getenv("SHADOW_MODEL_API_KEY", ""),
            model_timeout=float(os.getenv("SHADOW_MODEL_TIMEOUT", "30")),
            memory_path=os.getenv("SHADOW_MEMORY_PATH", "shadow_xai.db"),
            system_prompt=os.getenv("SHADOW_SYSTEM_PROMPT", cls.system_prompt),
            personality=os.getenv("SHADOW_PERSONALITY", "helpful"),
            max_agent_steps=int(os.getenv("SHADOW_MAX_AGENT_STEPS", "5")),
        )

    def public_dict(self) -> dict[str, object]:
        """Return configuration without secrets."""
        return {"provider": self.model_provider, "model": self.model_name, "personality": self.personality, "max_steps": self.max_agent_steps}
