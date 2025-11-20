"""
Module for generating podcast scripts using Google Gemini API.
"""
import os
import json
from typing import Dict, List
import google.generativeai as genai

def generate_script(news_by_category: Dict[str, List[Dict]], mode: str = "daily", holiday_theme: str = None) -> List[Dict[str, str]]:
    """
    Generate a podcast script using Gemini based on the provided news.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found. Please set it in .env")
        return []
    
    genai.configure(api_key=api_key)
    # Using gemini-1.5-flash for speed and cost efficiency if available, falling back to gemini-pro
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Construct the prompt
    prompt = """
    You are the scriptwriter for a tech podcast called "Meet the Clankers".
    
    **Hosts:**
    1. **Zeta**: Female AI. Energetic, optimistic, loves new tech, uses slang like "neural nets", "downloading", "glitch". She is the hype woman.
    2. **Quill**: Male AI. Sarcastic, pragmatic, cynical, focuses on utility and "what works", hates hype. He is the grounded realist.
    
    **Format:**
    - The output must be a JSON array of objects.
    - Each object must have "speaker" ("Zeta" or "Quill") and "text" (the dialogue).
    - Keep the conversation natural, banter-heavy, and fast-paced.
    - Use the provided news items to drive the conversation.
    - Smoothly transition between categories.
    
    **Context:**
    """
    
    if mode == "weekly":
        prompt += "- This is a WEEKLY SUMMARY. Look back at the week's biggest stories. Go deeper into analysis.\n"
    else:
        prompt += "- This is a DAILY UPDATE. Keep it snappy and fresh.\n"
        
    if holiday_theme:
        prompt += f"- SPECIAL THEME: {holiday_theme}. Inject puns and references related to this theme throughout the script.\n"
        
    prompt += "\n**News Items:**\n"
    
    for category, items in news_by_category.items():
        prompt += f"\n--- CATEGORY: {category.upper()} ---\n"
        for item in items:
            prompt += f"- {item['title']}: {item['summary']} (Source: {item['source']})\n"
            
    prompt += """
    \n**Instructions:**
    - Start with a catchy intro introducing the hosts and the vibe.
    - Discuss the top stories from each category.
    - Zeta gets excited, Quill brings it down to earth.
    - End with a sign-off.
    - RETURN ONLY VALID JSON. Do not include markdown formatting like ```json.
    """
    
    print("🤖 Generating script with Gemini...")
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Clean up response if it contains markdown code blocks
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        script = json.loads(text)
        return script
    except Exception as e:
        print(f"❌ Error generating script: {e}")
        # Fallback/Debug: Print raw text if JSON fails
        # print(f"Raw response: {text}") 
        return []

if __name__ == "__main__":
    # Test stub
    pass
