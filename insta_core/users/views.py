from django.shortcuts import render
from django.views.generic import TemplateView


class ProfileView(TemplateView):
    """Вьюшка для профиля"""
    template_name = 'profile.html'


class RegisterView(TemplateView):
    """Вьюшка для регистрации"""

    template_name = 'sign_up.html'


class LoginView(TemplateView):
    """Вьюшка для регистрации"""

    template_name = 'login.html'

