from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.modules.keywords.models import KeywordConfig
from app.modules.keywords.schemas import KeywordCreate, KeywordUpdate
from fastapi import HTTPException, status
from typing import List, Optional

async def create_keyword(db: AsyncSession, keyword_data: KeywordCreate, user_id: int) -> KeywordConfig:
    new_keyword = KeywordConfig(
        user_id=user_id,
        keyword_text = keyword_data.keyword_text
    )
    db.add(new_keyword)
    await db.commit()
    await db.refresh(new_keyword)
    return new_keyword

async def get_keywords(db: AsyncSession, user_id: int) -> List[KeywordConfig]:
    stmt = select(KeywordConfig).where(KeywordConfig.user_id == user_id).order_by(KeywordConfig.id)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_one_keyword(db: AsyncSession, keyword_id: int, user_id: int) -> Optional[KeywordConfig]:
    stmt = select(KeywordConfig).where(
        KeywordConfig.id == keyword_id,
        KeywordConfig.user_id == user_id
    )
    result = await db.execute(stmt)
    return result.scalars().first()

async def update_keyword(db: AsyncSession, keyword_id:int, keyword_data: KeywordUpdate, user_id:int) -> KeywordConfig:
    keyword = await get_one_keyword(db, keyword_id, user_id)
    
    if not keyword:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Keyword with ID {keyword_id} not found or you do not have permission."
        )
    keyword.keyword_text = keyword_data.keyword_text
    
    await db.commit()
    await db.refresh(keyword)
    return keyword

async def delete_keyword(db: AsyncSession, keyword_id: int, user_id: int) -> int:
    keyword = await get_one_keyword(db, keyword_id, user_id)
    
    if not keyword:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            deatil = f"Keyword with ID {keyword_id} not found or you do not have permission."
        )
    
    await db.delete(keyword)
    await db.commit()
    
    return keyword_id
    