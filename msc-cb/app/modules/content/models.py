from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, func
from app.core.database import Base

class RawContentConfig(Base):
    __tablename__ = "rawcontent"
    
    id=Column(Integer, primary_key=True, index=True)
    keyword_id = Column(Integer, ForeignKey("keyword.id"), nullable=False)
    source_type = Column(String(50), nullable=False)
    original_url = Column(String(500), nullable=False)
    raw_text = Column(Text, nullable=False)
    collected_at = Column(DateTime, default=func.now())
    
class CuratedContentConfig(Base):
    __tablename__ = "curatedcontent"
    
    id = Column(Integer, primary_key=True, index=True)
    raw_content_id = Column(Integer, ForeignKey("rawcontent.id"), nullable=False)
    summary_text = Column(Text, nullable=False)
    extracted_keywords = Column(Text, nullable=False)
    curated_at = Column(DateTime, server_default=func.now())