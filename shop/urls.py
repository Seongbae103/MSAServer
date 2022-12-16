from django.urls import path, re_path as url

from shop import Fashion_View

urlpatterns = [
    url(r'img', Fashion_View.fashion), #POST
    url(r'img/(?P<id>)$', Fashion_View.fashion) #GET
]