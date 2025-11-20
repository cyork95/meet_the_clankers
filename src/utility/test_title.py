import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from script_generator import generate_script
from dotenv import load_dotenv

load_dotenv()

news = {
    "tech": [
        {"title": "New AI Model Released", "summary": "Google released Gemini 2.5", "source": "TechCrunch"}
    ]
}

print("Testing generate_script with title generation...")
try:
    result = generate_script(news)
    if result and result[0]:
        script, title = result
        print(f"✅ Script generated successfully!")
        print(f"📌 Title: {title}")
        print(f"📝 Script has {len(script)} lines")
    else:
        print("❌ Script generation returned empty result.")
except Exception as e:
    print(f"❌ Script generation failed with error: {e}")
    import traceback
    traceback.print_exc()
