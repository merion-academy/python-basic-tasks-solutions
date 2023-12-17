from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

UserModel: AbstractUser = get_user_model()
