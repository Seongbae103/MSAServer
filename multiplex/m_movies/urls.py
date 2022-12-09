
from django.urls import re_path as url
from multiplex.m_movies import views

urlpatterns = [
    url(r'fake-faces', views.faces)
]