from typing import Type
from .base import CrudBase, ModelType
from models import CvInfo

class CrudCv(CrudBase):
    def __init__(self, model: Type[ModelType]):
        super().__init__(model)



crud_cv = CrudCv(CvInfo)