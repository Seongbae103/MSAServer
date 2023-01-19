from django.urls import re_path as url
from multiplex.movies import views

urlpatterns = [
    url(r'movie', views.movie),
    url(r'list', views.movie_list)
]
