from datetime import time
import json

from pydantic import BaseModel, ValidationError, validator

from api.exceptions import ApiValidationException


class Courier(BaseModel):
    courier_id: int
    courier_type: str
    regions: list[str]
    working_hours: list[str]

    @validator('working_hours')
    def time_range_check(cls, working_hours):
        for _time_range in working_hours:
            for _time in _time_range.split('-'):
                try:
                    time.fromisoformat(_time)
                except ValueError as e:
                    raise ValueError(f'{_time_range} is invalid time range format')
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
                invalid_list.append({'id:': courier_obj['courier_id']})
    except KeyError as e:
        raise ApiValidationException(message='invalid json structure')
    # except json.JSONDecodeError as e:
    #     raise ApiValidationException(message='json decode error')

    if invalid_list:
        raise ApiValidationException(message=json.dumps({'couriers': invalid_list}))

    return valid_list
