from typing import Dict
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer  

# import jwt

from core.config import settings
from models import User
from crud import crud_user

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl = "api/login/common",
    scopes = {"user": "common", "administrator": "super", "supervisor": "root"}
)

class ValidateAuth:
    def __init__(self, check_dept: bool) -> None:
        # 是否需要根据所属部门提供特殊权限，用于为人力资源部门全体成员提供查看全部简历的权限
        self.check_dept = check_dept

    async def __call__(
        self, 
        security_scopes: SecurityScopes,
        token: str = Depends(oauth2_scheme)
    ) -> Dict:
        try:
            # token_decode = jwt.decode(token, settings.SECRET_KEY, algorithms = settings.ALGORITHM)
            # openid = token_decode["openid"]
            s = Serializer(
                secret_key = settings.SECRET_KEY,
                expires_in = settings.TOKEN_EXPIRE_Time
            )
            token_decode = s.loads(token)
            openid = token_decode["openid"]
            
        except Exception as e:
            # 出现异常则为token过期
            print(e)
            raise settings.UNAUTHORIZED_EXCEPTION
    
        current_user = await crud_user.select_one_by(User.c.openid == openid)
        if not current_user:
            raise settings.CUSTOM_EXCEPTION(401, "用户不存在 请尝试重新扫码登录")
        
        if self.check_dept and current_user["department"] == "人力资源部":
            return current_user

        scopes = eval(current_user["role"])
        for scope in scopes:
            if scope in security_scopes.scopes:
                return current_user
        raise settings.UNAUTHORIZED_EXCEPTION

        
get_current_user = ValidateAuth(check_dept = False)
# 为人力资源部提供查看全部简历权限的特殊依赖
# get_special_user = ValidateAuth(check_dept = True)


async def validate_supervisor(form: OAuth2PasswordRequestForm = Depends()) -> Dict:
    # 此处算法后期记得更改
    def get_openid(usr: str, pwd: str) -> str:
        return usr + pwd
    openid = get_openid(form.username, form.password)
    supervisor = await crud_user.select_one_by(User.c.openid == openid)
    
    if not supervisor:
        raise settings.CUSTOM_EXCEPTION(503, "账号或密码错误")

    return supervisor

