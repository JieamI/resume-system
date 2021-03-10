from databases import Database

from core.config import settings
from main import app

# 创建数据库会话实例，为数据库操作提供异步IO支持
database = Database(settings.DATABASE_URI)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()