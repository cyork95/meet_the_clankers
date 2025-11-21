import pytest
from src.news_fetcher import fetch_news

def test_fetch_news_structure():
    """Test that fetch_news returns the correct structure."""
    # Mocking would be better, but for now we'll test the structure with a live call
    # or just check the function signature if we want to avoid network calls.
    # Let's do a live call but limit it to one category for speed.
    
    news = fetch_news(categories=["tech"], time_window="24h")
    
    assert isinstance(news, dict)
    if "tech" in news:
        assert isinstance(news["tech"], list)
        if len(news["tech"]) > 0:
            item = news["tech"][0]
            assert "title" in item
            assert "link" in item
            assert "summary" in item
            assert "source" in item

def test_fetch_news_invalid_category():
    """Test that invalid categories are handled gracefully."""
    news = fetch_news(categories=["invalid_category"])
    assert "invalid_category" not in news
