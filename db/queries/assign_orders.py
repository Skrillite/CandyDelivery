import datetime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql.ranges import RangeOperators
from functools import partial

from api.request.courier import CourierID
from db.database import DBSession
from db.models import DBCourier, DBOrder
from db.helpers import TIMERANGE, TimeRange


def assign(session: DBSession, courier_id: CourierID, assign_time: datetime.datetime) -> list[int]:
    orders: list[int] = session._session.execute(f"""select order_id from orders, couriers,
                                                    lateral unnest(orders.delivery_hours) as dh,
                                                    lateral unnest(couriers.working_hours) as wh
                                                    where couriers.courier_id = {courier_id.courier_id}
                                                    and orders.courier_id is Null
                                                    and orders.weight <= couriers.lifting_capacity
                                                    and orders.region = any(couriers.regions)
                                                    group by order_id
                                                    having (wh && dh).bool_or""").fetchall()
    for idx, i in enumerate(orders):
        orders[idx] = i[0]

    if orders:
        session.query(DBOrder).filter(DBOrder.order_id.in_(orders)) \
            .update({"courier_id": courier_id.courier_id, "assign_ids": orders, "assign_time": assign_time}
                    , synchronize_session=False)

    return orders
