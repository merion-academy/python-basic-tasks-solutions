from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    View,
)

from .forms import TodoItemForm
from .models import TodoItem


class ToDoItemsListView(
    LoginRequiredMixin,
    ListView,
):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TodoItemForm()
        return context

    def get_queryset(self):
        return TodoItem.objects.filter(author=self.request.user)


class ToDoItemCreateView(
    LoginRequiredMixin,
    CreateView,
):
    template_name = "todo_list/todoitem_form.html"
    form_class = TodoItemForm
    success_url = reverse_lazy("todo-list:items-list")

    def get_queryset(self):
        return TodoItem.objects.filter(author=self.request.user)

    def form_valid(self, form):
        # Assign the current user to the 'user' field of the ToDoItem
        form.instance.author = self.request.user
        return super().form_valid(form)


class ToDoItemDeleteView(
    LoginRequiredMixin,
    DeleteView,
):
    success_url = reverse_lazy("todo-list:items-list")

    def get_queryset(self):
        return TodoItem.objects.filter(author=self.request.user)


class ToDoItemToggleView(
    LoginRequiredMixin,
    View,
):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        todo_item: TodoItem = get_object_or_404(
            TodoItem,
            pk=pk,
            author=self.request.user,
        )
        todo_item.done = not todo_item.done
        todo_item.save()
        url = reverse("todo-list:items-list")
        return redirect(url)
