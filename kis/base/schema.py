from typing import TypeVar, Type, Union, List, Generic, Optional

from pydantic import BaseModel, Field, validator, root_validator
from pydantic.generics import GenericModel


class CreateTokenRespData(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class DestroyTokenRespData(BaseModel):
    code: str
    message: str


class GetHashKeyRespData(BaseModel):
    body: dict = Field(alias="BODY")
    hash: str = Field(alias="HASH")


# About Response
Data = TypeVar("Data")


class ResponseData(GenericModel, Generic[Data]):
    rt_cd: str = Field(alias="rt_cd", title="성공 실패 여부")
    msg_cd: str = Field(alias="msg_cd", title="응답코드")
    msg: str = Field(alias="msg1", title="응답메시지")
    data: Data = Field(alias="output", title="응답상세")
    fk100: Optional[str] = Field(None, alias="ctx_area_fk100", title="연속조회검색조건100")
    nk100: Optional[str] = Field(None, alias="ctx_area_nk100", title="연속조회키100")
    tr_id: str = Field(alias="tr_id", title="트랜잭션 ID")
    has_next: bool = Field(
        alias="tr_cont",
        title="연속조회여부",
        description="F or M: 다음 데이터 존재/ D or E: 마지막 데이터"
    )

    @validator("msg", "fk100", "nk100", pre=True)
    def strip(cls, text: str):
        return text.strip()

    @validator("has_next", pre=True)
    def convert_has_next(cls, tr_cont: str) -> bool:
        return tr_cont in ("F", "M")


Summary = TypeVar("Summary")
Detail = TypeVar("Detail")


class ResponseDataDetail(GenericModel, Generic[Summary, Detail]):
    rt_cd: str = Field(alias="rt_cd", title="성공 실패 여부")
    msg_cd: str = Field(alias="msg_cd", title="응답코드")
    msg: str = Field(alias="msg1", title="응답메시지")
    summary: Summary = Field(alias="output1", title="응답상세1")
    detail: Detail = Field(alias="output2", title="응답상세2")
    fk100: str = Field("", alias="ctx_area_fk100", title="연속조회검색조건100", repr=False)
    nk100: str = Field("", alias="ctx_area_nk100", title="연속조회키100", repr=False)
    tr_id: str = Field(alias="tr_id", title="트랜잭션 ID")
    has_next: bool = Field(
        alias="tr_cont",
        title="연속조회여부",
        description="F or M: 다음 데이터 존재/ D or E: 마지막 데이터"
    )

    @validator("msg", pre=True)
    def strip(cls, text: str):
        return text.strip()

    @validator("has_next", pre=True)
    def convert_has_next(cls, tr_cont: str) -> bool:
        return tr_cont in ("F", "M")

    @root_validator(pre=True)
    def validate_detail(cls, values: dict) -> dict:
        """
        주식 영업일자 column(stck_bsop_date)이 없는 item 은 제거
        """
        detail = values.get("items")
        if values.get("tr_id") in ("FHKST03010100", "FHKST03010200"):
            values.update(
                detail=[
                    item
                    for item in detail
                    if item.get("stck_bsop_date")
                ]
            )
        return values
