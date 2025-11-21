# Social Media Integration Guide for Meet the Clankers

This guide explains how to use the automated tweet generator to promote your podcast episodes on X (formerly Twitter).

## Features

- **Automated Tweet Generation**: Uses Gemini AI to create engaging tweets based on the episode script.
- **Multiple Styles**: Generates 3 different tweet options (Hook, Quote, Sarcastic).
- **Smart Context**: Analyzes the actual conversation between Zeta and Quill.
- **Ready-to-Post**: Includes the Spotify link and relevant hashtags.

## How to Use

### 1. Generate Tweets with Your Episode

Add the `--tweet` flag to your generation command:

```powershell
# Daily episode with tweets
python src/automated_generator.py --mode daily --categories ai,tech --tweet

# Thanksgiving episode with tweets
python src/automated_generator.py --mode daily --holiday "Thanksgiving" --tweet
```

### 2. Find Your Tweets

The tweets will be saved to a text file in the `outputs/tweets/` directory:

```
outputs/
  ├── scripts/
  ├── temp_audio/
  ├── tweets/
  │   └── [Episode_Title]_[Date]_tweets.txt
  └── [Episode_Title]_[Date].mp3
```

### 3. Post to X

1. Open the generated text file.
2. Choose your favorite tweet style.
3. Copy and paste it to X/Twitter.
4. Attach a video snippet or image if you like!

## Example Output

**Tweet 1 (The Hook):**
> Is AI actually getting smarter, or just better at faking it? 🤔
>
> Zeta and Quill debate the latest LLM benchmarks and what they mean for the future of coding.
>
> Listen now: https://open.spotify.com/show/0UelBMU4glDpp91tUpgzOG
>
> #AI #TechNews #MeetTheClankers

**Tweet 2 (The Quote):**
> Quill: "Great, another smart fridge. Just what I needed, my appliances judging my diet."
> Zeta: "But it orders kale automatically!"
>
> The Clankers are back with your daily tech fix. 🎙️
>
> https://open.spotify.com/show/0UelBMU4glDpp91tUpgzOG

## Automated Posting (Advanced)

To enable fully automated posting, you need to set up your X Developer credentials.

### 1. Get X API Credentials
1. Go to the [X Developer Portal](https://developer.twitter.com/en/portal/dashboard).
2. Sign up for a **Basic** (paid) or **Free** account.
   - *Note: Free tier has very limited posting capabilities.*
3. Create a new Project and App.
   - **Website URL**: `https://open.spotify.com/show/0UelBMU4glDpp91tUpgzOG`
   - **Callback URI**: `http://127.0.0.1:8080/callback`
4. In "User authentication settings", enable **Read and Write** permissions.
5. Generate your keys and tokens:
   - API Key & Secret
   - Access Token & Secret

### 2. Configure .env
Add these lines to your `.env` file:

```env
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
```

### 3. Run with Auto-Post
Add the `--post-tweet` flag to automatically post the first generated tweet:

```powershell
python src/automated_generator.py --mode daily --post-tweet
```

**What happens:**
1. Generates the episode
2. Generates 3 tweet options
3. Automatically posts the **first tweet** (The Hook) to your X account
4. Saves all tweets to the text file as backup

