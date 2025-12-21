import httpx, json, logging
from typing import Dict, Optional
from app.core import config
from app.modules.external.processor.base_llm_processor import BaseLLMProcessor, LLMProcessingResult

logger = logging.getLogger(__name__)

class OllamaReviewProcessor(BaseLLMProcessor):
    def __init__(self, api_base_url: str = config.settings.OLLAMA_API_URL, model_name: str =config.settings.OLLAMA_LLM_MODEL):
        super().__init__(api_key=None)
        self.api_base_url = api_base_url,
        self.model_name = model_name
        self.client = httpx.AsyncClient(
            base_url=api_base_url,
            headers={}
        )
        
    async def summarize_and_extract_keywords(self, raw_text: str) -> LLMProcessingResult:
        prompt = f"""
        당신은 게임 전문 비평가입니다. 다음 게임 리뷰를 읽고 핵심 내용을 장점, 단점으로 나누어 요약하세요.
        응답은 반드시 한국어로 작성하고, JSON 형식으로 답변하세요.

        [리뷰 내용]:
        {raw_text}

        [응답 예시]: (JSON 포맷만 반환)
        {{"summary_text": "..."}}
        """
        
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
        
        response = await self.client.post("/api/generate", json=data, timeout=120.0)
        response.raise_for_status()
        
        try:
            response_data = response.json()
            content = response_data["response"]
            llm_output = json.loads(content)
            
            return LLMProcessingResult(
                summary_text = llm_output["summary_text"],
                extracted_keywords = None
            )         
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"Ollama API returned {e.response.status_code}: {e.response.text}")
        except (httpx.RequestError, json.JSONDecodeError, KeyError) as e:
            raise RuntimeError(f"Ollama processing failed: {e}")