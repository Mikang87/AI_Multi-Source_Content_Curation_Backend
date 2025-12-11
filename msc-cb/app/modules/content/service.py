from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import join, func
from app.modules.content.models import CuratedContentConfig, RawContentConfig
from typing import List, Dict, Optional, Tuple

async def get_curated_contents(
    db: AsyncSession, 
    keyword_id: Optional[int] = None,
    page: int=1,
    size: int=20,
) -> Tuple[List[Dict], int]:
    base_join = join(CuratedContentConfig, RawContentConfig, CuratedContentConfig.raw_content_id== RawContentConfig.id)
    
    count_stmt = (
        select(func.count(CuratedContentConfig.id)).select_from(base_join)
    )
    
    if keyword_id is not None:
        count_stmt = count_stmt.where(RawContentConfig.keyword_id == keyword_id)
    
    total_count_reslut = await db.execute(count_stmt)
    total_count = total_count_reslut.scalar_one()
    
    data_stmt = (
        select(CuratedContentConfig, RawContentConfig.original_url, RawContentConfig.source_type)
        .select_from(base_join)
    )
    
    if keyword_id is not None:
        data_stmt = data_stmt.where(RawContentConfig.keyword_id == keyword_id)
        
    offset = (page-1)*size
    stmt = data_stmt.order_by(CuratedContentConfig.curated_at.desc()).limit(size).offset(offset)
    
    result = await db.execute(stmt)
    
    curated_list = []
    
    for curated_content, url, source_type in result.all():
        keywords = [k.strip() for k in (curated_content.extracted_keywords or "").split(",")]
        
        curated_list.append({
            "id": curated_content.id,
            "summary_text": curated_content.summary_text,
            "extracted_keywords": keywords,
            "curated_at": curated_content.curated_at,
            "raw_content_id": curated_content.raw_content_id,
            "original_url": url,
            "source_type": source_type
        })
    return curated_list, total_count

