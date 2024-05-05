from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.schemas.auth import Register, Login
from app.schemas.user import ResponseUser
from app.utils.password_hash import verify_password, get_password_hash


class AuthService:

    @staticmethod
    async def get_by_user_username(username: str, db: AsyncSession) -> Optional[User]:
        async with db.begin():
            result = await db.execute(select(User).where(User.username == username))
            user = result.scalars().first()
            return user

    @staticmethod
    async def login(data: Login, db: AsyncSession) -> ResponseUser:
        user = await AuthService.get_by_user_username(data.username, db)
        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return ResponseUser.model_validate(user)

    @staticmethod
    async def register(data: Register, db: AsyncSession) -> ResponseUser:
        existing_user = await AuthService.get_by_user_username(data.username, db)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        try:
            password_hash = get_password_hash(data.password)
            new_user_data = {**data.dict(), "password_hash": password_hash}
            del new_user_data["password"]
            new_user = User(**new_user_data)
            db.add(new_user)
            await db.commit()
        except Exception as e:
            raise (HTTPException(status_code=500, detail="Failed to register"))
        return ResponseUser.model_validate(new_user)
