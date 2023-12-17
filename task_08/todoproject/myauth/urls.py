from django.urls import path

from .views import UserCreationView, LoginView, LogoutView

app_name = "custom-auth"

urlpatterns = [
    path(
        "register/",
        UserCreationView.as_view(),
        name="user-register",
    ),
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
]
