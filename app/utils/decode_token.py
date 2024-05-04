import jwt
from fastapi import Depends, HTTPException

from app.utils.token import oauth2_scheme
from app.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.TOKEN_HASH_ALGORITHM


def decode_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")
        is_admin = payload.get('is_admin', False)
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return dict(id=user_id, is_admin=is_admin)

