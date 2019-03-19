from django.conf.urls import url, include
from django.urls import path

from article import views

app_name = 'article'

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('article-list/', views.article_list, name='article_list'),
]
