from os import getenv
from dotenv import load_dotenv

load_dotenv()


class SanicConfig:
    host = getenv('HOSTNAME', 'localhost')
    port = int(getenv('PORT', 8000))
    workers = int(getenv('WORKERS', 1))
    debug = bool(int(getenv('DEBUG', 0)))
