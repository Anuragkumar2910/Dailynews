import requests
import schedule
import time

# 🔐 Your credentials
import os
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("API_KEY")

# 📰 Function to fetch news
def get_news(query):
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&language=en&apiKey={API_KEY}"

    response = requests.get(url).json()
    articles = response.get("articles", [])[:3]

    news_text = ""
    for i, article in enumerate(articles, 1):
        news_text += f"{i}. {article['title']}\n"

    return news_text if news_text else "No updates available\n"

# 📩 Send message function
def send_message():
    general = get_news("india OR government OR economy")
    tech = get_news("AI OR technology OR semiconductor")
    sports = get_news("cricket OR sports India")

    message = f"""
📰 Daily Brief

🇮🇳 Top News:
{general}

💻 Tech:
{tech}

🏏 Sports:
{sports}

🔥 Stay updated, stay ahead!
"""

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}

    requests.post(url, data=data)

# ▶️ Run once immediately
send_message()

# ⏰ Schedule daily at 8 AM
schedule.every().day.at("08:00").do(send_message)

# 🔄 Keep running
while True:
    schedule.run_pending()
    time.sleep(60)
