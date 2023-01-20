from django.urls import re_path as url

from blog.b_posts import views

urlpatterns = [
    url(r'post', views.post),
    url(r'post-list', views.post_list),


]