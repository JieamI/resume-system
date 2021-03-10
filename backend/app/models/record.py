from sqlalchemy import Integer, String, Enum
from sqlalchemy import Table, Column, ForeignKey
from datetime import datetime

from db import metadata

Record = Table(
    "record",
    metadata,
    Column("id", Integer, primary_key = True, index = True),
    Column("department", Enum(
        '技术部', '设计部', '产品部', '产品运营', '新媒体运营', '人力资源部', '杂志部'
        ),
        ForeignKey("department.name"),
        nullable = False,
        index = True),
    Column("operator", String(160)),
    Column("operation", String(160)),
    Column("time", String(160), default = lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
)