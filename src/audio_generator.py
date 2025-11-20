"""
Module for generating audio from text using Google Cloud Text-to-Speech.
"""
import asyncio
import os
import subprocess
from typing import List, Dict
from google.cloud import texttospeech

# Voice Configuration - Using Google Cloud WaveNet voices
VOICES = {
    "Zeta": {
        "language_code": "en-US",
        "name": "en-US-Neural2-F",  # High-quality female voice
        "pitch": 2.0,  # Slightly higher pitch for energetic feel
        "speaking_rate": 1.1  # Slightly faster for enthusiasm
    },
    "Quill": {
        "language_code": "en-US",
        "name": "en-US-Neural2-D",  # High-quality male voice
        "pitch": -2.0,  # Slightly lower pitch for gravitas
        "speaking_rate": 0.95  # Slightly slower for measured delivery
    }
}

async def generate_audio_for_line(text: str, speaker: str, index: int, output_dir: str) -> str:
    """
    Generate audio for a single line of dialogue using Google Cloud TTS.
    Falls back to gTTS if Google Cloud TTS fails.
    """
    output_file = os.path.join(output_dir, f"{index:03d}_{speaker}.mp3")
    
    # Try Google Cloud TTS first
    try:
        def run_google_tts():
            client = texttospeech.TextToSpeechClient()
            
            # Get voice config for speaker
            voice_config = VOICES.get(speaker, VOICES["Zeta"])
            
            # Set up the synthesis input
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            # Configure voice parameters
            voice = texttospeech.VoiceSelectionParams(
                language_code=voice_config["language_code"],
                name=voice_config["name"]
            )
            
            # Configure audio settings
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                pitch=voice_config["pitch"],
                speaking_rate=voice_config["speaking_rate"]
            )
            
            # Perform the text-to-speech request
            response = client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            # Write the response to the output file
            with open(output_file, "wb") as out:
                out.write(response.audio_content)
        
        await asyncio.to_thread(run_google_tts)
        
    except Exception as e:
        print(f"⚠️ Google Cloud TTS failed for line {index}: {e}. Falling back to gTTS.")
        try:
            from gtts import gTTS
            # Run gTTS in a separate thread to avoid blocking the event loop
            def run_gtts():
                tts = gTTS(text=text, lang='en')
                tts.save(output_file)
            
            await asyncio.to_thread(run_gtts)
        except Exception as gtts_e:
            print(f"❌ gTTS also failed: {gtts_e}")
            return ""

    return output_file

async def generate_audio_files(script: List[Dict[str, str]], output_dir: str = "outputs/temp_audio") -> List[str]:
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
