from django.urls import re_path as url

from blog.b_views import views

urlpatterns = [
    url(r'view', views.view),
    url(r'view-list', views.view_list),


]