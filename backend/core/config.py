from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path

# Resolve .env at project root (two levels up from this file)
_ENV_PATH = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_ENV_PATH),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── API keys ──────────────────────────────────────────────────────────────
    anthropic_api_key: str
    tavily_api_key: str
    exa_api_key: str = ""  # optional — system degrades gracefully if absent

    # ── Backend ───────────────────────────────────────────────────────────────
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    backend_reload: bool = True
    allowed_origins: str = "http://localhost:3000"

    # ── Research config ───────────────────────────────────────────────────────
    tavily_results_per_query: int = 6
    exa_results_per_query: int = 5
    concurrent_claude_calls: int = 3
    claude_max_tokens: int = 3000

    @property
    def origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]

    @property
    def exa_enabled(self) -> bool:
        return bool(self.exa_api_key)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
