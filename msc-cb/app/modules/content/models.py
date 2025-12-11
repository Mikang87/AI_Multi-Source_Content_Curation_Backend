from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class RawContentConfig(Base):
    __tablename__ = "rawcontent"
    
    id=Column(Integer, primary_key=True, index=True)
    keyword_id = Column(Integer, ForeignKey("keyword.id", ondelete="CASCADE"), nullable=False)
    source_type = Column(String(50), nullable=False)
    original_url = Column(String(500), nullable=False)
    raw_text = Column(Text, nullable=False)
    collected_at = Column(DateTime, default=func.now())
    
    curated_content = relationship(
        "CuratedContentConfig",
        back_populates="raw_content",
        cascade="all, delete-orphan"
    )
    
    keyword = relationship(
        "KeywordConfig",
        back_populates="raw_contents"
    )
    
class CuratedContentConfig(Base):
    __tablename__ = "curatedcontent"
    
    id = Column(Integer, primary_key=True, index=True)
    raw_content_id = Column(Integer, ForeignKey("rawcontent.id", ondelete="CASCADE"), nullable=False)
    summary_text = Column(Text, nullable=False)
    extracted_keywords = Column(Text, nullable=False)
    curated_at = Column(DateTime, server_default=func.now())
    
    raw_content = relationship(
        "RawContentConfig",
        back_populates="curated_content"
    )