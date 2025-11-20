import sys
import os
# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from script_generator import generate_script
from dotenv import load_dotenv

load_dotenv()

news = {
    "tech": [
        {"title": "New AI Model Released", "summary": "Google released Gemini 2.5", "source": "TechCrunch"}
    ]
}

print("Testing generate_script with gemini-2.5-flash...")
try:
    script = generate_script(news)
    if script:
        print("✅ Script generated successfully!")
        print(script)
    else:
        print("❌ Script generation returned empty list.")
except Exception as e:
    print(f"❌ Script generation failed with error: {e}")
