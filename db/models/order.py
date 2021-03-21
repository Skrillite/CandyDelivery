from sqlalchemy import Integer, Column, VARCHAR, ARRAY, Float

from .base import BaseModel

class DBOrder(BaseModel):
    __tablename__ = 'orders'

    order_id = Column(Integer, unique=True, primary_key=True, nullable=False)
    weight = Column(Float(precision=2), nullable=False)
    region = Column(Integer, nullable=False)
    delivery_hours = Column(ARRAY(VARCHAR(11)), nullable=False)