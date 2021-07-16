from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ClientListCreateView, ClientDetailView

urlpatterns = [
    path('all-profiles/', ClientListCreateView.as_view(), name="all-profiles"),
    path('profile/<int:pk>/', ClientDetailView.as_view(), name="profile"),
]