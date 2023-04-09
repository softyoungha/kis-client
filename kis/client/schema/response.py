from typing import TypeVar, Type, Generic, Optional, Union, List

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

Data = TypeVar("Data", bound=Type[BaseModel])
Summary = TypeVar("Summary", bound=Type[BaseModel])
Detail = TypeVar("Detail", bound=Union[Type[BaseModel], List[Type[BaseModel]]])


class ResponseData(GenericModel, Generic[Data]):
    rt_cd: str = Field(alias="rt_cd", title="성공 실패 여부")
    msg_cd: str = Field(alias="msg_cd", title="응답코드")
    msg: str = Field(alias="msg1", title="응답메시지")
    data: Data = Field(alias="output", title="응답상세")


class ResponseDataDetail(GenericModel, Generic[Summary, Detail]):
    rt_cd: str = Field(alias="rt_cd", title="성공 실패 여부")
    msg_cd: str = Field(alias="msg_cd", title="응답코드")
    msg: str = Field(alias="msg1", title="응답메시지")
    summary: Summary = Field(alias="output1", title="응답상세1")
    detail: Detail = Field(alias="output2", title="응답상세2")
