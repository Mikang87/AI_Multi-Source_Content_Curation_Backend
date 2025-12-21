import httpx, logging
from typing import List, Optional
from app.modules.external.collector.base_collector import BaseCollector, CollectedData

logger = logging.getLogger(__name__)

class SteamCollector(BaseCollector):
    def __init__(self, api_key: str, keyword: str):
        super().__init__(api_key, keyword)
        self.search_url = "https://store.steampowered.com/api/storesearch"
        self.review_url = "https://store.steampowered.com/appreviews"
        
    @property
    def source_type(self) -> str:
        return "steam"
    
    async def _get_app_id(self) -> Optional[int]:
        try:
            params ={
                "term": self.keyword,
                "l": "korean",
                "cc": "KR"
            }
            response = await self.client.get(self.search_url, params=params)
            data = response.json()
            
            if data.get("total", 0) > 0:
                return data["items"][0]["id"]
            return None
        except Exception as e:
            logger.error(f"Failed to find AppID for {self.keyword}: {e}")
            return None
        
    async def collect(self) -> List[CollectedData]:
        app_id = await self._get_app_id()
        if not app_id:
            logger.warning(f"No game found for keyword: {self.keyword}")
            return []
        
        try:
            params = {
                "json": 1,
                "language": "korean",
                "filter": "recent",
                "num_per_page": 10
            }
            url = f"{self.review_url}/{app_id}"
            response = await self.client.get(url, params=params)
            data = response.json()
            
            if data.get("success") != 1:
                return []
            
            results = []
            for item in data.get("reviews", []):
                results.append({
                    "source_type": self.source_type,
                    "review_text": item["review"],
                    "language": "korean"
                })
            return results
        except Exception as e:
            logger.error(f"Error collecting Steam reviews for {app_id}: {e}")
            return []
        
    async def __aenter__(self):
        return self
    async def __aexit__(self, exc_type, exc_value, traceback):
        pass