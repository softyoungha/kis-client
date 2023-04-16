from dateutil.parser import parse
from datetime import datetime, date
from typing import Union, overload, Optional
import yaml


def read_text(file_path: str, encoding: str = "utf-8") -> str:
    with open(file_path, "r", encoding=encoding) as file:
        return file.read()


def write_text(text: str, file_path: str, encoding: str = "utf-8"):
    with open(file_path, "w", encoding=encoding) as file:
        file.write(text)


def load_yaml(file_path: str, encoding: str = "utf-8") -> Union[list, dict]:
    """load yaml file """
    with open(file_path, "r", encoding=encoding) as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data


def save_yaml(
        data: Union[list, dict], file_path: str, encoding: str = "utf-8"
):
    """save yaml file"""
    with open(file_path, "w", encoding=encoding) as file:
        file.write(yaml.dump(data))


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
