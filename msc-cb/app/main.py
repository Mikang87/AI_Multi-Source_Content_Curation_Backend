from fastapi import FastAPI

app = FastAPI(
    title="AI Curation Backend API",
    description="AI 기반 콘텐츠 큐레이션 백엔드 시스템",
    version="0.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)