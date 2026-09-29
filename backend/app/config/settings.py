from pydantic_settings import BaseSettings, SettingsConfigDict
# BaseSettings is a special Pydantic class designed for application configuration.
# SettingsConfigDict - This is used to configure how BaseSettings should behave.
class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int = 3306       #3306 is the standard MySQL port.
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()