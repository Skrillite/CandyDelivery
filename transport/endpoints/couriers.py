from sanic.request import Request
from sanic.response import BaseHTTPResponse

from transport.base import SanicEndpoint
from api.request import courier_list_validation

from db.queries import create_couriers
from db.database import DBSession
from db.exception import DBCourierExistsException, DBIntegrityException


class CreateCouriers(SanicEndpoint):

    async def method_post(self, request: Request, body: dict, *args, **kwargs) \
            -> BaseHTTPResponse:

        session: DBSession = self.database_context.get().make_session()

        request_model = courier_list_validation(body)

        try:
            db_employee = create_couriers(session, request_model)
        except DBCourierExistsException as e:
            raise self.method_not_implemented()

        try:
            session.commit_session()
        except DBIntegrityException as e:
            raise self.method_not_implemented()

        return await self.make_response_json(message='ok!')
