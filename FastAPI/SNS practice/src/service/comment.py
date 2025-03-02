from database.repository import CommentRepository


class CommentService:
    @staticmethod
    def add_comment(post_id: int, user_id: int, content: str, comment_repo: CommentRepository):
        return comment_repo.add_comment(post_id=post_id,
                                        user_id=user_id,
                                        content=content)

    @staticmethod
    def get_comments_by_post_id(post_id: int, comment_repo: CommentRepository):
        return comment_repo.get_comments_by_post_id(post_id=post_id)

    @staticmethod
    def get_comment_by_comment_id(comment_id: int, comment_repo: CommentRepository):
        return comment_repo.get_comment_by_comment_id(comment_id=comment_id)

    @staticmethod
    def update_comment(comment_id: int, user_id: int, new_content: str, comment_repo: CommentRepository):
        return comment_repo.update_comment(
            comment_id=comment_id,
            user_id=user_id,
            new_content=new_content
        )

    @staticmethod
    def delete_comment(comment_id: int, user_id: int, comment_repo: CommentRepository):
        comment_repo.delete_comment(comment_id=comment_id, user_id=user_id)