import asyncio
from app.modules.external.processor.base_llm_processor import BaseLLMProcessor, LLMProcessingResult
from typing import List

# 실제 LLM 연동 대신 사용될 더미 프로세서
class DummyLLMProcessor(BaseLLMProcessor):
    async def summarize_and_extract_keywords(self, raw_text: str) -> LLMProcessingResult:
        # 💡 Note: 실제 LLM API 호출 대신 비동기 작업을 흉내냅니다.
        await asyncio.sleep(1)
        # 원본 텍스트의 앞부분을 요약으로 가정합니다.
        # 실제로는 LLM에게 프롬프트를 전달하고 응답을 파싱합니다.
        summary = raw_text[:200].replace("\n"," ")+"..."
        # 키워드는 텍스트를 분리하여 임의로 추출한다고 가정합니다.
        words = raw_text.split()
        keywords = list(set([w.strip(",.") for w in words[:5]]))
        
        return LLMProcessingResult(
            summary_text=f"[DUMMY 요약]: {summary}",
            extracted_keywords = keywords
        )