from functools import wraps

from fastapi import HTTPException

from app.utils.decode_token import decode_token


def only_for_admin(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        token = kwargs.get("token")
        is_admin = decode_token(token).get("is_admin", False)
        if not is_admin:
            raise HTTPException(status_code=403, detail="Do not have permission")
        return await func(*args, **kwargs)

    return wrapper
