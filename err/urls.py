from django.urls import path
from django.conf.urls import url, include

import article.views
from err import views

app_name = 'err'

urlpatterns = [
    path('not_found/<e>/', views.not_found, name='not_found'),
    path('wrong_method', views.wrong_method, name='wrong_method'),
    path('wrong_input/<e>/', views.wrong_input, name='wrong_input'),
    path('no_permission/', views.no_permission, name='no_permission'),
    path('eggs/', views.eggs, name='eggs'),
]

urlpatterns += [
    url(r'^$', article.views.article_list),
]
