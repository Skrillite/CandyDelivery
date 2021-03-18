import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, TIMESTAMP ##


class BaseModel(declarative_base()):
    __abstract__ = True

    id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )

    def __repr__(self):
        return f'{self.__class__.__name__}'
