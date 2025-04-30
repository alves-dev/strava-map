import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # STRAVA
    STRAVA_ACCESS_TOKEN: str = None
    STRAVA_ACTIVITIES_AFTER: int = 1714231709

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

dotenv.load_dotenv()
setting = Settings()
