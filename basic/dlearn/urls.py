from django.urls import re_path as url

from basic.dlearn import iris
from basic.dlearn.fashion import Fashion_View
from basic.dlearn.number import Number_view
from basic.dlearn.iris import views
from basic.dlearn.fruits import fruitsviews



urlpatterns = [
    url(r'iris', iris.views.iris),
    url(r'fashion', Fashion_View.fashion), #POST
    url(r'fashion/(?P<id>)$', Fashion_View.fashion), #GET
    url(r'number', Number_view.number),
    url(r'number/(?P<id>)$', Number_view.number),
    url(r'fruits', fruitsviews.fruits)

]