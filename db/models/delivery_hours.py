from sqlalchemy import Integer, Column, ForeignKey

from .base import BaseModel
from db.helpers import TIMERANGE


class DBDeliveryHours(BaseModel):
    __tablename__ = 'delivery_hours'

    order_id = Column(Integer, ForeignKey('orders.order_id', ondelete='CASCADE'),
                        primary_key=True)
    hours = Column(TIMERANGE, primary_key=True)
