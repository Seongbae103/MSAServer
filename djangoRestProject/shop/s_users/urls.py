from django.urls import re_path as url
from shop.s_users import views

urlpatterns = [
    url(r'user', views.user),
    url(r'list', views.user_list),
]