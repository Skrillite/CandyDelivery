from sanic.exceptions import SanicException


class ApiValidationException(SanicException):
    def __init__(self, status_code=400, message=None):
        super(ApiValidationException, self).__init__(status_code=status_code, message=message)


class ApiResponseValidationException(SanicException):
    status_code = 500
