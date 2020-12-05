from datetime import datetime
from typing import List
from config import datetime_format


def sort_and_set_datetime(datetimes: List[datetime]) -> List[str]:
    datetimes.sort()
    datetime_str = [item.strftime(datetime_format) for item in datetimes]
    return list(set(datetime_str))
