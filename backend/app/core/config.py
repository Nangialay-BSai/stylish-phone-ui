from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    ENV: str = "dev"
    APP_NAME: str = "Safar Backend"
    DATABASE_URL: str = "postgresql+psycopg://safar:safar@localhost:5432/safar"
    REDIS_URL: str = "redis://localhost:6379/0"
    JWT_SECRET: str = "change-me"
    JWT_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_EXPIRE_MINUTES: int = 60 * 24 * 7


settings = Settings()
