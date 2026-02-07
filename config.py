import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# DeepSeek
DEFAULT_MODEL = "deepseek-chat"
DEFAULT_SYSTEM_PROMPT = "Voce e um assistente util e amigavel. Responda em portugues."
MAX_HISTORY_MESSAGES = 20
MAX_RESPONSE_TOKENS = 2048
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# Database
DATABASE_PATH = "bot_data.db"
