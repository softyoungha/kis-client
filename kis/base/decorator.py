from functools import wraps
from typing import Optional, Dict, Callable, Tuple, TypeVar, Union, Any, overload
from typing import Type, List

from pydantic import BaseModel

from kis.exceptions import KISBadArguments, KISSessionNotFound
from .schema import ResponseData, ResponseDataDetail
from .client import KisClientBase, SubClass

# typing
DataSchema = TypeVar("DataSchema", bound=BaseModel)
SummarySchema = TypeVar("SummarySchema", bound=Union[BaseModel, List[BaseModel]])
DetailSchema = TypeVar("DetailSchema", bound=Union[BaseModel, List[BaseModel]])
Func = Callable[..., Tuple[dict, dict]]
OrderFunc = Callable[..., Tuple[dict, dict, dict]]


@overload
def fetch(url: str) -> Callable[[Func], Callable[..., Dict[str, Any]]]:
    """
    get data from url with no pydantic schema
    :param url: fetch url
    """
    ...


@overload
def fetch(
        url: str,
        data_class: Type[DataSchema]
) -> Callable[
    [Func],
    Callable[..., ResponseData[DataSchema]]
]:
    """
    get data from url with pydantic schema(output1 only)
    :param url: fetch url
    :param data_class: output
    """
    ...


@overload
def fetch(
        url: str,
        summary_class: Type[SummarySchema],
        detail_class: Type[DetailSchema]
) -> Callable[
    [Func],
    Callable[..., ResponseDataDetail[SummarySchema, DetailSchema]]
]:
    """
    get data from url with pydantic schema(output1, output2)
    :param url: fetch url
    :param summary_class: output1
    :param detail_class: output2
    """
    ...


def fetch(
        url: str,
        data_class=None,
        summary_class=None,
        detail_class=None,
):
    """get data from url """

    def decorator(func: Func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            session = None
            for arg in args:
                if isinstance(arg, KisClientBase):
                    # if KisClientBase is passed as first argument
                    session = arg.session
                    break
                try:
                    # if Price, Trading, Balance are passed as first argument
                    client = getattr(arg, "client")
                    if isinstance(client, KisClientBase):
                        session = client.session
                        break
                except AttributeError:
                    continue

            if not session:
                raise KISSessionNotFound()

            headers, params = func(*args, **kwargs)
            res = session.get(
                url,
                headers=headers or None,
                params=params or None
            )
            data = res.json()
            data.update(
                tr_id=res.headers.get("tr_id"),
                tr_cont=res.headers.get("tr_cont")
            )
            from pprint import pprint
            pprint(data)

            if data_class:
                return ResponseData[data_class](**data)
            if summary_class or detail_class:
                if summary_class and detail_class:
                    return ResponseDataDetail[summary_class, detail_class](**data)
                raise KISBadArguments()
            return data

        return wrapper

    return decorator


@overload
def order(
        url: str,
        **kwargs
) -> Callable[[Func], Dict[str, Any]]:
    ...


@overload
def order(
        url: str,
        data_class: Type[DataSchema]
) -> Callable[[Func], ResponseData[DataSchema]]:
    ...


def order(
        url: str,
        data_class=None
):
    def decorator(func: Func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            session = None
            for arg in args:
                if isinstance(arg, KisClientBase):
                    # if KisClientBase is passed as first argument
                    client = arg
                    session = client.session
                    break
                try:
                    # if Price, Trading, Balance are passed as first argument
                    client = getattr(arg, "client")
                    if isinstance(client, KisClientBase):
                        session = client.session
                        break
                except AttributeError:
                    continue

            if session:
                raise KISSessionNotFound()

            headers, body = func(*args, **kwargs)

            # get hash key
            hash_key = session.get_hash_key(body).hash
            headers.update({"hashkey": hash_key})

            # post
            res = session.post(
                url,
                headers=headers or None,
                json=body
            )
            if data_class:
                return ResponseData[data_class](**res.json())
            return res.json()

        return wrapper

    return decorator
