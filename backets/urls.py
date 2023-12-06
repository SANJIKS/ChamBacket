from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import BacketViewSet


router = DefaultRouter()
router.register(r'backets', BacketViewSet, basename='backet')

urlpatterns = [
    path('', include(router.urls))
]