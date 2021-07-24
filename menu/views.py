from django.utils import translation
import django_filters.rest_framework
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter
from menu.serializers import MenuSerializerList, MenuSerializerDetail
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from django.db.models import Q
from django.conf import settings
from menu.models import Menu


class MenuListView(ListAPIView):
    serializer_class = MenuSerializerList
    queryset = Menu.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    def get(self, request, *args, **kwargs):
        language = kwargs["language"]
        if language in settings.MODELTRANSLATION_LANGUAGES:
            translation.activate(language)
        else:
            return Response({"detail": {"language_code": language,
                                        "error": "Language not found"}}, status=HTTP_404_NOT_FOUND)
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        category = self.request.GET.get("category")
        if category:
            try:
                return Menu.objects.filter(category_id=category)
            except ValueError:
                return Menu.objects.filter(category__slug__contains=category)
        else:
            return Menu.objects.all()


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


class MenuTitleSearchFilter(SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('title'):
            return ['title']
        return super(MenuTitleSearchFilter, self).get_search_fields(view, request)


class DishSearchFilter(SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('dish'):
            return ['day_1__dish_1__title', 'day_1__dish_2__title', 'day_1__dish_3__title',
                    'day_1__dish_4__title', 'day_1__dish_5__title',
                    'day_2__dish_1__title', 'day_2__dish_2__title', 'day_2__dish_3__title',
                    'day_2__dish_4__title', 'day_2__dish_5__title',
                    'day_3__dish_1__title', 'day_3__dish_2__title', 'day_3__dish_3__title',
                    'day_3__dish_4__title', 'day_3__dish_5__title',
                    'day_4__dish_1__title', 'day_4__dish_2__title', 'day_4__dish_3__title',
                    'day_4__dish_4__title', 'day_4__dish_5__title',
                    'day_5__dish_1__title', 'day_5__dish_2__title', 'day_5__dish_3__title',
                    'day_5__dish_4__title', 'day_5__dish_5__title',
                    'day_6__dish_1__title', 'day_6__dish_2__title', 'day_6__dish_3__title',
                    'day_6__dish_4__title', 'day_6__dish_5__title',
                    'day_7__dish_1__title', 'day_7__dish_2__title', 'day_7__dish_3__title',
                    'day_7__dish_4__title', 'day_7__dish_5__title',]
        return super(DishSearchFilter, self).get_search_fields(view, request)


class AverageCalorieSearchFilter(SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('calories'):
            return ['day_1__calories', 'day_2__calories', 'day_3__calories',
                    'day_4__calories', 'day_5__calories', 'day_6__calories',
                    'day_7__calories',]
        return super(AverageCalorieSearchFilter, self).get_search_fields(view, request)


class SearchDetailView(ListAPIView):
    serializer_class = MenuSerializerDetail
    queryset = Menu.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [MenuTitleSearchFilter, DishSearchFilter,
                       AverageCalorieSearchFilter]


    def get(self, request, *args, **kwargs):
        language = kwargs["language"]
        if language in settings.MODELTRANSLATION_LANGUAGES:
            translation.activate(language)
        else:
            return Response({"detail": {"language_code": language,
                                        "error": "Language not found"}}, status=HTTP_404_NOT_FOUND)
        return self.list(request, *args, **kwargs)
