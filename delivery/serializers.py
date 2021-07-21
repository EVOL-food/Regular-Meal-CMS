from rest_framework import serializers
from delivery.models import DeliveryVendor

class DeliveryVendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryVendor
        fields = ['title', 'description', 'price_one_delivery']
