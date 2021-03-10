from typing import Dict, List, Optional
from pydantic import BaseModel
from .base import BasicSchema

class UpdateState(BaseModel):
    show: bool

class InfoResponse(BasicSchema):
    show: bool
    mail_template: List[Dict]

class RecordResponse(BasicSchema):
    class Record(BaseModel):
        operator: str
        operation: str
        time: str
    data: List[Record]

class TemplateResponse(BasicSchema):
    class Template(BaseModel):
        title: str
        content: str
    mail_template: List[Optional[Template]]

class AddTemplate(BaseModel):
    title: str
    content: str
    
class RemoveTemplate(BaseModel):
    target: List[str]

class EditTemplate(BaseModel):
    title: str
    content: str