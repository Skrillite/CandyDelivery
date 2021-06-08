from api.request.courier import Courier
from db.database import DBSession
from db.models import DBCourier
from db.models import DBRegions
from db.models import DBWorkingHours


def create_courier(session: DBSession, courier: Courier) -> DBCourier:
    new_courier = DBCourier(
        courier_id=courier.courier_id,
        lifting_capacity=courier.courier_type,
    )

    session.add_model(new_courier)

    for region in courier.regions:
        session.add_model(
            DBRegions(
                courier_id=courier.courier_id,
                region=region
            )
        )

    for working_hours in courier.working_hours:
        session.add_model(
            DBWorkingHours(
                courier_id=courier.courier_id,
                hours=working_hours
            )
        )

    return new_courier


def write_couriers(session: DBSession, couriers: list[Courier]):
    #session.delete_table_data(DBCourier)

    for cr in couriers:
        create_courier(session, cr)
