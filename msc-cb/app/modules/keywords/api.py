from fastapi import APIRouter, Depends, status, HTTPException
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

@router.put(
    "/keywords/{keyword_id}",
    response_model=schemas.KeywordResponse,
    summary="키워드 수정 (소유자만 가능)"
)
async def update_keyword(
    keyword_id: int,
    keyword_in: schemas.KeywordUpdate,
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    updated_keyword = await service.update_keyword(
        db,
        keyword_id,
        keyword_in,
        current_user_id
    )
    return updated_keyword

@router.delete(
    "/keywords/{keyword_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.KeywordDelete,
    summary="키워드 삭제 (소유자만 가능)"
)
async def delete_keyword(
    keyword_id: int,
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    deleted_id = await service.delete_keyword(db, keyword_id, current_user_id)
    return {"message": f"Keyword with ID {deleted_id} successfully deleted.", "id": deleted_id}