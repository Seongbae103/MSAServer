from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from blog.posts.models import Post
from blog.posts.serializers import PostSerializer
from blog.tags.models import Tag
from blog.tags.serializers import TagSerializer
from blog.views.models import View
from blog.views.serializers import ViewSerializer
from multiplex.movies.models import Movie
from multiplex.showtimes.models import Showtime
from multiplex.showtimes.serializers import ShowtimeSerializer
from multiplex.theaters.models import Theater
from multiplex.theaters.serializers import TheaterSerializer
from shop.carts.models import Cart
from shop.carts.serializers import CartSerializer
from shop.categories.models import Category
from shop.categories.serializers import CategorySerializer


class CategoryRepository(object):

    def __init__(self):
        print(" CommentsRepository 객체 생성 ")

    def get_all(self):
        return Response(CategorySerializer(Category.objects.all(), many=True).data)

    def get_by_id(self):
        return Response(CategorySerializer(Category.objects.all(), many=True).data)



