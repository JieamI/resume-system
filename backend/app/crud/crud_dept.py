from typing import Type
from .base import CrudBase, ModelType
from models import Department

class CrudDept(CrudBase):
    def __init__(self, model: Type[ModelType]):
        super().__init__(model)

    
crud_dept = CrudDept(Department)