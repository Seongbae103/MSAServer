from django.urls import re_path as url
from basic.webcrawler.naver_movie import Views

urlpatterns = [
    url(r'naver-movie', Views.navermovie)

]