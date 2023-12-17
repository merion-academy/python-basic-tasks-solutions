from django.contrib.auth.forms import (
    UserCreationForm as UserCreationFormGeneric,
)

from .models import UserModel


class UserCreationForm(UserCreationFormGeneric):
    class Meta:
        model = UserModel
        fields = ("username", "password1", "password2")
