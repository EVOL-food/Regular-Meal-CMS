from menu.models import Menu
from menu.serializers import MenuSerializerList, MenuSerializerDetail
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend


class MenuListView(ListAPIView):
    serializer_class = MenuSerializerList
    queryset = Menu.objects.all()
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category__slug']


class MenuRetrieveView(RetrieveAPIView):
    serializer_class = MenuSerializerDetail
    queryset = Menu.objects.all()
    permission_classes = [AllowAny]
    lookup_field = 'slug'


