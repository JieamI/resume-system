from typing import List
from .base import BasicSchema
from pydantic import BaseModel

class AuthorityResponse(BasicSchema):
    class Authority(BaseModel):
        key: int
        nick: str
        department: str
        state: str
        openid: str
    data: List[Authority]
