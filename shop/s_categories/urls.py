from django.urls import re_path as url
from shop.s_categories import views

urlpatterns = [
    url(r'category', views.category),
    url(r'category-list', views.category_list),
]