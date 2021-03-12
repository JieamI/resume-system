from typing import Dict
from fastapi import APIRouter, Security, Body, BackgroundTasks
from sqlalchemy import and_

from core.config import settings
from models import User
from crud import crud_user
from core.depends import get_current_user
from schemas.authority import AuthorityResponse
from schemas.base import BasicSchema
from core.utils import addRecordTask


router = APIRouter()


@router.get("/getinfo", response_model = AuthorityResponse)
async def getAuthInfo(
    current_user: Dict = Security(get_current_user, scopes = ["administrator", "supervisor"])
) -> Dict:
    data = []
    if "supervisor" in eval(current_user["role"]):
        res = await crud_user.select_by(
            User.c.role.notlike("%supervisor%")
        )
    else:
        res = await crud_user.select_by(
            and_(
                User.c.department == current_user["department"],
                User.c.role.notlike("%supervisor%"),
                User.c.openid != current_user["openid"]
            )
        )

    if res:
        data = [{
            **item, 
            "state": "部门负责人" if "administrator" in item["role"] else "普通成员", 
            "key": index
        } for index, item in enumerate(res)]

    return {
        "code": 0,
        "data": data
    }


@router.post("/updateinfo", response_model = BasicSchema)
async def updateAuthority(
    task: BackgroundTasks,
    openid: str = Body(..., embed = True),
    current_user: Dict = Security(get_current_user, scopes = ["administrator", "supervisor"])
) -> Dict:
    user = await crud_user.select_one_by(User.c.openid == openid)
    if not user:
        raise settings.CUSTOM_EXCEPTION(503, "目标用户不存在")
    
    if "user" in user["role"]:
        targetRole = "['administrator']"
        operation = f"提高了{user['nick']}的权限"
    else:
        targetRole = "['user']"
        operation = f"移除了{user['nick']}的权限"

    await crud_user.update(
        condition = User.c.openid == openid,
        role = targetRole
    )

    # 添加后台任务
    task.add_task(addRecordTask, current_user["nick"], operation, current_user["department"])
    return {
        "code": 0
    }
