from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('composers', views.composers, name='composers'),
    path('practice_items', views.practice_items, name='practice_items'),

]
