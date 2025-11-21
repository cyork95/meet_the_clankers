"""
Shared utility functions for the project.
"""
import re
import numpy as np
from moviepy import AudioClip

def clean_text_for_tts(text: str) -> str:
    """
    Removes markdown formatting and special characters that shouldn't be read by TTS.
    
    Args:
        text: The input text with potential markdown.
        
    Returns:
        Cleaned text suitable for TTS.
    """
    # Remove bold/italic markers (* and _)
    text = re.sub(r'[\*_]', '', text)
    
    # Remove brackets and their content (often used for actions like [laughs])
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\(.*?\)', '', text)
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def generate_sound_effect(effect_type: str, output_path: str, duration_ms: int = 2000):
    """
    Generates a simple sound effect programmatically using moviepy.
    
    Args:
        effect_type: Type of effect ("glitch", "static", "silence")
        output_path: Path to save the MP3 file
        duration_ms: Duration in milliseconds
    """
    duration_sec = duration_ms / 1000.0
    
    if effect_type.lower() in ["glitch", "static"]:
        # Generate white noise using numpy
        def make_frame(t):
            # Generate random noise for stereo (2 channels)
            noise = np.random.normal(0, 0.1, (2,))  # Reduced amplitude for safety
            return noise
        
        audio_clip = AudioClip(make_frame, duration=duration_sec, fps=44100)
        audio_clip.write_audiofile(output_path, codec='libmp3lame')
    else:
        # Generate silence
        def make_frame(t):
            return np.array([0.0, 0.0])  # Stereo silence
        
        audio_clip = AudioClip(make_frame, duration=duration_sec, fps=44100)
        audio_clip.write_audiofile(output_path, codec='libmp3lame')
