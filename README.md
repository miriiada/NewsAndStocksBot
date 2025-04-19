# 📈 Yahoo News & Stocks Telegram Bot

A modern Telegram bot built with [aiogram](https://github.com/aiogram/aiogram), allowing users to fetch:

- 📰 The latest BBC News headlines
- 📊 Real-time stock prices from Yahoo Finance

> Powered by Python, BeautifulSoup, and requests.

---

## 🧠 Features

- 📢 Get top 5 BBC headlines with clickable links
- 💰 Get stock data for any ticker (e.g., AAPL, TSLA, NVDA)
- ⚡ Fast response using web scraping with headers
- 🛠 Built with `aiogram`, `bs4`, and `requests`

---

## 🛠 Requirements

- Python 3.9+
- Telegram bot token (from [@BotFather](https://t.me/BotFather))

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/yahoo-news-stock-bot.git
cd yahoo-news-stock-bot
```
### 2. Install dependencies
```bash
pip install -r requirements.txt
```
Or manually:
```bash
pip install aiogram requests beautifulsoup4
```
## 🔐 Configuration
Open the Python script and insert your bot token:
```python
TOKEN = 'your_bot_token'
```
## ▶️ Run the bot
```bash
python yahoo_news_stocks.py
```
## 💬 Usage
### Telegram Commands:

- `/start` — start the bot and show menu

- `/news` — get BBC news headlines

- `/stocks` <TICKER> — get stock data for symbol

### Keyboard Buttons:
- **News** — fetch latest headlines

- **Stocks** — get AAPL by default or any other ticker

- **Refresh** — reload news

- **Back** — return to main menu

## 🔗 Example Screenshot
(Add your screenshot or gif here if available)

## ⚙️ Technologies
- [aiogram](https://github.com/aiogram/aiogram) — async Telegram framework

- [requests](https://pypi.org/project/requests/) — HTTP requests

- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) — HTML parsing
