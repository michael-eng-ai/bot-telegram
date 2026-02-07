import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tenta carregar .env local (no Railway nao existe, e ok)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

# Debug: mostra quais vars estao presentes (sem mostrar valores)
logger.info(f"TELEGRAM_BOT_TOKEN presente: {bool(TELEGRAM_BOT_TOKEN)}")
logger.info(f"DEEPSEEK_API_KEY presente: {bool(DEEPSEEK_API_KEY)}")

# DeepSeek
DEFAULT_MODEL = "deepseek-chat"
DEFAULT_SYSTEM_PROMPT = "Voce e um assistente util e amigavel. Responda em portugues."
MAX_HISTORY_MESSAGES = 20
MAX_RESPONSE_TOKENS = 2048
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# Database
DATABASE_PATH = "bot_data.db"
