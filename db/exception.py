from base_exception import ApplicationException


class DBIntegrityException(ApplicationException):
    def __init__(self):
        super(DBIntegrityException, self).__init__(
            status_code=500,
            message="DBIntegrityException"
        )


class DBDataException(ApplicationException):
    def __init__(self):
        super(DBDataException, self).__init__(
            status_code=500,
            message="DBDataException"
        )


class DBDoesntExistsException(ApplicationException):
    def __init__(self):
        super(DBDoesntExistsException, self).__init__(
            status_code=400
        )
