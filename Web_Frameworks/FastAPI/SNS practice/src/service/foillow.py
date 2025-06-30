from database.orm import Follow
from database.repository import FollowRepository

class FollowService:
    @staticmethod
    def follow_user(follower_id: int, following_id: int, follow_repo: FollowRepository):
        if follower_id == following_id:
            raise ValueError("Can't Follow yourself")
        return follow_repo.create_follow(follower_id=follower_id, following_id=following_id)

    @staticmethod
    def unfollow_user(follower_id: int, following_id: int, follow_repo: FollowRepository):
        follow = follow_repo.delete_follow(follower_id, following_id)
        if not follow:
            raise ValueError("unfollowed User")


    @staticmethod
    def get_following_users(user_id: int, follow_repo: FollowRepository) -> list[Follow]:
        return follow_repo.get_following_list(user_id)

    @staticmethod
    def get_followers_users(user_id: int, follow_repo: FollowRepository) -> list[Follow]:
        return follow_repo.get_followers_list(user_id)