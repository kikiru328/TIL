from django.db import models
from common.models import TimeStampedModel
# Create your models here.
class Follow(TimeStampedModel):
    follower = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        related_name="followings"
        # follower: User -> User2 (Follower)
        # User2 -> User(followings)
    )

    following = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        related_name="followers"
        # following: User2 -> User (Following)
        # User -> User2 (followers)
    )

    class Meta:
        unique_together = ("follower", "following")