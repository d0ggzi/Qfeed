from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    BOT_TOKEN: str
    ADMIN_ID: int
    CLIENT_ID: int
    BOT_ID: int
    API_ID: int
    API_HASH: str

    POSTGRES_OUT_HOST: str
    POSTGRES_OUT_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str


settings = Settings()
