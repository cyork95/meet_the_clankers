"""
Module for generating horror narration using Google Cloud Text-to-Speech.
"""
import asyncio
import os
from google.cloud import texttospeech
from dotenv import load_dotenv
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.shared.utils import clean_text_for_tts

# Load environment variables
load_dotenv()

async def generate_horror_audio(text: str, output_file: str) -> str:
    """
    Generate audio for the horror story using Google Cloud TTS.
    
    Args:
        text: The story text.
        output_file: Path to save the audio file.
        
    Returns:
        Path to the generated audio file.
    """
    print("[INFO] Generating horror audio with Google Cloud TTS...")
    
    try:
        def run_google_tts():
            client = texttospeech.TextToSpeechClient()
            
            # Set up the synthesis input
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            # Configure voice parameters
            # Using a deep male voice (Studio-M or Journey-D if available, falling back to Wavenet-D)
            # "en-US-Studio-M" is a very high quality male voice.
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US",
                name="en-US-Studio-M" 
            )
            
            # Configure audio settings for horror effect
            # Pitch -5.0 for deep voice, Rate 0.85 for slow suspense
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                pitch=-5.0,
                speaking_rate=0.85,
                effects_profile_id=["headphone-class-device"]
            )
            
            # Perform the text-to-speech request
            response = client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Write the response to the output file
            with open(output_file, "wb") as out:
                out.write(response.audio_content)
                
        await asyncio.to_thread(run_google_tts)
        print(f"[SUCCESS] Audio saved to {output_file}")
        return output_file
        
    except Exception as e:
        print(f"[ERROR] Google Cloud TTS failed: {e}")
        return ""

if __name__ == "__main__":
    # Test
    text = "I realized too late... the footsteps were coming from inside the attic."
    asyncio.run(generate_horror_audio(text, "outputs/test_horror_google.mp3"))
