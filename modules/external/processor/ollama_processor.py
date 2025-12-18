import httpx, json
from app.modules.external.processor.base_llm_processor import BaseLLMProcessor, LLMProcessingResult
from app.core import config

class OllamaLLMProcessor(BaseLLMProcessor):
    def __init__(self, api_base_url: str = config.settings.OLLAMA_API_URL, model_name: str= config.settings.OLLAMA_LLM_MODEL):
        super().__init__(api_key=None)
        self.api_base_url = api_base_url
        self.model_name = model_name
        self.client = httpx.AsyncClient(
            base_url=api_base_url,
            headers={}
        )
        
    async def summarize_and_extract_keywords(self, raw_text: str) -> LLMProcessingResult:
        prompt = f"""
        당신은 전문적인 콘텐츠 큐레이터입니다.
        제공된 텍스트를 읽고 다음 두 가지 작업을 JSON 형식으로 수행하세요.
        1. 200자 이내로 핵심 내용만 요약(summary_text)합니다.
        2. 텍스트에서 가장 중요한 키워드 5개(extracted_keywords)를 추출합니다.

        [원문 텍스트]:
        {raw_text}
        
        [응답 형식]: (JSON 포맷만 반환)
        {{
          "summary_text": "...",
          "extracted_keywords": ["키워드1", "키워드2", "키워드3", "키워드4", "키워드5"]
        }}
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
            content = response_data['response']
            llm_output = json.loads(content)
            
            return LLMProcessingResult(
                summary_text = llm_output["summary_text"],
                extracted_keywords = llm_output["extracted_keywords"]
            )
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"Ollama API returned {e.response.status_code}: {e.response.text}")
        except (httpx.RequestError, json.JSONDecodeError, KeyError) as e:
            raise RuntimeError(f"Ollama processing failed: {e}")