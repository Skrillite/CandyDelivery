from sqlalchemy import Integer, Column, ForeignKey

from .base import BaseModel
from db.helpers import TIMERANGE


class DBWorkingHours(BaseModel):
    __tablename__ = 'working_hours'

    courier_id = Column(Integer, ForeignKey('couriers.courier_id', ondelete='CASCADE'),
                        primary_key=True)
    hours = Column(TIMERANGE, primary_key=True)
