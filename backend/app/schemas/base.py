from pydantic import BaseModel


class BasicSchema(BaseModel):
    code: int = 0
