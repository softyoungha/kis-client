from pydantic import BaseModel, Field


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

