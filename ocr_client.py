import os
import sys
import base64
import requests
import argparse
import json
from dotenv import load_dotenv

# 1. Load environment variables from .env
load_dotenv()
SERVER_IP = os.getenv("SERVER_IP")

def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: File '{image_path}' not found.")
        sys.exit(1)

def run_ocr(image_path, prompt):
    if not SERVER_IP:
        print("Error: SERVER_IP not found in .env file.")
        sys.exit(1)

    url = f"http://{SERVER_IP}:11434/api/generate"
    
    payload = {
        "model": "deepseek-ocr",
        "prompt": prompt,
        "images": [encode_image(image_path)],
        "stream": False,
        "options": {
            "num_thread": 16,
            "num_predict": 1024, # Limit output length to prevent long tail timeouts
            "temperature": 0     # Keep it deterministic for OCR
        }
    }

    print(f"Sending {image_path} to {SERVER_IP}...")
    try:
        response = requests.post(url, json=payload, timeout=300)
        response.raise_for_status()
        return response.json().get("response")
    except requests.exceptions.RequestException as e:
        return f"Request Failed: {e}"
    
def run_ocr_stream(image_path, prompt ):
    url = f"http://{SERVER_IP}:11434/api/generate"
    
    payload = {
        "model": "deepseek-ocr",
        "prompt": prompt,
        "images": [encode_image(image_path)],
        "stream": True,  # Enable streaming
    }

    print(f"Connecting to {SERVER_IP} (Streaming)...")
    
    # Use 'with' to keep the connection open for the stream
    with requests.post(url, json=payload, stream=True, timeout=300) as response:
        response.raise_for_status()
        
        print("\n--- OCR EXTRACTED TEXT ---")
        for line in response.iter_lines():
            if line:
                # Parse the JSON chunk
                chunk = json.loads(line)
                text_chunk = chunk.get("response", "")
                print(text_chunk, end="", flush=True)
                
                if chunk.get("done"):
                    print("\n\n--- Extraction Complete ---")

if __name__ == "__main__":
    # 2. Setup Command Line Arguments
    parser = argparse.ArgumentParser(description="Remote DeepSeek-OCR Client")
    parser.add_argument("image", help="Path to the local image file (JPG/PNG)")
    # Optional Argument for Prompt (defaults to Free OCR. if not provided)
    parser.add_argument(
        "--prompt", "-p", 
        default="Free OCR.", 
        help="Custom prompt for the model (e.g., '<|grounding|>Convert to markdown.')"
    )
    args = parser.parse_args()

    # Execute
    # result = run_ocr(args.image)
    result = run_ocr_stream(args.image, args.prompt)
    print("\n--- OCR RESULTS ---")
    print(result)