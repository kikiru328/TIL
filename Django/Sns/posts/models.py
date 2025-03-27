from django.db import models
from common.models import TimeStampedModel
# Create your models here.
class Post(TimeStampedModel):
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    user = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        related_name="posts"
    )

    def __str__(self):
        return self.title