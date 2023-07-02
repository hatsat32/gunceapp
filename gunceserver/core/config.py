from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "GuncerAppServer"
    DESCRIPTION: str = "Gunce Encrypted Journal/Diary Application Server API"
    OPENAPI_URL: str = "/api/openapi.json"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str

    # Oauth2
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # one week

    class Config:
        env_file = ".env"
