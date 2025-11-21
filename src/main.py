import argparse
import sys
import os
import json
from datetime import datetime

# Add root to path so we can import src.podcast
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    parser = argparse.ArgumentParser(description="Meet the Clankers - Multi-Show Generator")
    subparsers = parser.add_subparsers(dest="command", help="Available shows")

    # Podcast command
    podcast_parser = subparsers.add_parser("podcast", help="Generate News Podcast")
    podcast_parser.add_argument("--mode", choices=["daily", "weekly"], default="daily", help="Podcast mode: daily or weekly")
    podcast_parser.add_argument("--holiday", type=str, help="Optional holiday theme")
    podcast_parser.add_argument("--categories", type=str, default="ai,tech,business,science", help="Comma-separated list of categories")

    # Horror command
    horror_parser = subparsers.add_parser("horror", help="Generate Horror Show")
    horror_parser.add_argument("--prompt", type=str, help="Prompt for the horror story (optional, will auto-generate if omitted)")
    horror_parser.add_argument("--duration", type=str, choices=["short", "medium", "long"], default="medium", 
                               help="Target duration: short (3-5min), medium (5-7min), long (8-10min)")
    
    args = parser.parse_args()

    if args.command == "podcast":
        from src.podcast.run_podcast import generate_podcast
        categories = [c.strip() for c in args.categories.split(",")]
        generate_podcast(mode=args.mode, holiday=args.holiday, categories=categories)
    elif args.command == "horror":
        from src.horror.script_generator import generate_horror_script
        from src.horror.audio_generator import generate_horror_audio
        from src.horror.visual_generator import generate_horror_image
        from src.horror.video_producer import create_horror_video
        from src.shared.script_to_subtitles import script_to_subtitles
        import asyncio
        
        # Output directories
        script_dir = "outputs/horror_scripts"
        temp_dir = "outputs/horror_temp"
        episode_dir = "outputs/horror_episodes"
        os.makedirs(script_dir, exist_ok=True)
        os.makedirs(temp_dir, exist_ok=True)
        os.makedirs(episode_dir, exist_ok=True)
        
        # Generate script with duration parameter
        print(f"[INFO] Generating horror script (duration: {args.duration})...")
        script = generate_horror_script(args.prompt, duration=args.duration)
        
        if not script:
            print("[ERROR] Failed to generate script")
            return
        
        # Save script
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        script_file = os.path.join(script_dir, f"horror_{timestamp}.json")
        with open(script_file, "w") as f:
            json.dump(script, f, indent=2)
        print(f"[SUCCESS] Script saved: {script_file}")
        
        # Generate subtitles automatically
        subtitle_file = script_to_subtitles(script_file)
        
        # Generate audio
        audio_file = os.path.join(temp_dir, f"narration_{timestamp}.mp3")
        print("[INFO] Generating audio...")
        asyncio.run(generate_horror_audio(script["story"], audio_file))
        
        # Generate visual
        image_file = os.path.join(temp_dir, f"visual_{timestamp}.png")
        print("[INFO] Generating visual...")
        generate_horror_image(script["visual_prompt"], image_file)
        
        # Create video
        video_file = os.path.join(episode_dir, f"{script['title'].replace(' ', '_')}_{timestamp}.mp4")
        print("[INFO] Creating video...")
        create_horror_video(audio_file, image_file, video_file)
        
        print(f"\n[SUCCESS] Horror episode complete!")
        print(f"  Video: {video_file}")
        print(f"  Script: {script_file}")
        print(f"  Subtitles: {subtitle_file}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
