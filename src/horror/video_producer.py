"""
Module for assembling the horror video using MoviePy.
"""
from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip
import os

def create_horror_video(audio_file: str, image_file: str, output_file: str) -> str:
    """
    Create a video with the audio and image, applying a Ken Burns zoom effect.
    
    Args:
        audio_file: Path to the audio file.
        image_file: Path to the image file.
        output_file: Path to save the video file.
        
    Returns:
        Path to the generated video file.
    """
    print(f"[INFO] Assembling video from {audio_file} and {image_file}...")
    
    try:
        # 1. Load the audio
        audio = AudioFileClip(audio_file)
        
        # 2. Load the image and set it to the duration of the audio
        # Resize width to 1920 (1080p) to ensure quality
        clip = ImageClip(image_file).set_duration(audio.duration).resize(width=1920)
        
        # 3. Add a "Ken Burns" zoom effect
        # This effectively zooms in by 4% over the duration of the clip
        # lambda t: 1 + 0.04 * t  -> starts at scale 1, ends at 1 + 0.04 * duration
        # We need to normalize t by duration if we want a fixed percentage, 
        # but t grows from 0 to duration. 
        # Let's zoom in 10% over the whole clip.
        zoom_factor = 0.1
        clip = clip.resize(lambda t: 1 + (zoom_factor * t / audio.duration)) 
        
        # 4. Center the clip (important if resizing) and add audio
        clip = clip.set_position(('center', 'center')).set_audio(audio)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # 5. Export
        # fps=24 is standard for filmic look
        clip.write_videofile(output_file, fps=24, codec="libx264", audio_codec="aac")
        
        print(f"[SUCCESS] Video saved to {output_file}")
        return output_file
        
    except Exception as e:
        print(f"[ERROR] Error creating video: {e}")
        return ""

if __name__ == "__main__":
    # Test stub
    pass
