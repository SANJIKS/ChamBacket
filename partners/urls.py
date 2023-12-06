from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import PartnersViewSet


router = DefaultRouter()
router.register(r'partners', PartnersViewSet, basename='partner')

urlpatterns = [
    path('', include(router.urls))
]