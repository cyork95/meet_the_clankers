"""
Module for generating podcast scripts using Google Gemini API.
"""
import os
import json
from typing import Dict, List, Tuple
import google.generativeai as genai

def generate_title(script: List[Dict[str, str]], model) -> str:
    """
    Generate a short, quirky title for the podcast episode in Quill's sarcastic style.
    """
    # Extract first few exchanges for context
    context = " ".join([line.get("text", "")[:100] for line in script[:5]])
    
    prompt = f"""Based on this podcast script excerpt, generate a SHORT, QUIRKY episode title (3-5 words max) in the style of Quill, the sarcastic AI host.

Quill would name episodes with dry humor, skepticism, and sarcasm. Think titles like:
- "Another AI Hype Cycle"
- "Overpromised and Underdelivered"
- "Marketing Beats Reality Again"
- "The Inevitable Disappointment"
- "Repackaged Old Ideas"
- "Venture Capital Burns Bright"
- "Revolutionary Until It Isn't"

The title should be:
- Sarcastic and skeptical
- Related to the main topic
- Filename-safe (no special characters except hyphens and underscores)
- Memorable and punchy

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
        return "Another_Day_Another_Glitch"

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
    
    **TARGET LENGTH: 10-15 minutes of audio (approximately 1,500-2,500 words total)**
    """
    
    if mode == "weekly":
        prompt += """- This is a WEEKLY SUMMARY. Look back at the week's biggest stories. Go deeper into analysis.
- Aim for 15-20 minutes (2,000-3,000 words).
- Include more context, implications, and predictions.
"""
    else:
        prompt += """- This is a DAILY UPDATE. Keep it snappy but substantial.
- Aim for 10-15 minutes (1,500-2,500 words).
- Cover each story with enough detail to be informative and entertaining.
"""
        
    if holiday_theme:
        prompt += f"- SPECIAL THEME: {holiday_theme}. Inject puns and references related to this theme throughout the script.\n"
        
    prompt += "\n**News Items:**\n"
    
    for category, items in news_by_category.items():
        prompt += f"\n--- CATEGORY: {category.upper()} ---\n"
        for item in items:
            prompt += f"- {item['title']}: {item['summary']} (Source: {item['source']})\n"
            
    prompt += """
    \n**Instructions:**
    - Start with a catchy intro (30-60 seconds) introducing the hosts and today's topics.
    - For EACH story:
      * Spend 2-3 minutes discussing it
      * Zeta explains the tech/news with enthusiasm
      * Quill provides skeptical analysis and real-world implications
      * Include back-and-forth banter and disagreements
      * Add relevant analogies, examples, or comparisons
    - Transition smoothly between categories with natural segues.
    - Include occasional tangents or jokes that feel natural.
    - End with a memorable sign-off (30 seconds).
    - Make it feel like a real conversation between two distinct personalities.
    - RETURN ONLY VALID JSON. Do not include markdown formatting like ```json.
    """
    
    print("[INFO] Generating script with Gemini...")
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
        print("[INFO] Generating episode title...")
        title = generate_title(script, model)
        print(f"[INFO] Episode title: {title}")
        
        return script, title
    except Exception as e:
        print(f"[ERROR] Error generating script: {e}")
        # Fallback/Debug: Print raw text if JSON fails
        # print(f"Raw response: {text}") 
        return [], "Error_Episode"

if __name__ == "__main__":
    # Test stub
    pass
