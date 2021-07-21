from django.urls import path, include
from rest_framework import routers
from menu.views import MenuListView, MenuRetrieveView, MenuCategorySearchView

#router = routers.DefaultRouter()
#router.register(r'menus', MenuViewSet)

urlpatterns = [
    path('<str:language>/menu/', MenuListView.as_view(), name='menu-list'),
    path('<str:language>/menu/<int:id>/', MenuRetrieveView.as_view(), name='menu-detail'),
    path('<str:language>/menu/category/', MenuCategorySearchView.as_view(), name='search-detail')
]
