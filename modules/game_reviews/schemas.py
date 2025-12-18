from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from datetime import datetime

class CuratedGameReviewResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    
    id:int
    summary_text: str
    curated_at: datetime
    
class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="페이지 번호")
    size: int = Field(default=20, ge=1, le=100, description="페이지당 항목 수")
    
    keyword_id: Optional[int] = Field(default=None, description="특정 키워드 ID로 필터링")
    
class PaginatedCuratedGameReviewResponse(BaseModel):
    items: List[CuratedGameReviewResponse]
    total_count: int = Field(..., description="전체 항목 수")
    page: int = Field(..., ge=1, description="현재 페이지 번호")
    size: int = Field(..., ge=1, description="페이지당 항목 수")
    total_pages: int = Field(..., ge=1, description="전체 페이지 수")