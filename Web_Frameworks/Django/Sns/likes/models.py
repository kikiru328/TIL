from django.db import models
from common.models import TimeStampedModel
# Create your models here.
class Like(TimeStampedModel):
    user = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        related_name="likes"
    )

    post = models.ForeignKey(
        to="posts.Post",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="likes",
    )

    class Meta:
        unique_together = ("user", "post") #같은 글에 like는 한 번.
