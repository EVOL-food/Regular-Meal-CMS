from django.urls import path, include
from rest_framework import routers
from menu.views import MenuListView, MenuRetrieveView

#router = routers.DefaultRouter()
#router.register(r'menus', MenuViewSet)

urlpatterns = [
    path('menu/', MenuListView.as_view(), name='menu-list'),
    path('menu/<slug:slug>/', MenuRetrieveView.as_view(), name='menu-detail'),
]
