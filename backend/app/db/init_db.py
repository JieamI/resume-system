from sqlalchemy import text
import uuid
import random

from core.config import settings

# def init_cv(target, connection, **kw):
#     depts = ["技术部", "设计部", "产品部", "产品运营", "新媒体运营", "人力资源部", "杂志部"]
#     for i in range(0, 20):
#         connection.execute(
#             target.insert(),
#             {
#                 "sno": str(uuid.uuid4())[0: 13],
#                 "department": random.choice(depts),
#                 "sign": random.choice([True, False]),
#                 "state": random.choice(["未审核", "简历通过", "笔试完成", "面试完成", "已录取", "未录取"]),
#                 "name": "jack",
#                 "sex": random.choice(["男", "女"]),
#                 "birthday": "2020-11-20",
#                 "hometown": "四川内江",
#                 "nation": str(i),
#                 "college": "信息工程学院",
#                 "grade": "2020",
#                 "proclass": "电信2012",
#                 "dormitory": "南湖三舍",
#                 "phone": "12541253248",
#                 "qq": "1548562457",
#                 "mail": "1732615826@qq.com",
#                 "experience": "的爱妃上飞机飞啊飞粉丝风格吃饭金额哦i时间覅分附件二哦i书法家",
#                 "introduce": "发我打封测怀惠会从i阿红除非阿辉发警匪片踹会赤壁u撒好吃的hi但是佛",
#                 "reason": "阿萨ui我菜单黑i出覅就从i吃哦阿姐次哦不i啥除非"
#             }
#         )

def init_dept(target, connection, **kw):
    depts = ["技术部", "设计部", "产品部", "产品运营", "新媒体运营", "人力资源部", "杂志部"]
    for dept in depts:
        connection.execute(target.insert(), {"name": dept})



def init_user(target, connection, **kw):
    nick = ["jack", "mike", "rose", "john", "luna", "jie", "lucy"]
    depts = ["技术部", "设计部", "产品部", "产品运营", "新媒体运营", "人力资源部", "杂志部"]
    
    connection.execute(
        target.insert(), 
        {"nick": "supervisor", 
        "openid": settings.SUPERVISOR_USERNAME + settings.SUPERVISOR_PASSWORD, 
        "role": str(["supervisor"]), 
        "department": "人力资源部"}
    )
    

    # 以下待注释
    # for i, v in enumerate(nick):
    #     connection.execute(
    #         target.insert(), 
    #         {"nick": v, "department": depts[i], "openid": uuid.uuid4()}
    #     )


# def init_record(target, connection, **kw):
#     depts = ["技术部", "设计部", "产品部", "产品运营", "新媒体运营", "人力资源部", "杂志部"]
#     operator = ["jack", "mike", "rose", "john", "luna", "jie", "lucy"]
#     operation = ["更新了信息模板", "打开了部门展示", "关闭了部门展示", "提升了xxx的权限", "移除了管理员xxx"]
#     for i in range(0, 10):
#         connection.execute(
#             target.insert(),
#             {
#                 "department": random.choice(depts),
#                 "operator": random.choice(operator),
#                 "operation": random.choice(operation)
#             }
#         )


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
    default_value = text(
        '''
        CREATE TRIGGER default_value BEFORE INSERT ON cvinfo
        FOR EACH ROW SET new.time = now(), new.comment = "[]"
    
        '''    
    )
    connection.execute(default_value)
