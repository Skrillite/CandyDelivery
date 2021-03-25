from api.request.courier import DefCourier
from db.database import DBSession
from db.models import DBCourier
from db.exception import DBCourierExistsException


def patch_courier(_id: int, session: DBSession, courier: DefCourier):
    if session.get_courier_by_id(_id) is None:
        raise DBCourierExistsException

    patch_data = {
        key: value
        for key, value in courier.__dict__.items()
        if value is not None
    }

    session.query(DBCourier).where(DBCourier.courier_id == _id).update(patch_data)

