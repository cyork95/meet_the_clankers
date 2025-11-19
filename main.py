import argparse
import asyncio
import os
from dotenv import load_dotenv

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

    # TODO: Implement full pipeline
    # 1. Fetch News
    # 2. Generate Script
    # 3. Generate Audio
    # 4. Assemble Podcast

if __name__ == "__main__":
    main()
