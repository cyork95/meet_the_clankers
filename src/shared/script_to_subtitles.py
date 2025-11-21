"""
Utility to convert JSON scripts to plain text subtitle files.
"""
import json
import sys
import os

def script_to_subtitles(script_path: str, output_path: str = None):
    """
    Converts a JSON script to a plain text file with only dialogue.
    
    Args:
        script_path: Path to the JSON script file
        output_path: Optional output path. If not provided, uses same name with .txt extension
    """
    # Read the script
    with open(script_path, 'r', encoding='utf-8') as f:
        script = json.load(f)
    
    # Extract dialogue
    lines = []
    for entry in script:
        speaker = entry.get('speaker', '')
        text = entry.get('text', '')
        
        # Skip FX/Narrator lines
        if speaker in ['FX', 'SoundEffect', 'NARRATOR', 'Narrator']:
            continue
        
        # Format: Speaker: Text
        lines.append(f"{speaker}: {text}")
    
    # Determine output path
    if not output_path:
        output_path = script_path.replace('.json', '_subtitles.txt')
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(lines))
    
    print(f"[SUCCESS] Subtitles saved to: {output_path}")
    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_to_subtitles.py <script.json> [output.txt]")
        sys.exit(1)
    
    script_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    script_to_subtitles(script_path, output_path)
