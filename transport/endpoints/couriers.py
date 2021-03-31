from sanic.request import Request
from sanic.response import BaseHTTPResponse

from transport.base import SanicEndpoint
from api.request import *

from db.queries import write_couriers, patch_courier, get_courier_stats, check_ex_courier
from db.database import DBSession
from db.models import DBCourier
from api.exceptions import RequestValidationException
from api.request.courier import courier_lifting_capacity


class CreateCouriers(SanicEndpoint):

    async def method_post(self, request: Request, body: dict, *args, **kwargs) \
            -> BaseHTTPResponse:
        session: DBSession = self.database_context.get().make_session()

        request_model: list[Courier] = courier_list_validation(body)

        exs = check_ex_courier(session, [i.courier_id for i in request_model])
        if exs:
            raise RequestValidationException(body={"validation_error": {"couriers": [{"id": i} for i in exs]}})

        write_couriers(session, request_model)
        session.commit_session()

        _id = [{'id:': i.courier_id} for i in request_model]

        return await self.make_response_json(status=201, body={'couriers': _id})


class PatchCourier(SanicEndpoint):

    async def method_patch(self, request: Request, body: dict, *args, **kwargs) \
            -> BaseHTTPResponse:
        session: DBSession = self.database_context.get().make_session()

        request_model: DefCourier = patch_courier_validation(body)
        patch_courier(request.match_info['id'], session, request_model)

        session.commit_session()

        courier_row: DBCourier = session.get_courier_by_id(request.match_info['id'])
        courier_dict = {
            'courier_id': courier_row.courier_id,
            'courier_type': {v: k for k, v in courier_lifting_capacity.items()}[courier_row.lifting_capacity],
            'regions': courier_row.regions,
            'working_hours': [time_range.lower.__str__() + '-' + time_range.upper.__str__() for time_range in courier_row.working_hours]
        }

        return await self.make_response_json(status=200, body=courier_dict)


class GetCourier(SanicEndpoint):

    async def method_get(self, request: Request, body: dict, *args, **kwargs) \
            -> BaseHTTPResponse:
        session: DBSession = self.database_context.get().make_session()

        courier_id = request.match_info['id']
        courier_data = get_courier_stats(session, courier_id)

        return await self.make_response_json(courier_data)
