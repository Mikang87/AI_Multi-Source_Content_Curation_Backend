from app.modules.external.collector.base_collector import BaseCollector, CollectedData
from typing import List, Dict, Any

EXTERNAL_NEWS_API_URL = "https://newsapi.org/v2/everything"

class NewsCollector(BaseCollector):
    @property
    def source_type(self) -> str:
        return "NEWS"
    
    async def collect(self) -> List[CollectedData]:
        params = {
            "q": self.keyword,
            "apiKey": self.api_key,
            "language": "ko",
            "pageSize": 20,
            "sortBy": "publishedAt"
        }
        
        collected_items: List[CollectedData] = []
        
        try:
            response = await self.client.get(
                EXTERNAL_NEWS_API_URL,
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != "ok":
                print(f"NewsAPI returned error status: {data.get('code',"N/A")}")
                return []
            
            articles = data.get("articles", [])
            
            for article in articles:
                title = article.get("title", "")
                description = article.get("description", "")
                content = article.get("content", "")
                
                raw_text = f"제목: {title}\n\n설명: {description}\n\n내용: {content}"
                
                item = CollectedData(
                    source_type = self.source_type,
                    original_url = article.get("url","N/A"),
                    raw_text=raw_text
                )
                collected_items.append(item)
                
        except httpx.HTTPStatusError as e:
            print(f"HTTP Status Error ({e.response.status_code}) during News Collection: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during News Collection: {e}")
        return collected_items