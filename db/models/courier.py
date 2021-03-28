from sqlalchemy import Integer, Column, VARCHAR, ARRAY
from sqlalchemy.orm import relationship, backref

from .base import BaseModel
from db.helpers import TIMERANGE
from db.models.order import DBOrder


class DBCourier(BaseModel):
    __tablename__ = 'couriers'

    orders = relationship(DBOrder, backref="couriers", passive_deletes=True)

    courier_id = Column(Integer, unique=True, nullable=False, primary_key=True)
    lifting_capacity = Column(Integer, nullable=False)
    regions = Column(ARRAY(Integer), nullable=False)
    working_hours = Column(ARRAY(TIMERANGE))
