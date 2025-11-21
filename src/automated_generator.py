"""
Automated podcast generation and publishing script.
This script can be scheduled to run automatically at a specific time.
"""
import asyncio
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.news_fetcher import fetch_news
from src.script_generator import generate_script
from src.audio_generator import generate_audio_files
from src.podcast_producer import assemble_podcast
from src.tweet_generator import generate_tweets
from src.twitter_poster import post_tweets

load_dotenv()

async def generate_daily_episode(categories=None, mode="daily", holiday_theme=None, generate_tweet=False, post_tweet=False):
    """
    Generate a complete podcast episode automatically.
    """
    if categories is None:
        categories = ["ai", "tech", "business", "science"]
    
    print(f"[INFO] Starting automated podcast generation at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[INFO] Categories: {categories}")
    print(f"[INFO] Mode: {mode}")
    if holiday_theme:
        print(f"[INFO] Holiday Theme: {holiday_theme}")
    
    # 1. Fetch News
    print("\n[INFO] Fetching news...")
    time_window = "7d" if mode == "weekly" else "24h"
    news = fetch_news(time_window=time_window, categories=categories)
    
    if not news:
        print("[ERROR] No news found. Aborting.")
        return False
    
    # 2. Generate Script
    print("\n[INFO] Generating script...")
    result = generate_script(news, mode=mode, holiday_theme=holiday_theme)
    
    if not result or not result[0]:
        print("[ERROR] Script generation failed. Aborting.")
        return False
    
    script, title = result
    print(f"[INFO] Episode title: {title}")
    
    # 3. Save Script
    script_dir = "outputs/scripts"
    os.makedirs(script_dir, exist_ok=True)
    
    date_str = datetime.now().strftime('%Y%m%d')
    script_filename = os.path.join(script_dir, f"{title}_{date_str}.json")
    
    import json
    with open(script_filename, "w") as f:
        json.dump(script, f, indent=2)
    print(f"[INFO] Script saved to {script_filename}")
    
    # 3.5 Generate Tweets (Optional)
    if generate_tweet or post_tweet:
        print("\n[INFO] Generating promotional tweets...")
        tweets = generate_tweets(script, title)
        if tweets:
            tweet_dir = "outputs/tweets"
            os.makedirs(tweet_dir, exist_ok=True)
            tweet_filename = os.path.join(tweet_dir, f"{title}_{date_str}_tweets.txt")
            with open(tweet_filename, "w", encoding="utf-8") as f:
                for i, tweet in enumerate(tweets, 1):
                    f.write(f"--- Tweet {i} ---\n{tweet}\n\n")
            print(f"[INFO] Tweets saved to {tweet_filename}")
            
            # 3.6 Post to Twitter (Optional)
            if post_tweet:
                print("\n[INFO] Posting to X/Twitter...")
                # Post the first tweet option by default
                if post_tweets([tweets[0]]):
                    print("[SUCCESS] Successfully posted to Twitter!")
                else:
                    print("[WARN] Failed to post to Twitter.")
        else:
            print("[WARN] Tweet generation failed or returned empty.")

    # 4. Generate Audio
    print("\n[INFO] Generating audio...")
    audio_files = await generate_audio_files(script, output_dir="outputs/temp_audio")
    
    if not audio_files:
        print("[ERROR] Audio generation failed. Aborting.")
        return False
    
    # 5. Assemble Podcast
    print("\n[INFO] Assembling podcast...")
    output_filename = os.path.join("outputs", f"{title}_{date_str}.mp3")
    result = assemble_podcast(audio_files, output_file=output_filename)
    
    if result:
        print(f"\n[SUCCESS] Podcast generated successfully: {output_filename}")
        print(f"[INFO] Completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return True
    else:
        print("[ERROR] Podcast assembly failed.")
        return False

def main():
    """Main entry point for scheduled execution."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Automated Meet the Clankers Episode Generator")
    parser.add_argument("--mode", choices=["daily", "weekly"], default="daily", help="Podcast mode")
    parser.add_argument("--categories", type=str, default="ai,tech,business,science", 
                       help="Comma-separated categories")
    parser.add_argument("--holiday", type=str, default=None,
                       help="Holiday theme (e.g., 'Thanksgiving', 'Christmas', 'New Year')")
    parser.add_argument("--tweet", action="store_true", help="Generate promotional tweets")
    parser.add_argument("--post-tweet", action="store_true", help="Automatically post to X/Twitter (requires API keys)")
    
    args = parser.parse_args()
    categories = [c.strip() for c in args.categories.split(",")]
    
    # Run the async function
    success = asyncio.run(generate_daily_episode(
        categories=categories, 
        mode=args.mode,
        holiday_theme=args.holiday,
        generate_tweet=args.tweet,
        post_tweet=args.post_tweet
    ))
    
    # Exit with appropriate code for task scheduler
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
