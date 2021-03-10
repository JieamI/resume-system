from typing import Dict
from fastapi import APIRouter, Depends, Body, Security

from core import utils, security
from crud import crud_user
from models import User
from core.depends import get_current_user, validate_supervisor
from schemas.login import LoginResponse, UpdateResponse

router = APIRouter()


@router.post("/common", response_model = LoginResponse)
async def handleCommonLogin(code: str = Body(..., embed = True)) -> Dict:
    res_dic = await utils.getUserinfo(code)
    openid = res_dic["user_info"]["openid"]
    unionid = res_dic["user_info"]["unionid"]
    nick = res_dic["user_info"]["nick"]

    user = await crud_user.select_one_by(User.c.openid == openid)
    if user:
        scopes = eval(user["role"])
        department = user["department"]
    else:
        department = await utils.getDepartment(unionid)
        await crud_user.create([{"nick": nick, "openid": openid, "department": department}])
        scopes = ["user"]
    
    token = security.create_token(openid)

    return {
        "code": 0,
        "access_token": token, 
        "nick": nick,
        "department": department,
        "scopes": scopes
    }
   

@router.post("/super", response_model = LoginResponse)
async def handleSuperLogin(supervisor: Dict = Depends(validate_supervisor)) -> Dict:
    openid = supervisor["openid"]
    scopes = eval(supervisor["role"])
    department = supervisor["department"]
    nick = supervisor["nick"]
    token = security.create_token(openid)
    return {
        "code": 0,
        "access_token": token, 
        "nick": nick,
        "department": department,
        "scopes": scopes
    }


@router.get("/update", response_model = UpdateResponse)
async def handleUpdateInfo(
    current_user: Dict = Security(get_current_user, scopes = ["user", "administrator", "supervisor"])
) -> Dict:
    nick = current_user["nick"]
    department = current_user["department"]
    scopes = eval(current_user["role"])
    return {
        "code": 0,
        "nick": nick,
        "department": department,
        "scopes": scopes
    }
