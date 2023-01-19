from django.urls import re_path as url
from basic.dlearn.iris import views as iris_view
from basic.webcrawler.naver_movie import views as naver_movie_view

urlpatterns = [
    url(r'naver-movie', naver_movie_view.naver_movie)
]
