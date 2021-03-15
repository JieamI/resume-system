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
    def __init__(self) -> None:
        pass

    async def __call__(
        self, 
        security_scopes: SecurityScopes,
        token: str = Depends(oauth2_scheme)
    ) -> Dict:
        try:
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
        
        scopes = eval(current_user["role"])
        for scope in scopes:
            if scope in security_scopes.scopes:
                return current_user
        raise settings.UNAUTHORIZED_EXCEPTION

        
get_current_user = ValidateAuth()


# demo模式下的权限验证
async def validate_auth(form: OAuth2PasswordRequestForm = Depends()) -> Dict:
    def get_openid(usr: str, pwd: str) -> str:
        return usr + pwd
    openid = get_openid(form.username, form.password)
    current_user = await crud_user.select_one_by(User.c.openid == openid)
    
    if not current_user:
        raise settings.CUSTOM_EXCEPTION(503, "账号或密码错误")

    return current_user

