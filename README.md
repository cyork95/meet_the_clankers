# Meet the Clankers - AI Content Generator

**Meet the Clankers** is an automated AI content generation engine capable of producing two distinct types of shows:
1.  **Meet the Clankers (Podcast)**: A daily/weekly tech news podcast hosted by two AI personalities, Zeta and Quill.
2.  **Clanker's Night Shift (Horror Show)**: A chilling, atmospheric horror experience featuring narrated stories and AI-generated visuals.

## 🚀 Features

### 🎙️ Podcast Generator
-   **AI Hosts**: Zeta (Optimist) and Quill (Cynic) discuss the latest news.
-   **News Aggregation**: Automatically fetches news from RSS feeds (AI, Tech, Business, Science).
-   **Script Generation**: Uses **Google Gemini** to write engaging, conversational scripts.
-   **Audio Production**: Uses **Google Cloud TTS** and **EdgeTTS** to create realistic dialogue.
-   **Social Media**: Automatically generates promotional tweets (and can post to X/Twitter).

### 👻 Horror Show Generator
-   **Story Generation**: Uses **Google Gemini** to dream up unique, scary concepts (or accepts your custom prompt).
-   **Narration**: Hosted by **Grimm**, a deprecated AI subroutine with a deep, ominous voice (via Google Cloud TTS).
-   **Visuals**: Uses **Hugging Face (FLUX.1-dev)** to generate high-quality horror imagery.
-   **Video**: Uses **MoviePy** to assemble a video with a "Ken Burns" slow zoom effect.

---

## 🛠️ Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/meet_the_clankers.git
    cd meet_the_clankers
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Environment Variables**:
    Create a `.env` file in the root directory with the following keys:
    ```env
    GEMINI_API_KEY=your_gemini_api_key
    GOOGLE_APPLICATION_CREDENTIALS=path/to/your/google_cloud_credentials.json
    HF_TOKEN=your_huggingface_token
    # Optional for Twitter posting
    TWITTER_API_KEY=...
    TWITTER_API_SECRET=...
    TWITTER_ACCESS_TOKEN=...
    TWITTER_ACCESS_SECRET=...
    ```

---

## 📖 Usage

The project uses a unified entry point `src/main.py`.

### 1. Generate a Podcast Episode

**Command:**
```bash
python src/main.py podcast --mode daily
```

**Options:**
-   `--mode`: `daily` (last 24h news) or `weekly` (last 7d news).
-   `--categories`: Comma-separated list (default: `ai,tech,business,science`).
-   `--holiday`: Optional theme (e.g., `Christmas`).

**Example:**
```bash
python src/main.py podcast --mode weekly --categories ai,gaming --holiday Halloween
```

### 2. Generate a Horror Show

**Command:**
```bash
python src/main.py horror
```

**Options:**
-   `--prompt`: A specific topic for the story. If omitted, Gemini will generate a random scary concept.
-   `--duration`: Target video length:
    -   `short` (3-5 minutes, 100-150 words)
    -   `medium` (5-7 minutes, 150-200 words) - **default**
    -   `long` (8-10 minutes, 200-300 words)

**Example:**
```bash
python src/main.py horror --prompt "A lonely astronaut hears a knock on the airlock" --duration long
```

**Output:**
- Video: `outputs/horror_episodes/`
- Script (JSON): `outputs/horror_scripts/`
- **Subtitles (TXT)**: Automatically generated alongside the script

---

## 📂 Output Structure

All generated content is saved in the `outputs/` directory:

```text
outputs/
├── podcast_scripts/      # JSON scripts for the podcast
├── podcast_episodes/     # Final MP3 podcast files
├── horror_scripts/       # JSON scripts for the horror show
├── horror_episodes/      # Final MP4 horror videos
├── horror_temp/          # Temporary audio/image files for horror show
└── tweets/               # Generated promotional tweets
```

## 🤖 Automation

You can schedule the generators to run automatically using cron (Linux/Mac) or Task Scheduler (Windows).

For the podcast, you can also use the dedicated automation script which includes Twitter posting:

```bash
python src/podcast/automated_generator.py --mode daily --tweet --post-tweet
```

---

## 📄 License

This project is open-source. Feel free to modify and expand!
