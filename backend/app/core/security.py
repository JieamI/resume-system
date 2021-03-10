from datetime import datetime, timedelta
import jwt

from core.config import settings

def create_token(
    openid: str
) -> str:
    content = {
        "openid": openid,
        "exp": datetime.utcnow() + timedelta(days = settings.TOKEN_EXPIRE_DAYS)
    }
    token_encode = jwt.encode(content, settings.SECRET_KEY, algorithm = settings.ALGORITHM)
    return token_encode


