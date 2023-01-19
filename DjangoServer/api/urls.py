"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from api.views import test

urlpatterns = [
    path('', test),
    path("basic/algorithms/", include('basic.algorithms.urls')),
    path("basic/dlearn/", include('basic.dlearn.urls')),
    path("basic/mlearn/", include('basic.mlearn.urls')),
    path("basic/nlp/", include('basic.nlp.urls')),
    path("basic/pythonic/", include('basic.pythonic.urls')),
    path("basic/vision/", include('basic.vision.urls')),
    path("basic/webcrawler/", include('basic.webcrawler.urls')),
    path("blog/comments/", include('blog.comments.urls')),
    path("blog/posts/", include('blog.posts.urls')),
    path("blog/tags/", include('blog.tags.urls')),
    path("blog/views/", include('blog.views.urls')),
    path("common/main/", include('blog.views.urls')),
    path("multiplex/cinemas/", include('multiplex.cinemas.urls')),
    path("multiplex/movies/", include('multiplex.movies.urls')),
    path("multiplex/showtimes/", include('multiplex.showtimes.urls')),
    path("multiplex/theater_tickets/", include('multiplex.theater_tickets.urls')),
    path("multiplex/theaters/", include('multiplex.theaters.urls')),
    path("security/users/", include('security.users.urls')),
    path("shop/carts/", include('multiplex.movies.urls')),
    path("shop/categories/", include('shop.categories.urls')),
    path("shop/deliveries/", include('shop.deliveries.urls')),
    path("shop/orders/", include('shop.orders.urls')),
    path("shop/products/", include('shop.products.urls')),
]