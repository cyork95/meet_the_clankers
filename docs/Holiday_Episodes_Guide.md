# Holiday Episodes Quick Guide

## Thanksgiving Episode (November 28, 2025)

### Option 1: Run Manually on Thanksgiving Morning ⭐ RECOMMENDED

```powershell
# Navigate to project directory
cd "C:\Users\codyd\OneDrive\Documents\GitHub Projects\meet_the_clankers"

# Generate Thanksgiving episode
.venv\Scripts\python.exe src\automated_generator.py --mode daily --categories ai,tech,business,science --holiday "Thanksgiving"
```

**When to run:** Thanksgiving morning (or the night before)  
**Time needed:** 5-10 minutes to generate  
**Output:** `outputs/[Title]_20251128.mp3`

---

### Option 2: Create One-Time Scheduled Task

**For fully automated generation:**

1. Open Task Scheduler: `Win + R` → `taskschd.msc`
2. Create Task → Name: "Meet the Clankers Thanksgiving Episode"
3. **Trigger:** One time, November 28, 2025 at 3:00 AM
4. **Action:**
   - Program: `C:\Users\codyd\OneDrive\Documents\GitHub Projects\meet_the_clankers\.venv\Scripts\python.exe`
   - Arguments: `src\automated_generator.py --mode daily --categories ai,tech,business,science --holiday "Thanksgiving"`
   - Start in: `C:\Users\codyd\OneDrive\Documents\GitHub Projects\meet_the_clankers`
5. Save

**Test it first:**
```powershell
schtasks /run /tn "Meet the Clankers Thanksgiving Episode"
```

---

## What Makes It Special?

When you add `--holiday "Thanksgiving"`, the AI will:

✅ **Inject holiday-themed jokes and puns**
- "I'm thankful for neural networks!"
- "Unlike your uncle's dry turkey, this news is fresh"
- References to gratitude, family, feasts, etc.

✅ **Keep tech news relevant** but add festive flavor

✅ **Zeta and Quill banter** with holiday spirit
- Zeta: Enthusiastic about the holiday
- Quill: Sarcastically grateful for user data

---

## Other Holiday Episodes

### Christmas (December 25)
```powershell
.venv\Scripts\python.exe src\automated_generator.py --mode daily --categories ai,tech,business,science --holiday "Christmas"
```

### New Year (January 1)
```powershell
.venv\Scripts\python.exe src\automated_generator.py --mode daily --categories ai,tech,business,science --holiday "New Year"
```

### Halloween (October 31)
```powershell
.venv\Scripts\python.exe src\automated_generator.py --mode daily --categories ai,tech,business,science --holiday "Halloween"
```

### Valentine's Day (February 14)
```powershell
.venv\Scripts\python.exe src\automated_generator.py --mode daily --categories ai,tech,business,science --holiday "Valentine's Day"
```

---

## Tips for Holiday Episodes

1. **Run a day early** if you want to review before publishing
2. **Test the command** before the actual holiday to ensure it works
3. **Check the output** - holiday episodes might be slightly longer due to extra banter
4. **Promote it** - holiday episodes can attract more listeners!

---

## Troubleshooting

### "Command not recognized"
- Make sure you're in the project directory
- Check that `.venv` exists and is activated

### "No news found"
- Normal on holidays when fewer articles are published
- Try adding more categories or running the day before

### "Script generation failed"
- Check your `GEMINI_API_KEY` in `.env`
- Verify you have internet connection
- Check API quota limits

---

## Quick Reference

| Holiday | Date | Command Flag |
|---------|------|--------------|
| Thanksgiving | Nov 28 | `--holiday "Thanksgiving"` |
| Christmas | Dec 25 | `--holiday "Christmas"` |
| New Year | Jan 1 | `--holiday "New Year"` |
| Halloween | Oct 31 | `--holiday "Halloween"` |
| Valentine's Day | Feb 14 | `--holiday "Valentine's Day"` |
| Independence Day | Jul 4 | `--holiday "Independence Day"` |

---

**Bottom Line:** Just add `--holiday "Holiday Name"` to any generation command! 🎉
