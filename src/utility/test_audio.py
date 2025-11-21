import asyncio
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.audio_generator import generate_audio_files
import edge_tts
print(f"EdgeTTS Version: {edge_tts.__version__}")

async def main():
    print("Testing audio generation...")
    script = [
        {"speaker": "Zeta", "text": "Testing audio generation. One two three."},
        {"speaker": "Quill", "text": "This is a test. Do not panic."}
    ]
    try:
        files = await generate_audio_files(script, "test_audio_output")
        if files:
            print(f"✅ Generated {len(files)} files.")
            for f in files:
                print(f" - {f}")
        else:
            print("❌ No files generated.")
    except Exception as e:
        print(f"❌ Error generating audio: {e}")

if __name__ == "__main__":
    asyncio.run(main())
