from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="AINR_")

    app_name: str = "AI Noise Reducer Agent"
    environment: str = "dev"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    postgres_dsn: str = Field(default="postgresql://postgres:postgres@localhost:5432/ainr")
    qdrant_url: str = Field(default="http://localhost:6333")
    qdrant_collection: str = Field(default="knowledge_items")
    neo4j_uri: str = Field(default="bolt://localhost:7687")
    neo4j_user: str = Field(default="neo4j")
    neo4j_password: str = Field(default="password")

    request_timeout_seconds: float = 12.0
    max_article_words: int = 15000


settings = Settings()
