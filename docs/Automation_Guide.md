# Automated Podcast Publishing Guide

## You Don't Need to Be Awake at 5 AM!

Here's how to automate the entire process so episodes publish at 5 AM while you sleep.

---

## Option 1: Windows Task Scheduler (Recommended for Windows)

### Step 1: Create the Scheduled Task

1. **Open Task Scheduler**
   - Press `Win + R`
   - Type `taskschd.msc`
   - Press Enter

2. **Create New Task**
   - Click "Create Task" (not "Create Basic Task")
   - Name: "Meet the Clankers Daily Episode"
   - Description: "Automatically generate and prepare daily podcast episode"

3. **Configure Triggers**
   - Go to "Triggers" tab
   - Click "New"
   - **Begin the task:** On a schedule
   - **Settings:** Daily
   - **Start:** 3:00 AM (gives 2 hours before 5 AM publish time)
   - **Recur every:** 1 days
   - **Days:** Monday, Tuesday, Wednesday, Thursday, Friday
   - Click OK

4. **Configure Actions**
   - Go to "Actions" tab
   - Click "New"
   - **Action:** Start a program
   - **Program/script:** `C:\Users\codyd\OneDrive\Documents\GitHub Projects\meet_the_clankers\.venv\Scripts\python.exe`
   - **Add arguments:** `src\automated_generator.py --mode daily --categories ai,tech,business,science`
   - **Start in:** `C:\Users\codyd\OneDrive\Documents\GitHub Projects\meet_the_clankers`
   - Click OK

5. **Configure Conditions**
   - Go to "Conditions" tab
   - **Uncheck** "Start the task only if the computer is on AC power"
   - **Check** "Wake the computer to run this task" (if you want it to wake your PC)

6. **Configure Settings**
   - Go to "Settings" tab
   - **Check** "Run task as soon as possible after a scheduled start is missed"
   - **Check** "If the task fails, restart every: 10 minutes"
   - **Attempt to restart up to: 3 times**

7. **Save**
   - Click OK
   - Enter your Windows password if prompted

### Step 2: Test the Task

```powershell
# Test run the task manually
schtasks /run /tn "Meet the Clankers Daily Episode"

# Check task status
schtasks /query /tn "Meet the Clankers Daily Episode" /v
```

---

## Option 2: Python Script with Schedule Library

### Install Schedule Library
```bash
pip install schedule
```

### Create Scheduler Script

Create `src/scheduler.py`:

```python
import schedule
import time
import subprocess
import os

def run_daily_episode():
    """Run the automated episode generator."""
    print(f"Starting episode generation at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Path to your project
    project_dir = r"C:\Users\codyd\OneDrive\Documents\GitHub Projects\meet_the_clankers"
    python_exe = os.path.join(project_dir, ".venv", "Scripts", "python.exe")
    script_path = os.path.join(project_dir, "src", "automated_generator.py")
    
    # Run the generator
    result = subprocess.run(
        [python_exe, script_path, "--mode", "daily", "--categories", "ai,tech,business,science"],
        cwd=project_dir,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ Episode generated successfully")
    else:
        print(f"❌ Episode generation failed: {result.stderr}")

# Schedule the task for 3 AM every weekday
schedule.every().monday.at("03:00").do(run_daily_episode)
schedule.every().tuesday.at("03:00").do(run_daily_episode)
schedule.every().wednesday.at("03:00").do(run_daily_episode)
schedule.every().thursday.at("03:00").do(run_daily_episode)
schedule.every().friday.at("03:00").do(run_daily_episode)

print("📅 Scheduler started. Waiting for scheduled times...")
print("Episodes will generate at 3:00 AM Monday-Friday")

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
```

### Run Scheduler as Background Service

**Option A: Run in Terminal (keeps running)**
```bash
python src/scheduler.py
```

**Option B: Run as Windows Service** (more complex, but runs in background)
- Use NSSM (Non-Sucking Service Manager)
- Download from: https://nssm.cc/download

---

## Option 3: GitHub Actions (Cloud-Based, Free)

If you push your code to GitHub, you can use GitHub Actions to run automatically:

### Create `.github/workflows/daily-podcast.yml`:

```yaml
name: Generate Daily Podcast

on:
  schedule:
    # Runs at 3:00 AM ET (8:00 AM UTC) Monday-Friday
    - cron: '0 8 * * 1-5'
  workflow_dispatch:  # Allows manual trigger

jobs:
  generate-podcast:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Generate podcast episode
      env:
        GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        GOOGLE_APPLICATION_CREDENTIALS: ${{ secrets.GOOGLE_CREDENTIALS }}
      run: |
        python src/automated_generator.py --mode daily --categories ai,tech,business,science
    
    - name: Upload podcast to storage
      # Add your upload logic here (S3, Google Drive, etc.)
      run: echo "Upload to your hosting platform"
```

---

## Recommended Workflow

### Night Before (10 PM - Automated):
1. **Script runs at 3:00 AM** (while you sleep)
2. Fetches latest news
3. Generates script with AI
4. Creates audio files
5. Assembles final podcast
6. Saves to `outputs/` folder

### Morning (When You Wake Up):
1. **Review the episode** (optional, but recommended at first)
2. **Upload to podcast platforms** (Spotify, Apple Podcasts, etc.)
3. **Promote on social media**

### Fully Automated (Advanced):
- Use APIs to auto-upload to podcast platforms
- Use social media APIs to auto-post announcements
- Everything happens while you sleep!

---

## Upload Automation (Bonus)

### Auto-Upload to Podcast Platforms

Most platforms have APIs or RSS-based systems:

**Anchor/Spotify:**
- Upload via RSS feed
- Can automate with their API

**Apple Podcasts:**
- Upload via RSS feed
- Point to your hosted MP3 files

**YouTube:**
- Use YouTube API to auto-upload
- Can include static image + audio

### Simple RSS Feed Approach

1. Generate episode → Save to `outputs/`
2. Update RSS feed XML automatically
3. Podcast platforms auto-fetch from RSS
4. **You just need to host the files somewhere**

---

## My Recommendation for You

### Phase 1: Semi-Automated (Start Here)
1. **Set up Windows Task Scheduler** to run at 3:00 AM
2. Episode generates automatically while you sleep
3. **You wake up, review, and upload manually**
4. Takes 10-15 minutes of your time in the morning

### Phase 2: Fully Automated (Later)
1. Task Scheduler runs at 3:00 AM
2. Script auto-uploads to hosting
3. RSS feed auto-updates
4. Platforms auto-fetch new episode
5. **You just monitor and promote**

---

## Quick Start Commands

### Test the automated generator right now:
```bash
python src/automated_generator.py --mode daily --categories ai,tech
```

### Set up Windows Task Scheduler:
1. Run `taskschd.msc`
2. Follow the steps above
3. Test with manual run
4. Let it run automatically tomorrow at 3 AM

### Check if it worked:
```bash
# Check the outputs folder
ls outputs/

# Check the latest episode
ls outputs/*.mp3 | sort | tail -1
```

---

## Troubleshooting

### Task didn't run?
- Check Task Scheduler history
- Ensure computer was on (or set to wake)
- Check task conditions (AC power, etc.)

### Episode generation failed?
- Check logs in Task Scheduler
- Run manually to see errors
- Verify API keys are set in `.env`

### Want to change the schedule?
- Edit the task in Task Scheduler
- Change trigger time
- Save and test


---

## Special Holiday Episodes

### Generate a One-Time Holiday Episode

For special occasions like Thanksgiving, Christmas, or New Year, you can generate themed episodes with holiday-specific jokes and references.

#### Manual Command (Recommended for Special Episodes)

```powershell
# Thanksgiving Episode
.venv\Scripts\python.exe src\automated_generator.py --mode daily --categories ai,tech,business,science --holiday "Thanksgiving"

# Christmas Episode
.venv\Scripts\python.exe src\automated_generator.py --mode daily --categories ai,tech,business,science --holiday "Christmas"

# New Year Episode
.venv\Scripts\python.exe src\automated_generator.py --mode daily --categories ai,tech,business,science --holiday "New Year"
```

**What This Does:**
- Fetches the latest news from your selected categories
- Generates a script with **Thanksgiving-themed puns, jokes, and references** throughout
- Zeta and Quill will make holiday-related banter
- Creates the audio and assembles the final podcast
- Saves with a date-stamped filename in `outputs/`

#### Create a One-Time Scheduled Task for Thanksgiving

If you want to automate the Thanksgiving episode to generate automatically:

1. **Open Task Scheduler** (`Win + R` → `taskschd.msc`)
2. **Create New Task**
   - Name: "Meet the Clankers Thanksgiving Episode"
   - Description: "Generate Thanksgiving special episode"

3. **Configure Trigger**
   - **Begin the task:** On a schedule
   - **One time:** Thursday, November 28, 2025 at 3:00 AM
   - Click OK

4. **Configure Action**
   - **Program/script:** `C:\Users\codyd\OneDrive\Documents\GitHub Projects\meet_the_clankers\.venv\Scripts\python.exe`
   - **Add arguments:** `src\automated_generator.py --mode daily --categories ai,tech,business,science --holiday "Thanksgiving"`
   - **Start in:** `C:\Users\codyd\OneDrive\Documents\GitHub Projects\meet_the_clankers`

5. **Save and Test**
   ```powershell
   # Test it manually first
   schtasks /run /tn "Meet the Clankers Thanksgiving Episode"
   ```

#### What the Holiday Theme Does

When you add `--holiday "Thanksgiving"`, the AI script generator will:
- ✅ Inject Thanksgiving-themed puns and jokes
- ✅ Make references to turkey, gratitude, family gatherings, etc.
- ✅ Keep the tech news relevant but add holiday flavor
- ✅ Zeta might say things like "I'm thankful for neural networks!"
- ✅ Quill might sarcastically comment on "tech companies being grateful for user data"

**Example Output:**
```
Zeta: "Happy Thanksgiving, listeners! Today we're serving up a feast of tech news!"
Quill: "Yeah, and unlike your uncle's dry turkey, this news is actually fresh."
```

---

## Bottom Line


**You set it up once, it runs forever.**

1. Create the automated script ✅ (Done - `src/automated_generator.py`)
2. Set up Windows Task Scheduler (5 minutes)
3. Test it once
4. Go to sleep
5. Wake up to a new episode ready to upload

**Your 5 AM publishing schedule is now automated!** 🎉
