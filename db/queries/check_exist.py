from db.database import DBSession
from db.models import DBCourier, DBOrder


def check_ex_courier(session: DBSession, courier_ids_list: list[int]) -> list[int]:
    exist_ids = session.query(DBCourier.courier_id).filter(DBCourier.courier_id.in_(courier_ids_list)).all()
    return [i[0] for i in exist_ids]


def check_ex_order(session: DBSession, order_ids_lst: list[int]) -> list[int]:
    exist_ids = session.query(DBOrder.order_id).filter(DBOrder.order_id.in_(order_ids_lst)).all()
    return [i[0] for i in exist_ids]
