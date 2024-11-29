from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from users.models import CustomUser


class HomeView(TemplateView):
    """Вью для домашеней страницы"""
    template_name = "home.html"

    def get(self, request, *args, **kwargs):

        user = request.user
        if user.is_authenticated:
            user.follows.count()  # на скольких я подписался

            followers = CustomUser.objects.filter(follows=user)
            follows = user.follows.all()

            context = {
                "followers": followers,
                "follows": follows
            }
            return render(request, self.template_name, context)
        return redirect("login-url")
