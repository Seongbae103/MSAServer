from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import JsonResponse
from rest_framework.response import Response

from multiplex.m_teater_tickets.models import M_theaterTicket
from multiplex.m_teater_tickets.serializer import M_theaterTicketSerializer


# DAO
class M_theaterTicketRepository(object):
    def get_all(self):
        return Response(M_theaterTicketSerializer(M_theaterTicket.objects.all(), many=True).data)

    def find_teater_ticket_by_id(self):
        return Response(M_theaterTicketSerializer(M_theaterTicket.objects.all(), many=True).data)
