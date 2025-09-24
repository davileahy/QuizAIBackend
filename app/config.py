import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", None)

if GEMINI_API_KEY:
    logger.info("✅ Variável GEMINI_API_KEY carregada com sucesso do .env")
else:
    logger.warning("⚠️ GEMINI_API_KEY não encontrada. Defina no arquivo .env")
