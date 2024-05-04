from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db_session
from app.schemas.user import (
    UpdateUser,
    UpdatePassword,
    ResponseUser,
    UpdateUserResponse,
)
from app.utils.decode_token import decode_token
from app.utils.only_for_admin import only_for_admin
from app.utils.token import oauth2_scheme
from app.services.user import UserService

users_rout = APIRouter(prefix="/users", tags=["Users"])


@users_rout.get("/")
@only_for_admin
async def get_users(
    record_count_begin: int = 0,
    record_count_end: int = 10,
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(oauth2_scheme),
) -> list[ResponseUser]:
    users_data = await UserService.get_users(record_count_begin, record_count_end, db)
    return users_data


@users_rout.get("/me")
async def get_me(
    db=Depends(get_db_session), token: str = Depends(oauth2_scheme)
) -> ResponseUser:
    id = decode_token(token)["id"]
    user = await UserService.get_user(id, db)
    return user


@users_rout.get("/{id}")
async def get_user(
    id: int,
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(oauth2_scheme),
) -> ResponseUser:
    decoded_data = decode_token(token)
    client_id = decoded_data.get("id")
    is_admin = decoded_data.get("is_admin", False)
    if not (client_id == id or is_admin):
        raise HTTPException(status_code=404, detail="Do not have permission")
    user = await UserService.get_user(id, db)
    return user


@users_rout.patch("/{id}")
@only_for_admin
async def update_user(
    id: int,
    updated_data: UpdateUser,
    db=Depends(get_db_session),
    token: str = Depends(oauth2_scheme),
) -> UpdateUserResponse:
    updated_data.updated_at = datetime.utcnow()
    user = await UserService.update_user(id, updated_data, db)
    response = {"message": "User updated successfully", "user": user}
    return UpdateUserResponse.validate(response)


@users_rout.patch("/me/password")
async def update_user_password(
    password: UpdatePassword,
    db=Depends(get_db_session),
    token: str = Depends(oauth2_scheme),
) -> UpdateUserResponse:
    decoded_data = decode_token(token)
    id = decoded_data["id"]
    user = await UserService.update_user_password(id, password, db)
    response = {"message": "User password updated successfully", "user": user}
    return UpdateUserResponse.validate(response)


@users_rout.delete("/{id}")
@only_for_admin
async def delete_user(
    id: int,
    db=Depends(get_db_session),
    token: str = Depends(oauth2_scheme),
) -> UpdateUserResponse:
    user = await UserService.delete_user(id, db)
    response = {"message": "User deleted successfully", "user": user}
    return UpdateUserResponse.validate(response)
