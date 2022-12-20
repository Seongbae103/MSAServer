from django.urls import re_path as url
from basic.webcrawler import Views


urlpatterns = [
    url(r'navermovie', Views.navermovie)

]