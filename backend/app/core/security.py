# from datetime import datetime, timedelta
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer  


from core.config import settings

def create_token(
    openid: str
) -> str:
    content = {
        "openid": openid,
        # "exp": datetime.utcnow() + timedelta(days = settings.TOKEN_EXPIRE_DAYS)
    }
    # token_encode = jwt.encode(content, settings.SECRET_KEY, algorithm = settings.ALGORITHM)
    s = Serializer(
        secret_key = settings.SECRET_KEY,
        expires_in = settings.TOKEN_EXPIRE_Time
    )
    token_encode = s.dumps(content).decode()

    return token_encode


