from fastapi import APIRouter, Depends

from database.repository import PostRepository
from schema.response import PostSchema

router = APIRouter(prefix="/newsfeed")

@router.get("/", status_code=200, response_model=list[PostSchema])
def get_newsfeed_handler(post_repo: PostRepository = Depends()):
    return PostRepository.get_all_posts(post_repo)