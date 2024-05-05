from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import SalaryIncrease
from app.schemas.salary_increase import ResponseSalaryIncrease, RequestSalaryIncrease
from app.services.user import UserService


class SalaryIncreaseService:

    @staticmethod
    async def get_by_user_id(user_id: int, db: AsyncSession) -> SalaryIncrease:
        async with db.begin():
            result = await db.execute(
                select(SalaryIncrease).where(SalaryIncrease.user_id == user_id)
            )
        increase = result.scalars().first()
        if not increase:
            raise HTTPException(
                status_code=404, detail="Current salary for user not found"
            )
        return increase

    @staticmethod
    async def get_one(user_id: int, db: AsyncSession) -> ResponseSalaryIncrease:
        salary = await SalaryIncreaseService.get_by_user_id(user_id, db)
        return ResponseSalaryIncrease.model_validate(salary)

    @staticmethod
    async def get_all(
        begin: int,
        end: int,
        db: AsyncSession,
    ) -> List[ResponseSalaryIncrease]:
        try:
            async with db.begin():
                result = await db.execute(select(SalaryIncrease))
                all_increase_models = result.scalars().all()
                all_increase_schemas = [
                    ResponseSalaryIncrease.model_validate(increase_model)
                    for increase_model in all_increase_models[begin:end]
                ]
            return all_increase_schemas
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def create(
        data: RequestSalaryIncrease, db: AsyncSession
    ) -> ResponseSalaryIncrease:
        await UserService.get_user_by_id(data.user_id, db)
        try:
            async with db.begin():
                salary_data = data.dict()
                salary = SalaryIncrease(**salary_data)
                db.add(salary)
                await db.commit()
            return ResponseSalaryIncrease.model_validate(salary)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def update(
        data: RequestSalaryIncrease, db: AsyncSession
    ) -> ResponseSalaryIncrease:
        salary = await SalaryIncreaseService.get_by_user_id(data.user_id, db)
        try:
            async with db.begin():
                for key, value in data.dict().items():
                    setattr(salary, key, value)
                await db.commit()
                return ResponseSalaryIncrease.model_validate(salary)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def delete(user_id: int, db: AsyncSession) -> ResponseSalaryIncrease:
        salary = await SalaryIncreaseService.get_by_user_id(user_id, db)
        try:
            async with db.begin():
                await db.delete(salary)
                await db.commit()
            return ResponseSalaryIncrease.model_validate(salary)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


"""
class CurrentSalaryService:

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
"""
