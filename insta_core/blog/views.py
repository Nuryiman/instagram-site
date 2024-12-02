import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from blog.models import Publication, PublicationComment
from users.models import CustomUser


class HomeView(TemplateView):
    """Вью для домашней страницы"""
    template_name = "home.html"

    def get(self, request, *args, **kwargs):

        user = request.user
        if user.is_authenticated:
            user.follows.count()  # на скольких я подписался

            followers = CustomUser.objects.filter(follows=user)
            follows = user.follows.all()
            publications =(
                Publication.objects
                .select_related("author")
                .prefetch_related("likes", "comments")
                .filter(author__in=follows)
                .order_by("created_at")
            )
            for publication in publications:
                publication.user_likes = user in publication.likes.all()

            context = {
                "followers": followers,
                "follows": follows,
                "publications": publications
            }
            return render(request, self.template_name, context)
        return redirect("login-url")


class CreatePublicationView(View):
    """Вьюшка для создания публикации"""

    def post(self, request, *args, **kwargs):
        user = request.user

        data = request.POST

        description = data.get('description')
        preview = request.FILES.get('preview')

        Publication.objects.create(
            author=user,
            description=description,
            preview=preview
        )
        return redirect('home-url')


class LikedView(View):
    """Вьюшка чтобы ставить лайки"""

    def post(self, request, *args, **kwargs):

        user = request.user
        try:
            publication = Publication.objects.get(id=kwargs['pk'])
        except Publication.DoesNotExist:
            return JsonResponse({"success": False, "error": "Invalid request"})
        if user in publication.likes.all():
            publication.likes.remove(user)
            liked = False
        else:
            publication.likes.add(user)
            liked = True

        return JsonResponse({"success": True, "liked": liked})


class AddCommentView(View):
    """Вьюшка для добавления комментариев"""

    def post(self, request, *args, **kwargs):
        user = request.user
        data = json.loads(request.body)
        text = data['comment']
        print(text)

        try:
            publication = Publication.objects.get(id=kwargs['pk'])
        except Publication.DoesNotExist:
            return JsonResponse({"success": False, "error": "Invalid request"})

        comment = PublicationComment.objects.create(author=user, publication=publication, text=text)
        return JsonResponse({
            'success': True,
            'comment': {
                'user': comment.author.first_name,  # Имя пользователя
                'text': comment.text  # Текст комментария
            }})