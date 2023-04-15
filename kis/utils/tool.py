from dateutil.parser import parse
from datetime import datetime, date
from typing import Union, overload, Optional
import yaml


def load_yaml(file_path: str) -> Union[list, dict]:
    """ load yaml file """
    with open(file_path, "r", encoding="utf-8") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data


@overload
def as_datetime(obj: Union[str, datetime, date]) -> datetime:
    ...


@overload
def as_datetime(obj: Union[str, datetime, date], fmt: str) -> str:
    ...


def as_datetime(obj: Union[str, datetime, date], fmt: Optional[str] = None):
    """ convert str to datetime """
    if isinstance(obj, datetime):
        datetime_obj = obj
    elif isinstance(obj, date):
        datetime_obj = datetime.combine(obj, datetime.min.time())
    else:
        datetime_obj = parse(obj)
    if fmt:
        return datetime_obj.strftime(fmt)
    return datetime_obj
