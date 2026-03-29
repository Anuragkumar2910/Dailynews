import requests
import schedule
import time
import os

# 🔐 Environment variables
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("API_KEY")

# 🧠 Important keywords filter
IMPORTANT_KEYWORDS = [
    "India", "government", "policy", "economy", "budget",
    "ISRO", "election", "law", "AI", "technology",
    "cricket", "sports"
]

# 📰 Function to fetch filtered news
def get_news(query):
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&language=en&apiKey={API_KEY}"
    
    response = requests.get(url).json()
    articles = response.get("articles", [])

    filtered_news = []

    for article in articles:
        title = article.get("title", "")

        # Keep only relevant news
        if any(keyword.lower() in title.lower() for keyword in IMPORTANT_KEYWORDS):
            filtered_news.append(title)

        if len(filtered_news) == 3:
            break

    # fallback if no filtered results
    if not filtered_news:
        filtered_news = [a["title"] for a in articles[:3]]

    news_text = ""
    for i, title in enumerate(filtered_news, 1):
        news_text += f"{i}. {title}\n"

    return news_text if news_text else "No updates available\n"


# 📩 Send message
def send_message():
    national = get_news("India government OR election OR policy")
    international = get_news("world news OR geopolitics OR war")
    government = get_news("India economy OR budget OR RBI OR scheme")
    tech = get_news("AI OR technology OR semiconductor OR robotics")
    sports = get_news("cricket OR IPL OR sports India")
    trending = get_news("breaking news India OR trending India")

    message = f"""
📰 Daily Brief

🇮🇳 National:
{national}

🌍 International:
{international}

🏛️ Government & Economy:
{government}

💻 Tech:
{tech}

🏏 Sports:
{sports}

🔥 Trending:
{trending}
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
