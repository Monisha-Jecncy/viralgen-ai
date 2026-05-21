import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

    # Image settings
    IMAGE_WIDTH = 1024
    IMAGE_HEIGHT = 1024

    # Generation settings
    JOB_TIMEOUT_SECONDS = 120

    # Style prompts for different brand voices
    STYLE_PROMPTS = {
        "luxury": "Create a premium luxury advertisement. Use elegant, sophisticated language. Emphasize exclusivity, craftsmanship, and status. Visual should be opulent with gold/black tones.",
        "modern": "Create a contemporary, cutting-edge advertisement. Use trendy language, focus on innovation and technology. Visual should be sleek with neon/blue tones.",
        "minimal": "Create a minimalist, clean advertisement. Use very concise, powerful words. Less is more approach. Visual should be simple with white space.",
        "funny": "Create a humorous, entertaining advertisement. Use witty jokes, puns, and lighthearted language. Visual should be colorful and playful.",
        "professional": "Create a professional, trustworthy advertisement. Use formal language, focus on benefits and features. Visual should be clean and corporate.",
    }
