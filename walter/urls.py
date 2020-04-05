""" Walter URL Configuration
"""
from django.contrib import admin
from django.urls import include, path

#from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('<str:secret_key>/polls/', include('polls.urls')),
]
