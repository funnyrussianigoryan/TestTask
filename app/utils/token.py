from datetime import datetime, timedelta
import jwt
from fastapi.security import OAuth2PasswordBearer

from app.config import settings

from app.schemas.user import ResponseUser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.TOKEN_HASH_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(user: ResponseUser):
    to_encode = dict(id=user.id, is_admin=user.is_admin)
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
