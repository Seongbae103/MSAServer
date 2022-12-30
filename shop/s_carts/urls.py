from django.urls import re_path as url
from shop.s_carts import views

urlpatterns = [
    url(r'cart', views.cart),
    url(r'cart-list', views.cart_list),
]