from sqlalchemy import Integer, Column, VARCHAR, ARRAY
from sqlalchemy.orm import relationship, backref

from .base import BaseModel
from .order import DBOrder
from .regions import DBRegions
from .working_hours import DBWorkingHours


class DBCourier(BaseModel):
    __tablename__ = 'couriers'

    orders = relationship(DBOrder, backref="couriers", passive_deletes=True)
    regions = relationship(DBRegions, backref="couriers", passive_deletes=True)
    working_hours = relationship(DBWorkingHours, backref="couriers", passive_deletes=True)

    courier_id = Column(Integer, primary_key=True)
    lifting_capacity = Column(Integer, nullable=False)
