from datetime import time
from sqlalchemy import text
import uuid
import random

from core.config import settings

def init_cv(target, connection, **kw):
    depts = ["技术部", "设计部", "产品部", "产品运营", "新媒体运营", "人力资源部", "杂志部"]
    m = [i for i in range(3, 5)]
    d = [i for i in range(1, 31)]
    h = [i for i in range(0, 24)]
    ms = [i for i in range(0, 60)]
   
    for i in range(0, 20):
        connection.execute(
            target.insert(),
            {
                "sno": "%013d" %(i),
                "department": random.choice(depts),
                "sign": random.choice([True, False]),
                "state": random.choice(["未审核", "简历通过", "笔试完成", "面试完成", "已录取", "未录取"]),
                "name": f"JieamI_{i}",
                "sex": random.choice(["男", "女"]),
                "birthday": "2020-11-20",
                "hometown": "湖北武汉",
                "nation": "汉族",
                "college": "信息工程学院",
                "grade": "2020",
                "proclass": "电信2021",
                "dormitory": "南湖三舍",
                "phone": "12541253248",
                "qq": "1548562457",
                "mail": "1732615826@qq.com",
                "experience": f"这是我的经历{i}",
                "introduce": f"这是我的自我介绍{i}",
                "reason": f"这是我加入该部门的理由{i}",
                "time": "2021-%02d-%02d %02d:%02d:%02d" %(random.choice(m),random.choice(d),random.choice(h),random.choice(ms),random.choice(ms))
            }
        )


def init_dept(target, connection, **kw):
    depts = ["技术部", "设计部", "产品部", "产品运营", "新媒体运营", "人力资源部", "杂志部"]
    for dept in depts:
        connection.execute(target.insert(), {"name": dept})


def init_user(target, connection, **kw):
    nick = ["jack", "mike", "rose", "john", "luna", "jie", "lucy", "Amy", "Joke"]
    depts = ["技术部", "设计部", "产品部", "产品运营", "新媒体运营", "人力资源部", "杂志部"]
    
    connection.execute(
        target.insert(), 
        {"nick": "supervisor", 
        "openid": settings.SUPERVISOR_USERNAME + settings.SUPERVISOR_PASSWORD, 
        "role": str(["supervisor"]), 
        "department": "人力资源部"}
    )
    connection.execute(
        target.insert(), 
        {"nick": "administrator", 
        "openid": settings.ADMINISTRATOR_USERNAME + settings.ADMINISTRATOR_PASSWORD, 
        "role": str(["administrator"]), 
        "department": "技术部"}
    )
    connection.execute(
        target.insert(), 
        {"nick": "user", 
        "openid": settings.USER_USERNAME + settings.USER_PASSWORD, 
        "role": str(["user"]), 
        "department": "技术部"}
    )

    for i, v in enumerate(nick):
        connection.execute(
            target.insert(), 
            {"nick": v, "department": random.choice(depts), "openid": uuid.uuid4()}
        )


def init_record(target, connection, **kw):
    depts = ["技术部", "设计部", "产品部", "产品运营", "新媒体运营", "人力资源部", "杂志部"]
    operator = ["jack", "mike", "rose", "john", "luna", "jie", "lucy", "Amy", "Joke"]
    operation = ["更新了信息模板", "打开了部门展示", "关闭了部门展示", "提升了xxx的权限", "移除了管理员xxx"]
    for i in range(0, 10):
        connection.execute(
            target.insert(),
            {
                "department": random.choice(depts),
                "operator": random.choice(operator),
                "operation": random.choice(operation)
            }
        )


def dept_trigger(target, connection, **kw):
    default_value = text(
        '''
        CREATE TRIGGER default_template BEFORE INSERT ON department
        FOR EACH ROW SET new.mail_template = "[]"
    
        '''    
    )
    connection.execute(default_value)


def record_trigger(target, connection, **kw):
    default_time = text(
        '''
        CREATE TRIGGER record_time BEFORE INSERT ON record
        FOR EACH ROW SET new.time = now()
    
        '''    
    )
    connection.execute(default_time)


def cvinfo_trigger(target, connection, **kw):
    # 如果插入的记录已经包含time字段则不自动设置time
    default_value = text(
        '''
        CREATE TRIGGER default_value BEFORE INSERT ON cvinfo
        FOR EACH ROW 
        BEGIN
            SET new.comment = "[]";
            IF new.time is null THEN
                SET new.time = now();
            END IF;
        END
    
        '''    
    )
    connection.execute(default_value)
