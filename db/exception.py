from sanic.exceptions import SanicException

class DBIntegrityException(SanicException):
    status_code = 500

class DBCourierExistsException(SanicException):
    def __init__(self, courier_id):
        super(DBCourierExistsException, self).__init__(status_code=400, message=f'{courier_id} is exists')

