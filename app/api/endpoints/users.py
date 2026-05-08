"""Работа с аунтификацией и авторизацией пользователей"""

from sqlite3 import IntegrityError

from fastapi import APIRouter, Depends, HTTPException, Response
from app.api.models.user import User
from app.core.security import authenticate_user, create_jwt_token, get_password_hash, get_user_from_token, verify_password
from app.db.users_dao import UsersDAO


user_rourer = APIRouter(prefix="/user", tags=["User"])

@user_rourer.post("/register")
async def register_user(user_data: User) -> None:
    """Регистрируем пользователя"""
    hashed_password = await get_password_hash(user_data.password)
    await UsersDAO.add(name=user_data.name, password=hashed_password)


@user_rourer.post("/login")
async def login_user(response: Response, user_data: User) -> None:
    """Логиним пользователя"""
    user = await authenticate_user(user_data=user_data)
    if not user:
        raise HTTPException(status_code=401)
    access_token = await create_jwt_token({"sub": str(user_data.name)})
    response.set_cookie("jwt_token", access_token)


@user_rourer.post("/logout")
async def logout_user(response: Response) -> None:
    """Выходим из аккаунта(удаляем кеш с jwt токеном)"""
    response.delete_cookie("jwt_token")


