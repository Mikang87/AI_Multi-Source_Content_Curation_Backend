from sqlalchemy import Column, Integer, String
from app.core.database import Base

class KeywordConfig(Base):
    __tablename__ = "keyword"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    keyword_text = Column(String(100), unique=True, index=True, nullable=False)   