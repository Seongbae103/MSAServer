from django.urls import re_path as url

from basic.nlp.imdb import views

urlpatterns = [
    url(r'naver-movie-review', views.naver_movie_review),
]