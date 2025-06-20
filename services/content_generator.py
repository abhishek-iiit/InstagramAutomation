import logging
from io import BytesIO
from PIL import Image
import google.generativeai as genai
from google.generativeai import types
from config import GOOGLE_API_KEY, TEXT_MODEL_NAME, IMAGE_MODEL_NAME

# Configure the Gemini API client
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    text_model = genai.GenerativeModel(model_name=TEXT_MODEL_NAME)
    image_model = genai.GenerativeModel(model_name=IMAGE_MODEL_NAME)
except Exception as e:
    logging.critical(f"Failed to configure Gemini API: {e}")
    # Depending on the application, you might want to exit here.
    # For now, we'll let it fail on the first generation attempt.


def generate_creative_image_prompt(topic: str) -> str:
    """Uses Gemini to convert a simple topic into a detailed image generation prompt."""
    try:
        prompt = (f"Convert the following topic into a highly creative and detailed prompt for "
                  f"generating a visually stunning image: '{topic}'. The prompt should evoke a "
                  f"'viral' aesthetic and be suitable for an AI image generator.")
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


def generate_instagram_caption(topic: str) -> str:
    """Uses Gemini to create an engaging Instagram caption and hashtags."""
    try:
        prompt = (f"Generate an engaging Instagram caption and 15 relevant hashtags for the topic: '{topic}'. "
                  f"The caption should be short, shareable, and encourage interaction.")
        response = text_model.generate_content(prompt)
        caption = response.text
        logging.info(f"Generated caption: {caption}")
        return caption
    except Exception as e:
        logging.error(f"Error generating Instagram caption: {e}")
        return None