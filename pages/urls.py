from django.urls import include, path

from . import views

app_name = 'pages'
urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.user_logout, name='user_logout'),
    path('login/', views.user_login, name='user_login'),
    path('register/', views.register, name='register'),
    path('new_game/', views.new_game, name='new_game'),
    path('post_new_game/', views.post_new_game, name='post_new_game'),
    path('<str:game_id>/', views.index_game, name='index_game'),
    path('<str:game_id>/polls/', include('polls.urls')),
]
