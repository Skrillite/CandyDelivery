from sanic.request import Request
from sanic.response import BaseHTTPResponse

from transport.base import SanicEndpoint


class HealthEndpoint(SanicEndpoint):
    async def method_get(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        response = {
            "It's": "alive!"
        }

        return await self.make_response_json(response, status=200)
