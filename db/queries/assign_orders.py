import datetime
from sqlalchemy import distinct

from api.request.courier import CourierID
from db.database import DBSession
from db.models import DBCourier, DBOrder, DBDeliveryHours, DBRegions, DBWorkingHours


def assign(session: DBSession, courier_id: CourierID, assign_time: datetime.datetime) -> list[int]:
    orders = session.query(DBOrder, DBDeliveryHours.hours) \
        .join(DBDeliveryHours, DBOrder.order_id == DBDeliveryHours.order_id).subquery()

    couriers = session.query(DBCourier, DBWorkingHours.hours, DBRegions.region) \
        .join(DBWorkingHours, DBWorkingHours.courier_id == DBCourier.courier_id) \
        .join(DBRegions, DBRegions.courier_id == DBCourier.courier_id).subquery()

    suitable_orders = session.query(distinct(orders.c.order_id)) \
        .join(couriers, orders.c.region == couriers.c.region) \
        .filter((orders.c.weight <= couriers.c.lifting_capacity)
                & (orders.c.hours.overlaps(couriers.c.hours))).subquery()
    # TODO добавить в проверку статус заказа
    suitable_orders_ids = [i[0] for i in session.query(suitable_orders).all()]

    session.query(orders).filter(orders.c.order_id in suitable_orders_ids) \
        .update({"courier_id": courier_id.courier_id, "assign_ids": orders, "assign_time": assign_time}
                , synchronize_session=False)

    return suitable_orders_ids
