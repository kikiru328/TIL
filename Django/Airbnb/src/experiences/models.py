from django.db import models
from common.models import CommonModel

# Create your models here.

class Experience(CommonModel):
    name = models.CharField(max_length=250)
    country = models.CharField(max_length=50, default="South Korea")
    city = models.CharField(max_length=80, default="Seoul")
    host = models.ForeignKey("users.User", on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    address = models.CharField(max_length=250,)
    start = models.TimeField()
    end = models.TimeField()
    descriptions = models.TextField()
    pers = models.ManyToManyField("experiences.Perk")
    category = models.ForeignKey("categories.Category",
                                 null=True,
                                 blank=True,
                                 on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Perk(CommonModel):
    """ What is included on an Experience"""
    name = models.CharField(max_length=100,)
    details = models.CharField(max_length=250,
                               blank=True,
                               default="",)
    explanation = models.TextField(blank=True,
                                   default="",)

    def __str__(self):
        return self.name