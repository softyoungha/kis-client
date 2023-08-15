"""
# KIS API 응답 데이터 모델들을 정의합니다.

총 세가지 형태의 데이터 모델이 있습니다.

## Token

app_key, app_secret, account 요청을 보내 받아온 token 데이터입니다.

## ResponseData, ResponseDataDetail

GET을 통한 조회시 KIS에서 응답으로 주는 데이터 형태는 output이 1개인 경우와 2개인 경우(output1, output2)로
나뉩니다. output1개인 경우 ResponseData, output2개인 경우 ResponseDataDetail을 사용합니다.

- ResponseData 로 받아오는 응답은 response.data 로 접근 (output)
- ResponseDataDetail 로 받아오는 응답은 response.summary, response.detail로 접근(각각 output1, output2)

output이 두개인 경우는 보통 output1은 요약 데이터, output2는 상세 데이터로 나뉘어지기 때문에 pydantic model에서
summary, detail로 각각 이름을 정하였습니다. ResponseDataDetail 응답에서 detail은 대부분이 pagination된 결과이기 때문에
연속조회가 가능한 데이터이고, summary는 연속조회시 매번 같은 결과를 받습니다.
"""
from datetime import datetime
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, Field, validator
from pydantic.generics import GenericModel


class Token(BaseModel):
    """token model"""

    access_token: str
    token_type: str
    expired_at: int

    @property
    def is_expired(self) -> bool:
        return datetime.now().timestamp() > self.expired_at


class DestroyTokenRespData(BaseModel):
    code: str
    message: str


class GetHashKeyRespData(BaseModel):
    body: dict = Field(alias="BODY")
    hash: str = Field(alias="HASH")


# About Response
Data = TypeVar("Data")


class ResponseData(GenericModel, Generic[Data]):
    """KIS API 응답 데이터 모델 - only one output"""

    rt_cd: str = Field(alias="rt_cd", title="성공 실패 여부")
    msg_cd: str = Field(alias="msg_cd", title="응답코드")
    msg: str = Field(alias="msg1", title="응답메시지")
    data: Data = Field(alias="output", title="응답상세")
    fk100: Optional[str] = Field(
        "", alias="ctx_area_fk100", title="연속조회검색조건100", repr=False
    )
    nk100: Optional[str] = Field(
        "", alias="ctx_area_nk100", title="연속조회키100", repr=False
    )
    fk200: Optional[str] = Field(
        "", alias="ctx_area_fk200", title="연속조회검색조건200", repr=False
    )
    nk200: Optional[str] = Field(
        "", alias="ctx_area_nk200", title="연속조회키200", repr=False
    )
    tr_id: Optional[str] = Field(alias="tr_id", title="트랜잭션 ID")
    has_next: Optional[bool] = Field(
        alias="tr_cont",
        title="연속조회여부",
        description="F or M: 다음 데이터 존재/ D or E: 마지막 데이터",
    )

    @validator("msg", "fk100", "nk100", pre=True)
    def strip(cls, text: str):
        return text.strip()

    @validator("has_next", pre=True)
    def convert_has_next(cls, tr_cont: str) -> bool:
        if tr_cont:
            return tr_cont in ("F", "M")
        return False


Summary = TypeVar("Summary")
Detail = TypeVar("Detail")


class ResponseDataDetail(GenericModel, Generic[Summary, Detail]):
    """KIS API 응답 데이터 모델 - two output(output1, output2)"""

    rt_cd: str = Field(alias="rt_cd", title="성공 실패 여부")
    msg_cd: str = Field(alias="msg_cd", title="응답코드")
    msg: str = Field(alias="msg1", title="응답메시지")
    summary: Summary = Field(alias="output1", title="응답상세1")
    detail: Optional[Detail] = Field(alias="output2", title="응답상세2")
    fk100: Optional[str] = Field(
        "", alias="ctx_area_fk100", title="연속조회검색조건100", repr=False
    )
    nk100: Optional[str] = Field(
        "", alias="ctx_area_nk100", title="연속조회키100", repr=False
    )
    fk200: Optional[str] = Field(
        "", alias="ctx_area_fk200", title="연속조회검색조건200", repr=False
    )
    nk200: Optional[str] = Field(
        "", alias="ctx_area_nk200", title="연속조회키200", repr=False
    )
    tr_id: str = Field(alias="tr_id", title="트랜잭션 ID")
    has_next: bool = Field(
        alias="tr_cont",
        title="연속조회여부",
        description="F or M: 다음 데이터 존재/ D or E: 마지막 데이터",
    )

    @validator("msg", pre=True)
    def strip(cls, text: str):
        return text.strip()

    @validator("has_next", pre=True)
    def convert_has_next(cls, tr_cont: str) -> bool:
        if tr_cont:
            return tr_cont.upper() in ("F", "M")
        return False
