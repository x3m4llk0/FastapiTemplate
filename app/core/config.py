from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LOG_LEVEL: str

    LOG_LEVEL: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def POSTGRES_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

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

    CYPHER_SALT: str
    CYPHER_PASSWORD: str

    PROFILE_URL: str


    class Config:
        env_file = ".env"



settings = Settings()
