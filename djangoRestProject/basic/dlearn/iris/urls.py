from django.urls import re_path as url

from basic.dlearn.iris import views

urlpatterns = [
    url(r'irir$', views.iris)

]
