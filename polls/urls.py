from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('<int:round_id>/', views.index, name='index'), # /secret_key/polls/1/
    path('<int:round_id>/post_next_round/', views.post_next_round, name='post_next_round'),
    path('<int:round_id>/<int:question_id>/', views.detail, name='detail'),
    path('<int:round_id>/<int:question_id>/create/', views.create, name='create'),
    path('<int:round_id>/<int:question_id>/results/', views.results, name='results'),
    path('<int:round_id>/<int:question_id>/post_detail/', views.post_detail, name='post_detail'),
    path('<int:round_id>/<int:question_id>/post_create/', views.post_create, name='post_create'),
]
