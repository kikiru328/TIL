from fastapi import APIRouter, Depends, HTTPException

from database.repository import PostRepository
from schema.request import PostRequest
from schema.response import PostSchema
from service.post import PostService
from service.user import UserService

router = APIRouter(prefix="/posts")

@router.post("/", status_code=201, response_model=PostSchema)
def create_post_handler(
        request: PostRequest,
        post_repo: PostRepository = Depends(),
        current_user: int = Depends(UserService.get_current_user)
):
    post = PostService.create_post(
        content=request.content,
        user_id=current_user,
        post_repo=post_repo
    )
    return post

@router.get("/", status_code=200, response_model=list[PostSchema])
def get_all_posts_handler(
        post_repo: PostRepository = Depends()
):
    return PostService.get_all_posts(post_repo)

@router.get("/{post_id}", status_code=200, response_model=PostSchema)
def get_post_by_post_id_handler(
        post_id: int,
        post_repo: PostRepository = Depends()
):
    post = PostService.get_post_by_post_id(
        post_id=post_id,
        post_repo=post_repo
    )
    if not post:
        raise HTTPException(status_code=404, detail="Post Not Found")
    return post

@router.patch("/{post_id}", status_code=200, response_model=PostSchema)
def update_post_handler(
        request: PostRequest,
        post_id: int,
        post_repo: PostRepository = Depends(),
        current_user: int = Depends(UserService.get_current_user)
):
    post = PostService.get_post_by_post_id(post_id=post_id, post_repo=post_repo)
    if not post: # post 없음
        raise HTTPException(status_code=404, detail="Post Not Found")
    if post.user_id != current_user: # 본인이 아님
        raise HTTPException(status_code=403, detail="You can only edit your own posts")

    updated_post = PostService.update_post(
        post_id=post_id,
        new_content=request.content,
        post_repo=post_repo
    )
    return updated_post

@router.delete("/{post_id}", status_code=204)
def delete_post_handler(
        post_id: int,
        post_repo: PostRepository = Depends(),
        current_user: int = Depends(UserService.get_current_user) # 본인 확인
):
    post = PostService.get_post_by_post_id(post_id=post_id, post_repo=post_repo)

    if not post: # post 없음
        raise HTTPException(status_code=404, detail="Post Not Found")
    if post.user_id != current_user: # 본인이 아님
        raise HTTPException(status_code=403, detail="You can only delete your own posts")

    PostService.delete_post(post_id=post_id, post_repo=post_repo)