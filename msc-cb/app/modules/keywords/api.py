from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.auth import get_current_user_id
from app.modules.keywords import service, schemas
from typing import List

router = APIRouter()

@router.post(
    "/keywords",
    response_model = schemas.KeywordResponse,
    status_code=status.HTTP_201_CREATED,
    summary="새로운 키워드 등록"
)
async def register_new_keyword(
    keyword_in: schemas.KeywordCreate,
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    new_keyword = await service.create_keyword(db, keyword_in, current_user_id)
    return new_keyword

@router.get(
    "/keywords",
    response_model = List[schemas.KeywordResponse],
    summary="등록된 키워드 목록 조회"
)
async def list_keywords(
    db: AsyncSession=Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    keywords = await service.get_keywords(db, current_user_id)
    return keywords