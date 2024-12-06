from django.contrib.auth import login, logout
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from blog.models import Publication
from users.models import CustomUser, Chat, UserMessage


class MyProfileView(TemplateView):
    """Вьюшка для профиля"""
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        user = request.user

        if user.is_authenticated:
            followers = CustomUser.objects.filter(follows=user)
            publications = Publication.objects.filter(author=user)

            for item in publications:
                item.is_video = item.preview.url.lower().endswith(('.mp4', '.webm', '.ogg'))
                item.is_image = item.preview.url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))

            context = {
                "user": user,
                "followers": followers,
                "publications": publications,
            }
            return render(request, self.template_name, context)
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


class MakeLogoutView(View):

    def get(self, request, *args, **kwargs):

        logout(request)

        return redirect('login-url')


class MakeFollowView(View):
    """Вьюшка для подписки на другого пользователя"""

    def post(self, request, *args, **kwargs):
        user = request.user
        follow_user_id = kwargs['pk']
        try:
            follow_user = CustomUser.objects.get(id=follow_user_id)
        except CustomUser.DoesNotExist:
            return JsonResponse({"success": False, "error": "Invalid request"})

        if follow_user in request.user.follows.all():
            # Если подписан, отписываем
            request.user.follows.remove(follow_user)
            action = 'unfollowed'
        else:
            # Если не подписан, подписываем
            request.user.follows.add(follow_user)
            action = 'followed'

        return JsonResponse({'success': True, 'action': action})


class UserProfileView(TemplateView):
    """Вью для отображения профиля другого пользователя"""
    template_name = "profile.html"

    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(username=kwargs['username'])
        if user == self.request.user:
            return redirect('profile-url')
        followers = CustomUser.objects.filter(follows=user)
        publications = Publication.objects.filter(author=user)

            # for item in request.user.follows.all()
        request.user.followed = user in request.user.follows.all()

        context = {
            "user": user,
            "followers": followers,
            "publications": publications,
        }
        return render(request, self.template_name, context)


class SearchView(View):
    """Вью для поиска пользователей"""

    def get(self, request, *args, **kwargs):
        user = request.user  # Текущий пользователь
        query = request.GET.get("query", "").strip()  # Получаем запрос

        if query:
            # Ищем пользователей по username, first_name или last_name
            users = CustomUser.objects.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            ).exclude(id=user.id)  # Исключаем текущего пользователя из результатов

            # Формируем JSON-ответ
            filtered_users = [
                {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "avatar": user.avatar.url if user.avatar else '/static/images/anonim.png'
                }
                for user in users
            ]
            return JsonResponse({"success": True, "users": filtered_users})

        # Если запрос пустой
        return JsonResponse({"success": False, "users": []})


class UserMessagesView(TemplateView):
    """Вьюшка для чата пользователей"""
    template_name = 'messages.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect("login-url")

        chats = Chat.objects.filter(Q(user1=user) | Q(user2=user))
        try:
            chat = Chat.objects.get(id=kwargs['pk'])
        except Chat.DoesNotExist:
            return redirect("home-url")
        if chat.user1 == user:
            companion = chat.user2
        else:
            companion = chat.user1

        chat_messages = UserMessage.objects.filter(Q(sender=user, receiver=companion) |
                                                   Q(receiver=user, sender=companion)).order_by('created_at')

        context = {
            'chat': chat,
            'user': user,
            'companion': companion,
            'chats': chats,
            'chat_messages': chat_messages,
        }
        return render(request, self.template_name, context)


class EmptyChatsView(TemplateView):
    """Вью для пустого чата"""
    template_name = "messages.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        chats = Chat.objects.filter(Q(user1=user) | Q(user2=user))
        context = {
            'chats': chats
        }
        return context


class UserEmptyChatView(TemplateView):
    """Вью для еще не начатого чата"""
    template_name = 'messages.html'

    def get(self, request, *args, **kwargs):
        try:
            user = CustomUser.objects.get(username=kwargs['username'])
        except CustomUser.DoesNotExist:
            return redirect("home-url")
        context = {
            "user": user
        }
        return render(request, self.template_name, context)


class SendMessageView(View):
    def post(self, request, *args, **kwargs):
        user = request.user

        companion = CustomUser.objects.get(username=kwargs['username'])
        try:
            chat = Chat.objects.get(user1=user, user2=companion)
        except Chat.DoesNotExist:
            try:
                chat = Chat.objects.get(user2=user, user1=companion)
            except Chat.DoesNotExist:
                chat = Chat.objects.create(user1=user, user2=companion)

        message = request.POST['message']
        UserMessage.objects.create(
            sender=user,
            receiver=companion,
            text=message,
            chat=chat
        )
        return redirect('messages-url', pk=chat.id)
