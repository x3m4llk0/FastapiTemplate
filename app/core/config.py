from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LOG_LEVEL: str

    LOG_LEVEL: str

    PG_HOST: str
    PG_PORT: int
    PG_USER: str
    PG_PASS: str
    PG_NAME: str

    @property
    def POSTGRES_URL(self):
        return f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASS}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_NAME}"

    MONGO_HOST: str
    MONGO_PORT: str

    @property
    def MONGO_URL(self):
        return f"mongodb://{self.MONGO_HOST}:{self.MONGO_PORT}"

    REDIS_HOST: str
    REDIS_PORT: str

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    class Config:
        env_file = ".env"


settings = Settings()
