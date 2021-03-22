from pydantic import BaseModel, ValidationError, validator

from api.exceptions import RequestValidationException
from .helpers import time_range_check


class Order(BaseModel):
    order_id: int
    weight: float
    region: int
    delivery_hours: list[str]

    @validator('delivery_hours')
    def time_range_check(cls, delivery_hours):
        for _range in delivery_hours:
            time_range_check(_range)
        return delivery_hours

    class Config:
        extra = 'forbid'


def order_list_validation(input_dict: dict) -> list[Order]:
    invalid_list: list[dict[str, int]] = []
    valid_list: list[Order] = []

    try:
        for order_obj in input_dict["data"]:
            try:
                valid_list.append(Order.parse_obj(order_obj))
            except ValidationError as e:
                invalid_list.append({'id': order_obj['order_id']})
    except KeyError as e:
        raise RequestValidationException(body={'validation_error': f"missing {e.__str__()} field"})

    if invalid_list:
        raise RequestValidationException(body={'validation_error': {'couriers': invalid_list}})

    return valid_list
