from django.urls import re_path as url

from basic.nlp.korean_classify import views

urlpatterns = [
    url(r'naverimdb', views.korean_classify),
]
