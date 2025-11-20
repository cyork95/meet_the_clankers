"""
Module for generating podcast scripts using Google Gemini API.
"""
import os
import json
from typing import Dict, List, Tuple
import google.generativeai as genai

def generate_title(script: List[Dict[str, str]], model) -> str:
    """
    Generate a short, catchy title for the podcast episode based on the script.
    """
    # Extract first few exchanges for context
    context = " ".join([line.get("text", "")[:100] for line in script[:5]])
    
    prompt = f"""Based on this podcast script excerpt, generate a SHORT, CATCHY title (3-5 words max) for this episode.
    The title should be filename-safe (no special characters except hyphens and underscores).
    Return ONLY the title, nothing else.
    
    Script excerpt: {context}
    """
    
    try:
        response = model.generate_content(prompt)
        title = response.text.strip()
        # Clean up title for filename safety
        title = title.replace('"', '').replace("'", "").replace(':', '').replace('/', '-')
        title = title.replace('\\', '-').replace('|', '-').replace('?', '').replace('*', '')
        title = title.replace('<', '').replace('>', '').replace('.', '')
        title = '_'.join(title.split())  # Replace spaces with underscores
        return title[:50]  # Limit length
    except Exception as e:
        print(f"⚠️ Title generation failed: {e}. Using default.")
        return "Daily_Tech_Roundup"

def generate_script(news_by_category: Dict[str, List[Dict]], mode: str = "daily", holiday_theme: str = None) -> Tuple[List[Dict[str, str]], str]:
    """
    Generate a podcast script using Gemini based on the provided news.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found. Please set it in .env")
        return [], "Error_No_API_Key"
    
    genai.configure(api_key=api_key)
    # Using gemini-2.5-flash for speed and cost efficiency
    model = genai.GenerativeModel('gemini-2.5-flash')

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
    - The podcast is named "Meet the Clankers" because the HOSTS (Zeta and Quill) are the "Clankers".
    - Do NOT refer to the audience as "Clankers". Refer to them as "listeners", "humans", "folks", or "meatbags" (if Quill is speaking).
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
        
        # Generate title
        print("🎯 Generating episode title...")
        title = generate_title(script, model)
        print(f"📌 Episode title: {title}")
        
        return script, title
    except Exception as e:
        print(f"❌ Error generating script: {e}")
        # Fallback/Debug: Print raw text if JSON fails
        # print(f"Raw response: {text}") 
        return [], "Error_Episode"

if __name__ == "__main__":
    # Test stub
    pass
