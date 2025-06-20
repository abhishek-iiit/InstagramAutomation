import os
import csv
import random
import logging
from config import TRENDS_CSV_PATH

def get_trend_from_csv():
    """
    Reads trending topics from a local CSV file and returns one at random.
    """
    if not os.path.exists(TRENDS_CSV_PATH):
        logging.error(f"Trend CSV file not found at '{TRENDS_CSV_PATH}'.")
        return None

    try:
        with open(TRENDS_CSV_PATH, mode='r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            next(reader)  # Skip header
            trends = [row[0] for row in reader if row] # Read the first column of each row

        if not trends:
            logging.warning("The CSV file is empty or contains no trends.")
            return None

        # Select and return one trend at random from the list
        selected_trend = random.choice(trends)
        logging.info(f"Selected Trend from CSV: {selected_trend}")
        return selected_trend

    except Exception as e:
        logging.error(f"Error reading or processing the CSV file: {e}")
        return None