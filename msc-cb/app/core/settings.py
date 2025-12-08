from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_ENV: str = Field(..., env="APP_ENV")
    SECRET_KEY: str = Field(..., env="SECRET_KEY")

    MYSQL_HOST: str = Field(..., env="MYSQL_HOST")
    MYSQL_USER: str = Field(..., env="MYSQL_USER")
    MYSQL_ROOT_PASSWORD: str = Field(..., env="MYSQL_USER")
    MYSQL_PASSWORD: str = Field(..., env="MYSQL_PASSWORD")
    MYSQL_DATABASE: str = Field(..., env="MYSQL_DATABASE")
    
    REDIS_HOST: str = Field(..., env="REDIS_HOST")
    REDIS_PASSWORD: str = Field(..., env="REDIS_PASSWORD")
    CELERY_BROKER_URL: str = Field(..., env="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = Field(..., env="CELERY_RESULT_BACKEND")
    
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    NEWS_API_KEY: str = Field(..., env="NEWS_API_KEY")
    REDDIT_CLIENT_ID: str = Field(..., env="REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET: str = Field(..., env="REDDIT_CLIENT_SECRET")
    GITHUB_PAT_TOKEN: str = Field(..., env="GITHUB_PAT_TOKEN")
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}/{self.MYSQL_DATABASE}"
    
settings = Settings()