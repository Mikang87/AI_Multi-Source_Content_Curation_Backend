from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.modules.content import service, schemas
from typing import List, Optional

router = APIRouter()

@router.get(
    "/curated-content",
    response_model=List[schemas.CuratedContentResponse],
    summary="최종 큐레이션 결과 조회 및 키워드 필터링"
)
async def list_curated_contents(
    keyword_id: Optional[int] = Query(None, description="조회할 키워드 ID(없으면 전체 조회)"),
    db: AsyncSession=Depends(get_db),
):
    curated_contents = await service.get_curated_contents(db, keyword_id=keyword_id)
    
    return curated_contents