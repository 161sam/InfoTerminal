from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    os_url: str = Field("http://localhost:9200", alias="OS_URL")
    require_auth: bool = Field(False, alias="REQUIRE_AUTH")
    os_index: str = Field("docs", alias="OS_INDEX")

    rerank_enabled: bool = Field(False, alias="RERANK_ENABLED")
    rerank_topk: int = Field(50, alias="RERANK_TOPK")
    rerank_model: str = Field("sentence-transformers/all-MiniLM-L6-v2", alias="RERANK_MODEL")
    rerank_timeout_ms: int = Field(800, alias="RERANK_TIMEOUT_MS")
    rerank_cache_ttl_s: int = Field(1800, alias="RERANK_CACHE_TTL_S")

    class Config:
        env_file = ".env"
        case_sensitive = False
