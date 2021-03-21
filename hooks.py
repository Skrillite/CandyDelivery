from sqlalchemy import create_engine
from contextvars import ContextVar

from configs.configs import ApplicationConfigs
from db.database import DataBase


def init_db_posgresql(database_context: ContextVar):
    engine = create_engine(
        ApplicationConfigs.database.url,
        pool_pre_ping=True,
    )

    database = DataBase(connection=engine)
    assert database.check_connection()

    database_context.set(database)
