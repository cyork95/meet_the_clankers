# Walkthrough - Clanker's Night Shift & Project Reorganization

I have successfully integrated the new "Horror Show" mode and reorganized the project structure to support multiple content types.

## 1. Project Reorganization

The `src/` directory has been restructured to separate the Podcast logic from the new Horror logic:

- **`src/podcast/`**: Contains all logic for "Meet the Clankers" news podcast (script, audio, tweets).
- **`src/horror/`**: Contains the new logic for "Clanker's Night Shift".
- **`src/shared/`**: Reserved for common utilities.
- **`src/main.py`**: The new unified entry point for the application.

## 2. Clanker's Night Shift (Horror Show)

The new horror mode generates a short, atmospheric horror story with narration, visuals, and video effects.

### Components
- **Script**: Uses Gemini to generate a chilling story based on a prompt.
- **Audio**: Uses **Google Cloud TTS** (`en-US-Studio-M`) with pitch lowering (-5.0) and slow rate (0.85) for a deep, scary voice.
- **Visuals**: Uses **Hugging Face Inference API** (FLUX.1-dev or Stable Diffusion XL) to generate a high-definition horror image.
- **Video**: Uses **MoviePy** to combine the audio and image with a "Ken Burns" slow zoom effect.

### Usage
Run the horror show generator via the command line:

```bash
python src/main.py horror --prompt "The sound of scratching behind the wallpaper"
```

The output video will be saved to `outputs/horror_episodes/`.

## 3. Podcast Updates

- **Single Tweet**: The tweet generator now produces a single, high-quality promotional tweet instead of three options.
- **Usage**:
  ```bash
  python src/main.py podcast --mode daily
  ```

## 4. Requirements

Ensure you have the updated dependencies installed:

```bash
pip install -r requirements.txt
```

## 5. Configuration

Ensure your `.env` file has the following keys:
- `GEMINI_API_KEY`: For script generation.
- `GOOGLE_APPLICATION_CREDENTIALS`: JSON file path for Google Cloud TTS.
- `HF_TOKEN`: Hugging Face token for image generation (Get one free at huggingface.co).
