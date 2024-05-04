from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_NAME: str
    SECRET_KEY: str
    TOKEN_HASH_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"


settings = Settings()
