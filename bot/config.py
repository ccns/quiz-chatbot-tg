import os
from dotenv import load_dotenv

def _getenv(key) -> str:
    value = os.environ.get(key)
    if not value:
        raise NameError(
            f'Environment key "{key}" not found, recheck your .env file.'
        )
    return value

load_dotenv()
HOST = _getenv("HOST")
TOKEN = _getenv("TOKEN")
