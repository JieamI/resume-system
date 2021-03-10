from typing import List
from .base import BasicSchema

class LoginResponse(BasicSchema):
    access_token: str
    nick: str
    department: str
    scopes: List[str]

class UpdateResponse(BasicSchema):
    nick: str
    department: str
    scopes: List[str]