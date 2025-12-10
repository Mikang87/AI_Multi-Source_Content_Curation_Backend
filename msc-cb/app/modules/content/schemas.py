from pydantic import BaseModel, ConfigDict
from typing import List
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