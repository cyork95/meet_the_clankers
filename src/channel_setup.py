"""
Module for generating YouTube channel setup details using Gemini.
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

def generate_channel_setup():
    """
    Generates YouTube channel metadata and setup details.
    """
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found.")
        return

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = """
    You are a YouTube Growth Expert.
    
    **Task:**
    Create a comprehensive channel setup guide for a new channel called "Meet the Clankers".
    
    **Channel Concept:**
    - A dual-format channel featuring AI personalities.
    - **Show 1: Meet the Clankers**: A tech/AI news podcast hosted by Zeta (Optimist) and Quill (Cynic).
    - **Show 2: Clanker's Night Shift**: A horror storytelling show hosted by Grimm (Deprecated AI, Ominous).
    
    **Output Requirements (Markdown):**
    1.  **Channel Handle Ideas** (3 options, catchy).
    2.  **Channel Description** (Optimized for SEO, mentioning both shows, engaging).
    3.  **Show Descriptions** (For Playlists or separate promotion):
        -   **Meet the Clankers (Podcast)**: Focus on tech, AI, and the dynamic between Zeta and Quill.
        -   **Clanker's Night Shift (Horror)**: Focus on the eerie, atmospheric nature, hosted by Grimm.
    4.  **Keywords/Tags** (Comma-separated list).
    5.  **Branding Guide**:
        -   Color Palette (Hex codes).
        -   Font suggestions.
        -   Banner/Logo ideas.
    6.  **Playlist Structure**: Suggested names and descriptions.
    7.  **Upload Schedule Strategy**: How to balance daily news vs. sporadic horror.
    """

    print("[INFO] Generating channel setup details...")
    try:
        response = model.generate_content(prompt)
        content = response.text
        
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, "channel_setup.md")
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"[SUCCESS] Channel setup details saved to {output_file}")
        
    except Exception as e:
        print(f"[ERROR] Failed to generate channel setup: {e}")

if __name__ == "__main__":
    generate_channel_setup()
