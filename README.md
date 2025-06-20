# InstagramAutomation: AI-Powered Instagram Content Bot

An automated social media content creation bot that discovers trending topics,
generates stunning AI images and engaging captions using Google Gemini,
and posts them directly to Instagram.

## ✨ Core Features

🤖 Automated Workflow:
A complete, hands-off pipeline from idea to posted content.

📈 Trend Discovery:
Fetches trending topics from a local CSV file, which can be easily updated.

🎨 AI-Powered Content Creation: - Creative Prompts: Converts simple topics into detailed, viral-style prompts for image generation. - Stunning Visuals: Uses Google's Gemini model to generate high-quality, unique images. - Engaging Captions: Creates compelling captions with relevant hashtags to boost engagement.

📸 Seamless Instagram Upload:
Automatically logs in and uploads the generated content to your Instagram account.

🔧 Modular & Extensible:
Built with a clean, production-ready structure that is easy to maintain and extend.

## 🚀 How It Works

The bot follows a simple, powerful workflow:

[ 1. Discover Trend ] -> [ 2. Generate Image Prompt ] -> [ 3. Generate Image & Caption ] -> [ 4. Upload to Instagram ]
(trends.csv) (Gemini Pro) (Gemini & Gemini Pro) (instagrapi)

## 🛠️ Technology Stack

- Backend: Python
- AI & Content Generation: Google Gemini API (gemini-1.5-flash-latest for text, gemini-pro-vision for images)
- Instagram API Interaction: instagrapi
- Configuration: python-dotenv
- Image Handling: Pillow

## 📁 Project Structure

trend_to_gram/
├── main.py # Main orchestration script (entry point)
├── config.py # Handles configuration, API keys, and paths
├── trend_discoverer.py # Module for fetching trends
├── content_generator.py # Module for AI content generation (text/image)
├── instagram_uploader.py # Module for Instagram uploads
├── generated_images/ # Directory for saving generated images
│ └── .gitkeep
├── trends.csv # CSV file containing topics for content generation
├── .env # For storing secret keys
└── requirements.txt # Project dependencies

## ⚙️ Setup and Installation

1. Clone the Repository

   git clone <your-repository-url>
   cd trend_to_gram

2. Create a Virtual Environment

   # Windows

   python -m venv venv
   venv\\Scripts\\activate

   # macOS/Linux

   python3 -m venv venv
   source venv/bin/activate

3. Install Dependencies

   pip install -r requirements.txt

4. Configure Environment Variables

Create a `.env` file in the root directory:

    # --- Google AI Studio ---
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"

    # --- Instagram Credentials ---
    INSTA_USERNAME="YOUR_INSTAGRAM_USERNAME"
    INSTA_PASSWORD="YOUR_INSTAGRAM_PASSWORD"

5. Prepare the Trends File

trends.csv example:

    Topic
    "A cinematic shot of a wolf howling at a galaxy-filled moon"
    "A futuristic neon-lit city street in Tokyo at night"
    "An enchanted forest with glowing mushrooms and mystical creatures"
    "A majestic lion with a crown made of starlight"

## ▶️ Usage

To run the bot:

    python main.py

Example logs:

    INFO:--- Starting Trend-to-Gram Process ---
    INFO:All configurations and credentials loaded successfully.
    INFO:Selected Trend from CSV: A majestic lion with a crown made of starlight
    INFO:Generated image prompt: ...
    INFO:Image successfully generated and saved to generated_images/a_majestic_lion...jpg
    INFO:Generated caption: ...
    INFO:Attempting to log in to Instagram...
    INFO:Login successful. Uploading photo...
    INFO:Successfully uploaded '...' to Instagram.
    INFO:--- Trend-to-Gram Process Completed Successfully! ---

## 🧩 Module Breakdown

- main.py: Orchestrates the full workflow.
- config.py: Loads environment variables and settings.
- trend_discoverer.py: Sources trending topics (currently from CSV).
- content_generator.py: Interfaces with Google Gemini API to create prompts, images, captions.
- instagram_uploader.py: Handles Instagram login and uploads.

## 💡 Customization and Extension

- Integrate `pytrends` for real-time Google Trends.
- Add support for Pinterest, Twitter, etc.
- Implement scheduling via APScheduler.
- Customize images with Pillow (watermarks, overlays).

## ⚠️ Important Considerations

- **API Usage & Costs:** Monitor your Google Gemini API usage and cost.
- **Instagram Policy:** Avoid frequent/spammy posts; automation may breach Instagram's Terms of Service.

## 📜 License

Licensed under the MIT License. See `LICENSE` for details.
"""
