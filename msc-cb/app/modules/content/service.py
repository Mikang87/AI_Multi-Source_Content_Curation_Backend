from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import join
from app.modules.content.models import CuratedContentConfig, RawContentConfig
from typing import List, Dict, Optional

async def get_curated_contents(db: AsyncSession, keyword_id: Optional[int] = None) ->List[Dict]:
    stmt = (
        select(CuratedContentConfig, RawContentConfig.original_url, RawContentConfig.source_type).select_from(
            join(CuratedContentConfig, RawContentConfig, CuratedContentConfig.raw_content_id == RawContentConfig.id)
        )
    )
    
    if keyword_id is not None:
        stmt = stmt.where(RawContentConfig.keyword_id == keyword_id)
    
    stmt = stmt.order_by(CuratedContentConfig.curated_at.desc())
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
    return curated_list