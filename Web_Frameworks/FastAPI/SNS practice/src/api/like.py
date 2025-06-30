from fastapi import APIRouter, Depends

from database.repository import LikeRepository
from schema.response import LikeSchema
from service.like import LikeService
from service.user import UserService

router = APIRouter(prefix="/posts")

@router.post("/{post_id}/like", status_code=201, response_model=LikeSchema)
def like_post_handler(
        post_id: int,
        like_repo: LikeRepository = Depends(),
        current_user: int = Depends(UserService.get_current_user)
):
    LikeService.add_like(post_id=post_id, user_id=current_user, like_repo=like_repo)
    like_count = LikeService.count_like(post_id=post_id, like_repo=like_repo)
    return LikeSchema(
        post_id=post_id,
        user_id=current_user,
        message="Liked",
        like_count=like_count
    )
@router.delete("/{post_id}/like", status_code=201)
def unlike_post_handler(
        post_id: int,
        like_repo: LikeRepository = Depends(),
        current_user: int = Depends(UserService.get_current_user)
):
    LikeService.remove_like(post_id=post_id, user_id=current_user, like_repo=like_repo)

@router.get("/{post_id}/like/count", status_code=200, response_model=LikeSchema)
def get_like_count_handler(
        post_id: int,
        like_repo: LikeRepository = Depends()
):
    like_count = LikeService.count_like(post_id=post_id, like_repo=like_repo)
    return {
        "post_id": post_id,
        "like_count": like_count
    }
