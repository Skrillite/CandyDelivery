from sqlalchemy import Integer, Column, ForeignKey

from .base import BaseModel


class DBRegions(BaseModel):
    __tablename__ = 'regions'

    courier_id = Column(Integer, ForeignKey('couriers.courier_id', ondelete='CASCADE'),
                        primary_key=True)
    region = Column(Integer, primary_key=True)
