from typing import Dict, List
from fastapi import APIRouter, Security, BackgroundTasks

from crud import crud_dept, crud_record
from core.config import settings
from core.utils import addRecordTask
from models import Department, Record
from core.depends import get_current_user
from schemas.dept import (
    InfoResponse, 
    UpdateState, 
    RecordResponse, 
    AddTemplate, 
    RemoveTemplate, 
    TemplateResponse,
    EditTemplate
)
from schemas.base import BasicSchema


router = APIRouter()

@router.get("/getinfo", response_model = InfoResponse)
async def handleGetInfo(
    current_user: Dict = Security(get_current_user, scopes = ["user", "administrator", "supervisor"])
) -> Dict:
    dept = await crud_dept.select_one_by(Department.c.name == current_user["department"])
    show = dept["show"]
    template = eval(dept["mail_template"])

    return {
        "code": 0,
        "show": show,
        "mail_template": template
    }

@router.post("/updatestate", response_model = BasicSchema)
async def updateState(
    task: BackgroundTasks,
    data: UpdateState,
    current_user: Dict = Security(get_current_user, scopes = ["administrator", "supervisor"]),
) -> Dict:
    show = data.show
    try:
        await crud_dept.update(
            condition = Department.c.name == current_user["department"],
            show = show
        )
    except:
        raise settings.CUSTOM_EXCEPTION(503, "状态更新失败")
    
    # 添加后台任务
    operation = f"打开了部门展示" if show else "关闭了部门展示"
    task.add_task(addRecordTask, current_user["nick"], operation, current_user["department"])
    return {
        "code": 0
    }


@router.get("/getrecord", response_model = RecordResponse)
async def getRecord(
    current_user: Dict = Security(get_current_user, scopes = ["administrator", "supervisor"])
) -> List[Dict]:
    data = await crud_record.select_by(
        Record.c.department == current_user["department"],
        order_by = Record.c.time.desc()
        )
    return {
        "code": 0,
        "data": data
    }


@router.get("/getshow")
async def getShow() -> List[Dict]:
    showingDept = await crud_dept.select_by(
        Department.c.show == True
    )

    resList = [ item["name"] for item in showingDept ]

    return {
        "code": 0,
        "data": resList
    }


@router.post("/addtemplate", response_model = TemplateResponse)
async def addTemplate(
    task: BackgroundTasks,
    addInfo: AddTemplate,
    current_user: Dict = Security(get_current_user, scopes = ["user", "administrator", "supervisor"])
) -> Dict:
    dept = await crud_dept.select_one_by(
        Department.c.name == current_user["department"]
    )
    template = eval(dept["mail_template"])
    for each in template:
        if each["title"] == addInfo.title:
            raise settings.CUSTOM_EXCEPTION(503, "模板名称已存在")
    
    template.append(addInfo.dict())
    await crud_dept.update(
        condition = Department.c.name == current_user["department"],
        mail_template = str(template)
    )

    # 添加后台任务
    operation = f"添加了信息模板【{addInfo.title}】"
    task.add_task(addRecordTask, current_user["nick"], operation, current_user["department"])

    return {
        "code": 0,
        "mail_template": template
    }

@router.post("/removetemplate", response_model = TemplateResponse)
async def removeTemplate(
    task: BackgroundTasks,
    data: RemoveTemplate,
    current_user: Dict = Security(get_current_user, scopes = ["user", "administrator", "supervisor"])
) -> Dict:
    target = data.target
        
    dept = await crud_dept.select_one_by(
        Department.c.name == current_user["department"]
    )        
    template = eval(dept["mail_template"])
    
    removedList = []
    for title in target:
        for each in template:
            if(each["title"] == title):
                template.remove(each)
                removedList.append(title)
    
    if not removedList:
        raise settings.CUSTOM_EXCEPTION(503, "模板不存在")

    await crud_dept.update(
        condition = Department.c.name == current_user["department"],
        mail_template = str(template)
    )

    # 添加后台任务  
    operation = f"删除了信息模板【{'|'.join(removedList)}】"
    task.add_task(addRecordTask, current_user["nick"], operation, current_user["department"])
    return {
        "code": 0,
        "mail_template": template

    }

@router.post("/edittemplate", response_model = TemplateResponse)
async def editTemplate(
    task: BackgroundTasks,
    editInfo: EditTemplate,
    current_user: Dict = Security(get_current_user, scopes = ["user", "administrator", "supervisor"])
) -> Dict:
    dept = await crud_dept.select_one_by(
        Department.c.name == current_user["department"]
    )        
    template = eval(dept["mail_template"])
    
    for each in template:
        if each["title"] == editInfo.title:
            each["content"] = editInfo.content
            each["title"] = editInfo.title
            await crud_dept.update(
                condition = Department.c.name == current_user["department"],
                mail_template = str(template)
            )

            # 添加后台任务  
            operation = f"更新了信息模板【{editInfo.title}】"
            task.add_task(addRecordTask, current_user["nick"], operation, current_user["department"])
            return {
                "code": 0,
                "mail_template": template
            }
    
    raise settings.CUSTOM_EXCEPTION(503, "模板不存在")