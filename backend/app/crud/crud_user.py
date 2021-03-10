from typing import Type
from .base import CrudBase, ModelType
from models import User

class CrudUser(CrudBase):
    def __init__(self, model: Type[ModelType]):
        super().__init__(model)



crud_user = CrudUser(User)