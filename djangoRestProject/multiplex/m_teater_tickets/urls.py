from django.urls import re_path as url

from multiplex.m_teater_tickets import views

urlpatterns = [
    url(r'teater_ticket', views.teater_ticket),
    url(r'teater_ticket-list', views.teater_ticket_list),
]
