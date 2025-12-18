from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class GameReviewConfig(Base):
    __tablename__ = "game_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    keyword_id = Column(Integer, ForeignKey("keyword.id"), nullable=False)
    source = Column(String(50), nullable=False)
    language = Column(String(50), nullable=False)
    review_text = Column(Text, nullable=False)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    curated_review = relationship(
        "CuratedGameReviewConfig",
        back_populates="game_reviews",
        cascade="all, delete-orphan"
    )
    
    keyword = relationship(
        "KeywordConfig",
        back_populates="game_reviews"
    )
    
class CuratedGameReviewConfig(Base):
    __tablename__= "curated_game_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    game_review_id = Column(Integer, ForeignKey("game_reviews.id", ondelete="CASCADE"), nullable=False)
    summary_text = Column(Text, nullable=False)
    curated_at = Column(DateTime, server_default=func.now())
    
    game_reviews = relationship(
        "GameReviewConfig",
        back_populates="curated_review"
    )
    