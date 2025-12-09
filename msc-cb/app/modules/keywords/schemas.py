from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class KeywordCreate(BaseModel):
    keyword_text: str

class KeywordResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    
    id: int
    user_id: int
    keyword_text: str
