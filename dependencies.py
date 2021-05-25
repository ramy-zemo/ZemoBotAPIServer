import jwt

from tortoise.models import Model
from passlib.hash import bcrypt
from tortoise import fields
from fastapi import HTTPException, status
from config import JWT_SECRET


# User Objects
class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    password_hash = fields.CharField(128)
    is_admin = fields.BooleanField(default=False, null=True)
    API_KEY = fields.CharField(1280, default="", null=True)

    def verify_password(self, password):
        if password == self.password_hash:
            return True

        return bcrypt.verify(password, self.password_hash)


# Check if User is Valid
async def authenticate_user(username: str, password: str):
    user = ""

    try:
        user = await User.get(username=username)
    except:
        pass

    if not user or not user.verify_password(password):
        user = ""

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')

    return user


# Check if User is Valid
async def authenticate_admin(username: str, password: str):
    user = ""

    try:
        user = await User.get(username=username)
    except:
        pass

    if not user or not user.verify_password(password):
        user = ""

    if not user or not user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')

    return user


# Check if User Token is Valid
async def authenticate_user_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    except:
        return False

    return await authenticate_user(payload.get('username'), payload.get('password_hash'))


# Check if Admin Token is Valid
async def authenticate_admin_token(API_Key: str):
    try:
        payload = jwt.decode(API_Key, JWT_SECRET, algorithms=['HS256'])
    except:
        return False

    return await authenticate_admin(payload.get('username'), payload.get('password_hash'))
