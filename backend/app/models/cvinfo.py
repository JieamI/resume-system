from sqlalchemy import String, Boolean, Enum, Text
from sqlalchemy import Table, Column, ForeignKey, text
from datetime import datetime

from sqlalchemy.sql.expression import false

from db import metadata

CvInfo = Table(
    "cvinfo",
    metadata,
    Column("sno", String(64), primary_key = True, index = True),
    Column("department", Enum(
        "技术部", "设计部", "产品部", "产品运营", "新媒体运营", "人力资源部", "杂志部"
        ),
        ForeignKey("department.name"),
        primary_key = True,
        nullable = false,
        index = True),
    Column("sign", Boolean, server_default = text("0")),
    Column("state", Enum("未审核", "简历通过", "笔试完成", "面试完成", "已录取", "未录取"), server_default = "未审核"),
    Column("name", String(160)),
    Column("sex", Enum("男", "女")),
    Column("birthday", String(160)),
    Column("hometown", String(160)),
    Column("nation", String(160)),
    Column("college", String(160)),
    Column("grade", String(160)),
    Column("proclass", String(160)),
    Column("dormitory", String(160)),
    Column("phone", String(160)),
    Column("qq", String(160)),
    Column("mail", String(160)),
    Column("experience", Text),
    Column("introduce", Text),
    Column("reason", Text),
    Column("comment", Text),
    Column("time", String(160), default = lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
)