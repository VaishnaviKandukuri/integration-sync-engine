from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GITHUB_TOKEN: str
    GITHUB_USERNAME: str

    AIRTABLE_TOKEN: str
    AIRTABLE_BASE_ID: str
    AIRTABLE_TABLE_NAME: str = "Contributors"

    DATABASE_URL: str = "sqlite:///./sync_engine.db"

    class Config:
        env_file = ".env"


settings = Settings()