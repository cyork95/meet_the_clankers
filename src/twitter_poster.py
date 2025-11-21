"""
Module for posting tweets to X (Twitter) using the API v2.
"""
import os
import time
import tweepy
from typing import List, Optional

def post_tweets(tweets: List[str], reply_to_status_id: str = None) -> bool:
    """
    Post a list of tweets as a thread to X/Twitter.
    
    Args:
        tweets: List of tweet strings to post
        reply_to_status_id: Optional ID of a tweet to reply to
        
    Returns:
        True if successful, False otherwise
    """
    # 1. Get Credentials
    api_key = os.getenv("TWITTER_API_KEY")
    api_secret = os.getenv("TWITTER_API_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    
    if not all([api_key, api_secret, access_token, access_token_secret]):
        print("[ERROR] Missing Twitter API credentials in .env")
        print("   Required: TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET")
        return False
        
    try:
        # 2. Authenticate (API v2)
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        
        print("[INFO] Authenticated with X/Twitter API")
        
        # 3. Post Tweets
        previous_tweet_id = reply_to_status_id
        
        for i, tweet_text in enumerate(tweets):
            print(f"   Posting tweet {i+1}/{len(tweets)}...")
            
            # Check length (basic check, Tweepy handles some, but good to be safe)
            if len(tweet_text) > 280:
                print(f"[WARN] Tweet {i+1} is too long ({len(tweet_text)} chars). Truncating...")
                tweet_text = tweet_text[:277] + "..."
            
            response = client.create_tweet(
                text=tweet_text,
                in_reply_to_tweet_id=previous_tweet_id
            )
            
            previous_tweet_id = response.data['id']
            print(f"   [SUCCESS] Posted! ID: {previous_tweet_id}")
            
            # Small delay between tweets in a thread
            time.sleep(1)
            
        return True
        
    except tweepy.errors.Forbidden as e:
        print(f"[ERROR] Twitter API Forbidden (403): {e}")
        print("   Check your permissions (Read and Write) and subscription tier.")
        return False
    except tweepy.errors.Unauthorized as e:
        print(f"[ERROR] Twitter API Unauthorized (401): {e}")
        print("   Check your API keys and tokens.")
        return False
    except Exception as e:
        print(f"[ERROR] Error posting to Twitter: {e}")
        return False

if __name__ == "__main__":
    # Test stub
    pass
