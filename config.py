import os
from dotenv import load_dotenv
import logging

# Load environment variables from a .env file
load_dotenv(override=True)

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- API Keys and Credentials ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
INSTA_USERNAME = os.getenv("INSTA_USERNAME")
INSTA_PASSWORD = os.getenv("INSTA_PASSWORD")

# --- Model Names ---
TEXT_MODEL_NAME = "gemini-1.5-flash-latest"
IMAGE_MODEL_NAME = "gemini-2.0-flash-preview-image-generation"

# --- File and Directory Paths ---
TRENDS_CSV_PATH = "constants/trends.csv"
GENERATED_IMAGES_DIR = "constants/generated_images"

def validate_config():
    """Validates that all necessary environment variables are set."""
    required_vars = {
        "GOOGLE_API_KEY": GOOGLE_API_KEY,
        "INSTA_USERNAME": INSTA_USERNAME,
        "INSTA_PASSWORD": INSTA_PASSWORD
    }
    missing_vars = [key for key, value in required_vars.items() if value is None]
    if missing_vars:
        error_message = f"Missing required environment variables: {', '.join(missing_vars)}"
        logging.critical(error_message)
        raise ValueError(error_message)
    logging.info("All configurations and credentials loaded successfully.")