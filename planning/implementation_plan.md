# Meet the Clankers - Implementation Plan

## Goal Description
Create an automated podcast generator called "Meet the Clankers" featuring two AI hosts, Zeta (Energetic Tech Enthusiast) and Quill (Sarcastic Pragmatist). The system will fetch daily tech news, generate a scripted conversation between the hosts, convert the text to speech using distinct voices, and assemble the final audio file.

## User Review Required
> [!IMPORTANT]
> **LLM API Key**: The system requires an LLM (Large Language Model) to generate the script. I will implement it using Google's Gemini API. You will need a `GEMINI_API_KEY`.
> **TTS Provider**: I plan to use `edge-tts` (Microsoft Edge's online TTS) as it provides high-quality neural voices for free without an API key.
> **News Source**: I will use RSS feeds from major tech blogs (e.g., TechCrunch, The Verge) to fetch news without requiring a paid news API.

## Cost Analysis
This project is designed to be **extremely low cost or free** to run daily.
- **News Fetching**: **$0**. RSS feeds are free.
- **Script Generation (Gemini)**: **$0**. Google's Gemini API (via Google AI Studio) offers a generous **Free Tier** (currently 15 RPM, 1M TPM) which is more than enough for a daily podcast generation. *Note: Your Gemini Advanced subscription is for the chat interface, but the API has its own free tier.*
- **Audio (EdgeTTS)**: **$0**. Uses the free Microsoft Edge online text-to-speech service.
- **Compute**: **$0**. Runs locally on your machine.

## Proposed Changes

### Project Structure
I will create a modular Python project:
- `main.py`: Entry point.
- `news_fetcher.py`: Handles fetching and filtering news.
- `script_generator.py`: Handles LLM interaction to write the script.
- `audio_generator.py`: Handles TTS conversion.
- `podcast_producer.py`: Stitches audio together.

### Dependencies
- `google-generativeai`: For script generation.
- `feedparser`: For fetching RSS news feeds.
- `edge-tts`: For text-to-speech.
- `pydub`: For audio manipulation (stitching).
- `python-dotenv`: For managing environment variables.

### Component Details

#### [NEW] [main.py](file:///c:/Users/codyd/OneDrive/Documents/GitHub Projects/meet_the_clankers/main.py)
- Entry point.
- Accepts CLI arguments: `--mode` (daily, weekly), `--holiday` (optional), and `--categories` (list, e.g., "tech,politics,weather").
- Logic:
    - **Daily**: Fetches last 24h news for specified categories.
    - **Weekly**: Fetches last 7 days news, selects top stories per category.
    - **Holiday**: Injects holiday theme.

#### [NEW] [news_fetcher.py](file:///c:/Users/codyd/OneDrive/Documents/GitHub Projects/meet_the_clankers/news_fetcher.py)
- Function `fetch_news(time_window="24h", categories=["tech"])`:
    - Uses a dictionary of RSS feeds mapped to categories.
    - **Default Sources** (Focused on factual/unbiased reporting):
        - **AI (The Clankers' Fav)**: TechCrunch AI, Wired AI, The Verge AI.
        - **Tech**: TechCrunch, The Verge, Ars Technica.
        - **Politics/World**: Reuters (Top News), AP News (Top News), BBC World.
        - **Business/Finance**: CNBC, Bloomberg (Technology), WSJ (Tech).
        - **Entertainment/Gaming**: Polygon (Gaming), Variety (Film/TV), IGN.
        - **Science/Health**: ScienceDaily, Reuters Health, Nature.
    - Fetches and filters news for each requested category.
    - Returns a structured dictionary: `{"tech": [items], "politics": [items]}`.

#### [NEW] [script_generator.py](file:///c:/Users/codyd/OneDrive/Documents/GitHub Projects/meet_the_clankers/script_generator.py)
- Function `generate_script(news_by_category, mode="daily", holiday_theme=None)`:
    - **Structure**: Generates a script with distinct segments.
    - **Transitions**: Instructs the LLM to write smooth transitions between topics (e.g., Zeta shifting from a cool gadget to the weather forecast).
    - **Prompts**: Adjusted to handle multiple topics in one flow.
    - Uses `google.generativeai` to generate the script.
    - Request a JSON or structured output separating lines by speaker.

#### [NEW] [audio_generator.py](file:///c:/Users/codyd/OneDrive/Documents/GitHub Projects/meet_the_clankers/audio_generator.py)
- Function `generate_audio(script)`:
    - Iterates through the script.
    - **Zeta (Energetic)**: Uses `en-US-AriaNeural` (Bright, clear female voice).
    - **Quill (Pragmatic)**: Uses `en-US-GuyNeural` (Calm, deep male voice).
    - Calls `edge-tts` to generate audio for each line.
    - Saves temporary audio clips.

#### [NEW] [podcast_producer.py](file:///c:/Users/codyd/OneDrive/Documents/GitHub Projects/meet_the_clankers/podcast_producer.py)
- Function `assemble_podcast(audio_files)`:
    - Uses `pydub` to concatenate clips with a slight pause between them.
    - Exports final MP3.

## Verification Plan

### Automated Tests
- I will run the script generation with dummy data to verify prompt effectiveness.
- I will generate a short sample audio to verify TTS and stitching.

### Manual Verification
- Listen to the generated "Meet the Clankers" episode to ensure the personalities (Energetic vs. Sarcastic) shine through and the audio quality is good.
