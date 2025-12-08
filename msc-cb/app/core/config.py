from .settings import Settings

settings: Settings = Settings()

API_CHANNEL_MAPPING = {
    "news": "News API",
    "reddit": "Reddit API",
    "github": "GitHub API"
}

DEFAULT_TASK_TIMEOUT_SECONDS = 300
API_VERSION="v0.0.0"