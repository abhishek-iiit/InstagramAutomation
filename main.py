import os
import logging
import config
from services.trend_discoverer import get_trend_from_csv
from services.content_generator import (
    generate_creative_image_prompt,
    generate_image_with_gemini,
    generate_instagram_caption
)
from services.instagram_uploader import upload_to_instagram

def main():
    """
    Main function to orchestrate the Trend-to-Gram workflow.
    """
    logging.info("--- Starting Trend-to-Gram Process ---")

    # 1. Validate Configuration
    try:
        config.validate_config()
    except ValueError as e:
        logging.critical(f"Configuration error: {e}. Exiting.")
        return # Exit if config is invalid

    # 2. Create directory for images if it doesn't exist
    if not os.path.exists(config.GENERATED_IMAGES_DIR):
        os.makedirs(config.GENERATED_IMAGES_DIR)
        logging.info(f"Created directory: {config.GENERATED_IMAGES_DIR}")

    # 3. Get a Trend
    # trend = get_trend_from_csv()
    # Using a hardcoded trend for reliable testing, as in the original script.
    trend = "A majestic lion with a crown made of starlight"
    if not trend:
        logging.error("Could not retrieve a trend. Halting process.")
        return

    # 4. Generate Content
    image_prompt = generate_creative_image_prompt(trend)
    if not image_prompt:
        logging.error("Failed to generate an image prompt. Halting process.")
        return

    # Create a safe filename for the image
    safe_filename = "".join(c for c in trend if c.isalnum() or c in (' ', '_')).rstrip()
    image_filename = f"{safe_filename.replace(' ', '_')}.jpg"
    image_path = os.path.join(config.GENERATED_IMAGES_DIR, image_filename)

    # Generate the image
    generated_path = generate_image_with_gemini(image_prompt, image_path)
    if not generated_path:
        logging.error("Failed to generate the image. Halting process.")
        return

    # Generate the caption
    caption = generate_instagram_caption(trend)
    if not caption:
        logging.error("Failed to generate a caption. Halting process.")
        return

    # 5. Upload to Instagram
    success = upload_to_instagram(
        username=config.INSTA_USERNAME,
        password=config.INSTA_PASSWORD,
        image_path=generated_path,
        caption=caption
    )

    if success:
        logging.info("--- Trend-to-Gram Process Completed Successfully! ---")
    else:
        logging.error("--- Trend-to-Gram Process Failed During Upload. ---")

if __name__ == "__main__":
    main()