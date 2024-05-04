from typing import List
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.current_salary import ResponseCurrentSalary, RequestCurrentSalary

from app.services.user import UserService
from app.db.models import CurrentSalary


class CurrentSalaryService:

    @staticmethod
    async def get_by_user_id(user_id: int, db: AsyncSession) -> CurrentSalary:
        async with db.begin():
            result = await db.execute(
                select(CurrentSalary).where(CurrentSalary.user_id == user_id)
            )
        salary = result.scalars().first()
        if not salary:
            raise HTTPException(
                status_code=404, detail="Current salary for user not found"
            )
        return salary

    @staticmethod
    async def get_one(user_id: int, db: AsyncSession) -> ResponseCurrentSalary:
        salary = await CurrentSalaryService.get_by_user_id(user_id, db)
        return ResponseCurrentSalary.model_validate(salary)

    @staticmethod
    async def get_all(
        begin: int,
        end: int,
        db: AsyncSession,
    ) -> List[ResponseCurrentSalary]:
        try:
            async with db.begin():
                result = await db.execute(select(CurrentSalary))
                all_salaries_models = result.scalars().all()
                all_salaries_schemas = [
                    ResponseCurrentSalary.model_validate(salary_model)
                    for salary_model in all_salaries_models[begin:end]
                ]
            return all_salaries_schemas
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def create(
        data: RequestCurrentSalary, db: AsyncSession
    ) -> ResponseCurrentSalary:
        await UserService.get_user_by_id(data.user_id, db)
        try:
            async with db.begin():
                salary_data = data.dict()
                salary = CurrentSalary(**salary_data)
                db.add(salary)
                await db.commit()
            return ResponseCurrentSalary.model_validate(salary)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def update(
        data: RequestCurrentSalary, db: AsyncSession
    ) -> ResponseCurrentSalary:
        salary = await CurrentSalaryService.get_by_user_id(data.user_id, db)
        try:
            async with db.begin():
                for key, value in data.dict().items():
                    setattr(salary, key, value)
                await db.commit()
                return ResponseCurrentSalary.model_validate(salary)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def delete(user_id: int, db: AsyncSession) -> ResponseCurrentSalary:
        salary = await CurrentSalaryService.get_by_user_id(user_id, db)
        try:
            async with db.begin():
                await db.delete(salary)
                await db.commit()
            return ResponseCurrentSalary.model_validate(salary)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
