from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.modules.curation_task.models import TaskLogConfig
from app.core.celery_app import celery_app
from typing import Optional, Dict
from datetime import datetime

async def get_and_update_task_status(db: AsyncSession, celery_task_id: str) -> Optional[TaskLogConfig]:
    stmt = select(TaskLogConfig).where(TaskLogConfig.celery_task_id == celery_task_id)
    result = await db.execute(stmt)
    task_log = result.scalar_one_or_none()
    
    task_meta = celery_app.AsyncResult(celery_task_id)
    celery_status = task_meta.status
    
    task_log.status = celery_status
    
    if celery_status in ("SUCCESS", "FAILURE") and task_log.completed_at is None:
        task_log.completed_at = datetime.now()
        
    await db.commit()
    await db.refresh(task_log)
    
    return task_log, task_meta.result

def format_task_response(task_log: TaskLogConfig, task_result: Dict) -> Dict:
    return{
        "celery_task_id": task_log.celery_task_id,
        "status": task_log.status,
        "requested_at": task_log.requested_at,
        "completed_at": task_log.completed_at,
        "keyword_id": task_log.keyword_id,
        "result": task_result if isinstance(task_result, dict) else {"detail": str(task_result)}
    }