from django.urls import re_path as url

from api.dlearn.fashion import Fashion_View

urlpatterns = [
    url(r'img', Fashion_View.fashion), #POST
    url(r'img/(?P<id>)$', Fashion_View.fashion) #GET
]