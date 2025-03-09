from fastapi import APIRouter, Depends, HTTPException
from database.repository import FollowRepository
from schema.response import FollowSchema
from service.foillow import FollowService
from service.user import UserService

router = APIRouter(prefix="/users")

@router.post("/{user_id}/follow", status_code=201, response_model=FollowSchema)
def follow_user_handler(
        user_id: int,
        follow_repo: FollowRepository = Depends(),
        current_user: int = Depends(UserService.get_current_user)
):
    try:
        follow = FollowService.follow_user(
            follower_id=current_user,
            following_id=user_id,
            follow_repo=follow_repo
        )
        return FollowSchema(
            follower_id=follow.follower_id,
            following_id=follow.following_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{user_id}/follow", status_code=204)
def unfollow_user_handler(
        user_id: int,
        follow_repo: FollowRepository = Depends(),
        current_user: int = Depends(UserService.get_current_user)
):
    try:
        FollowService.unfollow_user(
            follower_id=current_user,
            following_id=user_id,
            follow_repo=follow_repo
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}/following", status_code=200, response_model=list[FollowSchema])
def get_following_users_handler(
        user_id: int,
        follow_repo: FollowRepository = Depends()
):
    following_list = FollowService.get_following_users(user_id, follow_repo)
    return [FollowSchema(follower_id=f.follower_id, following_id=f.following_id) for f in following_list]


@router.get("/{user_id}/followers", status_code=200, response_model=list[FollowSchema])
def get_followers_users_handler(
        user_id: int,
        follow_repo: FollowRepository = Depends()
):

    followers_list = FollowService.get_followers_users(user_id, follow_repo)
    return [FollowSchema(follower_id=f.follower_id, following_id=f.following_id) for f in followers_list]
