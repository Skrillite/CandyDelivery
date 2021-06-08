import datetime
from sqlalchemy import distinct, update

from api.request.courier import CourierID
from db.database import DBSession
from db.models import DBCourier, DBOrder, DBDeliveryHours, DBRegions, DBWorkingHours


def assign(session: DBSession, courier_id: CourierID, assign_time: datetime.datetime) -> list[int]:
    orders = session.query(DBOrder, DBDeliveryHours.hours) \
        .join(DBDeliveryHours, DBOrder.order_id == DBDeliveryHours.order_id).subquery()

    couriers = session.query(DBCourier, DBWorkingHours.hours, DBRegions.region) \
        .join(DBWorkingHours, DBWorkingHours.courier_id == DBCourier.courier_id) \
        .join(DBRegions, DBRegions.courier_id == DBCourier.courier_id).subquery()

    suitable_orders = session.query(orders) \
        .join(couriers, orders.c.region == couriers.c.region) \
        .filter((orders.c.weight <= couriers.c.lifting_capacity)
                & (orders.c.hours.overlaps(couriers.c.hours))
                & (orders.c.courier_id == None)).subquery()

    suitable_orders_ids = [i[0] for i in session.query(distinct(suitable_orders.c.order_id)).all()]

    session.query(DBOrder).filter(DBOrder.order_id.in_(suitable_orders_ids)) \
        .update({
                    DBOrder.courier_id: courier_id.courier_id,
                    DBOrder.assign_time: assign_time
                }, synchronize_session=False)


    return suitable_orders_ids
