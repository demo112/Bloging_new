from django.urls import path
from django.conf.urls import url, include
from err import views
app_name = 'err'

urlpatterns = [
    path('', views.back_index, name='back_index'),
]
