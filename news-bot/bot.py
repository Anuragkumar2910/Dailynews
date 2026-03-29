import requests
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("API_KEY")

used_titles = set()

# 🧠 Category-specific keyword filters
CATEGORY_KEYWORDS = {
    "national": ["india", "government", "policy", "election"],
    "international": ["world", "war", "country", "global", "russia", "china"],
    "government": ["budget", "economy", "rbi", "scheme", "policy"],
    "tech": ["ai", "technology", "robot", "semiconductor", "startup"],
    "sports": ["cricket", "match", "ipl", "football", "tournament"],
    "trending": ["breaking", "update", "big", "latest"]
}

# 🚫 Words to ignore (junk filter)
IGNORE_WORDS = ["version", "release", "pypi", "library", "package"]

def get_news(query, category):
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&language=en&apiKey={API_KEY}"
    
    response = requests.get(url).json()
    articles = response.get("articles", [])

    news_list = []

    for article in articles:
        title = article.get("title", "").lower()

        if not title:
            continue

        # ❌ Skip duplicates
        if title in used_titles:
            continue

        # ❌ Skip junk
        if any(word in title for word in IGNORE_WORDS):
            continue

        # ✅ Keep only category-relevant news
        if not any(word in title for word in CATEGORY_KEYWORDS[category]):
            continue

        used_titles.add(title)
        news_list.append(title.title())

        if len(news_list) == 3:
            break

    return "\n".join([f"{i+1}. {t}" for i, t in enumerate(news_list)]) or "No relevant updates\n"


def send_message():
    global used_titles
    used_titles.clear()

    national = get_news("India politics", "national")
    international = get_news("global news war geopolitics", "international")
    government = get_news("India economy budget RBI", "government")
    tech = get_news("AI technology semiconductor", "tech")
    sports = get_news("cricket IPL sports India", "sports")
    trending = get_news("breaking news India", "trending")

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


send_message()
