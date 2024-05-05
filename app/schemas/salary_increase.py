from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class RequestSalaryIncrease(BaseModel):
    user_id: int
    new_salary: int
    increase_date: date
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class ResponseSalaryIncrease(BaseModel):
    user_id: int
    new_salary: int
    created_by: Optional[int] = None
    increase_date: date
    updated_at: Optional[datetime] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ResponseUpdateSalaryIncrease(BaseModel):
    message: str
    current_salary: ResponseSalaryIncrease
