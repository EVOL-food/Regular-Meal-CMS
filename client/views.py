from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from .permissions import IsOwnerProfileOrReadOnly
from .serializers import ClientSerializer


class ClientListCreateView(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ClientSerializer
    permission_classes = IsAuthenticated

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class ClientDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsOwnerProfileOrReadOnly, IsAuthenticated]