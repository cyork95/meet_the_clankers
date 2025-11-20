# Google Cloud Text-to-Speech Setup Guide

## Why Google Cloud TTS?
- **4 million free characters/month** (plenty for daily podcasts)
- **WaveNet/Neural2 voices** - extremely natural sounding
- **1 million free WaveNet characters/month**
- Much better quality than gTTS

## One-Time Setup Steps

### 1. Create Google Cloud Account
1. Go to https://console.cloud.google.com
2. Sign up (new users get $300 free credit)
3. Create a new project (e.g., "meet-the-clankers")

### 2. Enable Text-to-Speech API
1. In Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for "Cloud Text-to-Speech API"
3. Click "Enable"

### 3. Create Service Account Credentials
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Fill in:
   - **Service account name**: `podcast-tts`
   - **Role**: "Cloud Text-to-Speech User"
4. Click "Done"
5. Click on the created service account
6. Go to "Keys" tab → "Add Key" → "Create new key"
7. Choose "JSON" and click "Create"
8. **Save the downloaded JSON file securely** (e.g., `google-tts-credentials.json`)

### 4. Configure Environment Variable
Add to your `.env` file:
```
GOOGLE_APPLICATION_CREDENTIALS=path/to/google-tts-credentials.json
```

**Example:**
```
GOOGLE_APPLICATION_CREDENTIALS=C:\Users\codyd\OneDrive\Documents\GitHub Projects\meet_the_clankers\google-tts-credentials.json
```

### 5. Update .gitignore
Make sure your credentials file is NOT committed to git:
```
google-tts-credentials.json
*.json
```

## After Setup
Once you've completed these steps, let me know and I'll:
1. Install `google-cloud-texttospeech` library
2. Update `audio_generator.py` to use Google Cloud TTS
3. Configure high-quality WaveNet voices for Zeta and Quill
4. Keep gTTS as fallback

## Cost Estimate
- **Free tier**: 4M characters/month (Standard), 1M characters/month (WaveNet)
- **Average podcast**: ~5,000 characters
- **You can generate**: ~200 WaveNet podcasts/month for FREE
