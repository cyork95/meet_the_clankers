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
    parser.add_argument("--categories", type=str, default="ai,tech,business,science", help="Comma-separated list of categories (ai, tech, business, science, entertainment, politics)")
    
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
    result = generate_script(news, mode=args.mode, holiday_theme=args.holiday)
    
    if not result or not result[0]:
        print("❌ Script generation failed. Exiting.")
        return
    
    script, title = result
    
    # Save script with title and date
    script_dir = "outputs/scripts"
    if not os.path.exists(script_dir):
        os.makedirs(script_dir)
    
    date_str = datetime.now().strftime('%Y%m%d')
    script_filename = os.path.join(script_dir, f"{title}_{date_str}.json")
    
    with open(script_filename, "w") as f:
        import json
        json.dump(script, f, indent=2)
    print(f"📝 Script saved to {script_filename}")

    # 3. Generate Audio
    audio_files = asyncio.run(generate_audio_files(script, output_dir="outputs/temp_audio"))
    
    if not audio_files:
        print("❌ Audio generation failed. Exiting.")
        return

    # 4. Assemble Podcast
    output_filename = os.path.join("outputs", f"{title}_{date_str}.mp3")
    assemble_podcast(audio_files, output_file=output_filename)

if __name__ == "__main__":
    main()
