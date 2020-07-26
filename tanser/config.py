from starlette.config import Config
from starlette.datastructures import URL

config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=False)

API_PORT = config("API_PORT", cast=int, default=8000)
API_ADDRESS = config("API_ADDRESS", cast=str, default="0.0.0.0")

TELEGRAM_REST_API_URL = config("TELEGRAM_REST_API_URL", cast=URL)
TELEGRAM_API_ID = config("TELEGRAM_API_ID", cast=int)
TELEGRAM_API_HASH = config("TELEGRAM_API_HASH", cast=str)
TELEGRAM_BOT_TOKEN = config("TELEGRAM_BOT_TOKEN", cast=str)
