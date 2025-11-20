# Meet the Clankers - Walkthrough

I have successfully implemented the "Meet the Clankers" AI Podcast Generator. This system fetches daily news, generates a witty script between two AI hosts (Zeta and Quill), converts it to audio using distinct voices, and assembles a final podcast episode.

## Features Implemented
- **News Fetching**: Fetches latest headlines from RSS feeds (Tech, AI, Politics, etc.).
- **Script Generation**: Uses Google Gemini API to generate banter-heavy scripts.
- **Audio Generation**: Uses EdgeTTS for high-quality neural voices (Zeta=Female, Quill=Male).
- **Podcast Assembly**: Stitches clips together with silence using Pydub.
- **Modes**: Supports Daily (`--mode daily`) and Weekly (`--mode weekly`) episodes.
- **Quality Assurance**: Includes unit tests and linting.

## Verification Results

### Automated Tests
I ran the unit tests using `pytest` and they passed successfully.

```bash
$ python -m pytest
============================= test session starts =============================
collected 3 items

tests\test_news_fetcher.py ..                                            [ 66%]
tests\test_script_generator.py .                                         [100%]

============================= 3 passed in 27.65s ==============================
```

### Linting
I ran `pylint` to ensure code quality. The score has been improved by fixing import orders, docstrings, and unused variables.

### Manual Verification Steps
To generate a podcast, run the following command:

```bash
python main.py --mode daily --categories "ai,tech"
```

This will:
1. Fetch news for AI and Tech.
2. Generate a script (saved to `latest_script.json`).
3. Generate audio clips (in `temp_audio/`).
4. Export the final MP3 (e.g., `meet_the_clankers_daily_20251120.mp3`).

## Next Steps
- **Add Music**: Integrate intro/outro music mixing.
- **Deploy**: Set up a GitHub Action to run this daily and upload to a podcast host.
