from django.urls import re_path as url

from shop.s_orders import views

urlpatterns = [
    url(r'order', views.order),
    url(r'list', views.order_list),
]