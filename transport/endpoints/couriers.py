from sanic.request import Request
from sanic.response import BaseHTTPResponse

from transport.base import SanicEndpoint
from api.request import courier_list_validation, Courier

from db.queries import overwrite_couriers
from db.database import DBSession


class CreateCouriers(SanicEndpoint):

    async def method_post(self, request: Request, body: dict, *args, **kwargs) \
            -> BaseHTTPResponse:
        session: DBSession = self.database_context.get().make_session()

        request_model: list[Courier] = courier_list_validation(body)
        overwrite_couriers(session, request_model)
        session.commit_session()

        _id = [{'id:': i.courier_id} for i in request_model]

        return await self.make_response_json(status=201, body={'couriers': _id})
