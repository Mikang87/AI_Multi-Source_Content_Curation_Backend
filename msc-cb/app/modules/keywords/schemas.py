from pydantic import BaseModel, ConfigDict

class KeywordCreate(BaseModel):
    keyword_text: str

class KeywordResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    
    id: int
    user_id: int
    keyword_text: str

class KeywordUpdate(BaseModel):
    keyword_text: str

class KeywordDelete(BaseModel):
    message: str = "Keyword succesfully deleted."
    id: int