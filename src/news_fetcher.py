"""
Module for fetching news from RSS feeds.
"""
import time
from datetime import datetime, timedelta
from typing import Dict, List
import feedparser

# Default RSS Feeds
RSS_FEEDS = {
    "ai": [
        "https://techcrunch.com/category/artificial-intelligence/feed/",
        "https://www.wired.com/feed/category/ai/latest/rss",
        "https://www.theverge.com/rss/ai/index.xml"
    ],
    "tech": [
        "https://techcrunch.com/feed/",
        "https://www.theverge.com/rss/index.xml",
        "http://feeds.arstechnica.com/arstechnica/index"
    ],
    "politics": [
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        "https://feeds.npr.org/1004/rss.xml"
    ],
    "business": [
        "https://www.cnbc.com/id/10001147/device/rss/rss.html",
        "https://feeds.bloomberg.com/technology/news.xml"
    ],
    "entertainment": [
        "https://www.polygon.com/rss/index.xml",
        "https://www.ign.com/rss/articles.xml"
    ],
    "science": [
        "https://www.sciencedaily.com/rss/top_news.xml",
        "http://feeds.nature.com/nature/rss/current"
    ]
}

def parse_date(entry):
    """Attempt to parse the date from an RSS entry."""
    try:
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            return datetime.fromtimestamp(time.mktime(entry.published_parsed))
        if hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            return datetime.fromtimestamp(time.mktime(entry.updated_parsed))
    except Exception:
        pass
    return datetime.now()

def fetch_news(time_window: str = "24h", categories: List[str] = ["tech"]) -> Dict[str, List[Dict]]:
    """
    Fetch news from RSS feeds for the given categories and time window.
    """
    news_data = {}
    
    # Calculate cutoff time
    now = datetime.now()
    if time_window == "24h":
        cutoff = now - timedelta(hours=24)
    elif time_window == "7d":
        cutoff = now - timedelta(days=7)
    else:
        cutoff = now - timedelta(hours=24) # Default
        
    print(f"📰 Fetching news since {cutoff.strftime('%Y-%m-%d %H:%M')}...")

    for category in categories:
        if category not in RSS_FEEDS:
            print(f"⚠️ Category '{category}' not found. Skipping.")
            continue
            
        print(f"  🔍 Checking {category} sources...")
        category_news = []
        
        for url in RSS_FEEDS[category]:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries:
                    pub_date = parse_date(entry)
                    if pub_date > cutoff:
                        category_news.append({
                            "title": entry.title,
                            "link": entry.link,
                            "summary": getattr(entry, 'summary', ''),
                            "published": pub_date.strftime("%Y-%m-%d %H:%M"),
                            "source": feed.feed.title if hasattr(feed, 'feed') and hasattr(feed.feed, 'title') else url
                        })
            except Exception as e:
                print(f"    ❌ Error fetching {url}: {e}")
                
        # Sort by date (newest first) and limit
        category_news.sort(key=lambda x: x['published'], reverse=True)
        
        # Limit logic: 5 for daily, 10 for weekly
        limit = 5 if time_window == "24h" else 10
        news_data[category] = category_news[:limit]
        print(f"    ✅ Found {len(news_data[category])} stories for {category}.")
        
    return news_data

if __name__ == "__main__":
    # Test run
    news = fetch_news(categories=["ai", "tech"])
    import json
    print(json.dumps(news, indent=2))
