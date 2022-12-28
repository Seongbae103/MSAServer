from django.urls import re_path as url

from security.users import views as uviews
from security.posts import views as pviews


urlpatterns = [
    url(r'user-list', uviews.user_list),
    url(r'login', uviews.login),
]
