from fastapi import APIRouter, Depends, Query

from database.repository import PostRepository, NewsfeedRepository
from schema.response import PostSchema
from service.newsfeeed import NewsfeedService
from service.user import UserService

router = APIRouter(prefix="/newsfeed")

@router.get("/", status_code=200, response_model=list[PostSchema])
def get_newsfeed_handler(
        limit: int = Query(10, get=1, le=50),
        offset: int = Query(0, get = 0),
        newsfeed_repo: NewsfeedRepository = Depends(),
        current_user: int = Depends(UserService.get_current_user)
):
    return NewsfeedService.get_newsfeed(
        user_id=current_user,
        newsfeed_repo=newsfeed_repo,
        limit=limit,
        offset=offset
    )