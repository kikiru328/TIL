from django.db import models
from common.models import TimeStampedModel
# Create your models here.
class Comment(TimeStampedModel):
    user = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        related_name="comments"
    )

    post = models.ForeignKey(
        to="posts.Post",
        on_delete=models.CASCADE,
        related_name="comments"
    )

    payload = models.CharField(max_length=150)