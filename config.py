import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Railway limita variaveis custom — DS key pode vir junto com GEMINI separada por |
_gemini_raw = os.environ.get("GEMINI_API_KEY", "")
if "|" in _gemini_raw:
    GEMINI_API_KEY, DEEPSEEK_API_KEY = _gemini_raw.split("|", 1)
else:
    GEMINI_API_KEY = _gemini_raw or None
    DEEPSEEK_API_KEY = os.environ.get("DS_API_KEY")

logger.info(f"TELEGRAM_BOT_TOKEN presente: {bool(TELEGRAM_BOT_TOKEN)}")
logger.info(f"DEEPSEEK_API_KEY presente: {bool(DEEPSEEK_API_KEY)}")
logger.info(f"GEMINI_API_KEY presente: {bool(GEMINI_API_KEY)}")

# DeepSeek (texto)
DEFAULT_MODEL = "deepseek-chat"
DEFAULT_SYSTEM_PROMPT = "Voce e um assistente util e amigavel. Responda em portugues."
MAX_HISTORY_MESSAGES = 20
MAX_RESPONSE_TOKENS = 2048
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# Gemini (imagem + audio)
GEMINI_MODEL = "gemini-2.5-flash-preview-04-17"

# Database
DATABASE_PATH = "bot_data.db"
