from sqlalchemy import Integer, Column, ForeignKey

from .base import BaseModel


class DBAssignIds(BaseModel):
    __tablename__ = 'assign_ids'

    order_id = Column(Integer, ForeignKey('orders.order_id', ondelete='CASCADE'),
                        primary_key=True)
    assign_id = Column(Integer, ForeignKey('orders.order_id', ondelete='CASCADE'),
                        primary_key=True)
