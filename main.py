import os
import csv
import random
import logging
import base64
import requests
from dotenv import load_dotenv
from pytrends.request import TrendReq
import google.generativeai as genai
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from PIL import Image
from io import BytesIO

from google.generativeai import types

# --- 1. SETUP AND CONFIGURATION ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
INSTA_USERNAME = os.getenv("INSTA_USERNAME")
INSTA_PASSWORD = os.getenv("INSTA_PASSWORD")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# This model is for text generation
text_model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

# This model is specifically for image generation, taken from your reference
image_model = genai.GenerativeModel(model_name="gemini-2.0-flash-preview-image-generation")


# --- 2. TREND DISCOVERY MODULE ---
def get_trend_from_csv(filename="trends.csv"):
    """
    Reads a list of trending topics from a local CSV file and returns one at random.
    """
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        return None

    try:
        with open(filename, mode='r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            header = next(reader)  # Skip the header row
            trends = [row[0] for row in reader] # Read the first column of each row

        if not trends:
            print("Error: The CSV file is empty or has no trends.")
            return None

        # Select and return one trend at random from the list
        selected_trend = random.choice(trends)
        print(f"Selected Trend from CSV: {selected_trend}")
        return selected_trend

    except Exception as e:
        print(f"Error reading or processing the CSV file: {e}")
        return None

# --- 3. GOOGLE TRENDS CONTENT GENERATION MODULE ---
def generate_creative_image_prompt(topic):
    """Uses Gemini to convert a simple topic into a detailed image generation prompt."""
    try:
        prompt = f"Convert the following topic into a highly creative and detailed prompt for generating a visually stunning image: '{topic}'. The prompt should evoke a 'viral' aesthetic and be suitable for an AI image generator."
        response = text_model.generate_content(prompt)
        image_prompt = response.text
        logging.info(f"Generated image prompt: {image_prompt}")
        return image_prompt
    except Exception as e:
        logging.error(f"Error generating image prompt: {e}")
        return None

def generate_image_with_gemini(image_prompt: str, image_filename: str) -> str:
    from google import genai
    from google.genai import types
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=image_prompt,
        config=types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE']
        )
    )

    # Extract image from response
    found_image = False
    for candidate in response.candidates:
        for part in candidate.content.parts:
            if getattr(part, "inline_data", None) is not None:
                image = Image.open(BytesIO(part.inline_data.data))
                image.save(image_filename)
                found_image = True
                break
        if found_image:
            break

    if not found_image:
        raise ValueError("No image data found in the Gemini API response.")

    return image_filename

def generate_instagram_caption(topic):
    """Uses Gemini to create an engaging caption and relevant hashtags for a topic."""
    try:
        prompt = f"Generate an engaging Instagram caption and 15 relevant hashtags for the topic: '{topic}'. The caption should be short, shareable, and encourage interaction."
        response = text_model.generate_content(prompt)
        caption = response.text
        logging.info(f"Generated caption: {caption}")
        return caption
    except Exception as e:
        logging.error(f"Error generating caption: {e}")
        return None

# --- 4. INSTAGRAM UPLOAD MODULE ---
def upload_to_instagram(username, password, image_path, caption):
    """Logs into Instagram and uploads the image with the caption."""
    try:
        client = Client()
        client.login(username, password)
        client.photo_upload(
            path=image_path,
            caption=caption
        )
        logging.info("Successfully uploaded to Instagram.")
        return True
    except Exception as e:
        logging.error(f"Error uploading to Instagram: {e}")
        return False

# # --- 5. MAIN EXECUTION LOGIC ---
def main():
    """Main function to orchestrate the entire workflow."""
    if not os.path.exists("generated_images"):
        os.makedirs("generated_images")

    # trend = get_trend_from_csv()
    trend = "A majestic lion with a crown made of starlight"
    if not trend: return

    image_prompt = generate_creative_image_prompt(trend)
    if not image_prompt: return

    safe_filename = "".join(c for c in trend if c.isalnum() or c in (' ', '_')).rstrip()
    image_filename = f"generated_images/{safe_filename.replace(' ', '_')}.jpg"
    image_path = generate_image_with_gemini(image_prompt, image_filename)
    if not image_path: return

    caption = generate_instagram_caption(trend)
    if not caption: return

    upload_to_instagram(INSTA_USERNAME, INSTA_PASSWORD, image_path, caption)

    logging.info("Trend-to-Gram process completed successfully!")

if __name__ == "__main__":
    main()