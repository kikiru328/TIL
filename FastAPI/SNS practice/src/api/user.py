from fastapi import APIRouter, HTTPException, Depends

from database.orm import User
from database.repository import UserRepository, PostRepository
from schema.request import SignUpRequest, LogInRequest
from schema.response import UserSchema, JWTSchema, PostSchema
from service.post import PostService
from service.user import UserService

router = APIRouter(prefix="/users")

@router.post("/sign-up", status_code=201, response_model=UserSchema)
def user_sign_up_handler(
        request: SignUpRequest,
        user_repo: UserRepository = Depends(),
):
    # 1. username 중복 확인
    user = user_repo.get_user_by_username(request.username)
    if user: # 이미 있다면
        raise HTTPException(status_code=400, detail="Username already exists")

    # 2. 비밀번호 Hash 암호화
    hashed_password = UserService.hash_password(plain_password=request.password)

    # 3. 사용자 정보 생성
    new_user: User = User.create(
        username=request.username,
        hashed_password=hashed_password
    )

    # 4. 사용자 정보 저장
    new_user: User = user_repo.save_user(new_user)

    return new_user

@router.post("/log-in")
def user_log_in_handler(
        request: LogInRequest,
        user_repo: UserRepository = Depends()
):
    # 1. username 사용자 조회
    user = user_repo.get_user_by_username(request.username)
    if not user: # DB에 없을 경우
        raise HTTPException(status_code=404, detail="User Not Found")

    # 2. verify password
    if not UserService.verify_password(
        plain_password=request.password, # 입력한 Password
        hashed_password=user.password # db Password
    ):
        raise HTTPException(status_code=404, detail="Invalid Password")

    # 3. JWT! (token)
    access_token = UserService.create_jwt(user.username)
    return JWTSchema(access_token=access_token)

@router.get("/{user_id}/posts", response_model=list[PostSchema])
def get_user_posts_handler(
        user_id: int,
        post_repo: PostRepository = Depends()
):
    return PostService.get_user_posts(user_id=user_id, post_repo=post_repo)