from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central place every API key and tunable lives. Nothing here is hardcoded —
    values come from environment variables (.env locally, host dashboard in prod).
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    gemini_api_key: str = ""
    qdrant_url: str = ""
    qdrant_api_key: str = ""
    sarvam_api_key: str = ""
    openweather_api_key: str = ""
    agmarknet_api_key: str = ""

    # Tunables — safe defaults, override via env if needed
    retrieval_top_k: int = 4
    retrieval_min_score: float = 0.55
    live_api_timeout_seconds: float = 3.0
    rate_limit_per_minute: str = "20/minute"


settings = Settings()
