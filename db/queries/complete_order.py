from api.request import OrderComplete
from db.database import DBSession
from db.models import DBOrder
from db.exception import DBDoesntExistsException


def complete_order_query(session: DBSession, rdata: OrderComplete):
    assign_ids: list[int] = session.query(DBOrder.assign_ids).filter((DBOrder.courier_id == rdata.courier_id)
                                                                     & (DBOrder.order_id == rdata.order_id)
                                                                     & (DBOrder.complete_time == None)).first()

    if assign_ids:
        session.query(DBOrder).filter(DBOrder.order_id.in_(assign_ids.assign_ids)
                                      & (DBOrder.order_id != rdata.order_id)
                                      & (DBOrder.complete_time == None))\
            .update({"assign_time": rdata.complete_time}, synchronize_session=False)

        session.query(DBOrder).filter(DBOrder.order_id == rdata.order_id)\
            .update({"complete_time": rdata.complete_time}, synchronize_session=False)
    else:
        raise DBDoesntExistsException
