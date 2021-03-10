from typing import Type
from .base import CrudBase, ModelType
from models import Record

class CrudRecord(CrudBase):
    def __init__(self, model: Type[ModelType]):
        super().__init__(model)



crud_record = CrudRecord(Record)