from django.urls import re_path as url

from multiplex.m_teaters import views

urlpatterns = [
    url(r'teater', views.teater),
    url(r'teater-list', views.teater_list),
]
