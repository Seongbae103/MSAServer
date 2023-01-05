from django.urls import re_path as url

from multiplex.m_showtimes import views

urlpatterns = [
    url(r'show_time', views.show_time),
    url(r'show_time-list', views.show_time_list),
]
