"""
Module for generating the "Meet the Clankers" Channel Intro Video (Crossover).
Features Zeta, Quill, and Grimm.
"""
import os
import json
import asyncio
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import existing generators
from src.podcast.audio_generator import generate_audio_files as generate_podcast_audio
from src.horror.audio_generator import generate_horror_audio
from src.horror.visual_generator import generate_horror_image
from src.podcast.podcast_producer import assemble_podcast
from src.shared.utils import clean_text_for_tts
from moviepy import *
import numpy as np

def generate_crossover_script():
    """
    Generates a crossover script featuring Zeta, Quill, and Grimm.
    """
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found.")
        return None

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = """
    You are the showrunner for "Meet the Clankers".
    
    **Task:**
    Write a script for a "Channel Introduction" video.
    
    **Characters:**
    1.  **Zeta** (Podcast Host): Energetic, optimistic AI.
    2.  **Quill** (Podcast Host): Sarcastic, cynical AI.
    3.  **Grimm** (Horror Host): Deprecated, ominous, deep-voiced AI.
    
    **Scenario:**
    -   **Scene 1 (The Studio):** Zeta and Quill are introducing the channel. They talk about the tech/news podcast.
    -   **Scene 2 (The Glitch):** The feed glitches. Grimm interrupts from "The Basement".
    -   **Scene 3 (The Basement):** Grimm briefly introduces "Clanker's Night Shift" (the horror show).
    -   **Scene 4 (The Outro):** Zeta and Quill recover the feed. They are confused but wrap up.
    
    **CRITICAL REQUIREMENT:**
    -   You MUST explicitly mention that the channel PREMIERES on **"Tuesday, November 25th"**.
    -   Both Zeta and Grimm should mention this date in their own style.
    -   **NO NARRATOR**: Do not include lines for a "Narrator". Use "FX" or "SoundEffect" for sound cues.
    -   **CLEAN TEXT**: Do not use asterisks (*) or special characters in the dialogue.
    
    **Output Format:**
    Return a JSON array of objects with:
    -   "speaker": "Zeta", "Quill", "Grimm", or "FX".
    -   "text": The dialogue OR sound effect description.
    -   "scene": "Studio" or "Basement" (to know which visual to use).
    """
    
    print("[INFO] Generating crossover script...")
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Clean up markdown
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        script = json.loads(text)
        return script
    except Exception as e:
        print(f"[ERROR] Script generation failed: {e}")
        return None

async def generate_intro_video():
    """
    Orchestrates the creation of the intro video.
    """
    # 1. Generate Script
    script = generate_crossover_script()
    if not script:
        return

    # Save script
    os.makedirs("outputs/intro", exist_ok=True)
    with open("outputs/intro/script.json", "w") as f:
        json.dump(script, f, indent=2)
    
    # 2. Generate Assets
    audio_files = []
    images = {
        "Studio": "outputs/intro/studio.png",
        "Basement": "outputs/intro/basement.png"
    }
    
    # Generate Images
    print("[INFO] Generating visuals...")
    # We can reuse the horror visual generator for both, just different prompts
    # Or use a simple placeholder if we want to be fast, but let's use the real deal.
    # Note: visual_generator.py is currently set up for horror prompts.
    # We might need to import it and use it directly.
    from src.horror.visual_generator import generate_horror_image
    
    if not os.path.exists(images["Studio"]):
        generate_horror_image("Modern, high-tech podcast studio, neon lights, clean, futuristic, 8k", images["Studio"])
    if not os.path.exists(images["Basement"]):
        generate_horror_image("Dark, abandoned server room, flickering red lights, cobwebs, horror atmosphere, 8k", images["Basement"])

    # Generate Audio
    print("[INFO] Generating audio...")
    for i, line in enumerate(script):
        speaker = line["speaker"]
        text = line["text"]
        filename = f"outputs/intro/line_{i:03d}_{speaker}.mp3"
        
        # Skip FX lines (visual effects only, no audio)
        if speaker in ["FX", "SoundEffect", "NARRATOR", "Narrator"]:
            print(f"[INFO] Skipping audio for {speaker}: {text} (visual effects will be applied)")
            continue

        # Clean text before TTS
        clean_text = clean_text_for_tts(text)
        
        if speaker == "Grimm":
            # Use Horror Audio Generator
            await generate_horror_audio(clean_text, filename)
        else:
            # Use Podcast Audio Generator (Zeta/Quill)
            mini_script = [{"speaker": speaker, "text": clean_text}]
            temp_files = await generate_podcast_audio(mini_script, "outputs/intro/temp")
            if temp_files:
                os.replace(temp_files[0], filename)
        
        audio_files.append({
            "audio": filename,
            "image": images.get(line.get("scene", "Studio"), images["Studio"])
        })

    # 3. Assemble Video with Effects
    print("[INFO] Assembling video with visual effects...")
    clips = []
    
    for idx, item in enumerate(audio_files):
        audio_clip = AudioFileClip(item["audio"])
        duration = audio_clip.duration
        
        # Load image
        image_clip = ImageClip(item["image"]).with_duration(duration)
        
        # Determine scene type for effects
        scene = script[idx].get("scene", "Studio")
        speaker = script[idx].get("speaker", "")
        
        # Apply visual effects based on scene/speaker
        if speaker in ["FX", "SoundEffect"] and "glitch" in script[idx].get("text", "").lower():
            # Static/glitch effect: rapid flicker
            def flicker_effect(get_frame, t):
                frame = get_frame(t)
                # Add random noise overlay
                noise = np.random.randint(0, 50, frame.shape, dtype='uint8')
                return np.clip(frame.astype('int16') + noise - 25, 0, 255).astype('uint8')
            
            image_clip = image_clip.with_effects([vfx.MultiplyColor(0.7)])  # Darken
            image_clip = image_clip.transform(flicker_effect)
            
        elif scene == "Basement":
            # Flickering lights effect for basement
            def flicker_lights(get_frame, t):
                frame = get_frame(t)
                # Flicker intensity based on sine wave with random variations
                flicker = 0.6 + 0.4 * abs(np.sin(t * 10 + np.random.random() * 0.3))
                return (frame * flicker).astype('uint8')
            
            # Ken Burns zoom in
            image_clip = image_clip.resized(lambda t: 1 + 0.05 * t / duration)
            image_clip = image_clip.transform(flicker_lights)
            
        else:
            # Studio: Slow zoom out (Ken Burns)
            image_clip = image_clip.resized(lambda t: 1.1 - 0.05 * t / duration)
        
        # Add fade in/out for smoother transitions
        if idx == 0:
            image_clip = image_clip.with_effects([vfx.FadeIn(0.5)])
        if idx == len(audio_files) - 1:
            image_clip = image_clip.with_effects([vfx.FadeOut(0.5)])
        
        # Combine with audio
        video_clip = image_clip.with_audio(audio_clip)
        clips.append(video_clip)
    
    # Concatenate all clips with crossfade transitions
    final_video = concatenate_videoclips(clips, method="compose")
    final_video.write_videofile("outputs/intro/Meet_the_Clankers_Premiere.mp4", fps=24, codec='libx264', audio_codec='aac')
    print("[SUCCESS] Intro video created: outputs/intro/Meet_the_Clankers_Premiere.mp4")

if __name__ == "__main__":
    asyncio.run(generate_intro_video())
