from .settings import Settings

settings: Settings = Settings()

API_CHANNEL_MAPPING = {
    "news": "News API",
    "reddit": "Reddit API",
    "github": "GitHub API"
}

DEFAULT_TASK_TIMEOUT_SECONDS = 300
ACCESS_TOKEN_EXPIRE_MINUTES = 30
API_VERSION="v0.1.0"


