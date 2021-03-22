from pydantic import BaseModel, ValidationError, validator

from api.exceptions import RequestValidationException
from .helpers import time_range_check


class Courier(BaseModel):
    courier_id: int
    courier_type: str
    regions: list[int]
    working_hours: list[str]

    @validator('working_hours')
    def time_range_validation(cls, working_hours):
        for _time_range in working_hours:
            time_range_check(_time_range)
        return working_hours

    @validator('courier_type')
    def courier_types_check(cls, courier_type):
        if courier_type not in ['foot', 'bike', 'car']:
            raise ValueError(f'{courier_type} is not allowed type')
        return courier_type

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
