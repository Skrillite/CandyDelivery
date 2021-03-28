from base_exception import ApplicationException


class RequestValidationException(ApplicationException):
    def __init__(self, body: dict = None):
        super(RequestValidationException, self).__init__(status_code=400, body=body)


class ResponseValidationException(ApplicationException):
    def __init__(self, message: str):
        super(ResponseValidationException, self).__init__(status_code=500, message=message)
