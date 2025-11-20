import asyncio
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from audio_generator import generate_audio_files

async def main():
    print("Testing Google Cloud TTS audio generation...")
    script = [
        {"speaker": "Zeta", "text": "Hey listeners! Welcome to Meet the Clankers. I'm Zeta, your favorite AI optimist!"},
        {"speaker": "Quill", "text": "And I'm Quill. Here to keep things grounded while Zeta gets overly excited about every new gadget."}
    ]
    try:
        files = await generate_audio_files(script, "test_google_tts")
        if files:
            print(f"✅ Generated {len(files)} files with Google Cloud TTS.")
            for f in files:
                print(f" - {f}")
        else:
            print("❌ No files generated.")
    except Exception as e:
        print(f"❌ Error generating audio: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
