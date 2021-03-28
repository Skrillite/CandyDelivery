from sqlalchemy.sql import func

from db.models import DBCourier, DBOrder
from db.database import DBSession
from db.exception import DBDoesntExistsException
from api.request.courier import courier_lifting_capacity


def get_courier_stats(session: DBSession, courier_id: int) -> dict:
    courier: DBCourier = session.query(DBCourier) \
        .filter(DBCourier.courier_id == courier_id).first()

    if not courier:
        raise DBDoesntExistsException

    lead_time = []

    for reg in courier.regions:
        lead_time.append(session.query(func.avg(DBOrder.complete_time - DBOrder.assign_time))
                         .filter((DBOrder.region == reg) & (DBOrder.courier_id == courier_id)).first())

    lead_time = [i[0] for i in lead_time if i[0] is not None]
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
        'working_hours': [time_range.__str__().strip('[]') for time_range in courier.working_hours],
        'earnings': 0
    }

    if len(lead_time) > 0:
        courier_data.update({
            'rating': float(f"{(60 * 60 - min(min(lead_time).total_seconds(), 60 * 60)) / (60 * 60) * 5:.2f}"),
            'earnings': len(lead_time) * (500 * courier_rate[courier.lifting_capacity])
        })

    return courier_data
