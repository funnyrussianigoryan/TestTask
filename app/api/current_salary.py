from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db_session
from app.schemas.current_salary import (
    ResponseCurrentSalary,
    ResponseUpdateCurrentSalary,
    RequestCurrentSalary,
)
from app.services.current_salary import CurrentSalaryService
from app.utils.only_for_admin import only_for_admin
from app.utils.decode_token import decode_token
from app.utils.token import oauth2_scheme

current_salary_rout = APIRouter(prefix="/current_salary", tags=["Current salary"])


@current_salary_rout.get("/")
@only_for_admin
async def get_all(
    record_count_begin: int = 0,
    record_count_end: int = 10,
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(oauth2_scheme),
) -> List[ResponseCurrentSalary]:
    salaries_data = await CurrentSalaryService.get_all(
        record_count_begin, record_count_end, db
    )
    return salaries_data


@current_salary_rout.get("/my")
async def get_my(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db_session)
) -> ResponseCurrentSalary:
    user_id = decode_token(token).get("id")
    return await CurrentSalaryService.get_one(user_id, db)


@current_salary_rout.post("/")
@only_for_admin
async def create(
    data: RequestCurrentSalary,
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(oauth2_scheme),
) -> ResponseUpdateCurrentSalary:
    data.created_by = decode_token(token).get("id")
    current_salary = await CurrentSalaryService.create(data, db)
    response = {
        "message": "User current salary created successfully",
        "current_salary": current_salary,
    }
    return ResponseUpdateCurrentSalary.validate(response)


@current_salary_rout.patch("/")
@only_for_admin
async def update(
    data: RequestCurrentSalary,
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(oauth2_scheme),
) -> ResponseUpdateCurrentSalary:
    data.created_by = decode_token(token).get("id")
    data.updated_at = datetime.utcnow()
    current_salary = await CurrentSalaryService.update(data, db)
    response = {
        "message": "User current salary updated successfully",
        "current_salary": current_salary,
    }
    return ResponseUpdateCurrentSalary.validate(response)


@current_salary_rout.delete("/{user_id}")
@only_for_admin
async def delete(
    user_id: int,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db_session),
) -> ResponseUpdateCurrentSalary:
    current_salary = await CurrentSalaryService.delete(user_id, db)
    response = {
        "message": "User current salary deleted successfully",
        "current_salary": current_salary,
    }
    return ResponseUpdateCurrentSalary.validate(response)


@current_salary_rout.get("/{user_id}")
async def get_one(
    user_id: int,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db_session),
) -> ResponseCurrentSalary:
    decoded_data = decode_token(token)
    client_id = decoded_data.get("id")
    is_admin = decoded_data.get("is_admin", False)
    if not (client_id == id or is_admin):
        raise HTTPException(status_code=404, detail="Do not have permission")
    return await CurrentSalaryService.get_one(user_id, db)
