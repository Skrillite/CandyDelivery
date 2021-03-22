from api.request.courier import DefCourier
from db.database import DBSession
from db.models import DBCourier


def patch_courier(_id: int, session: DBSession, courier: DefCourier):
    if courier.courier_type is not None:
        session.query(DBCourier).where(DBCourier.courier_id == _id).update({"courier_type": courier.courier_type})
    if courier.regions is not None:
        session.query(DBCourier).where(DBCourier.courier_id == _id).update({"regions": courier.regions})
    if courier.working_hours is not None:
        session.query(DBCourier).where(DBCourier.courier_id == _id).update({"working_hours": courier.working_hours})




