from django.urls import re_path as url

from blog.b_tags import views

urlpatterns = [
    url(r'tag', views.tag),
    url(r'tag-list', views.tag_list),


]