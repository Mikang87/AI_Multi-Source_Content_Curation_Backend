from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from datetime import datetime

def keywords_from_str(value):
    if isinstance(value, str):
        return [k.strip() for k in value.split(",")]
    return []

class CuratedContentResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes = True
    )
    id: int
    summary_text: str
    extracted_keywords: List[str]
    curated_at: datetime

    raw_content_id: int
    original_url: str
    source_type: str
    
class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="페이지 번호")
    size: int = Field(default=20, ge=1, le=100, description="페이지당 항목 수")
    
    keyword_id: Optional[int] = Field(default=None, description="특정 키워드 ID로 필터링")

class PaginatedCuratedContentResponse(BaseModel):
    items: List[CuratedContentResponse]
    total_count: int = Field(..., description="전체 항목 수")
    page: int = Field(..., ge=1, description="현재 페이지 번호")
    size: int = Field(..., ge=1, description="페이지당 항목 수")
    total_pages: int = Field(..., ge=1, description="전체 페이지 수")
    
    