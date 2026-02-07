import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini
DEFAULT_MODEL = "gemini-2.0-flash"
DEFAULT_SYSTEM_PROMPT = "Voce e um assistente util e amigavel. Responda em portugues."
MAX_HISTORY_MESSAGES = 20
MAX_RESPONSE_TOKENS = 2048

# Database
DATABASE_PATH = "bot_data.db"
