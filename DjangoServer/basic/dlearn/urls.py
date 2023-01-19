from django.urls import re_path as url
from basic.dlearn.iris import views as iris_view
from basic.dlearn.fashion import views as fashion_view

urlpatterns = [
    url(r'iris', iris_view.iris),
    url(r'fashion', fashion_view.fashion)
]
