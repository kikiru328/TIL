import bcrypt
from jose import jwt
from datetime import datetime, timedelta


class UserService:
    encoding: str = "UTF-8"
    secret_key: str = "0aba04354dda020d17c2d0f778cbaa13f42100c6621aa855bd982857c94545e1"
    jwt_algorithm: str = "HS256"
    def hash_password(self, plain_password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(
            plain_password.encode(self.encoding),
            salt=bcrypt.gensalt(),
        )
        return hashed_password.decode(self.encoding)

    def verify_password(
            self, plain_password: str, hashed_password: str) -> bool:
        # try/except
        return bcrypt.checkpw(
            plain_password.encode(self.encoding),
            hashed_password.encode(self.encoding)
        )

    def create_jwt(self, username: str) -> str:
        return jwt.encode(
            {
                "sub": username,
                "exp": datetime.now() + timedelta(days=1),
             },
            self.secret_key,
            algorithm=self.jwt_algorithm,
        )