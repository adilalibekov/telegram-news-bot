import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from config import BOT_TOKEN, CATEGORIES
from api_client import NewsAPIClient

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
news_client = NewsAPIClient()


def format_article(article):
    """Форматирование новости для отправки"""
    title = article.get('title', 'Без заголовка')
    description = article.get('description', 'Нет описания')
    url = article.get('url', '')
    source = article.get('source', {}).get('name', 'Неизвестно')
    
    text = f"📰 <b>{title}</b>\n\n"
    text += f"{description}\n\n"
    text += f"🔗 <a href='{url}'>Читать полностью</a>\n"
    text += f"📌 Источник: {source}"
    
    return text


def get_main_keyboard():
    """Создание главной клавиатуры"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📰 Главные новости")],
            [KeyboardButton(text="💼 Бизнес"), KeyboardButton(text="⚽ Спорт")],
            [KeyboardButton(text="💻 Технологии"), KeyboardButton(text="🎬 Развлечения")],
            [KeyboardButton(text="🔬 Наука"), KeyboardButton(text="🏥 Здоровье")],
        ],
        resize_keyboard=True
    )
    return keyboard


@dp.message(CommandStart())
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    welcome_text = (
        "👋 Привет! Я бот для получения новостей!\n\n"
        "📋 Доступные команды:\n"
        "/top - Главные новости\n"
        "/search <текст> - Поиск новостей\n\n"
        "Или используй кнопки ниже! 👇"
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard())


@dp.message(Command("top"))
async def cmd_top(message: Message):
    """Обработчик команды /top - главные новости"""
    await message.answer("⏳ Загружаю главные новости...")
    
    articles = await news_client.get_top_headlines()
    
    if articles:
        for article in articles[:3]:  # Отправляем только первые 3
            text = format_article(article)
            await message.answer(text, parse_mode='HTML')
    else:
        await message.answer("❌ Не удалось загрузить новости. Попробуй позже.")


@dp.message(Command("search"))
async def cmd_search(message: Message):
    """Обработчик команды /search - поиск новостей"""
    # Получаем текст после команды
    query = message.text.replace('/search', '').strip()
    
    if not query:
        await message.answer("❌ Укажи ключевое слово для поиска!\nПример: /search bitcoin")
        return
    
    await message.answer(f"🔍 Ищу новости по запросу: {query}...")
    
    articles = await news_client.search_news(query)
    
    if articles:
        for article in articles[:3]:
            text = format_article(article)
            await message.answer(text, parse_mode='HTML')
    else:
        await message.answer(f"❌ Новостей по запросу '{query}' не найдено.")


@dp.message(F.text == "📰 Главные новости")
async def btn_top_news(message: Message):
    """Обработчик кнопки главных новостей"""
    await cmd_top(message)


@dp.message(F.text == "💼 Бизнес")
async def btn_business(message: Message):
    """Обработчик кнопки Бизнес"""
    await message.answer("⏳ Загружаю новости бизнеса...")
    articles = await news_client.get_top_headlines(category='business')
    
    if articles:
        for article in articles[:3]:
            text = format_article(article)
            await message.answer(text, parse_mode='HTML')
    else:
        await message.answer("❌ Не удалось загрузить новости.")


@dp.message(F.text == "⚽ Спорт")
async def btn_sports(message: Message):
    """Обработчик кнопки Спорт"""
    await message.answer("⏳ Загружаю спортивные новости...")
    articles = await news_client.get_top_headlines(category='sports')
    
    if articles:
        for article in articles[:3]:
            text = format_article(article)
            await message.answer(text, parse_mode='HTML')
    else:
        await message.answer("❌ Не удалось загрузить новости.")


@dp.message(F.text == "💻 Технологии")
async def btn_tech(message: Message):
    """Обработчик кнопки Технологии"""
    await message.answer("⏳ Загружаю новости технологий...")
    articles = await news_client.get_top_headlines(category='technology')
    
    if articles:
        for article in articles[:3]:
            text = format_article(article)
            await message.answer(text, parse_mode='HTML')
    else:
        await message.answer("❌ Не удалось загрузить новости.")


@dp.message(F.text == "🎬 Развлечения")
async def btn_entertainment(message: Message):
    """Обработчик кнопки Развлечения"""
    await message.answer("⏳ Загружаю новости развлечений...")
    articles = await news_client.get_top_headlines(category='entertainment')
    
    if articles:
        for article in articles[:3]:
            text = format_article(article)
            await message.answer(text, parse_mode='HTML')
    else:
        await message.answer("❌ Не удалось загрузить новости.")


@dp.message(F.text == "🔬 Наука")
async def btn_science(message: Message):
    """Обработчик кнопки Наука"""
    await message.answer("⏳ Загружаю научные новости...")
    articles = await news_client.get_top_headlines(category='science')
    
    if articles:
        for article in articles[:3]:
            text = format_article(article)
            await message.answer(text, parse_mode='HTML')
    else:
        await message.answer("❌ Не удалось загрузить новости.")


@dp.message(F.text == "🏥 Здоровье")
async def btn_health(message: Message):
    """Обработчик кнопки Здоровье"""
    await message.answer("⏳ Загружаю новости о здоровье...")
    articles = await news_client.get_top_headlines(category='health')
    
    if articles:
        for article in articles[:3]:
            text = format_article(article)
            await message.answer(text, parse_mode='HTML')
    else:
        await message.answer("❌ Не удалось загрузить новости.")


async def main():
    """Запуск бота"""
    print("🤖 Бот запущен!")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
