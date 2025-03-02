from datetime import datetime, timedelta

from jose import jwt, JWTError
import bcrypt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException

from database.repository import UserRepository
from security import get_access_token


class UserService:

    SECRET_KEY = "$2b$12$w9dbBaVyLfsfilhcux6KLO0qzOif2.G1sHfx1Ayk0grojhqUsDR/a" #admin hashed pwd
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_EXPIRE = timedelta(days=1)

    # basic encoding = "UTF-8"

    @staticmethod
    def hash_password(plain_password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(
            password=plain_password.encode(),
            salt=bcrypt.gensalt()
        )
        return hashed_password.decode()

    @staticmethod
    def verify_password(plain_password: str,
                        hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password=plain_password.encode(),
            hashed_password=hashed_password.encode()
        )

    @staticmethod
    def create_jwt(username: str) -> str:
        return jwt.encode(
            #paylaod
            {
                "sub": username, #submission,
                "exp": datetime.now() + UserService.JWT_ACCESS_EXPIRE
            },
            # secret Key
            UserService.SECRET_KEY,
            algorithm=UserService.JWT_ALGORITHM
        )

    @staticmethod
    def decode_jwt(access_token: str) -> str | None:
        try:
            payload: dict = jwt.decode(
                token=access_token,
                key=UserService.SECRET_KEY,
                algorithms=[UserService.JWT_ALGORITHM]
            )
            return payload.get("sub") # username
        except JWTError:
            return None

    @staticmethod
    def get_current_user(
            access_token: str = Depends(get_access_token),
            user_repo: UserRepository = Depends()
    ) -> int:
        try: # verify
            payload: dict = jwt.decode(
                token=access_token,
                key=UserService.SECRET_KEY,
                algorithms=[UserService.JWT_ALGORITHM]
            )
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid Access Token"
                )
        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Invalid Access Token"
            )

        user = user_repo.get_user_by_username(username)
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        return user.id

