
class ApplicationException(Exception):
    def __init__(self, status_code, body: dict = None, message: str = None):
        self.status_code = status_code

        if body is None and message is not None:
            self.body = {'message': message}
        else:
            self.body = body
