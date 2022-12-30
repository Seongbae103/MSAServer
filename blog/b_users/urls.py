from django.urls import re_path as url
from blog.b_users import views


urlpatterns = [
    url(r'user', views.user),
    url(r'user-list', views.user_list),


]