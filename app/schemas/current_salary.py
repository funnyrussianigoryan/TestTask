from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class RequestCurrentSalary(BaseModel):
    user_id: int
    salary: int
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class ResponseCurrentSalary(BaseModel):
    user_id: int
    salary: int
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ResponseUpdateCurrentSalary(BaseModel):
    message: str
    current_salary: ResponseCurrentSalary
