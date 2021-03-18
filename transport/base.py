from typing import Iterable
from sanic.request import Request
from sanic.response import BaseHTTPResponse, json
from http import HTTPStatus

class SanicEndpoint:

    def __init__(self, uri: str, methods: Iterable, *args, **kwargs):
        self.uri = uri
        self.methods = methods
        self.__name__ = self.__class__.__name__

    async def __call__(self, request: Request, *args, **kwargs):
        return await self.handler(request)

    async def handler(self, request: Request, *args, **kwargs):

        body = {}
        body.update(await self.import_body_json(request))
        body.update(await self.import_body_headers(request))

        return await self._method(request, body, *args, **kwargs)

    async def _method(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        method = request.method.lower()
        func_name = f'method_{method}'

        if hasattr(self, func_name):
            func = getattr(self, func_name)
            return await func(request, body, *args, **kwargs)
        return await self.method_not_allowed()

    @staticmethod
    async def make_response_json(
            body: dict = None,
            message: str = None,
            status: int = 200) -> BaseHTTPResponse:
        if body is None:
            body = {
                'message': message or HTTPStatus(status).phrase(),
            }

        return json(body, status)

    @staticmethod
    async def import_body_json(request: Request) -> dict:
        if 'application/json' in request.content_type and request.json is not None:
            return dict(request.json)
        return {}

    @staticmethod
    async def import_headers_json(request: Request) -> dict:
        return {
            header : value
            for header, value in request.headers.items()
            if header.lower().startswith('-x') ##
        }

    async def method_not_allowed(self) -> BaseHTTPResponse:
        return await self.make_response_json(status=501)

    async def method_not_implemented(self) -> BaseHTTPResponse:
        return await self.make_response_json(status=501)

    async def method_get(self, request: Request, body: dict, *args, **kwargs):
        return await self.method_not_implemented()

    async def method_post(self, request: Request, body: dict, *args, **kwargs):
        return await self.method_not_implemented()

    async def method_patch(self, request: Request, body: dict, *args, **kwargs):
        return await self.method_not_implemented()

    async def method_delete(self, request: Request, body: dict, *args, **kwargs):
        return await self.method_not_implemented()
