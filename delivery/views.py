from delivery.serializers import DeliveryVendorSerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from delivery.models import DeliveryVendor

class DeliveryVendorListView(ListAPIView):
    serializer_class = DeliveryVendorSerializer
    queryset = DeliveryVendor.objects.all()
    permission_classes = [AllowAny]

