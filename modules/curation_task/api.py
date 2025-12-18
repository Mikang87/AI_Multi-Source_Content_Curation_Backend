from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.modules.curation_task import schemas, service
from app.modules.curation_task.models import TaskLogConfig
from app.modules.curation_task.worker import curation_workflow_task, game_review_curation_workflow_task

router = APIRouter()
review_router = APIRouter()

@router.post(
    "/curation-tasks",
    response_model = schemas.TaskRequestResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="키워드 기반 큐레이션 작업 요청"
)
async def request_curation_task(
    request_in: schemas.TaskRequest,
    db: AsyncSession = Depends(get_db)
):
    keyword_id = request_in.keyword_id
    
    task_result = curation_workflow_task.delay(keyword_id)
    celery_task_id = task_result.id
    
    new_task_log = TaskLogConfig(
        keyword_id = keyword_id,
        celery_task_id = celery_task_id,
        status="Pending"
    )
    db.add(new_task_log)
    await db.commit()
    await db.refresh(new_task_log)
    
    return schemas.TaskRequestResponse(
        celery_task_id=celery_task_id,
        status="Pending",
        message="Curation task submitted succesfully."
    )
    
@router.get(
    "/curation-task/{task-id}",
    response_model=schemas.TaskStatusResponse,
    summary="비동기 작업 상태 조회"
)
async def get_task_status(
    task_id: str,
    db: AsyncSession = Depends(get_db)
):
    task_log_data, task_result_data = await service.get_and_update_task_status(db, task_id)
    
    if not task_log_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task ID '{task_id}' not found in TaskLog."
        )
        
    return service.format_task_response(task_log_data, task_result_data)

@review_router.post(
    "/review-curation-tasks",
    response_model = schemas.TaskRequestResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="키워드 기반 큐레이션 작업 요청"
)
async def request_curation_task(
    request_in: schemas.TaskRequest,
    db: AsyncSession = Depends(get_db)
):
    keyword_id = request_in.keyword_id
    
    task_result = game_review_curation_workflow_task.delay(keyword_id)
    celery_task_id = task_result.id
    
    new_task_log = TaskLogConfig(
        keyword_id = keyword_id,
        celery_task_id = celery_task_id,
        status="Pending"
    )
    db.add(new_task_log)
    await db.commit()
    await db.refresh(new_task_log)
    
    return schemas.TaskRequestResponse(
        celery_task_id=celery_task_id,
        status="Pending",
        message="Curation task submitted succesfully."
    )
    
@review_router.get(
    "/review-curation-task/{task-id}",
    response_model=schemas.TaskStatusResponse,
    summary="비동기 작업 상태 조회"
)
async def get_task_status(
    task_id: str,
    db: AsyncSession = Depends(get_db)
):
    task_log_data, task_result_data = await service.get_and_update_task_status(db, task_id)
    
    if not task_log_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task ID '{task_id}' not found in TaskLog."
        )
        
    return service.format_task_response(task_log_data, task_result_data)