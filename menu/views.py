from django.shortcuts import render
from rest_framework import viewsets
from menu.models import Menu
from menu.serializers import MenuSerializerList, MenuSerializerDetail
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


class MenuListView(ListAPIView):
    serializer_class = MenuSerializerList
    queryset = Menu.objects.all()
    permission_classes = [AllowAny]
    lookup_field = 'slug'


class MenuRetrieveView(RetrieveAPIView):
    serializer_class = MenuSerializerDetail
    queryset = Menu.objects.all()
    permission_classes = [AllowAny]
    lookup_field = 'slug'


