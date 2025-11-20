"""
Module for generating audio from text using EdgeTTS.
"""
import asyncio
import os
from typing import List, Dict
import edge_tts

# Voice Configuration
VOICES = {
    "Zeta": "en-US-AriaNeural",  # Energetic Female
    "Quill": "en-US-GuyNeural"   # Calm/Sarcastic Male
}

async def generate_audio_for_line(text: str, speaker: str, index: int, output_dir: str) -> str:
    """
    Generate audio for a single line of dialogue.
    """
    voice = VOICES.get(speaker, "en-US-AriaNeural") # Default to Zeta
    output_file = os.path.join(output_dir, f"{index:03d}_{speaker}.mp3")
    
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    return output_file

async def generate_audio_files(script: List[Dict[str, str]], output_dir: str = "temp_audio") -> List[str]:
    """
    Generate audio files for the entire script.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print(f"🔊 Generating audio for {len(script)} lines...")
    audio_files = []
    
    tasks = []
    for i, line in enumerate(script):
        speaker = line.get("speaker")
        text = line.get("text")
        if speaker and text:
            tasks.append(generate_audio_for_line(text, speaker, i, output_dir))
            
    # Run concurrently
    audio_files = await asyncio.gather(*tasks)
    
    # Sort to ensure correct order based on index
    audio_files.sort()
    
    print(f"✅ Generated {len(audio_files)} audio clips.")
    return list(audio_files)

def combine_audio_files(audio_files: List[str], output_file: str) -> str:
    """
    Combine multiple audio files into a single file using ffmpeg.
    """
    if not audio_files:
        print("❌ No audio files to combine.")
        return ""

    # Create a temporary file list for ffmpeg
    list_file_path = "file_list.txt"
    with open(list_file_path, "w", encoding="utf-8") as f:
        for audio_file in audio_files:
            # ffmpeg requires absolute paths or relative paths. 
            # We'll use absolute paths to be safe and escape backslashes.
            abs_path = os.path.abspath(audio_file).replace("\\", "/")
            f.write(f"file '{abs_path}'\n")

    print(f"🔗 Combining {len(audio_files)} files into {output_file}...")
    
    try:
        # Run ffmpeg command
        # -f concat: use concat demuxer
        # -safe 0: allow unsafe file paths (needed for absolute paths)
        # -i list_file_path: input file list
        # -c copy: copy stream without re-encoding (fast)
        # -y: overwrite output file
        command = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", list_file_path,
            "-c", "copy",
            "-y",
            output_file
        ]
        
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"✅ Podcast generated successfully: {output_file}")
        
        # Clean up list file
        os.remove(list_file_path)
        return output_file
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running ffmpeg: {e}")
        return ""
    except FileNotFoundError:
        print("❌ ffmpeg not found. Please ensure ffmpeg is installed and in your PATH.")
        return ""

if __name__ == "__main__":
    # Test stub
    import subprocess # Import here for the test stub if needed, but it's better at top level
    
    async def main():
        test_script = [
            {"speaker": "Zeta", "text": "Hello world! This is Zeta."},
            {"speaker": "Quill", "text": "And this is Quill. Thrilled to be here."}
        ]
        files = await generate_audio_files(test_script)
        if files:
            combine_audio_files(files, "test_podcast.mp3")

    asyncio.run(main())
