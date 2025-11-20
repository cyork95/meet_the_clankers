import argparse
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from news_fetcher import fetch_news
from script_generator import generate_script
from audio_generator import generate_audio_files
from podcast_producer import assemble_podcast

# Load environment variables
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Meet the Clankers - AI Podcast Generator")
    parser.add_argument("--mode", choices=["daily", "weekly"], default="daily", help="Podcast mode: daily or weekly")
    parser.add_argument("--holiday", type=str, help="Optional holiday theme (e.g., 'Christmas')")
    parser.add_argument("--categories", type=str, default="ai,tech,politics", help="Comma-separated list of categories")
    
    args = parser.parse_args()
    
    categories = [c.strip() for c in args.categories.split(",")]
    
    print(f"🤖 Meet the Clankers: Initializing...")
    print(f"🎙️ Mode: {args.mode}")
    print(f"📚 Categories: {categories}")
    if args.holiday:
        print(f"🎉 Holiday Theme: {args.holiday}")

    # 1. Fetch News
    news = fetch_news(time_window="7d" if args.mode == "weekly" else "24h", categories=categories)
    
    if not news:
        print("❌ No news found. Exiting.")
        return

    # 2. Generate Script
    script = generate_script(news, mode=args.mode, holiday_theme=args.holiday)
    
    if not script:
        print("❌ Script generation failed. Exiting.")
        return
        
    # Save script for debug
    with open("latest_script.json", "w") as f:
        import json
        json.dump(script, f, indent=2)
    print("📝 Script saved to latest_script.json")

    # 3. Generate Audio
    audio_files = asyncio.run(generate_audio_files(script))
    
    if not audio_files:
        print("❌ Audio generation failed. Exiting.")
        return

    # 4. Assemble Podcast
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_filename = os.path.join(output_dir, f"meet_the_clankers_{args.mode}_{datetime.now().strftime('%Y%m%d')}.mp3")
    assemble_podcast(audio_files, output_file=output_filename)

if __name__ == "__main__":
    main()
