from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.schemas.auth import Register, Login
from app.schemas.user import ResponseUser
from app.utils.password_hash import verify_password, get_password_hash


class AuthService:
    @classmethod
    async def login(cls, data: Login, db: AsyncSession) -> ResponseUser:
        db_rows = await db.execute(select(User).filter(User.username == data.username))
        user = db_rows.scalars().first()
        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return ResponseUser.model_validate(user)

    @classmethod
    async def register(cls, data: Register, db: AsyncSession) -> ResponseUser:
        new_user_data = dict(data)
        password = new_user_data["password"]
        new_user_data["password_hash"] = get_password_hash(password)
        del new_user_data["password"]
        new_user = User(**new_user_data)
        db.add(new_user)
        await db.commit()
        return ResponseUser.model_validate(new_user)
