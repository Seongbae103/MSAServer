from django.urls import re_path as url

from multiplex.m_cinemas import views

urlpatterns = [
    url(r'cinema', views.cinema),
    url(r'cinema-list', views.cinema_list),
]
