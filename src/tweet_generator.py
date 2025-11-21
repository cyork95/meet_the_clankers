"""
Module for generating social media tweets using Google Gemini API.
"""
import os
import json
import google.generativeai as genai
from typing import List, Dict, Optional

def generate_tweets(script_content: List[Dict[str, str]], episode_title: str, model_name: str = 'gemini-2.5-flash') -> List[str]:
    """
    Generate engaging tweets based on the podcast script content.
    
    Args:
        script_content: List of dicts containing speaker and text
        episode_title: The title of the episode
        model_name: The Gemini model to use
        
    Returns:
        List of generated tweets
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found. Please set it in .env")
        return []
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    
    # Prepare context from script (first 2000 chars to save tokens but get gist)
    # Or better, combine all text until we hit a reasonable length limit
    full_text = " ".join([f"{item['speaker']}: {item['text']}" for item in script_content])
    # Truncate if too long (approx 10k chars should be enough context)
    context = full_text[:15000]
    
    spotify_link = "https://open.spotify.com/show/0UelBMU4glDpp91tUpgzOG"
    
    prompt = f"""
    You are the social media manager for the "Meet the Clankers" AI podcast.
    
    **Podcast Hosts:**
    - **Zeta**: Enthusiastic, tech-optimist AI.
    - **Quill**: Sarcastic, cynical, realist AI.
    
    **Task:**
    Generate 3 different tweets to promote the latest episode titled "{episode_title}".
    
    **Tweet Styles:**
    1. **The Hook**: A catchy summary of the most interesting topic discussed.
    2. **The Quote**: A funny or insightful exchange between Zeta and Quill (paraphrased if needed).
    3. **The Quill Special**: A sarcastic, dry take on the news from Quill's perspective.
    
    **Requirements:**
    - MUST include the link: {spotify_link}
    - MUST be under 280 characters.
    - Use relevant hashtags like #AI #TechNews #Podcast #MeetTheClankers.
    - Be engaging and sound like a human (or a very clever AI) wrote it.
    - Do NOT include "Tweet 1:", "Tweet 2:" labels in the output. Just separate them with "---".
    
    **Episode Context:**
    {context}
    """
    
    try:
        print("[INFO] Generating tweets with Gemini...")
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Split by separator
        tweets = [t.strip() for t in text.split("---") if t.strip()]
        
        return tweets
        
    except Exception as e:
        print(f"[ERROR] Error generating tweets: {e}")
        return []

if __name__ == "__main__":
    # Test stub
    pass
