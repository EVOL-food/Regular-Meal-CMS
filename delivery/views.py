from delivery.serializers import DeliveryVendorSerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from delivery.models import DeliveryVendor
from django.utils import translation
from django.conf import settings
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND

class DeliveryVendorListView(ListAPIView):
    serializer_class = DeliveryVendorSerializer
    queryset = DeliveryVendor.objects.all()
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        language = kwargs["language"]
        if language in settings.MODELTRANSLATION_LANGUAGES:
            translation.activate(language)
        else:
            return Response({"detail": {"language_code": language,
                                        "error": "Language not found"}}, status=HTTP_404_NOT_FOUND)
        return self.list(request, *args, **kwargs)