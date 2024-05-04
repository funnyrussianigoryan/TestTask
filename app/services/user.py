from typing import List
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UpdateUser, UpdatePassword, ResponseUser
from app.utils.password_hash import get_password_hash
from app.db.models import User


class UserService:
    @staticmethod
    async def get_user_by_id(id: int, db: AsyncSession) -> User:
        async with db.begin():
            user = await db.get(User, id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    async def get_users(
        begin: int,
        end: int,
        db: AsyncSession,
    ) -> List[ResponseUser]:
        try:
            async with db.begin():
                result = await db.execute(select(User))
                all_users_models = result.scalars().all()
                all_users_schemas = [
                    ResponseUser.model_validate(user_model)
                    for user_model in all_users_models[begin:end]
                ]
            return all_users_schemas
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def get_user(id: int, db: AsyncSession) -> ResponseUser:
        user = await UserService.get_user_by_id(id, db)
        return ResponseUser.model_validate(user)

    @staticmethod
    async def update_user(
        id: int, updated_data: UpdateUser, db: AsyncSession
    ) -> ResponseUser:
        user = await UserService.get_user_by_id(id, db)
        try:
            async with db.begin():
                for key, value in updated_data.dict(exclude_none=True).items():
                    setattr(user, key, value)
            await db.commit()
            return ResponseUser.model_validate(user)
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def update_user_password(
        id: int, password: UpdatePassword, db: AsyncSession
    ) -> ResponseUser:
        user = await UserService.get_user_by_id(id, db)
        try:
            async with db.begin():
                new_password_hash = get_password_hash(password.new_password)
                user.password_hash = new_password_hash
            await db.commit()
            return ResponseUser.model_validate(user)
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def delete_user(id: int, db: AsyncSession) -> ResponseUser:
        user = await UserService.get_user_by_id(id, db)
        try:
            async with db.begin():
                await db.delete(user)
            await db.commit()
            return ResponseUser.model_validate(user)
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
