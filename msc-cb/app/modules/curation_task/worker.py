from app.core.celery_app import celery_app
from app.core.database import AsyncSessionLocal
from app.modules.curation_task.models import TaskLogConfig
from app.modules.keywords.models import KeywordConfig # KeywordConfig 임포트 확인
from app.modules.content.models import RawContentConfig, CuratedContentConfig
from app.modules.external.collector.news_collector import NewsCollector
from app.modules.external.processor.llm_processor import DummyLLMProcessor
from app.core import config
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import asyncio, logging
from typing import List

logger = logging.getLogger(__name__)

async def save_raw_contents(session:AsyncSession, keyword_id:int, collected_data_list)-> List[RawContentConfig]:
    raw_contents = [
        RawContentConfig(
            keyword_id=keyword_id,
            source_type=data["source_type"],
            original_url=data["original_url"],
            raw_text=data["raw_text"]           
        ) for data in collected_data_list
    ]
    session.add_all(raw_contents)
    await session.commit()
    return raw_contents

async def save_curated_content(session: AsyncSession, raw_content_id: int, processed_result) -> CuratedContentConfig:
    keywords_str = ", ".join(processed_result["extracted_keywords"])
    
    curated = CuratedContentConfig(
        raw_content_id=raw_content_id,
        summary_text=processed_result["summary_text"],
        extracted_keywords=keywords_str,
        curated_at=datetime.now()
    )
    session.add(curated)
    await session.commit()
    await session.refresh(curated)
    return curated

async def _run_curation_workflow(db: AsyncSession, task_log: TaskLogConfig, keyword_id: int, keyword_text: str):
    NEWS_API_KEY = config.settings.NEWS_API_KEY
    LLM_API_KEY = "DUMMY_LLM_KEY"
    total_processed_count = 0
    
    try:
        task_log.status = "RUNNING"
        await db.commit()
        
        logger.info(f"Starting data colletion for keyword ID: {keyword_id} with text: {keyword_text}...")
        
        async with NewsCollector(api_key=NEWS_API_KEY, keyword=keyword_text) as collector:
            collected_data = await collector.collect()
            
        if not collected_data:
            logger.warning("No data collected. Workflow finished early.")
            task_log.status = "SUCCESS"
            task_log.completed_at = datetime.now()
            await db.commit()
            return {
                "status": "SUCCESS",
                "message": "No content found for the keyword"
            }
            
        raw_contents = await save_raw_contents(db, keyword_id, collected_data)
        logger.info(f"Saved {len(raw_contents)} raw content items.")
        
        processor = DummyLLMProcessor(api_key=LLM_API_KEY)
        
        for raw_item in raw_contents:
            logger.info(f"Processing RawContent ID: {raw_item.id}...")
            
            processed_result = await processor.summarize_and_extract_keywords(raw_item.raw_text)
            
            await save_curated_content(db, raw_item.id, processed_result)
            total_processed_count += 1
            
        task_log.status = "SUCCESS"
        task_log.completed_at = datetime.now()
        await db.commit()
        
        logger.info(f"Workflow successfully completed for keyword ID: {keyword_id}. Processed {total_processed_count} items.")
        
        return {
            "status": "SUCCESS",
            "message": "Curation workflow successfully completed.",
            "collected_count": len(collected_data),
            "processed_cound": total_processed_count
        }
    except Exception as e:
        logger.error(f"Error in curation workflow for keyword ID {keyword_id}: {e}", exc_info=True)
        await db.rollback()
        task_log.status = "FAILURE"
        task_log.completed_at = datetime.now()
        await db.commit()
        
        return {
            "status": "FAILURE",
            "message": f"Curation workflow failed: {e.__class__.__name__}: {e}"
        }
    
@celery_app.task(name="curation_tasks.start_workflow", bind=True)
def curation_workflow_task(self, keyword_id: int):
    try:
        async def get_initial_task_log_and_db():
            async with AsyncSessionLocal() as db:
                await asyncio.sleep(0.05)
                result_log = await db.execute(select(TaskLogConfig).where(TaskLogConfig.celery_task_id == self.request.id))
                task_log = result_log.scalars().first()
                if not task_log:
                    raise Exception(f"TaskLog not found for Celery ID: {self.request.id}")
                
                result_keyword = await db.execute(select(KeywordConfig).where(KeywordConfig.id == keyword_id))
                keyword = result_keyword.scalars().first()
                if not keyword:
                    raise Exception(f"Keyword not found for ID: {keyword_id}")
                
                return await _run_curation_workflow(db, task_log, keyword_id, keyword.keyword_text)
                
        final_result = asyncio.run(get_initial_task_log_and_db())
        return final_result
    except Exception as e:
        logger.error(f"Unhandled critical error during workflow execution: {e}", exc_info=True)
        
        return {
            "status": "FAILURE",
            "message": f"CRITICAL: Unhandled Celery/Asyncio initialization error. Type: {e.__class__.__name__}: {str(e)}"
        }