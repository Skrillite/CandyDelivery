from typing import Tuple
from contextvars import ContextVar

from transport import endpoints


def get_routes(database_context: ContextVar) -> Tuple:
    return (
        endpoints.HealthEndpoint(
            uri='/', methods=['GET'], context=database_context,
        ),
        endpoints.CreateCouriers(
            uri='/couriers', methods=['POST'], context=database_context,
        ),
        endpoints.CreateOrders(
            uri='/orders', methods=['POST'], context=database_context,
        ),
        endpoints.PatchCourier(
            uri='/couriers/<id>', methods=['PATCH'], context=database_context,
        ),
        endpoints.AssignOrders(
            uri='/orders/assign', methods=['POST'], context=database_context,
        ),
        endpoints.CompleteOrder(
            uri='/orders/complete', methods=['POST'], context=database_context,
        )
    )
