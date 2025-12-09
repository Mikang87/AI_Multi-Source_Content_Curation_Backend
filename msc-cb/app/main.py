from fastapi import FastAPI
from app.modules.keywords.api import router as keywords_router
from app.modules.curation_task.api import router as curation_task_router
from app.modules.content.api import router as content_router

app = FastAPI(
    title="AI Curation Backend API",
    description="AI 기반 콘텐츠 큐레이션 백엔드 시스템",
    version="0.0.6",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(keywords_router, prefix="/api/v1", tags=["Keywords"])
app.include_router(curation_task_router, prefix="/api/v1", tags=["Curation Tasks"])
app.include_router(content_router, prefix="/api/v1", tags=["Curated Content"])