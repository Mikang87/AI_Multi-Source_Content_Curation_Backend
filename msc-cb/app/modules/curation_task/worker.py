from app.core.celery_app import celery_app
import logging, time

logger = logging.getLogger(__name__)

@celery_app.task(name="curation_tasks.start_workflow")
def curation_workflow_task(keyword_id: int):
    logger.info(f"Task received for keyword ID: {keyword_id}. Starting curation workflow.")
    logger.info(f"Curation workflow completed for keyword ID: {keyword_id}.")
    #TODO: 작업 상태 업데이트 (DB Tasklog) 로직 추가 예정
    return {
        "status": "SUCCESS", 
        "message":f"Curated content generated for keyword {keyword_id}",
        "colleted_count": 5
    }