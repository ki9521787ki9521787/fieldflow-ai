from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "FieldFlow AI"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"
    SECRET_KEY: str = "replace-me-with-a-strong-secret-key"
    JWT_SECRET_KEY: str = "replace-me-with-a-strong-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    ALLOWED_HOSTS: str = "localhost,127.0.0.1"
    PASSWORD_PEPPER: str = "fieldflow-ai-pepper"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
