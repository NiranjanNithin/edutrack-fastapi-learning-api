from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "EduTrack API"
    database_url: str = "sqlite:///./edutrack.db"

settings = Settings()