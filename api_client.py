import aiohttp
from config import NEWS_API_KEY, NEWS_API_URL


class NewsAPIClient:
    """Класс для работы с News API"""
    
    def __init__(self):
        self.api_key = NEWS_API_KEY
        self.base_url = NEWS_API_URL
    
    async def get_top_headlines(self, country='us', category=None):
        """Получить главные новости"""
        url = f"{self.base_url}/top-headlines"
        params = {
            'apiKey': self.api_key,
            'country': country,
            'pageSize': 5  # Количество новостей
        }
        
        if category:
            params['category'] = category
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('articles', [])
                else:
                    return []
    
    async def search_news(self, query):
        """Поиск новостей по ключевому слову"""
        url = f"{self.base_url}/everything"
        params = {
            'apiKey': self.api_key,
            'q': query,
            'pageSize': 5,
            'sortBy': 'publishedAt'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('articles', [])
                else:
                    return []
