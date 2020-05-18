"""CMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('message/view/1/', views.message1, name='user1'),
    path('message/view/2/', views.message2, name='user2'),
    path('message/view/3/', views.message3, name='user3'),
    path('history/', views.history, name='history'),
    path('notice-board/', views.notice, name='notice'),
    path('notice-board/show-notice/<str:slug>', views.show_notice, name='show-notice'),
    path('library/', views.library_book, name='library'),
    path('library/books/<str:slug>', views.show_book, name='book'),
    path('photos/gallery', views.gallery, name='photo'),
    
    # path('privacy', views.privacy, name='privacy'),
    # path('terms', views.terms, name='terms'),
    
]

