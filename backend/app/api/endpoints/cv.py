from typing import Dict, List
from fastapi import UploadFile, File, Form
from fastapi.param_functions import Body
from sqlalchemy import and_
from fastapi import APIRouter, Security, BackgroundTasks
from datetime import datetime, timedelta

from crud import crud_cv
from models import CvInfo
from core.config import settings
from core.utils import addRecordTask, send_email
from core.depends import get_current_user
from schemas.base import BasicSchema
from schemas.cv import CvinfoResponse, UpdateState, UpdateSign, CvComment, CvInfoRequest, RemoveCv

router = APIRouter()

@router.get("/getinfo", response_model = CvinfoResponse)
async def handleGetCv(
    current_user: Dict = Security(get_current_user, scopes = ["user", "administrator", "supervisor"])
) -> Dict:
    if current_user["department"] == "人力资源部" or "supervisor" in eval(current_user["role"]):
        cvList = await crud_cv.select_by()
    else:
        cvList = await crud_cv.select_by(CvInfo.c.department == current_user["department"])
    
    return {
        "code": 0,
        "cvList": cvList
    }


@router.post("/updatestate", response_model = BasicSchema)
async def updateState(
    cvInfo: UpdateState,
    task: BackgroundTasks,
    current_user: Dict = Security(get_current_user, scopes = ["administrator", "supervisor"])
) -> Dict:
    cv = await crud_cv.select_one_by(CvInfo.c.sno == cvInfo.sno)
    if not cv:
        raise settings.CUSTOM_EXCEPTION(503, "简历信息不存在")
    try:
        await crud_cv.update(
            condition = CvInfo.c.sno == cvInfo.sno,
            state = cvInfo.state
        )
    except Exception as e:
        print(e)
        raise settings.CUSTOM_EXCEPTION(503, "状态更新失败")  
    
    operation = f"将{cvInfo.name}的状态设为{cvInfo.state}"
    task.add_task(addRecordTask, current_user["nick"], operation, current_user["department"])
    return {
        "code": 0
    }


@router.post("/updatesign", response_model = BasicSchema)
async def updateSign(
    cvInfo: UpdateSign,
    task: BackgroundTasks,
    current_user: Dict = Security(get_current_user, scopes = ["administrator", "supervisor"])
) -> Dict:
    cv = await crud_cv.select_one_by(CvInfo.c.sno == cvInfo.sno)
    if not cv:
        raise settings.CUSTOM_EXCEPTION(503, "简历信息不存在")
    
    try:
        await crud_cv.update(
            condition = CvInfo.c.sno == cvInfo.sno,
            sign = cvInfo.sign
        )
    except:
        raise settings.CUSTOM_EXCEPTION(503, "状态更新失败")  
    
    operation = f"标记{cvInfo.name}" if cvInfo.sign else f"取消标记{cvInfo.name}"
    task.add_task(addRecordTask, current_user["nick"], operation, current_user["department"])
    return {
        "code": 0
    }


@router.post("/comment", response_model = BasicSchema)
async def handleComment(
    commentData: CvComment,
    current_user: Dict = Security(get_current_user, scopes = ["user", "administrator", "supervisor"])
) -> Dict:
    cv = await crud_cv.select_one_by(CvInfo.c.sno == commentData.sno)
    if not cv:
        raise settings.CUSTOM_EXCEPTION(503, "简历信息不存在")
    commentList = eval(cv["comment"])
    # 更新评论
    for each in commentList:
        if each["nick"] == current_user["nick"]:
            each["content"] = commentData.content
            each["score"] = commentData.score
            try:
                await crud_cv.update(
                    condition = CvInfo.c.sno == commentData.sno,
                    comment = str(commentList)
                )
            except:
                raise settings.CUSTOM_EXCEPTION(503, "评价提交失败") 
            return { "code": 0 } 
    
    # 新增评论
    newComment = {"nick": current_user["nick"], "content": "", "score": ""}
    newComment["content"] = commentData.content
    newComment["score"] = commentData.score
    commentList.append(newComment)
    try:
        await crud_cv.update(
            condition = CvInfo.c.sno == commentData.sno,
            comment = str(commentList)
        )
    except:
        raise settings.CUSTOM_EXCEPTION(503, "评价提交失败") 
    return {
        "code": 0
    }


@router.post("/getcomment")
async def getComment(
    sno: str = Body(..., embed = True),
    current_user: Dict = Security(get_current_user, scopes = ["user", "administrator", "supervisor"])
) -> Dict:
    cv = await crud_cv.select_one_by(
        CvInfo.c.sno == sno
    )
    commentList = eval(cv["comment"])
    
    return {
        "code": 0,
        "data": commentList
    }


@router.post("/remove", response_model = BasicSchema)
async def removeCv(
    task: BackgroundTasks,
    data: RemoveCv,
    current_user: Dict = Security(get_current_user, scopes = ["administrator", "supervisor"])
) -> Dict:
    targetList = data.target
    for each in targetList:
        try:
            await crud_cv.delete(and_(
                CvInfo.c.sno == each.sno,
                CvInfo.c.name == each.name
            ))
        except Exception as e:
            print(e)
            continue
    
    operation = f"移除了{targetList[0].name}等人的简历"
    task.add_task(addRecordTask, current_user["nick"], operation, current_user["department"])
    return {
        "code": 0
    }


@router.post("/apply", response_model = BasicSchema)
async def applyCv(
    cvinfo: CvInfoRequest,
) -> Dict:
    cv = await crud_cv.select_one_by(and_(
        CvInfo.c.sno == cvinfo.sno,
        CvInfo.c.department == cvinfo.department
    ))
    # 存在则更新简历
    if cv:
        info_dict = cvinfo.dict()
        # 除去联合主键字段，避免更新报错
        info_dict.pop("sno")
        info_dict.pop("department")
        try:
            await crud_cv.update(
                condition = and_(
                    CvInfo.c.sno == cvinfo.sno,
                    CvInfo.c.department == cvinfo.department
                ),
                **info_dict
            )
        except Exception as e:
            print(e)
            raise settings.CUSTOM_EXCEPTION(503, "简历更新失败")
        
    else:
    # 否则创建新简历
        try:
            await crud_cv.create([cvinfo.dict()])
        except Exception as e:
            print(e)
            raise settings.CUSTOM_EXCEPTION(503, "简历提交失败")
    
    return {
        "code": 0
    }


@router.post("/sendemail")
async def sendEmail(
    task: BackgroundTasks,
    current_user: Dict = Security(get_current_user, scopes = ["administrator", "supervisor"]),
    content: str = Form(...),
    subject: str = Form(...),
    recipients: List[str] = Form(...),
    file: UploadFile = File(None)
):
    if not recipients:
        raise settings.CUSTOM_EXCEPTION(503, "没有简历被选中")
    try:
        await send_email(
            recipients,
            subject,
            content,
            file
        )
    except Exception as e:
        print(e)
        raise settings.CUSTOM_EXCEPTION(503, "邮件发送失败")
    
    operation = "发送了邮件"
    task.add_task(addRecordTask, current_user["nick"], operation, current_user["department"])

    return {
        "code": 0
    }

# 获取时间片段
@router.get("/timesection")
async def getTimeSection(
    # current_user: Dict = Security(get_current_user, scopes = ["user", "administrator", "supervisor"]),
):
    section = []
    cvList = await crud_cv.select_by(
        order_by = CvInfo.c.time
    )
    
    if not cvList:
        return {
            "code": 0,
            "section": section
        }

    firstDate = datetime.strptime(cvList[0]["time"], "%Y-%m-%d %H:%M:%S")
    lastDate = datetime.strptime(cvList[-1]["time"], "%Y-%m-%d %H:%M:%S")
    while True:
        nextDate = firstDate + timedelta(days = 6)
        if(nextDate >= lastDate):
            section.append("%02d.%02d-%02d.%02d" %(firstDate.month, firstDate.day, nextDate.month, nextDate.day))
            break

        section.append("%02d.%02d-%02d.%02d" %(firstDate.month, firstDate.day, nextDate.month, nextDate.day))
        firstDate = nextDate + timedelta(days = 1)

    return {
        "code": 0,
        "section": section
    }

@router.get("/statistics")
async def getStatistics(
    start: str,
    end: str,
    # current_user: Dict = Security(get_current_user, scopes = ["user", "administrator", "supervisor"]),
):
    # 兼容末尾判断
    end = end + "1"
    cvList = await crud_cv.select_by(
        and_(
            start <= CvInfo.c.time,
            end >= CvInfo.c.time
        ),
        order_by = CvInfo.c.time
    )
    if not cvList:
        return {
            "code": 0,
            "data": {
                "pie_data": [{"name": dept, "value": 0} for dept in list(settings.DEPARTMENT_MAP.keys())],
                "list_data": {}
            }
        }
    pieCounter = [item["department"] for item in cvList]
    listCounter = [item["time"].split(" ")[0] for item in cvList]
    pie_data =  [{"name": dept, "value": pieCounter.count(dept)} for dept in list(settings.DEPARTMENT_MAP.keys())]
    list_data = {}
    
    first_date = datetime.strptime(start, "%Y-%m-%d")
    for i in range(0, 7):
        date = first_date + timedelta(days = i)
        str_date = datetime.strftime(date, "%Y-%m-%d")
        list_data[str_date] = listCounter.count(str_date)

    return {
        "code": 0,
        "data": {
            "pie_data": pie_data,
            "list_data": list_data
        }
    } 


# import random
# @router.get("/test")
# async def test():
#     m = [i for i in range(3, 5)]
#     d = [i for i in range(1, 31)]
#     h = [i for i in range(0, 24)]
#     ms = [i for i in range(0, 60)]
#     for i in range(0, 20):
#         await crud_cv.update(
#             condition = CvInfo.c.nation == str(i),
#             time = "2021-%02d-%02d %02d:%02d:%02d" %(random.choice(m),random.choice(d),random.choice(h),random.choice(ms),random.choice(ms))
#         )

#     return 0