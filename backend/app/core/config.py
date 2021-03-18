from typing import Dict, List
from fastapi import status, HTTPException
from pydantic import BaseSettings

class Settings(BaseSettings):
    API_PREFIX: str = "/api"

    # 钉钉扫码登录配置
    APP_ID: str = "xxxxx"
    APP_SECRET: str = "xxxxx" 
    ACCESS_APPKEY: str = "xxxxx"
    ACCESS_APPSECRET: str = "xxxxx"
    
    # 密钥及算法配置
    SECRET_KEY: str = "xxxxx"

    # Token相关配置(s)
    TOKEN_EXPIRE_Time: int = 604800
    
    # 跨域配置
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # mysql服务器配置
    MYSQL_NAME: str = "xxxxx"
    MYSQL_HOST: str = "xxxxx"
    MYSQL_PORT: str = "xxxxx"
    MYSQL_USER: str = "xxxxx"
    MYSQL_PASSWORD: str = "xxxxx"
    DATABASE_URI: str = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_NAME}?charset=utf8"

    # HTTP错误配置
    def custom_exception(self, status_code: int ,detail: str) -> HTTPException:
        return HTTPException(status_code, detail = detail)
    CUSTOM_EXCEPTION =  custom_exception
    UNAUTHORIZED_EXCEPTION = HTTPException(status.HTTP_401_UNAUTHORIZED, detail = "权限不足")
    SERVICE_EXCEPTION = HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail = "服务异常")

    DEPARTMENT_MAP: Dict = {
        "技术部": ["前端组", "服务端组", "移动客户端组", "基础架构组"], 
        "设计部": ["交互视觉设计组", "用户研究组"],
        "产品部": [],
        "产品运营": [],
        "新媒体运营": [],
        "人力资源部": [],
        "杂志部": [],
    }

    # 超级管理员账号密码配置
    SUPERVISOR_USERNAME: str = "supervisor" 
    SUPERVISOR_PASSWORD: str = "supervisor"

    ADMINISTRATOR_USERNAME: str = "administrator" 
    ADMINISTRATOR_PASSWORD: str = "administrator"

    USER_USERNAME: str = "user"
    USER_PASSWORD: str = "user"

    # 邮箱发送服务配置
    USERNAME_MAIL: str = "xxxxx"
    PASSWORD_MAIL: str = "xxxxx"

    class Config:
        case_sensitive = True

settings = Settings()
