from django.urls import path
from delivery.views import DeliveryVendorListView

urlpatterns = [
    path('delivery/', DeliveryVendorListView.as_view(), name='delivery-list'),

]