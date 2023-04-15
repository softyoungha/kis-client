from functools import wraps
from typing import Optional, Dict, Callable, Tuple, TypeVar, Union, Any, Type, overload

from pydantic import BaseModel

from kis.exceptions import KISSessionNotFound
from .schema import ResponseData
from .client import KisClientBase

DataSchema = TypeVar("DataSchema", bound=BaseModel)
OrderFunc = Callable[..., Tuple[dict, dict, dict]]


@overload
def order(
        url: str,
        **kwargs
) -> Callable[[OrderFunc], Dict[str, Any]]:
    ...


@overload
def order(
        url: str,
        data_class: Type[DataSchema]
) -> Callable[[OrderFunc], ResponseData[DataSchema]]:
    ...


def order(
        url: str,
        data_class=None
):
    def decorator(func: OrderFunc):
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

            headers, params, body = func(*args, **kwargs)

            # get hash key
            hash_key = session.get_hash_key(body).hash
            headers.update({"hashkey": hash_key})

            # post
            res = session.post(
                url,
                headers=headers or None,
                params=params or None,
                json=body
            )
            if data_class:
                return ResponseData[data_class](**res.json())
            return res.json()

        return wrapper

    return decorator
