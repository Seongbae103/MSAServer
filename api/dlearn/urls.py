from django.urls import re_path as url
from api.dlearn.fashion import Fashion_View
from api.dlearn.number import Number_view
from api.dlearn.iris import views

urlpatterns = [
    url(r'iris', views.iris),
    url(r'fashion', Fashion_View.fashion), #POST
    url(r'fashion/(?P<id>)$', Fashion_View.fashion), #GET
    url(r'number', Number_view.number),
    url(r'number/(?P<id>)$', Number_view.number)

]