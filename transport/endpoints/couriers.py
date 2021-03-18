from sanic.request import Request
from sanic.response import BaseHTTPResponse

from transport.base import SanicEndpoint


class ImportCouriers(SanicEndpoint):
    async def method_post(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        pass