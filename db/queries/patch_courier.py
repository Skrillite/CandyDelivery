from api.request.courier import DefCourier
from db.database import DBSession
from db.models import DBCourier
from db.exception import DBDoesntExistsException


def patch_courier(_id: int, session: DBSession, courier: DefCourier):
    if not session.get_courier_by_id(_id):
        raise DBDoesntExistsException

    patch_data = {
        key: value
        for key, value in courier.__dict__.items()
        if value is not None
    }

    session.query(DBCourier).filter(DBCourier.courier_id == _id).update(patch_data)

