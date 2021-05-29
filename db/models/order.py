from sqlalchemy import Integer, Column, ARRAY, \
    Float, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from .base import BaseModel
from .delivery_hours import DBDeliveryHours


class DBOrder(BaseModel):
    __tablename__ = 'orders'

    delivery_hours = relationship(DBDeliveryHours, backref="orders", passive_deletes=True)


    order_id = Column(Integer, primary_key=True)
    courier_id = Column(Integer, ForeignKey('couriers.courier_id', ondelete='CASCADE'))
    weight = Column(Float(precision=2), nullable=False)
    region = Column(Integer, nullable=False)
    assign_time = Column(TIMESTAMP(timezone=True), nullable=True)
    complete_time = Column(TIMESTAMP(timezone=True), nullable=True)
    assign_ids = Column(ARRAY(Integer), nullable=True)