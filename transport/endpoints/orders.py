from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.exceptions import RequestValidationException
from api.request import order_list_validation, Order
from transport.base import SanicEndpoint
from db.queries import write_orders, check_ex_order
from db.database import DBSession


class CreateOrders(SanicEndpoint):

    async def method_post(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        session: DBSession = self.database_context.get().make_session()

        request_model: list[Order] = order_list_validation(body)

        exs = check_ex_order(session, [i.order_id for i in request_model])
        if exs:
            raise RequestValidationException(body={"validation_error": {"orders": [{"id": i} for i in exs]}})

        write_orders(session, request_model)
        session.commit_session()

        _id = [{'id:': i.order_id} for i in request_model]

        return await self.make_response_json(status=201, body={'orders': _id})
