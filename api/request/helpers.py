from datetime import time


def time_range_check(time_range: str):
    if len(time_list := time_range.split('-')) != 2:
        raise ValueError
    for _time in time_list:
        try:
            time.fromisoformat(_time)
        except ValueError as e:
            raise ValueError(f'{time_range} is invalid time range format')