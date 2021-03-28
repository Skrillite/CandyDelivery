from api.request.courier import Courier
from db.database import DBSession
from db.models import DBCourier
from db.exception import DBDoesntExistsException


def create_courier(session: DBSession, courier: Courier) -> DBCourier:
    new_courier = DBCourier(
        courier_id=courier.courier_id,
        lifting_capacity=courier.courier_type,
        regions=courier.regions,
        working_hours=courier.working_hours
    )

    # if session.get_courier_by_id(courier.courier_id):
    #     raise DBCourierExistsException(courier.courier_id)

    session.add_model(new_courier)

    return new_courier


def overwrite_couriers(session: DBSession, couriers: list[Courier]):
    session.delete_table_data(DBCourier)

    for cr in couriers:
        create_courier(session, cr)
