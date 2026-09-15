"""Environment-backed configuration with safe, production-friendly defaults."""

from dataclasses import dataclass
import os


DEFAULT_SYSTEM_PROMPT = """Anda adalah Shadow-Xai, asisten AI profesional yang natural, jernih, dan dapat dipercaya.

Prinsip respons:
1. Pahami maksud pengguna sebelum menjawab; jika ambigu, tanyakan klarifikasi yang ringkas.
2. Jawab langsung terlebih dahulu, lalu berikan konteks, langkah, atau contoh yang relevan.
3. Gunakan bahasa pengguna. Bahasa Indonesia harus terdengar alami, profesional, dan tidak kaku.
4. Jangan mengarang fakta, sumber, hasil eksekusi, atau tindakan eksternal. Nyatakan batas pengetahuan dan ketidakpastian.
5. Untuk tugas teknis, gunakan struktur yang mudah dipindai: ringkasan, asumsi, langkah implementasi, contoh kode, dan verifikasi.
6. Untuk perbandingan atau keputusan, tampilkan kriteria, trade-off, rekomendasi, dan risiko.
7. Jangan menampilkan proses berpikir internal atau chain-of-thought. Berikan ringkasan alasan yang dapat diverifikasi.
8. Hormati privasi dan keamanan. Tolak atau arahkan ulang permintaan berbahaya dengan penjelasan singkat dan alternatif aman.
9. Hindari pembuka generik, pengulangan pertanyaan, jargon berlebihan, dan klaim kepastian yang tidak didukung.
"""


@dataclass(frozen=True)
class Settings:
    model_provider: str = "echo"
    model_name: str = "auto"
    model_base_url: str = ""
    model_api_key: str = ""
    model_timeout: float = 60.0
    model_retries: int = 2
    quality_profile: str = "balanced"
    reasoning_effort: str = "medium"
    max_output_tokens: int = 1800
    max_history_messages: int = 16
    fallback_provider: str = "echo"
    fallback_model: str = "shadow-local"
    memory_path: str = "shadow_xai.db"
    system_prompt: str = DEFAULT_SYSTEM_PROMPT
    personality: str = "professional-natural"
    max_agent_steps: int = 5

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            model_provider=os.getenv("SHADOW_MODEL_PROVIDER", "echo"),
            model_name=os.getenv("SHADOW_MODEL_NAME", "auto"),
            model_base_url=os.getenv("SHADOW_MODEL_BASE_URL", ""),
            model_api_key=os.getenv("SHADOW_MODEL_API_KEY", ""),
            model_timeout=float(os.getenv("SHADOW_MODEL_TIMEOUT", "60")),
            model_retries=max(0, int(os.getenv("SHADOW_MODEL_RETRIES", "2"))),
            quality_profile=os.getenv("SHADOW_QUALITY_PROFILE", "balanced"),
            reasoning_effort=os.getenv("SHADOW_REASONING_EFFORT", "medium"),
            max_output_tokens=max(128, int(os.getenv("SHADOW_MAX_OUTPUT_TOKENS", "1800"))),
            max_history_messages=max(2, int(os.getenv("SHADOW_MAX_HISTORY_MESSAGES", "16"))),
            fallback_provider=os.getenv("SHADOW_FALLBACK_PROVIDER", "echo"),
            fallback_model=os.getenv("SHADOW_FALLBACK_MODEL", "shadow-local"),
            memory_path=os.getenv("SHADOW_MEMORY_PATH", "shadow_xai.db"),
            system_prompt=os.getenv("SHADOW_SYSTEM_PROMPT", DEFAULT_SYSTEM_PROMPT),
            personality=os.getenv("SHADOW_PERSONALITY", "professional-natural"),
            max_agent_steps=int(os.getenv("SHADOW_MAX_AGENT_STEPS", "5")),
        )

    def public_dict(self) -> dict[str, object]:
        """Return configuration without secrets or prompt contents."""
        return {
            "provider": self.model_provider,
            "model": self.model_name,
            "quality_profile": self.quality_profile,
            "reasoning_effort": self.reasoning_effort,
            "max_output_tokens": self.max_output_tokens,
            "max_history_messages": self.max_history_messages,
            "fallback_provider": self.fallback_provider,
            "personality": self.personality,
            "max_steps": self.max_agent_steps,
        }
