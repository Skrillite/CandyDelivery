from http import HTTPStatus


class ApplicationException(Exception):
    def __init__(self, status_code=500, body: dict = None, message: str = None):
        self.status_code = status_code

        if body is None:
            self.body = {'message': message or HTTPStatus(status_code).phrase}
        else:
            self.body = body
