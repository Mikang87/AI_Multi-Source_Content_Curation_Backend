from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.modules.content import service, schemas
from app.core.auth import get_current_user_id
from typing import List, Optional
import math

router = APIRouter()

@router.get(
    "/curated-content",
    response_model=schemas.PaginatedCuratedContentResponse,
    summary="최종 큐레이션 결과 조회 및 키워드 필터링 (필터링 및 페이징 적용)"
)
async def list_curated_contents(
    params: schemas.PaginationParams = Depends(),
    db: AsyncSession=Depends(get_db)
):
    items, total_count = await service.get_curated_contents(
        db,
        keyword_id=params.keyword_id,
        page=params.page,
        size=params.size
    )
    
    if total_count==0:
        total_pages = 1
    else:
        total_pages = math.ceil(total_count/params.size)
    
    return schemas.PaginatedCuratedContentResponse(
        items=items,
        total_count=total_count,
        page=params.page,
        size=params.size,
        total_pages=total_pages
    )