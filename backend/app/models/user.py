from sqlalchemy import Integer, String, Enum
from sqlalchemy import Table, Column, ForeignKey

from db import metadata

User = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key = True, index = True),
    Column("nick", String(160), nullable = False),
    Column("openid", String(160), unique = True, nullable = False, index = True),
    Column("department", Enum(
        '技术部', '设计部', '产品部', '产品运营', '新媒体运营', '人力资源部', '杂志部'
        ),
        ForeignKey("department.name"),
        nullable = False),
    # 考虑到未来可能存在的权限扩展，更改为以列表形式存储权限
    # Column("role", Enum("user", "administrator", "supervisor"), nullable = False, server_default = "user")
    Column("role", String(60), nullable = False, server_default = "['user']")
)





