from api.request.courier import DefCourier
from db.database import DBSession
from db.models import DBCourier, DBOrder
from db.exception import DBDoesntExistsException


def patch_courier(_id: int, session: DBSession, courier: DefCourier):
    if not session.get_courier_by_id(_id):
        raise DBDoesntExistsException

    patch_data = {
        key: value
        for key, value in courier.__dict__.items()
        if value is not None
    }

    if 'courier_type' in patch_data and patch_data['courier_type']:
        patch_data['lifting_capacity'] = patch_data['courier_type']
        del patch_data['courier_type']

    session.query(DBCourier).filter(DBCourier.courier_id == _id).update(patch_data, synchronize_session=False)

    unsuitable: set[int] = session._session.execute(
        f"""select orders.order_id from orders
            join couriers on orders.courier_id = couriers.courier_id
            join
                (select (not(dh && wh)).bool_and as bl, order_id
                 from orders, couriers,
                lateral unnest(orders.delivery_hours) as dh,
                lateral unnest(couriers.working_hours) as wh
                where couriers.courier_id = {_id}
                group by order_id, couriers.courier_id) as bll
            on bll.order_id = orders.order_id
            where orders.complete_time is Null
            and orders.courier_id = {_id}
            and (bll.bl = True
            or orders.weight > couriers.lifting_capacity
            or orders.region != all(couriers.regions))""").fetchall()

    unsuitable = {i[0] for i in unsuitable}

    if unsuitable:
        session.query(DBOrder)\
            .filter(DBOrder.order_id.in_(unsuitable))\
            .update({'assign_time': None, 'courier_id': None, 'assign_ids': None}, synchronize_session=False)

        ids = session.query(DBOrder.assign_ids).filter(DBOrder.courier_id == _id).first()
        if ids:
            new_assign_ids = [i for i in ids.assign_ids if i not in unsuitable]
            session.query(DBOrder).filter(DBOrder.courier_id == _id)\
                .update({'assign_ids': new_assign_ids}, synchronize_session=False)