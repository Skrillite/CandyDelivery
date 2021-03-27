import psycopg2.extras
from sqlalchemy.engine import create_engine
from sqlalchemy.dialects import postgresql
from sqlalchemy import types
from sqlalchemy.exc import ProgrammingError

from configs.configs import ApplicationConfigs


class TimeRange(psycopg2.extras.Range):
    pass


class TIMERANGE(postgresql.ranges.RangeOperators, types.UserDefinedType):
    def get_col_spec(self, **kwargs):
        return 'timerange'


def timerange_type_reg():
    engine = create_engine(ApplicationConfigs.database.url)

    with engine.connect() as connection:
        try:
            connection.execute("CREATE TYPE timerange AS RANGE(subtype = time)")
        except ProgrammingError as e:
            pass

    connection = engine.raw_connection()
    cursor = connection.cursor()

    psycopg2.extras.register_range('timerange', TimeRange, cursor, globally=True)

    cursor.close()
    connection.close()