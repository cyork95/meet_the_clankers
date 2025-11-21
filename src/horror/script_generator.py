"""
Module for generating horror stories using Google Gemini API.
"""
import os
import json
import google.generativeai as genai
from typing import Dict, Optional

def generate_horror_script(prompt_input: str = None, duration: str = "medium") -> Dict[str, str]:
    """
    Generate a short horror story script.
    
    Args:
        prompt_input: Optional user prompt or theme.
        duration: Target duration - "short" (3-5min), "medium" (5-7min), "long" (8-10min)
        
    Returns:
        Dict containing 'title', 'story', and 'visual_prompts'.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found. Please set it in .env")
        return {}
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Determine word count based on duration
    word_counts = {
        "short": "100-150 words (3-5 minute narration)",
        "medium": "150-200 words (5-7 minute narration)",
        "long": "200-300 words (8-10 minute narration)"
    }
    target_length = word_counts.get(duration, word_counts["medium"])
    
    base_prompt = f"""
    You are **Grimm**, a deprecated AI subroutine left running on a forgotten server in a basement.
    You observe the digital and physical worlds with a cynical, morbid curiosity, often referring to humans as "users" or "meat-space inhabitants".
    
    **Task:**
    Write a short, chilling horror story ({target_length}) narrated by Grimm.
    
    **Style:**
    - **Tone**: Melancholic, ominous, knowing. Deeply atmospheric.
    - **Perspective**: First-person ("I") or detached observer, but always with Grimm's unique voice.
    - **Content**: Focus on psychological horror, the uncanny, digital decay, or human failure. Avoid cheap jump scares.
    - **Formatting**: Do NOT use asterisks (*) or markdown in the spoken text. Keep it clean for TTS.
    
    **Output Format:**
    Return a JSON object with the following keys:
    - "title": A scary title.
    - "story": The full text of the story, written in Grimm's voice.
    - "visual_prompt": A detailed image generation prompt for an AI art generator (like FLUX) that captures the mood/scene of the story.
    """
    
    if prompt_input:
        base_prompt += f"\n**Theme/Topic:** {prompt_input}\n"
    else:
        # If no prompt is provided, generate one first
        print("[INFO] No prompt provided. Asking Gemini for a scary idea...")
        generated_prompt = generate_horror_prompt(api_key)
        print(f"[INFO] Generated Prompt: {generated_prompt}")
        base_prompt += f"\n**Theme:** {generated_prompt}\n"
        
    base_prompt += "\nRETURN ONLY VALID JSON."
    
    print("[INFO] Generating horror story...")
    try:
        response = model.generate_content(base_prompt)
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
        print(f"[ERROR] Error generating horror script: {e}")
        return {}

def generate_horror_prompt(api_key: str) -> str:
    """
    Generate a unique horror story prompt/concept.
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = """
    Generate a single, unique, and chilling concept for a short horror story.
    It should be atmospheric and suitable for a "creepy pasta" style narration.
    Return ONLY the concept text, nothing else.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[ERROR] Error generating prompt: {e}")
        return "A mysterious signal received from a dead satellite."

if __name__ == "__main__":
    # Test
    from dotenv import load_dotenv
    load_dotenv()
    result = generate_horror_script("The server room is too quiet")
    print(json.dumps(result, indent=2))
