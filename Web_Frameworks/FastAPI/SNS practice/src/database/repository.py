from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from database.connection import get_db
from database.orm import User, Post, Like, Comment, Follow
from sqlalchemy import func


class UserRepository:
    def __init__(self, session: Session = Depends(get_db)):
        # user table 활용
        self.session = session

    def get_user_by_username(self, username: str) -> User | None:
        return self.session.scalar(
            select(User).where(User.username == username)
        )

    def save_user(self, user: User) -> User:
        self.session.add(instance=user)
        self.session.commit()
        self.session.refresh(instance=user)
        return user


class PostRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def create_post(self, post: Post) -> Post:
        self.session.add(instance=post)
        self.session.commit()
        self.session.refresh(instance=post)
        return post

    def get_all_posts(self) -> list[Post]:
        return list(self.session.scalars(
            select(Post).order_by(Post.created_at.desc())).all()
                    )

    def get_posts_by_user(self, user_id: int) -> list[Post]:
        return list(self.session.scalars(
            select(Post).where(Post.user_id == user_id).order_by(
                Post.created_at.desc())).all()
        )

    def get_post_by_post_id(self, post_id: int) -> Post | None:
        return self.session.get(Post, post_id)

    def update_post(self, post_id: int, new_content: str) -> Post:
        post = self.get_post_by_post_id(post_id=post_id)
        if post:
            post.content = new_content
            self.session.commit()
            self.session.refresh(instance=post)
        return post

    def delete_post(self, post_id: int) -> None:
        post = self.get_post_by_post_id(post_id=post_id)
        if post:
            self.session.delete(instance=post)
            self.session.commit()


class LikeRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def add_like(self, post_id: int, user_id: int):
        existing_like = self.session.scalar(
            select(Like).where(Like.post_id == post_id,
                               Like.user_id == user_id)
        )
        if not existing_like:
            like = Like(post_id=post_id, user_id=user_id)
            self.session.add(instance=like)
            self.session.commit()
            self.session.refresh(instance=like)

    def remove_like(self, post_id: int, user_id: int):
        like = self.session.scalar(
            select(Like).where(Like.post_id == post_id,
                               Like.user_id == user_id)
        )
        if like:
            self.session.delete(instance=like)
            self.session.commit()

    def get_like_count(self, post_id: int) -> int:
        return self.session.scalar(
            select(func.count()).where(Like.post_id == post_id)
        )

class CommentRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def add_comment(self, post_id: int, user_id: int, content: str
                       ) -> Comment:
        comment = Comment(post_id=post_id, user_id=user_id, content=content)
        self.session.add(instance=comment)
        self.session.commit()
        self.session.refresh(instance=comment)
        return comment

    def get_comments_by_post_id(self, post_id: int) -> list[Comment]:
        return list(
            self.session.scalars(
            select(Comment).where(Comment.post_id == post_id).order_by(
                Comment.created_at.asc())).all()
            )
    def get_comment_by_comment_id(self, comment_id: int) -> Comment | None:
        return self.session.get(Comment, comment_id)

    def update_comment(self, comment_id: int, user_id: int, new_content: str) -> Comment:
        comment = self.get_comment_by_comment_id(comment_id=comment_id)
        if comment and comment.user_id == user_id:
            comment.content = new_content
            self.session.commit()
            self.session.refresh(instance=comment)
        return comment

    def delete_comment(self, comment_id: int, user_id: int) -> None:
        comment = self.get_comment_by_comment_id(comment_id=comment_id)
        if comment and comment.user_id == user_id:
            self.session.delete(comment)
            self.session.commit()

class FollowRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def create_follow(self, follower_id: int, following_id: id) -> Follow:
        follow = Follow(follower_id=follower_id, following_id=following_id)
        self.session.add(follow)
        self.session.commit()
        self.session.refresh(follow)
        return follow

    def delete_follow(self,  follower_id: int, following_id: id) -> None:
        follow = self.session.scalar(
            select(Follow).where(
                Follow.follower_id == follower_id,
                Follow.following_id == following_id
            )
        )

        if follow:
            self.session.delete(follow)
            self.session.commit()

    def get_following_list(self, user_id: int) -> list[Follow]:
        return list(
            self.session.scalars(
                select(Follow).where(Follow.follower_id == user_id)
            ).all()
        )

    def get_followers_list(self, user_id: int) -> list[Follow]:
        return list(
            self.session.scalars(
                select(Follow).where(Follow.following_id == user_id)
            ).all()
        )

class NewsfeedRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_newsfeed(self, user_id: int, limit: int = 10, offset: int = 0) -> list[Post]:
        following_ids = self.session.scalars(
            select(Follow.following_id).where(Follow.follower_id == user_id)
        ).all()

        if not following_ids:
            return []
        return list(self.session.scalars(
            select(Post)
            .where(Post.user_id.in_(following_ids))
            .order_by(desc(Post.created_at))
            .limit(limit)
            .offset(offset)
        ).all())