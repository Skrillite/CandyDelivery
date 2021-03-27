from sanic.request import Request
from sanic.response import BaseHTTPResponse

from transport.base import SanicEndpoint
from api.request import order_complete_validation, OrderComplete
from db.database import DBSession
from db.queries import complete_order_query


class CompleteOrder(SanicEndpoint):

    async def method_post(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        session: DBSession = self.database_context.get().make_session()

        request_model: OrderComplete = order_complete_validation(body)
        complete_order_query(session, request_model)
        session.commit_session()

        return await self.make_response_json({"order_id": request_model.order_id}, status=200)
