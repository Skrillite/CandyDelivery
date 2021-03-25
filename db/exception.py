from base_exception import ApplicationException
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


class DBCourierExistsException(ApplicationException):
    def __init__(self):
        super(DBCourierExistsException, self).__init__(
            status_code=400
        )
