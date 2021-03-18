from sqlalchemy import Integer, Column, VARCHAR, ARRAY

from .base import BaseModel


class DBCourier(BaseModel):
    __tablename__ = 'employees'

    courier_id = Column(Integer, unique=True, nullable=False)
    courier_type = Column(VARCHAR(4), nullable=False)
    regions =  Column(ARRAY(Integer), nullable=False)
    working_hourse = Column(ARRAY(VARCHAR(11)), nullable=False)
