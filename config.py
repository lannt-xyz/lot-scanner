from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):

    # Database Related
    sqlalchemy_database_uri: str
    sqlalchemy_echo: str
    database_schema: str

    # GEMINI API KEY
    gemini_api_key: str
    gemini_model_id: str
    
    # Auth Settings
    auth_secret_key: str

    # Google OAuth settings
    google_client_id: str
    google_client_secret: str

    # Scan Limit Settings
    scan_limit_guest: int = 0
    scan_limit_user: int = 0

    # pylint: disable=too-few-public-methods
    class Config:
        env_file = Path(Path(__file__).resolve().parent) / ".env"
        print(f'environment created - {Path(Path(__file__).resolve().name)}')

settings = Settings()
