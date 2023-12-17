from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class TodoItem(models.Model):
    text = models.CharField(
        max_length=50,
        null=False,
    )
    done = models.BooleanField(
        null=False,
        default=False,
    )
    author = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        null=False,
    )
