"""
URL configuration for insta_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from blog.views import HomeView, CreatePublicationView, LikedView, AddCommentView
from users.views import (MyProfileView, RegisterView, LoginView, MakeRegisterView, MakeLoginView,
                         MakeFollowView, UserProfileView, SearchView, UserMessagesView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', MyProfileView.as_view(), name='profile-url'),
    path('', HomeView.as_view(), name='home-url'),
    path('login/', LoginView.as_view(), name='login-url'),
    path('make-login/', MakeLoginView.as_view(), name='make-login-url'),
    path('register/', RegisterView.as_view(), name='register-url'),
    path('make-register/', MakeRegisterView.as_view(), name='make-register-url'),
    path('follow-unfollow/<int:pk>/', MakeFollowView.as_view(), name='toggle-follow'),
    path('create-publication/', CreatePublicationView.as_view(), name='create-publication'),
    path('liked-publication/<int:pk>/', LikedView.as_view(), name='liked-url'),
    path('add-comment/<int:pk>/', AddCommentView.as_view(), name='add-comment'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='user-profile'),
    path('search/', SearchView.as_view(), name='search-url'),
    path('messages/', UserMessagesView.as_view(), name='messages-url'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
