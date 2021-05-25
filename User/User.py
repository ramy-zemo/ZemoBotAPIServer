import jwt

from fastapi import APIRouter
from tortoise.contrib.pydantic import pydantic_model_creator
from passlib.hash import bcrypt
from fastapi import Depends
from fastapi import HTTPException, status
from dependencies import authenticate_user_token, authenticate_user, authenticate_admin_token, User
from config import JWT_SECRET


router = APIRouter()


User_Pydantic = pydantic_model_creator(User, name='User')
UserIN_Pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)


@router.post('/create_user', response_model=User_Pydantic, tags=["User"])
@router.post('/create_user', response_model=User_Pydantic, tags=["User"])
async def create_user(username: str, password: str, user=Depends(authenticate_user_token)):
    user_obj = User(username=username, password_hash=password, is_admin=False)
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)


@router.post('/create_admin', response_model=User_Pydantic, tags=["User"])
async def create_admin(username: str, password: str, admin=Depends(authenticate_admin_token)):
    user_obj = User(username=username, password_hash=bcrypt.hash(password), is_admin=True)

    user = await UserIN_Pydantic.from_tortoise_orm(user_obj)

    token = jwt.encode(user.dict(), JWT_SECRET)
    user_obj.API_KEY = token

    await user_obj.save()

    return await User_Pydantic.from_tortoise_orm(user_obj)


@router.get('/get_all_users', tags=["User"])
async def get_all_users(admin=Depends(authenticate_admin_token)):
    return await User.filter()


@router.get('/generate_token', tags=['User'])
async def generate_token(user=Depends(authenticate_user)):
    user = await User_Pydantic.from_tortoise_orm(user)
    token = jwt.encode(user.dict(), JWT_SECRET)
    return {"Token": token, "Type": "OpenAPI"}


@router.delete('/delete_user', tags=['User'])
async def delete_user(username: str = "", user_id: int = 0, admin=Depends(authenticate_admin_token)):
    if not username and not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have to provide either a username or an ID"
        )
    if user_id:
        user_obj = User.filter(id=user_id)
    else:
        user_obj = User.filter(username=username)

    await user_obj.delete()

    return "Account successfully deleted."
