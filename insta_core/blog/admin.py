from django.contrib import admin
from django.utils.html import format_html

from blog.models import Publication, PublicationComment


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['author', 'description', 'image_tag']

    def image_tag(self, obj):
        return format_html('<img src="{}" width="100px"/>'.format(obj.preview.url))

    image_tag.short_description = 'превью-изображения'


@admin.register(PublicationComment)
class PublicationCommentAdmin(admin.ModelAdmin):
    list_display = ['publication', 'author', 'text']
