from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_ENV: str = Field(..., env="APP_ENV")
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field(..., env="ALGORITHM")

    MYSQL_HOST: str = Field(..., env="MYSQL_HOST")
    MYSQL_USER: str = Field(..., env="MYSQL_USER")
    MYSQL_ROOT_PASSWORD: str = Field(..., env="MYSQL_USER")
    MYSQL_PASSWORD: str = Field(..., env="MYSQL_PASSWORD")
    MYSQL_DATABASE: str = Field(..., env="MYSQL_DATABASE")
    
    REDIS_HOST: str = Field(..., env="REDIS_HOST")
    REDIS_PASSWORD: str = Field(..., env="REDIS_PASSWORD")
    CELERY_BROKER_URL: str = Field(..., env="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = Field(..., env="CELERY_RESULT_BACKEND")
    
    OLLAMA_API_URL: str = Field(..., env="OLLAMA_API_URL")
    OLLAMA_LLM_MODEL: str = Field(..., env="OLLAMA_LLM_MODEL")
    NEWS_API_KEY: str = Field(..., env="NEWS_API_KEY")
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}/{self.MYSQL_DATABASE}"
    
settings = Settings()