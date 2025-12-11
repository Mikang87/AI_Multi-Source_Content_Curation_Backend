from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class TaskLogConfig(Base):
    __tablename__ = "tasklog"
    
    id = Column(Integer, primary_key=True, index=True)  
    keyword_id = Column(Integer, ForeignKey("keyword.id", ondelete="CASCADE"), nullable=False)
    celery_task_id = Column(String(100), unique=True, index=True, nullable=False)
    status = Column(String(100), default="Pending", nullable=False)
    requested_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)
    
    keyword = relationship(
        "KeywordConfig",
        back_populates="task_logs"
    )