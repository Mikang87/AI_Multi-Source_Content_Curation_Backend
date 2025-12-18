from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class TaskRequest(BaseModel):
    keyword_id: int

class TaskRequestResponse(BaseModel):
    celery_task_id: str
    status: str
    message: str
    
class TaskStatusResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    
    celery_task_id: str
    status: str
    requested_at: datetime
    completed_at: Optional[datetime] = None
    keyword_id: int
    result: Optional[dict] = None
    