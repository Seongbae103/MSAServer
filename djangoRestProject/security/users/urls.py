from django.urls import re_path as url

from security.users import views

urlpatterns = [
    url(r'user$', views.user),
    url(r'user-list$', views.user_list),
    url(r'user-list/name$', views.user_list_by_name),
    url(r'login', views.login)
]
