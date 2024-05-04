from pydantic import BaseModel

from app.schemas.user import ResponseUser


class Register(BaseModel):
    username: str
    name: str
    surname: str
    password: str


class RegisterAdmin(BaseModel):
    username: str
    name: str
    surname: str
    password: str
    is_admin: bool = True


class ResponseAuth(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"
    user: ResponseUser


class Login(BaseModel):
    username: str
    password: str
