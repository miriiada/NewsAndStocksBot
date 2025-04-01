from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import requests
from bs4 import BeautifulSoup
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token
TOKEN = 'your_bot_token'
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Headers for web requests
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Main menu keyboard
main_menu = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="News"), types.KeyboardButton(text="Stocks")],
        [types.KeyboardButton(text="Refresh")]
    ],
    resize_keyboard=True
)

# Function to parse BBC headlines
def get_bbc_headlines():
    url = "https://www.bbc.com/news"
    try:
        logger.info(f"Fetching news from {url}")
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        headlines = soup.find_all("h2", {"data-testid": "card-headline"})
        news_list = []
        for headline in headlines[:5]:
            text = headline.text.strip()
            link_tag = headline.find_parent("a")
            link = "https://www.bbc.com" + link_tag["href"] if link_tag and "href" in link_tag.attrs else "#"
            news_list.append({"text": text, "link": link})
        logger.info(f"Found {len(news_list)} headlines")
        return news_list if news_list else [{"text": "No news found", "link": "#"}]
    except requests.RequestException as e:
        logger.error(f"Failed to load news: {str(e)}")
        return [{"text": f"Error loading news: {str(e)}", "link": "#"}]

# Function to parse Yahoo stock by ticker
def get_stock_data(ticker="AAPL"):
    url = f"https://finance.yahoo.com/quote/{ticker}/"
    try:
        logger.info(f"Fetching stock data from {url}")
        time.sleep(2)  # Delay to avoid rate limits
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        price = soup.find("span", {"data-testid": "qsp-price"})
        change = soup.find("span", {"data-testid": "qsp-price-change"})
        percent = soup.find("span", {"data-testid": "qsp-price-change-percent"})
        if price and change and percent:
            return {
                "price": price.text,
                "change": change.text,
                "percent": percent.text
            }
        logger.warning("Some stock data missing")
        return {"price": "N/A", "change": "N/A", "percent": "N/A"}
    except requests.RequestException as e:
        logger.error(f"Failed to load stock data: {str(e)}")
        return {"price": f"Error: {str(e)}", "change": "N/A", "percent": "N/A"}

# Handler for /start command
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    logger.info(f"User {message.from_user.id} started the bot")
    await message.reply("Hello! I'm a bot for BBC news and stocks. Use /news or /stocks <ticker> (e.g., /stocks TSLA)!", reply_markup=main_menu)

# Handler for /news, "News", and "Refresh"
@dp.message(lambda message: message.text in ["/news", "News", "Refresh"])
async def send_news(message: types.Message):
    logger.info(f"User {message.from_user.id} requested news with '{message.text}'")
    if message.text == "Refresh":
        await message.reply("Refreshing news...")
    headlines = get_bbc_headlines()
    news_text = "Latest BBC News:\n\n" + "\n".join([f"{i}. {h['text']}" for i, h in enumerate(headlines, 1)])
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=f"Read more {i}", callback_data=f"news_{i-1}")]
            for i in range(1, len(headlines) + 1)
        ] + [[types.InlineKeyboardButton(text="Back", callback_data="back")]]
    )
    await message.reply(news_text, reply_markup=keyboard)

# Handler for /stocks and "Stocks"
@dp.message(lambda message: message.text.startswith(("/stocks", "Stocks")))
async def send_stocks(message: types.Message):
    logger.info(f"User {message.from_user.id} requested stocks with '{message.text}'")
    args = message.text.split(maxsplit=1)
    ticker = args[1].upper() if len(args) > 1 else "AAPL"  # Default to AAPL if no ticker
    await message.reply(f"Fetching stock data for {ticker}...")
    stock = get_stock_data(ticker)
    stock_text = (
        f"{ticker} Stock:\n"
        f"Price: {stock['price']} USD\n"
        f"Change: {stock['change']} USD\n"
        f"Percent: {stock['percent']}"
    )
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[[types.InlineKeyboardButton(text="Back", callback_data="back")]]
    )
    await message.reply(stock_text, reply_markup=keyboard)

# Handler for "Read more" buttons
@dp.callback_query(lambda query: query.data.startswith("news_"))
async def send_news_link(query: types.CallbackQuery):
    logger.info(f"User {query.from_user.id} clicked 'Read more' for {query.data}")
    news_index = int(query.data.split("_")[1])
    headlines = get_bbc_headlines()
    if 0 <= news_index < len(headlines):
        link = headlines[news_index]["link"]
        await query.message.reply(f"Link to the news:\n{link}")
    else:
        await query.message.reply("News not found.")
    await query.answer()

# Handler for "Back" button
@dp.callback_query(lambda query: query.data == "back")
async def back_to_menu(query: types.CallbackQuery):
    logger.info(f"User {query.from_user.id} clicked 'Back'")
    await query.message.reply("Back to main menu!", reply_markup=main_menu)
    await query.answer()

# Run the bot
async def main():
    logger.info("Starting bot polling...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("Bot stopped")

if __name__ == "__main__":
    asyncio.run(main())