# Available News Categories

## Default Categories
The podcast now defaults to: **ai, tech, business, science**

## All Available Categories

### 🤖 AI
- TechCrunch AI
- Wired AI
- The Verge AI
- AI News

### 💻 Tech
- TechCrunch
- The Verge
- Ars Technica
- Engadget

### 💼 Business
- CNBC
- Bloomberg Technology
- Reuters Business

### 🔬 Science
- Science Daily
- Nature
- New Scientist

### 🎬 Entertainment
- Polygon
- IGN
- Hollywood Reporter

### 🏛️ Politics
- BBC World News
- NPR Politics
- Politico

### 🎮 Gaming
- Polygon
- IGN
- GameSpot

### 🚀 Space
- NASA Breaking News
- Space.com

## Usage Examples

### Default (AI, Tech, Business, Science)
```bash
python src/main.py --mode daily
```

### Custom Categories
```bash
# Just AI and Tech
python src/main.py --mode daily --categories ai,tech

# Tech and Gaming
python src/main.py --mode daily --categories tech,gaming

# Everything except politics
python src/main.py --mode daily --categories ai,tech,business,science,entertainment,gaming,space

# Weekly roundup with all categories
python src/main.py --mode weekly --categories ai,tech,business,science,entertainment,politics,gaming,space
```

## Tips
- **Daily mode**: Stick to 3-5 categories for a focused 10-15 minute episode
- **Weekly mode**: Can handle more categories (5-8) for a 15-20 minute episode
- More categories = longer episodes and more diverse content
