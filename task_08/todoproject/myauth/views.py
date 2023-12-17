from django.contrib.auth import authenticate, login
from django.contrib.auth.views import (
    LoginView as LoginViewGeneric,
    LogoutView as LogoutViewGeneric,
)
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserCreationForm
from .models import UserModel


class UserCreationView(CreateView):
    model = UserModel
    form_class = UserCreationForm
    success_url = reverse_lazy("todo-list:items-list")
    template_name = "registration/register.html"

    def form_valid(self, form):
        # Create the user
        response = super().form_valid(form)

        # Log in the user
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        user = authenticate(username=username, password=password)
        login(self.request, user)

        return response


class LoginView(LoginViewGeneric):
    next_page = reverse_lazy("index")


class LogoutView(LogoutViewGeneric):
    http_method_names = ["get", "post", "options"]
    next_page = reverse_lazy("index")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
