import psycopg2.extras
from sqlalchemy.engine import create_engine
from sqlalchemy.dialects import postgresql
from sqlalchemy import types
from sqlalchemy.exc import ProgrammingError
from sqlalchemy_utils.types.range import RangeType, ContinuousRangeComparator
from intervals import AbstractInterval
from datetime import time

from configs.configs import ApplicationConfigs


class PSTimeRange(psycopg2.extras.Range):
    pass


class TIMERANGE(postgresql.ranges.RangeOperators, types.UserDefinedType):
    def get_col_spec(self) -> str:
        return 'timerange'


class TimeInterval(AbstractInterval):
    type = time
    
    def __init__(self, *args, **kwargs):
        self.type = time
        super(TimeInterval, self).__init__(*args, **kwargs)


class TimeRange(RangeType):
    impl = TIMERANGE
    comparator_factory = ContinuousRangeComparator

    def __init__(self, *args, **kwargs):
        super(TimeRange, self).__init__(*args, **kwargs)
        self.interval_class = TimeInterval


def timerange_type_reg():
    engine = create_engine(ApplicationConfigs.database.url)

    with engine.connect() as connection:
        try:
            connection.execute("CREATE TYPE timerange AS RANGE(subtype = time)")
        except ProgrammingError as e:
            pass

    connection = engine.raw_connection()
    cursor = connection.cursor()
    psycopg2.extras.register_range('timerange', PSTimeRange, cursor, globally=True)
    cursor.close()
    connection.close()

    postgresql.base.ischema_names['timerange'] = TIMERANGE