from functools import wraps
from typing import Optional, Dict, Callable, Tuple, TypeVar, Union, Any, overload

from kis.client.schema.response import ResponseData, ResponseDataDetail
from kis.exceptions import KISBadArguments
from typing import Type, List
from pydantic import BaseModel
from . import KisClientBase

DataSchema = TypeVar("DataSchema", bound=Type[BaseModel])


class Order:
    # order
    OriginReturn = TypeVar("OriginReturn", bound=Tuple[dict, dict, dict])
    OriginFunc = Callable[..., OriginReturn]
    NewReturn = Union[
        Dict[str, Any],
        ResponseData[DataSchema],
    ]
    NewFunc = Callable[..., NewReturn]


def order(
        url: str,
        data_class: Optional[DataSchema] = None
) -> Callable[[Order.OriginFunc], Order.NewFunc]:
    def decorator(func: Order.OriginFunc) -> Order.NewFunc:
        @wraps(func)
        def wrapper(client: KisClientBase, *args, **kwargs):
            headers, params, body = func(client, *args, **kwargs)
            res = client.session.post(
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
