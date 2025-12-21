import httpx
from abc import ABC, abstractmethod
from typing import List, Dict, Optional

class CollectedData(Dict):
    source_type: str
    original_url: str
    raw_text: str

class BaseCollector(ABC):
    def __init__(self, keyword: str, api_key: Optional[str]=None):
        self.api_key = api_key
        self.keyword = keyword
        self.client = httpx.AsyncClient(timeout=15.0)
        
@abstractmethod
async def collect(self) -> List[CollectedData]:
    pass

@property
@abstractmethod
def source_type(self) -> str:
    pass

async def __aenter__(self):
    return self

async def __aexit__(self, exc_type, exc_val, exc_tb):
    await self.client.aclose()