import os

from dotenv import load_dotenv

load_dotenv()

class PotgresConfig():
    name = os.getenv('POSTGRES_DB', 'cundydelivery')
    user = os.getenv('POSTGRES_USER', 'root')
    password = os.getenv('POSTGRES_PASSWORD', 'not_password')
    host = os.getenv('POSTGRES_HOST', 'localhost')
    port = os.getenv('POSTRES_PORT', '5432')
    url = rf'postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}'
