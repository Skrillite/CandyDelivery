from sqlalchemy.sql import func
from datetime import timedelta

from db.models import DBCourier, DBOrder
from db.database import DBSession
from db.exception import DBDoesntExistsException
from api.request.courier import courier_lifting_capacity


def get_courier_stats(session: DBSession, courier_id: int) -> dict:
    courier: DBCourier = session.query(DBCourier) \
        .filter(DBCourier.courier_id == courier_id).first()

    if not courier:
        raise DBDoesntExistsException

    avg_by_reg = []

    for reg in courier.regions:
        avg_by_reg.append(session.query(func.avg(DBOrder.complete_time - DBOrder.assign_time)).group_by(DBOrder.order_id)
                         .filter((DBOrder.region == reg)
                                 & (DBOrder.courier_id == courier_id)
                                 & (DBOrder.complete_time != None)).all())

    completed_order: int = 0
    lead_time: list[timedelta] = []

    for time_in_reg in avg_by_reg:
        if len(time_in_reg) > 0:
            counter: timedelta = timedelta(0)
            for i in time_in_reg:
                counter += i[0]

            completed_order += len(time_in_reg)
            lead_time.append(counter / len(time_in_reg))

    courier_type = {v: k for k, v in courier_lifting_capacity.items()}[courier.lifting_capacity]

    courier_rate = {
        10: 2,
        15: 5,
        50: 9
    }

    courier_data = {
        'courier_id': courier.courier_id,
        'courier_type': courier_type,
        'regions': courier.regions,
        'working_hours': [time_range.lower.__str__() + '-' + time_range.upper.__str__() for time_range in courier.working_hours],
        'earnings': 0
    }

    if completed_order > 0:
        courier_data.update({
            'rating': float(f"{(60 * 60 - min(min(lead_time).total_seconds(), 60 * 60)) / (60 * 60) * 5:.2f}"),
            'earnings': completed_order * (500 * courier_rate[courier.lifting_capacity])
        })

    return courier_data
