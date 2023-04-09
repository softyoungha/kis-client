from functools import wraps
from typing import Optional, Dict, Callable, Tuple, TypeVar, Union, Any, overload

from kis.client.schema.response import ResponseData, ResponseDataDetail
from kis.exceptions import KISBadArguments
from typing import Type, List
from pydantic import BaseModel
from . import KisClientBase

# typing
DataSchema = TypeVar("DataSchema", bound=Type[BaseModel])
SummarySchema = TypeVar("SummarySchema", bound=Type[BaseModel])
DetailSchema = TypeVar("DetailSchema", bound=Type[Union[BaseModel, List[BaseModel]]])
OriginReturn = TypeVar("OriginReturn", bound=Tuple[dict, dict])
OriginFunc = Callable[..., OriginReturn]
NewReturn = Union[
    Dict[str, Any],
    ResponseData[DataSchema],
    ResponseDataDetail[SummarySchema, DetailSchema]
]
NewFunc = Callable[..., NewReturn]

@overload
def fetch(url: str, **kwargs) -> Callable[[OriginFunc], Callable[..., Dict[str, Any]]]: ...

@overload
def fetch(
        url: str,
        data_class: DataSchema,
        **kwargs
) -> Callable[
    [OriginFunc],
    Callable[..., ResponseData[DataSchema]]
]: ...


@overload
def fetch(
        url: str,
        summary_class: SummarySchema,
        detail_class: DetailSchema,
        **kwargs
) -> Callable[
    [OriginFunc],
    Callable[..., ResponseDataDetail[SummarySchema, DetailSchema]]
]: ...


def fetch(
        url: str,
        data_class: Optional[DataSchema] = None,
        summary_class: Optional[SummarySchema] = None,
        detail_class: Optional[DetailSchema] = None,
) -> Callable[[OriginFunc], NewFunc]:
    def decorator(func: OriginFunc) -> NewFunc:

        @wraps(func)
        def wrapper(client: KisClientBase, *args, **kwargs):
            headers, params = func(client, *args, **kwargs)
            res = client.session.get(
                url,
                headers=headers or None,
                params=params or None
            )
            data = res.json()
            if data_class:
                return ResponseData[data_class](**data)
            if summary_class or detail_class:
                if summary_class and detail_class:
                    return ResponseDataDetail[summary_class, detail_class](**data)
                raise KISBadArguments()
            return data

        return wrapper

    return decorator