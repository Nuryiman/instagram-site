from django.core.validators import FileExtensionValidator
from django.db import models

from users.models import CustomUser


class Publication(models.Model):
    """Моделька для публикаций"""

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='publications')
    description = models.TextField(max_length=1000)

    preview = models.FileField(upload_to='previews',
                               validators=[FileExtensionValidator(
                                   allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv', 'png', 'jpg', 'jpeg'])])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(CustomUser, related_name='likes')

# class PublicationGallery(models.Model):
#     """Моделька для галереи публикации"""
#
#     publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='publication_gallery')
#     file = models.FileField(upload_to='gallery/', null=True,
#                                validators=[FileExtensionValidator(
#                                    allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv', 'png', 'jpg', 'jpeg'])])
#


class Hashtag(models.Model):
    """Моделька для хэштегов"""

    title = models.CharField(max_length=255)
    publication = models.ManyToManyField(Publication, related_name='hashtags')


class PublicationComment(models.Model):
    """Моделька для комментариев"""

    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.TextField()
    updated_at = models.TextField()


