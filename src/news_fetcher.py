"""
Module for fetching news from RSS feeds.
"""
import time
import re
from datetime import datetime, timedelta, timezone
from time import mktime
from typing import Dict, List
import feedparser

# Default RSS Feeds
RSS_FEEDS = {
    "ai": [
        "https://techcrunch.com/category/artificial-intelligence/feed/",
        "https://www.wired.com/feed/category/ai/latest/rss",
        "https://www.theverge.com/rss/ai/index.xml",
        "https://www.artificialintelligence-news.com/feed/"
    ],
    "tech": [
        "https://techcrunch.com/feed/",
        "https://www.theverge.com/rss/index.xml",
        "http://feeds.arstechnica.com/arstechnica/index",
        "https://www.engadget.com/rss.xml"
    ],
    "politics": [
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        "https://feeds.npr.org/1004/rss.xml",
        "https://www.politico.com/rss/politics08.xml"
    ],
    "business": [
        "https://www.cnbc.com/id/10001147/device/rss/rss.html",
        "https://feeds.bloomberg.com/technology/news.xml",
        "https://feeds.reuters.com/reuters/businessNews"
    ],
    "entertainment": [
        "https://www.polygon.com/rss/index.xml",
        "https://www.ign.com/rss/articles.xml",
        "https://www.hollywoodreporter.com/feed/"
    ],
    "science": [
        "https://www.sciencedaily.com/rss/top_news.xml",
        "http://feeds.nature.com/nature/rss/current",
        "https://www.newscientist.com/feed/home"
    ],
    "gaming": [
        "https://www.polygon.com/rss/index.xml",
        "https://www.ign.com/rss/articles.xml",
        "https://www.gamespot.com/feeds/news/"
    ],
    "space": [
        "https://www.nasa.gov/rss/dyn/breaking_news.rss",
        "https://www.space.com/feeds/all"
    ]
}

def fetch_news(time_window: str = "24h", categories: List[str] = None) -> Dict[str, List[Dict]]:
    """
    Fetch news from RSS feeds based on time window and categories.
    """
    if categories is None:
        categories = ["ai", "tech", "business", "science"]
        
    # Calculate cutoff time
    now = datetime.now(timezone.utc)
    if time_window == "24h":
        cutoff = now - timedelta(hours=24)
    elif time_window == "7d":
        cutoff = now - timedelta(days=7)
    else:
        cutoff = now - timedelta(hours=24)
        
    print(f"[INFO] Fetching news since {cutoff.strftime('%Y-%m-%d %H:%M')}...")
    
    all_news = {}
    
    for category in categories:
        if category not in RSS_FEEDS:
            print(f"[WARN] Category '{category}' not found. Skipping.")
            continue
            
        print(f"\n[INFO] Checking {category.upper()} feeds...")
        category_news = []
        
        for feed_url in RSS_FEEDS[category]:
            try:
                feed = feedparser.parse(feed_url)
                print(f"  - Parsing {feed.feed.get('title', feed_url)}...")
                
                for entry in feed.entries:
                    # Parse publication date
                    published_time = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        published_time = datetime.fromtimestamp(mktime(entry.published_parsed), timezone.utc)
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        published_time = datetime.fromtimestamp(mktime(entry.updated_parsed), timezone.utc)
                        
                    if published_time and published_time > cutoff:
                        # Clean up summary (remove HTML tags)
                        summary = entry.get('summary', '')
                        summary = re.sub('<[^<]+?>', '', summary) # Simple HTML stripper
                        
                        category_news.append({
                            'title': entry.title,
                            'link': entry.link,
                            'summary': summary[:500] + "..." if len(summary) > 500 else summary,
                            'source': feed.feed.get('title', 'Unknown Source'),
                            'published': published_time.strftime('%Y-%m-%d %H:%M')
                        })
            except Exception as e:
                print(f"[ERROR] Failed to parse {feed_url}: {e}")
                
        # Sort by date (newest first) and limit
        category_news.sort(key=lambda x: x['published'], reverse=True)
        all_news[category] = category_news[:5] # Top 5 per category
        print(f"  [SUCCESS] Found {len(category_news)} recent items for {category}.")
        
    total_items = sum(len(items) for items in all_news.values())
    print(f"\n[SUCCESS] Total news items fetched: {total_items}")
    return all_news

if __name__ == "__main__":
    # Test run
    news = fetch_news(categories=["ai", "tech"])
    import json
    print(json.dumps(news, indent=2, default=str))
