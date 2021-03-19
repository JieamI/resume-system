# Databases provides simple asyncio support for a range of databases.
from sqlalchemy import create_engine, MetaData, event

from core.config import settings
from .init_db import init_dept, init_user, init_cv, init_record, cvinfo_trigger, record_trigger, dept_trigger
from .session import database


metadata = MetaData()
import models

# 监听department表的创建，创建后初始化数据
event.listen(models.Department, "after_create", dept_trigger)
event.listen(models.Record, "after_create", record_trigger)
event.listen(models.CvInfo, "after_create", cvinfo_trigger)

event.listen(models.Department, "after_create", init_dept)
event.listen(models.User, "after_create", init_user)
event.listen(models.CvInfo, "after_create", init_cv)
event.listen(models.Record, "after_create", init_record)


engine = create_engine(settings.DATABASE_URI)
metadata.drop_all(engine)
metadata.create_all(engine) 

