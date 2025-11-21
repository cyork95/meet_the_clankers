"""
Test script to verify X/Twitter API credentials.
"""
import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    print("[INFO] Testing X/Twitter API Connection...")
    
    api_key = os.getenv("TWITTER_API_KEY")
    api_secret = os.getenv("TWITTER_API_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    
    # Check if keys exist
    if not api_key: print("[ERROR] Missing TWITTER_API_KEY"); return
    if not api_secret: print("[ERROR] Missing TWITTER_API_SECRET"); return
    if not access_token: print("[ERROR] Missing TWITTER_ACCESS_TOKEN"); return
    if not access_token_secret: print("[ERROR] Missing TWITTER_ACCESS_TOKEN_SECRET"); return

    try:
        # Authenticate
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        
        # Get own user info to verify read access
        me = client.get_me()
        if me.data:
            print(f"[SUCCESS] Authentication Successful! Connected as: @{me.data.username}")
            
            # Try to post a test tweet (optional, maybe user doesn't want to spam)
            # print("Attempting to post test tweet...")
            # response = client.create_tweet(text="Beep boop. Meet the Clankers API test successful!")
            # print(f"[SUCCESS] Test tweet posted! ID: {response.data['id']}")
        else:
            print("[WARN] Authenticated, but couldn't fetch user data.")
            
    except tweepy.errors.Forbidden as e:
        print(f"[ERROR] Forbidden (403): {e}")
        print("   Check if your App has 'Read and Write' permissions enabled in Developer Portal.")
    except tweepy.errors.Unauthorized as e:
        print(f"[ERROR] Unauthorized (401): {e}")
        print("   Check if your API Keys and Access Tokens are correct.")
        print("   Did you regenerate tokens AFTER changing permissions?")
    except Exception as e:
        print(f"[ERROR] Connection Failed: {e}")

if __name__ == "__main__":
    test_connection()
