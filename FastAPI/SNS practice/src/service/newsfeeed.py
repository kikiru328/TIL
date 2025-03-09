from database.repository import NewsfeedRepository


class NewsfeedService:
    @staticmethod
    def get_newsfeed(user_id: int, newsfeed_repo: NewsfeedRepository, limit: int = 10, offset: int = 0):
        return newsfeed_repo.get_newsfeed(user_id=user_id, limit=limit, offset=offset)

