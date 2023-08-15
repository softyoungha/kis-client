import os
from datetime import datetime, time, date
from typing import Union, overload, Optional, List

import pandas as pd
import pytz
import yaml
from dateutil.parser import parse
from pydantic import BaseModel


def read_text(file_path: str, encoding: str = "utf-8") -> str:
    with open(file_path, "r", encoding=encoding) as file:
        return file.read()


def write_text(text: str, file_path: str, encoding: str = "utf-8"):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
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
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
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


def is_korea_market_open() -> bool:
    """Check if the market is open."""
    now = datetime.now()
    if now.weekday() >= 5:
        # 토/일
        return False
    if now.hour < 9 or (now.hour >= 15 and now.minute > 30):
        # 9시 이전, 15시 이후
        return False
    if now.hour == 9 and now.minute < 5:
        # 9시 5분 이전
        return False
    return True


def is_us_market_hours():
    # 현재 시간을 EST로 변환
    now_est = datetime.now().astimezone(pytz.timezone('US/Eastern'))

    # 미국 주식 시장이 열려 있는 평일인지 확인
    if 0 <= now_est.weekday() <= 4:
        # 미국 주식 시장이 열려 있는 시간인지 확인
        if time(hour=9, minute=30) <= now_est.time() <= time(hour=16):
            return True
    return False


def model_to_df(data: List[BaseModel]) -> pd.DataFrame:
    rows = [row.dict() for row in data]
    return pd.DataFrame(rows)
