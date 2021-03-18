from typing import Tuple

from transport import endpoints


def get_routes() -> Tuple:
    return (
        endpoints.HealthEndpoint(
            uri='/', methods=['GET', 'POST'],
        ),
        endpoints.ImportCouriers(
            uri='couriers', methods=['POST'],
        )
    )
