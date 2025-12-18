from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import join, func
from app.modules.game_reviews.models import GameReviewConfig, CuratedGameReviewConfig
from typing import List, Dict, Optional, Tuple

async def get_curated_game_reviews(
    db: AsyncSession,
    keyword_id: Optional[int] = None,
    page: int=1,
    size: int=20
) -> Tuple[List[Dict], int]:
    base_join = join(CuratedGameReviewConfig, GameReviewConfig, CuratedGameReviewConfig.game_review_id==GameReviewConfig.id)
    
    count_stmt = (
        select(func.count(CuratedGameReviewConfig.id)).select_from(base_join)
    )
    
    if keyword_id is None:
        count_stmt = count_stmt.where(GameReviewConfig.keyword_id == keyword_id)
        
    total_count_result = await db.execute(count_stmt)
    total_count = total_count_result.scalar_one()
    
    data_stmt = (
        select(CuratedGameReviewConfig, GameReviewConfig.source)
        .select_from(base_join)
    )
    
    if keyword_id is not None:
        data_stmt = data_stmt.where(GameReviewConfig.keyword_id==keyword_id)
    
    offset = (page-1)*size
    stmt = data_stmt.order_by(CuratedGameReviewConfig.curated_at.desc()).limit(size).offset(offset)
    
    result = await db.execute(stmt)
    
    curated_list = []
    
    for curated_content, source in result.all():
        curated_list.append({
            "id": curated_content.id,
            "summary_text": curated_content.summary_text,
            "source": source,
            "curated_at": curated_content.curated_at
        })
    
    return curated_list, total_count