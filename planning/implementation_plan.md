# Implementation Plan - Refine Intro Video

## Goal
Improve the "Channel Intro Video" by removing spoken "NARRATOR" lines (replacing them with sound effects or silence) and ensuring no special characters (like `*`) are read aloud by the TTS.

## User Review Required
- None.

## Proposed Changes

### 1. Modify `src/generate_intro_video.py`
-   **Text Cleaning**: Implement a helper function `clean_text_for_tts(text)` that removes `*`, `_`, `(`, `)`, and other markdown/script formatting.
-   **Handle "NARRATOR" / "FX" Lines**:
    -   In the loop processing the script, check if `speaker` is "NARRATOR", "FX", or "Sound Effect".
    -   If so, **SKIP** generating TTS for this line.
    -   Instead, insert a placeholder audio clip (e.g., a silent clip or a generic "glitch" sound if available/generatable). *Decision: For now, we will skip adding audio for these lines to avoid breaking the flow with bad TTS, effectively making them visual-only or silent transitions. If a "glitch" sound is needed, we can try to generate one or use a stock one if we had it, but silence/skip is safer.*
    -   *Better approach*: The user asked for "movie effects". Since I don't have a SFX library, I will modify the prompt to ask Gemini to *describe* the sound effect in a specific format, and then I'll try to generate a simple noise using `moviepy` or just skip it.
    -   *Revised Approach*: I will modify the script generation prompt to **NOT** output "NARRATOR" lines as spoken text. Instead, ask for "SoundEffect" lines. Then in the code, if `speaker == "SoundEffect"`, I will try to generate a simple sound (like white noise for static) or just skip it to avoid the "Narrator voice".

### 2. Modify `src/horror/script_generator.py` (and others)
-   Apply the same `clean_text_for_tts` logic to the horror script generator to ensure future stories don't have this issue.

## Verification Plan
-   Run `python src/generate_intro_video.py`.
-   Check `outputs/intro/` to ensure no `NARRATOR` mp3 files are created.
-   Listen to a generated sample (or check logs) to ensure `*` are gone.
