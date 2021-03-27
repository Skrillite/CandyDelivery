from datetime import datetime

from sanic.request import Request
from sanic.response import BaseHTTPResponse

from transport.base import SanicEndpoint
from api.request import courier_id_validation, CourierID
from db.queries import assign
from db.database import DBSession


class AssignOrders(SanicEndpoint):

    async def method_post(self, request: Request, body: dict, *args, **kwargs) \
            -> BaseHTTPResponse:
        session: DBSession = self.database_context.get().make_session()

        assign_time = datetime.utcnow()
        request_model: CourierID = courier_id_validation(body)
        order_ids: list[int] = assign(session, request_model, assign_time)
        session.commit_session()

        body = {"orders": [{'id': i} for i in order_ids]}
        if order_ids:
            body.update({'assign_time': assign_time.isoformat()[:-4] + 'Z'})
        return await self.make_response_json(body)