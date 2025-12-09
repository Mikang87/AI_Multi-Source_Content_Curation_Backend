from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.modules.keywords.models import KeywordConfig
from app.modules.keywords.schemas import KeywordCreate
from typing import List

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