from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env_dev`
        env_file=(".env_dev", ".env.prod"),
    )
    api_version: str
    database_url: str


settings = Settings()


def get_settings():
    """
    Dependency to get settings instance
    """
    return settings
