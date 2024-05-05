from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db_session

from app.schemas.salary_increase import (
    ResponseSalaryIncrease,
    RequestSalaryIncrease,
    ResponseUpdateSalaryIncrease,
)
from app.services.salary_increase import SalaryIncreaseService
from app.utils.only_for_admin import only_for_admin
from app.utils.decode_token import decode_token
from app.utils.token import oauth2_scheme

salary_increase_rout = APIRouter(prefix="/salary_increase", tags=["Salary increase"])


@salary_increase_rout.get("/")
@only_for_admin
async def get_all(
    record_count_begin: int = 0,
    record_count_end: int = 10,
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(oauth2_scheme),
) -> List[ResponseSalaryIncrease]:
    salaries_data = await SalaryIncreaseService.get_all(
        record_count_begin, record_count_end, db
    )
    return salaries_data


@salary_increase_rout.get("/my")
async def get_my(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db_session)
) -> ResponseSalaryIncrease:
    user_id = decode_token(token).get("id")
    return await SalaryIncreaseService.get_one(user_id, db)


@salary_increase_rout.post("/")
@only_for_admin
async def create(
    data: RequestSalaryIncrease,
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(oauth2_scheme),
) -> ResponseUpdateSalaryIncrease:
    data.created_by = decode_token(token).get("id")
    salary_increase = await SalaryIncreaseService.create(data, db)
    response = {
        "message": "User current salary created successfully",
        "current_salary": salary_increase,
    }
    return ResponseUpdateSalaryIncrease.validate(response)


@salary_increase_rout.get("/{user_id}")
async def get_one(
    user_id: int,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db_session),
) -> ResponseSalaryIncrease:
    decoded_data = decode_token(token)
    client_id = decoded_data.get("id")
    is_admin = decoded_data.get("is_admin", False)
    if not (client_id == id or is_admin):
        raise HTTPException(status_code=404, detail="Do not have permission")
    return await SalaryIncreaseService.get_one(user_id, db)


@salary_increase_rout.patch("/")
@only_for_admin
async def update(
    data: RequestSalaryIncrease,
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(oauth2_scheme),
) -> ResponseUpdateSalaryIncrease:
    data.created_by = decode_token(token).get("id")
    data.updated_at = datetime.utcnow()
    increase = await SalaryIncreaseService.update(data, db)
    response = {
        "message": "User current salary updated successfully",
        "current_salary": increase,
    }
    return ResponseUpdateSalaryIncrease.validate(response)


@salary_increase_rout.delete("/{user_id}")
@only_for_admin
async def delete(
    user_id: int,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db_session),
) -> ResponseUpdateSalaryIncrease:
    increase = await SalaryIncreaseService.delete(user_id, db)
    response = {
        "message": "User current salary deleted successfully",
        "current_salary": increase,
    }
    return ResponseUpdateSalaryIncrease.validate(response)
