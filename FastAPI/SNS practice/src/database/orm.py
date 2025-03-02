from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, UniqueConstraint

Base = declarative_base()

class User(Base): # mysql User table
    __tablename__ = "users" #same as db table name

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(256), unique=True, nullable=False)
    password = Column(String(256), nullable=False)

    @classmethod
    def create(cls, username: str, hashed_password: str) -> "User":
        return cls(
            username=username,
            password=hashed_password
        )

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(String(1000), nullable=False)
    created_at = Column(DateTime, default=func.now())  # 글 작성 시간

    # created_at: auto, Post(인자값 적용 X)
    user = relationship("User", backref="posts") # Post -> User

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer,
                     ForeignKey("posts.id", ondelete="CASCADE"),
                     nullable=False)
    user_id = Column(Integer,
                     ForeignKey("users.id", ondelete="CASCADE"),
                     nullable=False)

    __table_args__ = (UniqueConstraint(
        "post_id", "user_id", name="unique_like"
    ),)

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer,
                     ForeignKey("posts.id", ondelete="CASCADE"),
                     nullable=False)
    user_id = Column(Integer,
                     ForeignKey("users.id", ondelete="CASCADE"),
                     nullable=False)
    content = Column(String(300), nullable=False)
    created_at = Column(DateTime, default=func.now())



