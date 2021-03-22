from sanic.exceptions import SanicException


class DBIntegrityException(SanicException):
    def __init__(self):
        super(DBIntegrityException, self).__init__(
            status_code=530,
            message="DBIntegrityException"
        )


class DBDataException(SanicException):
    def __init__(self):
        super(DBDataException, self).__init__(
            status_code=530,
            message="DBDataException"
        )


class DBCourierExistsException(SanicException):
    def __init__(self, courier_id):
        super(DBCourierExistsException, self).__init__(status_code=400, message=f'{courier_id} is exists')
