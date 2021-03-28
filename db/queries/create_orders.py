from api.request.order import Order
from db.database import DBSession
from db.models import DBOrder


def create_order(session: DBSession, order: Order) -> DBOrder:
    new_order = DBOrder(
        order_id=order.order_id,
        weight=order.weight,
        region=order.region,
        delivery_hours=order.delivery_hours
    )

    session.add_model(new_order)

    return new_order


def overwrite_orders(session: DBSession, orders: list[Order]):
    session.delete_table_data(DBOrder)

    for order in orders:
        create_order(session, order)
