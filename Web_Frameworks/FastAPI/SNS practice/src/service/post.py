from database.orm import Post
from database.repository import PostRepository


class PostService:
    @staticmethod
    def create_post(
            content: str,
            user_id: int,
            post_repo: PostRepository
    ) -> Post:
        new_post = Post(user_id=user_id, content=content)
        return post_repo.create_post(new_post)

    @staticmethod
    def get_all_posts(post_repo: PostRepository):
        return post_repo.get_all_posts()

    @staticmethod
    def get_user_posts(user_id: int, post_repo: PostRepository):
        return post_repo.get_posts_by_user(user_id=user_id)

    @staticmethod
    def get_post_by_post_id(post_id: int, post_repo: PostRepository):
        return post_repo.get_post_by_post_id(post_id=post_id)

    @staticmethod
    def update_post(post_id: int, new_content: str, post_repo: PostRepository):
        return post_repo.update_post(post_id=post_id, new_content=new_content)

    @staticmethod
    def delete_post(post_id: int, post_repo: PostRepository):
        post_repo.delete_post(post_id)

