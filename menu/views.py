from django.utils import translation
import django_filters.rest_framework
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter
from menu.serializers import MenuSerializerList, MenuSerializerDetail
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from django.conf import settings
from menu.models import Menu


class MenuListView(ListAPIView):
    serializer_class = MenuSerializerList
    queryset = Menu.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ["category__title", "category__slug", "category__id"]

    def get(self, request, *args, **kwargs):
        language = kwargs["language"]
        if language in settings.MODELTRANSLATION_LANGUAGES:
            translation.activate(language)
        else:
            return Response({"detail": {"language_code": language,
                                        "error": "Language not found"}}, status=HTTP_404_NOT_FOUND)
        return self.list(request, *args, **kwargs)


class MenuRetrieveView(RetrieveAPIView):
    serializer_class = MenuSerializerDetail
    queryset = Menu.objects.all()
    permission_classes = [AllowAny]
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        language = kwargs["language"]
        if language in settings.MODELTRANSLATION_LANGUAGES:
            translation.activate(language)
        else:
            return Response({"detail": {"language_code": language,
                                        "error": "Language not found"}}, status=HTTP_404_NOT_FOUND)
        return self.retrieve(request, *args, **kwargs)


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

    def get(self, request, *args, **kwargs):
        language = kwargs["language"]
        if language in settings.MODELTRANSLATION_LANGUAGES:
            translation.activate(language)
        else:
            return Response({"detail": {"language_code": language,
                                        "error": "Language not found"}}, status=HTTP_404_NOT_FOUND)
        return self.list(request, *args, **kwargs)
