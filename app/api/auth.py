from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db_session
from app.schemas.auth import Register, ResponseAuth, Login
from app.services.auth import AuthService
from app.utils.token import create_access_token

auth_rout = APIRouter(prefix="/auth", tags=["Auth"])


@auth_rout.post("/login")
async def login(
    data: Login, db: AsyncSession = Depends(get_db_session)
) -> ResponseAuth:
    user = await AuthService.login(data, db)
    access_token = create_access_token(user)
    response = {
        "message": "User authorized successfully",
        "access_token": access_token,
        "token_type": "bearer",
        "user": user,
    }
    return ResponseAuth.validate(response)


@auth_rout.post("/register/")
async def register(
    data: Register, db: AsyncSession = Depends(get_db_session)
) -> ResponseAuth:
    new_user = await AuthService.register(data, db)
    access_token = create_access_token(new_user)
    response = {
        "message": "User authorized successfully",
        "access_token": access_token,
        "token_type": "bearer",
        "user": new_user,
    }
    return ResponseAuth.validate(response)
