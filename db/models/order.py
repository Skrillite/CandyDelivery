from sqlalchemy import Integer, Column, ARRAY, \
    Float, ForeignKey, DateTime

from .base import BaseModel
from db.helpers import TIMERANGE


class DBOrder(BaseModel):
    __tablename__ = 'orders'

    order_id = Column(Integer, unique=True, primary_key=True, nullable=False)
    courier_id = Column(Integer, ForeignKey('couriers.courier_id'))
    weight = Column(Float(precision=2), nullable=False)
    region = Column(Integer, nullable=False)
    delivery_hours = Column(ARRAY(TIMERANGE), nullable=False)
    assign_time = Column(DateTime, nullable=True)
    complete_time = Column(DateTime, nullable=True)