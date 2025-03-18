from django.db import models

from common.models import CommonModel


# Create your models here.
class ChattingRoom(CommonModel):

    participants = models.ManyToManyField(
        "users.User",
    )

class Message(CommonModel):

    text = models.TextField()
    user = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    room = models.ForeignKey(
        "direct_messages.ChattingRoom",
        on_delete=models.CASCADE,
    )