from database.repository import LikeRepository


class LikeService:
    @staticmethod
    def add_like(post_id: int, user_id: int, like_repo: LikeRepository):
        like_repo.add_like(post_id=post_id, user_id=user_id)

    @staticmethod
    def remove_like(post_id: int, user_id: int, like_repo: LikeRepository):
        like_repo.remove_like(post_id=post_id, user_id=user_id)

    @staticmethod
    def count_like(post_id: int, like_repo: LikeRepository):
        return like_repo.get_like_count(post_id=post_id)