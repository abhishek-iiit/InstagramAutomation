import logging
from instagrapi import Client
from instagrapi.exceptions import LoginRequired

def upload_to_instagram(username: str, password: str, image_path: str, caption: str) -> bool:
    """
    Logs into Instagram and uploads a photo with a given caption.

    Returns:
        True if upload is successful, False otherwise.
    """
    client = Client()
    try:
        logging.info("Attempting to log in to Instagram...")
        client.login(username, password)
        logging.info("Login successful. Uploading photo...")
        client.photo_upload(
            path=image_path,
            caption=caption
        )
        logging.info(f"Successfully uploaded '{image_path}' to Instagram.")
        return True
    except LoginRequired:
        logging.error("Instagram login required. Please check your credentials or session.")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred during Instagram upload: {e}")
        return False