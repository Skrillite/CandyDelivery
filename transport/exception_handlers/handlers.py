from sanic.request import Request
from sanic.response import json, raw

from api.exceptions import *
from db.exception import *
from base_exception import ApplicationException


def get_exc_handlers():
    return (
        RequestValidationHandler,
        ResponseValidationHandler,
        EmptyRequestValidationExceptionHandler,
        DBCourierExistExceptionHandler
    )


class BasicValidationHandler:
    exception: ApplicationException

    @staticmethod
    def handler(request: Request, exception: ApplicationException):
        if exception.body is not None:
            return json(exception.body, exception.status_code)
        else:
            return raw('', exception.status_code)


class RequestValidationHandler(BasicValidationHandler):
    exception = RequestValidationException


class ResponseValidationHandler(BasicValidationHandler):
    exception = ResponseValidationException


class EmptyRequestValidationExceptionHandler(BasicValidationHandler):
    exception = EmptyValidationException


class DBCourierExistExceptionHandler(BasicValidationHandler):
    exception = DBDoesntExistsException
