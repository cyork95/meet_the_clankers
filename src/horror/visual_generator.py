"""
Module for generating horror visuals using Hugging Face Inference API.
"""
import os
from huggingface_hub import InferenceClient
from PIL import Image
import io

def generate_horror_image(prompt: str, output_file: str) -> str:
    """
    Generate a horror image based on the prompt using Hugging Face Inference API.
    
    Args:
        prompt: The image generation prompt.
        output_file: Path to save the image.
        
    Returns:
        Path to the generated image file.
    """
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        print("❌ HF_TOKEN not found. Please set it in .env")
        return ""
        
    client = InferenceClient(token=hf_token)
    
    print(f"[INFO] Generating image with Hugging Face (FLUX.1-dev): {prompt[:50]}...")
    
    try:
        # Using FLUX.1-dev as requested, or fallback to SDXL if needed
        # model="black-forest-labs/FLUX.1-dev"
        # Note: FLUX might require a pro subscription or have availability issues on free tier.
        # If it fails, we can try "stabilityai/stable-diffusion-xl-base-1.0"
        
        image = client.text_to_image(
            prompt,
            model="black-forest-labs/FLUX.1-dev" 
        )
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        image.save(output_file)
        print(f"[SUCCESS] Image saved to {output_file}")
        return output_file
        
    except Exception as e:
        print(f"[WARN] FLUX generation failed: {e}")
        print("[INFO] Retrying with Stable Diffusion XL...")
        try:
            image = client.text_to_image(
                prompt,
                model="stabilityai/stable-diffusion-xl-base-1.0"
            )
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            image.save(output_file)
            print(f"[SUCCESS] Image saved to {output_file}")
            return output_file
        except Exception as e2:
            print(f"[ERROR] All image generation attempts failed: {e2}")
            return ""

if __name__ == "__main__":
    # Test
    from dotenv import load_dotenv
    load_dotenv()
    generate_horror_image("gloomy abandoned hospital hallway, cinematic lighting, hyperrealistic, 8k, horror atmosphere", "outputs/test_horror_hf.png")
