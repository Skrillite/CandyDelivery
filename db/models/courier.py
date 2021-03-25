from sqlalchemy import Integer, Column, VARCHAR, ARRAY
from sqlalchemy.orm import relationship

from .base import BaseModel
from sqlalchemy.dialects.postgresql import TSRANGE
from db.helpers import TIMERANGE


class DBCourier(BaseModel):
    __tablename__ = 'couriers'

    #orders = relationship("DBOrder", backref="couriers")

    courier_id = Column(Integer, unique=True, nullable=False, primary_key=True)
    courier_type = Column(VARCHAR(4), nullable=False)
    regions = Column(ARRAY(Integer), nullable=False)
    working_hours = Column(ARRAY(TIMERANGE))
