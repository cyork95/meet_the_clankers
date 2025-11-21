"""
Module for assembling audio clips into a final podcast using FFmpeg directly.
This avoids pydub/audioop dependencies while maintaining high quality (silence insertion).
"""
import subprocess
import os
from typing import List

def generate_silence_clip(duration_sec: float, output_file: str = "silence.mp3"):
    """Generate a silence clip using FFmpeg."""
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", "anullsrc=r=24000:cl=mono",
        "-t", str(duration_sec),
        "-q:a", "9",
        output_file
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def assemble_podcast(audio_files: List[str], output_file: str = "meet_the_clankers_episode.mp3"):
    """
    Stitch together audio files into a single podcast episode using FFmpeg concat demuxer.
    """
    print(f"[INFO] Assembling podcast from {len(audio_files)} clips...")
    
    # Create a temporary file list for FFmpeg
    list_file = "concat_list.txt"
    silence_file = "temp_silence.mp3"
    
    try:
        # Generate 0.5s silence
        generate_silence_clip(0.5, silence_file)
        
        with open(list_file, "w", encoding="utf-8") as f:
            for file_path in audio_files:
                # FFmpeg requires forward slashes and escaped paths
                safe_path = file_path.replace("\\", "/")
                f.write(f"file '{safe_path}'\n")
                f.write(f"file '{silence_file}'\n")
        
        # Run FFmpeg concat
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", list_file,
            "-c", "copy",
            output_file
        ]
        
        print("[INFO] Running FFmpeg...")
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print("[SUCCESS] Podcast saved successfully!")
        return output_file
        
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] FFmpeg failed: {e}")
        print("👉 Ensure FFmpeg is installed and in your PATH.")
        return None
    except Exception as e:
        print(f"[ERROR] Error assembling podcast: {e}")
        return None
    finally:
        # Cleanup
        if os.path.exists(list_file):
            os.remove(list_file)
        if os.path.exists(silence_file):
            os.remove(silence_file)

if __name__ == "__main__":
    pass
