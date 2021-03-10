from typing import Any, Dict, Type, TypeVar, Generic, List
from sqlalchemy import Table

from db import database

ModelType = TypeVar("ModelType", bound = Table)

class CrudBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model


    async def select_one_by(self, condition: Any = True) -> Dict:
        query = self.model.select().where(condition)
        res = await database.fetch_one(query)
        return dict(res.items()) if res else res


    async def select_by(self, condition: Any = True, order_by: Any = True) -> List[Dict]:
        query = self.model.select().where(condition).order_by(order_by)
        res_lis =  await database.fetch_all(query)
        return [dict(res.items()) for res in res_lis] if res_lis else []
        

    async def create(self, items: List[Dict]) -> None:
        query = self.model.insert()
        await database.execute_many(query, values = items)


    async def update(self, *, condition: Any = True, **args) -> None:
        query = self.model.update().values(args).where(condition)
        await database.execute(query)


    async def delete(self, condition: Any = True) -> None:
        query = self.model.delete().where(condition)
        await database.execute(query)