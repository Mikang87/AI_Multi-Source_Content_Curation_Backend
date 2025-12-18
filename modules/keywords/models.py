from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class KeywordConfig(Base):
    __tablename__ = "keyword"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    keyword_text = Column(String(100), unique=True, index=True, nullable=False)
    
    raw_contents = relationship(
        "RawContentConfig",
        back_populates="keyword",
        cascade="all, delete-orphan"
    )
    
    task_logs = relationship(
        "TaskLogConfig",
        back_populates="keyword",
        cascade="all, delete-orphan"
    )
    
    game_reviews = relationship(
        "GameReviewConfig",
        back_populates="keyword",
        cascade="all, delete-orphan"
    )