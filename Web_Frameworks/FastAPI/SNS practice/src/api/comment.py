from fastapi import APIRouter, Depends, HTTPException

from database.repository import CommentRepository
from schema.request import CommentRequest
from schema.response import CommentSchema
from service.comment import CommentService
from service.user import UserService

router = APIRouter(prefix="/posts")

@router.post("/{post_id}/comments", status_code=201, response_model=CommentSchema)
def add_comment_handler(
        post_id: int,
        request: CommentRequest,
        comment_repo: CommentRepository = Depends(),
        current_user: int = Depends(UserService.get_current_user),
):
    comment = CommentService.add_comment(
        post_id=post_id,
        user_id=current_user,
        content=request.content,
        comment_repo=comment_repo
    )
    if not comment:
        raise HTTPException(status_code=404, detail="Comment Not Found.")
    if comment.user_id != current_user:
        raise HTTPException(status_code=404, detail="You can only edit your own comments.")
    return comment

@router.get("/{post_id}/comments", status_code=200, response_model=list[CommentSchema])
def get_comments_handler(
        post_id: int,
        comment_repo: CommentRepository = Depends()
):
    return CommentService.get_comments_by_post_id(
        post_id=post_id,
        comment_repo=comment_repo
    )

@router.patch("/{post_id}/comments/{comment_id}", status_code=200,
              response_model=CommentSchema)
def update_comment_handler(
        comment_id: int,
        request: CommentRequest,
        comment_repo: CommentRepository = Depends(),
        current_user: int = Depends(UserService.get_current_user),
):
    comment = CommentService.get_comment_by_comment_id(
        comment_id=comment_id,
        comment_repo=comment_repo
    )
    if not comment:
        raise HTTPException(status_code=404, detail="Comment Not Found.")
    if comment.user_id != current_user:
        raise HTTPException(status_code=404, detail="You can only edit your own comments.")

    updated_comment = CommentService.update_comment(
        comment_id=comment_id,
        user_id=current_user,
        new_content=request.content,
        comment_repo=comment_repo
    )
    return updated_comment

@router.delete("/{post_id}/comments/{comment_id}", status_code=204)
def delete_comment_handler(
        comment_id: int,
        comment_repo: CommentRepository = Depends(),
        current_user: int = Depends(UserService.get_current_user)
):

    comment = CommentService.get_comment_by_comment_id(
        comment_id=comment_id,
        comment_repo=comment_repo
    )
    if not comment:
        raise HTTPException(status_code=404, detail="Comment Not Found")
    if comment.user_id != current_user:
        raise HTTPException(status_code=403, detail="You can only delete your own comments")

    CommentService.delete_comment(comment_id=comment_id, user_id=current_user, comment_repo=comment_repo)
