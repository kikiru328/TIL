from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):

    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    class LanguageChoices(models.TextChoices):
        ENG = ("eng", "Eng")
        KO = ("ko", "Ko")

    username = models.CharField(max_length=50,
                                unique=True,)
    first_name = models.CharField(max_length=150,)
    last_name = models.CharField(max_length=150,)
    avatar = models.ImageField()
    gender = models.CharField(max_length=10,
                              choices=GenderChoices.choices,
                              default=GenderChoices.MALE)
    language = models.CharField(max_length=10,
                                choices=LanguageChoices.choices,
                                default=LanguageChoices.KO)


