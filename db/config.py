import os

from dotenv import load_dotenv

load_dotenv()

class PotgresConfig():
    name = os.getenv('POSTGRES_DB', 'CandyDelivery')
    user = os.getenv('POSTGRES_USER', 'admin')
    password = os.getenv('POSTGRES_PASSWORD', 'temp')
    host = os.getenv('POSTGRES_HOST', 'CandyDelivery-db')
    port = os.getenv('POSTRES_PORT', '5432')
    url = rf'postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}'
