from sanic.request import Request
from sanic.response import json

from api.exceptions import RequestValidationException, ResponseValidationException
from db.exception import DBDataException, DBIntegrityException, DBCourierExistsException


def get_exc_handlers():
    return (
        RequestValidationHandler,
        ResponseValidationHandler
    )


class BasicValidationHandler:
    exception: Exception

    @staticmethod
    def handler(request: Request, exception: Exception):
        return json(exception.body, exception.status_code)


class RequestValidationHandler(BasicValidationHandler):
    exception = RequestValidationException


class ResponseValidationHandler(BasicValidationHandler):
    exception = ResponseValidationException
