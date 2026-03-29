import requests
import os

# 🔐 Environment variables
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("API_KEY")

# 🧠 Store used titles to avoid duplicates
used_titles = set()

# 📰 Function to fetch news (no duplicates)
def get_news(query):
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&language=en&apiKey={API_KEY}"
    
    response = requests.get(url).json()
    articles = response.get("articles", [])

    news_list = []

    for article in articles:
        title = article.get("title", "")

        # Skip empty or duplicate titles
        if not title or title in used_titles:
            continue

        # Add to used set
        used_titles.add(title)
        news_list.append(title)

        if len(news_list) == 3:
            break

    return "\n".join([f"{i+1}. {t}" for i, t in enumerate(news_list)]) or "No updates available\n"


# 📩 Send message
def send_message():
    global used_titles
    used_titles.clear()  # Reset daily

    national = get_news("India politics OR government OR election")
    international = get_news("world geopolitics OR war OR global news")
    government = get_news("India economy OR budget OR RBI OR scheme")
    tech = get_news("AI technology OR semiconductor OR robotics OR startup")
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

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)


# ▶️ Run once (for GitHub Actions)
send_message()
