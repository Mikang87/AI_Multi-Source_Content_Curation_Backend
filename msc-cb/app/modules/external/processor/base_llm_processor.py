from abc import ABC, abstractmethod
from typing import Dict, List, Any

class LLMProcessingResult(Dict):
    summary_text: str
    extracted_keywords: List[str]
    
class BaseLLMProcessor(ABC):
    def __init__(self, api_key: str):
        self.api_key = api_key

    @abstractmethod
    async def summarize_and_extract_keywords(self, raw_text: str) -> LLMProcessingResult:
        pass