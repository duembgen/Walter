from django.urls import include, path

from . import views

app_name = 'pages'
urlpatterns = [
    path('', views.index, name='index'),
    path('new_game/', views.new_game, name='new_game'),
    path('<str:game_id>/', views.post_new_game, name='post_new_game'),
    path('<str:game_id>/polls/', include('polls.urls'), name='polls'),
]