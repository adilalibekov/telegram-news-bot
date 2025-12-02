import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

# Получаем токены
BOT_TOKEN = os.getenv('BOT_TOKEN')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

# Проверка что токены загрузились
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле!")
if not NEWS_API_KEY:
    raise ValueError("NEWS_API_KEY не найден в .env файле!")

# Базовый URL для News API
NEWS_API_URL = 'https://newsapi.org/v2'

# Категории новостей
CATEGORIES = [
    'business',
    'entertainment', 
    'health',
    'science',
    'sports',
    'technology'
]
