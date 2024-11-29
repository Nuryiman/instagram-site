from django.shortcuts import render
from django.views.generic import TemplateView

from users.models import CustomUser


class HomeView(TemplateView):
    """Вью для домашеней страницы"""
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = {
            "users": CustomUser.objects.all()   # TODO: Сделай потом тут рекомендуемые пользователи
        }
        return context

