from pydantic import BaseSettings
from pathlib import Path, PosixPath


class Settings(BaseSettings):
    APP_NAME: str = "GuncerAppServer"
    DESCRIPTION: str = "Gunce Encrypted Journal/Diary Application Server API"
    VERSION: str = "0.1.0"
    OPENAPI_URL: str = "/api/openapi.json"
    DEBUG: bool = False

    # PATHS
    APP_PATH: PosixPath = Path(__file__).parent.parent.resolve()
    WRITE_PATH: PosixPath = APP_PATH.parent.joinpath("writable")
    PUBLIC_PATH: PosixPath = APP_PATH.parent.joinpath("public")

    # Database releted
    DATABASE_URL: str = f"sqlite:///{WRITE_PATH}/database.db"

    # Oauth2
    SECRET_KEY: str = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # one week

    class Config:
        env_file = ".env"
