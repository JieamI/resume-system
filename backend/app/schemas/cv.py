from typing import List, Optional
from pydantic import BaseModel
from .base import BasicSchema

class CvInfoRequest(BaseModel):
    sno: str
    department: str
    name: str
    sex: str
    birthday: str
    hometown: str
    nation: str
    college: str
    grade: str
    proclass: str
    dormitory: str
    phone: str
    qq: str
    mail: str
    experience: str
    introduce: str
    reason: str

class CvinfoResponse(BasicSchema):
    class Response(CvInfoRequest):
        sign: bool
        state: str
        comment: str
        time: str
    cvList: List[Optional[Response]]

class UpdateState(BaseModel):
    sno: str
    name: str
    state: str

class UpdateSign(BaseModel):
    sno: str
    name: str
    sign: bool

class CvComment(BaseModel):
    sno: str
    content: str
    score: int

class RemoveCv(BaseModel):
    class targetCv(BaseModel):
        sno: str
        name: str
    target: List[targetCv]