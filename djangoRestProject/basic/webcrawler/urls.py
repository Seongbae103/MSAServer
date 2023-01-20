from django.urls import re_path as url
from basic.webcrawler.naver_movie import views

urlpatterns = [
    url(r'naver-movie', views.navermovie)

]