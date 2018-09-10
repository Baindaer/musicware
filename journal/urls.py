from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('composers', views.composers, name='composers'),
    path('practice_items', views.practice_items, name='practice_items'),
    path('playlists', views.playlists, name='playlists'),
    path('playlists', views.playlists, name='playlists'),
    path('playlist_view/<int:playlist_id>', views.playlist_view, name='playlist_view'),
    path('delete_playlist_line/<int:line_id>', views.delete_playlist_line, name='delete_playlist_line'),
    path('move_playlist_line/<int:line_id>/<str:dir>', views.move_playlist_line, name='move_playlist_line'),
    path('playlist_item_add/<int:line_id>/<str:dir>', views.move_playlist_line, name='move_playlist_line'),

]
