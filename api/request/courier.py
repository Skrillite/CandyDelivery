from pydantic import BaseModel, ValidationError, validator

from api.exceptions import RequestValidationException
from .helpers import time_range_check
from db.helpers import TimeRange

courier_lifting_capacity = {
    'foot': 10,
    'bike': 15,
    'car': 50
}


class Courier(BaseModel):
    courier_id: int
    courier_type: str
    regions: list[int]
    working_hours: list[str]

    @validator('working_hours')
    def time_range_validation(cls, working_hours):
        for _time_range in working_hours:
            time_range_check(_time_range)

        for idx, i in enumerate(working_hours):
            _time = i.split('-')
            working_hours[idx] = TimeRange(_time[0], _time[1], '[]')

        return working_hours

    @validator('courier_type')
    def courier_types_check(cls, courier_type):
        if courier_type not in ['foot', 'bike', 'car']:
            raise ValueError(f'{courier_type} is not allowed type')
        return courier_lifting_capacity[courier_type]

    class Config:
        extra = 'forbid'


def courier_list_validation(input_dict: dict) -> list[Courier]:
    invalid_list: list[dict[str, int]] = []
    valid_list: list[Courier] = []

    try:
        for courier_obj in input_dict['data']:
            try:
                valid_list.append(Courier.parse_obj(courier_obj))
            except ValidationError as e:
                invalid_list.append({'id': courier_obj['courier_id']})
    except KeyError as e:
        raise RequestValidationException(body={'validation_error': f"missing {e.__str__()} field"})

    if invalid_list:
        raise RequestValidationException(body={'validation_error': {'couriers': invalid_list}})

    return valid_list


class DefCourier(Courier):
    def __new__(cls, *args, **kwargs):
        if 'courier_id' in cls.__fields__:
            del cls.__fields__['courier_id']
        return super(DefCourier, cls).__new__(cls)

    courier_type: str = None
    regions: list[int] = None
    working_hours: list[str] = None

    @validator('courier_type')
    def courier_types_check(cls, courier_type):
        if courier_type not in ['foot', 'bike', 'car']:
            raise ValueError(f'{courier_type} is not allowed type')
        return courier_lifting_capacity[courier_type]


def patch_courier_validation(input_dict: dict) -> DefCourier:
    try:
        obj = DefCourier.parse_obj(input_dict)
    except ValidationError as e:
        raise RequestValidationException

    return obj


class CourierID(BaseModel):
    courier_id: int

    class Config:
        extra = 'forbid'


def courier_id_validation(input_dict: dict) -> CourierID:
    try:
        obj = CourierID.parse_obj(input_dict)
    except ValidationError as e:
        raise RequestValidationException

    return obj
