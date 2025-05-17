import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # STRAVA
    STRAVA_ACTIVITIES_AFTER: int = 1714231709  # 2024-24-27 15:28
    STRAVA_CLIENT_ID: str
    STRAVA_CLIENT_SECRET: str
    STRAVA_REDIRECT_URI: str = 'http://localhost'
    STRAVA_SCOPE: str = 'activity:read_all'

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


dotenv.load_dotenv()
setting = Settings()
