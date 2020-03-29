from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('<int:round_id>/', views.index, name='index'), # /secret_key/polls/1/
    path('<int:round_id>/<int:question_id>/', views.detail, name='detail'),
    path('<int:round_id>/<int:question_id>/create/', views.create, name='create'),
    path('<int:round_id>/<int:question_id>/results/', views.results, name='results'),
    path('<int:round_id>/<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:round_id>/<int:question_id>/submit/', views.submit, name='submit')
]
