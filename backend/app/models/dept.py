from sqlalchemy import Boolean, Enum, Text
from sqlalchemy import Table, Column, text

from db import metadata

Department = Table(
    "department",
    metadata,
    Column("name", Enum(
        '技术部', '设计部', '产品部', '产品运营', '新媒体运营', '人力资源部', '杂志部'
        ),
        primary_key = True),
    Column("show", Boolean, server_default = text("1")),
    Column("mail_template", Text)
)