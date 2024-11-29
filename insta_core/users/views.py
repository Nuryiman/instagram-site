from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from users.models import CustomUser


class ProfileView(TemplateView):
    """Вьюшка для профиля"""
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        user = request.user

        if user.is_authenticated:
            followers = CustomUser.objects.filter(follows=user)
            print(followers)

            context = {
                "followers": followers
            }
            return render(request, self.template_name, context)
        else:
            return redirect('login-url')


class RegisterView(TemplateView):
    """Вьюшка для регистрации"""

    template_name = 'sign_up.html'


class MakeRegisterView(View):
    """Вьюшка для успешной регистрации"""

    def post(self, request, *args, **kwargs):

        data = request.POST

        username = data.get('username')
        user_exists = CustomUser.objects.filter(username=username).exists()
        if user_exists:
            error = "Пользователь с таким юзернеймом уже существует"
            return render(request, 'sign_up.html', {'error': error})

        first_name = data['first_name']
        last_name = data['last_name']
        password1 = data['password1']
        password2 = data['password2']
        if password1 == password2:
            user = CustomUser.objects.create_user(username=username, password=password1, first_name=first_name,
                                                  last_name=last_name)
            login(request, user)
            return redirect('profile-url')
        else:
            error = "Пароли не совпадают"
            return render(request, 'sign_up.html', {'error': error})


class LoginView(TemplateView):
    """Вьюшка для регистрации"""

    template_name = 'login.html'


class MakeLoginView(View):

    def post(self, request, *args, **kwargs):

        data = request.POST

        username = data.get('username')
        password = data.get('password')
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            error = "Пользователь с таким юзернеймом не найден"
            return render(request, 'login.html', {'error': error})

        correct = user.check_password(password)

        if correct:
            login(request, user)
            return redirect("home-url")

        else:
            error = "Неверный пароль"
            return render(request, 'login.html', {'error': error})


class MakeFollowView(View):
    """Вьюшка для подписки на другого пользователя"""

    def post(self, request, *args, **kwargs):
        user = request.user
        follow_user_id = kwargs['pk']

        follow_user = CustomUser.objects.get(id=follow_user_id)
        if follow_user == user:
            return redirect("profile-url")

        user.follows.add(follow_user)
        user.save()
        return redirect('home-url')


# TODO: implement unfollow