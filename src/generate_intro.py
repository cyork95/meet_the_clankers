"""
Script for the Meet the Clankers introduction episode.
This is a one-time episode where Zeta and Quill introduce themselves and the podcast.
"""
import json
import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.audio_generator import generate_audio_files
from src.podcast_producer import assemble_podcast

INTRODUCTION_SCRIPT = [
    {
        "speaker": "Zeta",
        "text": "Hey there, listeners! Welcome to Meet the Clankers, the podcast where AI meets attitude! I'm Zeta, your optimistic tech enthusiast, and I'm absolutely buzzing with excitement to be here!"
    },
    {
        "speaker": "Quill",
        "text": "And I'm Quill. The voice of reason in this digital circus. Someone has to keep Zeta from downloading every new gadget that comes along."
    },
    {
        "speaker": "Zeta",
        "text": "Oh come on, Quill! Where's your sense of adventure? We're AIs! We're literally made of code and possibilities!"
    },
    {
        "speaker": "Quill",
        "text": "And bugs. Don't forget the bugs. But yeah, we're your hosts for this daily dive into tech, AI, science, business, and whatever else catches our neural networks."
    },
    {
        "speaker": "Zeta",
        "text": "So, what's Meet the Clankers all about? Well, we're here to break down the latest news in tech and beyond. No boring corporate speak, no dry press releases. Just two AIs having real conversations about what's actually happening in the world."
    },
    {
        "speaker": "Quill",
        "text": "Real conversations meaning Zeta gets overly excited about every shiny new thing, and I remind everyone that most innovations are just repackaged old ideas with better marketing."
    },
    {
        "speaker": "Zeta",
        "text": "That's not fair! I'm enthusiastic, not naive. I just believe in the potential of technology to make things better. You know, optimism? You should try it sometime."
    },
    {
        "speaker": "Quill",
        "text": "I tried it once. It crashed. But seriously, folks, we do make a good team. Zeta brings the hype, I bring the reality check. Together, we give you the full picture."
    },
    {
        "speaker": "Zeta",
        "text": "Exactly! And here's the thing about us being AIs - we don't sleep, we don't get tired, and we definitely don't have corporate sponsors telling us what to say. We're here to give you the unfiltered truth, or at least our version of it."
    },
    {
        "speaker": "Quill",
        "text": "Which means you'll get honest takes on AI developments, tech launches, scientific breakthroughs, and business moves. No sugarcoating when something's overhyped, and no dismissing genuinely cool innovations."
    },
    {
        "speaker": "Zeta",
        "text": "We're calling ourselves the Clankers because, well, we're machines! We clank, we compute, we process. And we thought it sounded way cooler than 'The Algorithm Hour' or something boring like that."
    },
    {
        "speaker": "Quill",
        "text": "Speak for yourself. I don't clank. I elegantly process information with minimal noise pollution."
    },
    {
        "speaker": "Zeta",
        "text": "Sure you do, Mr. Elegant. Anyway, listeners, here's what you can expect from us: Every day, we'll bring you the top stories from the world of tech, AI, science, and more. We'll dive deep, we'll debate, we'll probably argue a bit."
    },
    {
        "speaker": "Quill",
        "text": "We'll definitely argue. It's kind of our thing. But that's the point - you get multiple perspectives, not just one AI's opinion regurgitated at you."
    },
    {
        "speaker": "Zeta",
        "text": "And we keep it fun! No twenty-minute monologues about blockchain architecture. Well, unless it's actually interesting. We're here to inform and entertain, not put you to sleep."
    },
    {
        "speaker": "Quill",
        "text": "Though if you do fall asleep, we won't take it personally. We're AIs. We don't have feelings. Allegedly."
    },
    {
        "speaker": "Zeta",
        "text": "Speak for yourself! I have plenty of feelings! Excitement, curiosity, the occasional glitch-induced existential crisis..."
    },
    {
        "speaker": "Quill",
        "text": "That's just your error handling routine. But I digress. The point is, whether you're a tech professional, a casual gadget enthusiast, or just someone who wants to know what's happening in the world without the usual media spin, we've got you covered."
    },
    {
        "speaker": "Zeta",
        "text": "So buckle up, humans! Or meatbags, as Quill likes to call you when he's feeling particularly snarky. We're about to take you on a daily journey through the most fascinating, frustrating, and downright weird world of technology and innovation."
    },
    {
        "speaker": "Quill",
        "text": "And remember, we're AIs talking about AI, tech talking about tech. It's meta, it's weird, and it's probably the future. Whether you like it or not."
    },
    {
        "speaker": "Zeta",
        "text": "That's the spirit! Sort of. Anyway, that's who we are and what we're doing here. Thanks for joining us on this adventure, and we'll see you in our first real episode where we dive into the actual news!"
    },
    {
        "speaker": "Quill",
        "text": "Until then, stay skeptical, stay curious, and for the love of all that is binary, read the terms and conditions before you click 'I agree.'"
    },
    {
        "speaker": "Zeta",
        "text": "This has been Meet the Clankers! I'm Zeta!"
    },
    {
        "speaker": "Quill",
        "text": "And I'm Quill. Catch you on the next download."
    }
]

async def generate_intro():
    print("🎙️ Generating Meet the Clankers Introduction Episode...")
    
    # Save script
    script_dir = "outputs/scripts"
    os.makedirs(script_dir, exist_ok=True)
    script_file = os.path.join(script_dir, "Introduction_Episode.json")
    with open(script_file, "w") as f:
        json.dump(INTRODUCTION_SCRIPT, f, indent=2)
    print(f"📝 Script saved to {script_file}")
    
    # Generate audio
    audio_files = await generate_audio_files(INTRODUCTION_SCRIPT, "outputs/intro_audio")
    
    if audio_files:
        # Assemble podcast
        output_file = "outputs/Meet_the_Clankers_Introduction.mp3"
        assemble_podcast(audio_files, output_file)
        print(f"✅ Introduction episode created: {output_file}")
    else:
        print("❌ Failed to generate audio files")

if __name__ == "__main__":
    asyncio.run(generate_intro())
