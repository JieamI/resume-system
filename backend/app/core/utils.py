from base64 import standard_b64encode
from typing import Dict
import urllib.parse
import hmac
import time
import aiohttp
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication 
import aiosmtplib
from fastapi.datastructures import UploadFile

from core.config import settings
from crud import crud_record

def GenUrlSignature(
    app_secret: str, 
    time_stamp: str
) -> str:
    digest = hmac.HMAC(
        key = app_secret.encode('utf-8'),
        msg = time_stamp.encode('utf-8'),
        digestmod = hmac._hashlib.sha256
    ).digest()

    signature = standard_b64encode(digest).decode('utf-8')
    signature_encode = urllib.parse.quote(signature)
    return signature_encode


async def getUserinfo(code: str) -> Dict[str, str]:
    access_key = settings.APP_ID
    time_stamp = str(round(time.time()*1000))
    signature = GenUrlSignature(settings.APP_SECRET, time_stamp)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url = f"https://oapi.dingtalk.com/sns/getuserinfo_bycode?accessKey={access_key}&timestamp={time_stamp}&signature={signature}",
                json = {"tmp_auth_code": code}
            ) as resp:
                res = await resp.json()
    except:
        raise settings.CUSTOM_EXCEPTION(401, "授权码无效 请尝试重新登录")

    # 验证授权码是否有效
    if res['errcode'] != 0:
        raise settings.CUSTOM_EXCEPTION(401, "授权码无效 请尝试重新登录")
    return res


async def getDepartment(unionid: str) -> str:
    depts = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url = f"https://oapi.dingtalk.com/gettoken?appkey={settings.ACCESS_APPKEY}&appsecret={settings.ACCESS_APPSECRET}"
            ) as resp:
                res = await resp.json()
                access_token = res["access_token"]
            async with session.get(
                url = f"https://oapi.dingtalk.com/user/getUseridByUnionid?access_token={access_token}&unionid={unionid}"
            ) as resp:
                res = await resp.json()
                userid = res["userid"]
            async with session.get(
                url = f"https://oapi.dingtalk.com/user/get?access_token={access_token}&userid={userid}"
            ) as resp:
                res = await resp.json()
                dept_id = res["department"]
            for id in dept_id:
                async with session.get(
                    url = f"https://oapi.dingtalk.com/department/get?access_token={access_token}&id={id}"
                ) as resp:
                    res = await resp.json()
                    depts.append(res["name"])
    except:
        raise settings.SERVICE_EXCEPTION

    for dept in depts:
        for k, v in settings.DEPARTMENT_MAP.items():
            if dept == k:
                return k
            if dept in v:
                return k
    raise settings.CUSTOM_EXCEPTION(503, "所属部门不合法")


# 后台任务添加操作记录
async def addRecordTask(
    operator: str, 
    operation: str, 
    department: str
) -> None:
    await crud_record.create([{
        "operator": operator,
        "operation": operation,
        "department": department
    }])


async def send_email(
    recipients: list, 
    subject: str,
    content: str, 
    file: UploadFile = None
):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = 'Token团队'
    msg.attach(MIMEText(content))

    if file:
        attachment = MIMEApplication(await file.read(), file.content_type)
        attachment.add_header('Content-Disposition', 'attachment', filename = file.filename)
        msg.attach(attachment)

    await aiosmtplib.send(
        msg,
        sender = settings.USERNAME_MAIL,
        username = settings.USERNAME_MAIL,
        password = settings.PASSWORD_MAIL,
        hostname = "smtp.qq.com",
        port = 465,
        use_tls = True,
        recipients = recipients
    )