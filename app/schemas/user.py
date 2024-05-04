from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class UpdateUser(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    is_admin: Optional[bool] = None
    updated_at: datetime = datetime.utcnow()


class UpdatePassword(BaseModel):
    new_password: str


class ResponseUser(BaseModel):
    id: int
    name: str
    surname: str
    username: str
    is_admin: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UpdateUserResponse(BaseModel):
    message: str
    user: ResponseUser
