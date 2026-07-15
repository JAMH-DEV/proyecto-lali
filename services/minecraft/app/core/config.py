from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "LALI Minecraft Service"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    MINECRAFT_API_HOST: str = "0.0.0.0"
    MINECRAFT_API_PORT: int = 8001

    MINECRAFT_RCON_HOST: str = "minecraft"
    MINECRAFT_RCON_PORT: int = 25575
    MINECRAFT_RCON_PASSWORD: str = ""
    MINECRAFT_RCON_TIMEOUT: int = 10

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()