from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from app.core.database import Base

class KeywordConfig(Base):
    __tablename__ = "keyword_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    keyword_text = Column(String(100), unique=True, index=True, nullable=False)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())