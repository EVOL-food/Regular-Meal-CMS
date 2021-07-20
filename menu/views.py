from menu.models import Menu
from menu.serializers import MenuSerializerList, MenuSerializerDetail
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


class MenuListView(ListAPIView):
    serializer_class = MenuSerializerList
    queryset = Menu.objects.all()
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category__slug']
    search_fields = ['slug']


class MenuRetrieveView(RetrieveAPIView):
    serializer_class = MenuSerializerDetail
    queryset = Menu.objects.all()
    permission_classes = [AllowAny]
    lookup_field = 'slug'


class SearchDetailView(ListAPIView):
    serializer_class = MenuSerializerDetail
    queryset = Menu.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['slug',
                     'day_1__dish_1__slug', 'day_1__dish_2__slug', 'day_1__dish_3__slug',
                     'day_1__dish_4__slug', 'day_1__dish_5__slug',
                     'day_2__dish_1__slug', 'day_2__dish_2__slug', 'day_2__dish_3__slug',
                     'day_2__dish_4__slug', 'day_2__dish_5__slug',
                     'day_3__dish_1__slug', 'day_3__dish_2__slug', 'day_3__dish_3__slug',
                     'day_3__dish_4__slug', 'day_3__dish_5__slug',
                     'day_4__dish_1__slug', 'day_4__dish_2__slug', 'day_4__dish_3__slug',
                     'day_4__dish_4__slug', 'day_4__dish_5__slug',
                     'day_5__dish_1__slug', 'day_5__dish_2__slug', 'day_5__dish_3__slug',
                     'day_5__dish_4__slug', 'day_5__dish_5__slug',
                     'day_6__dish_1__slug', 'day_6__dish_2__slug', 'day_6__dish_3__slug',
                     'day_6__dish_4__slug', 'day_6__dish_5__slug',
                     'day_7__dish_1__slug', 'day_7__dish_2__slug', 'day_7__dish_3__slug',
                     'day_7__dish_4__slug', 'day_7__dish_5__slug',
                     'day_1__calories', 'day_2__calories', 'day_3__calories',
                     'day_4__calories', 'day_5__calories', 'day_6__calories',
                     'day_7__calories',
                     ]

